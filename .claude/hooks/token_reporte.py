#!/usr/bin/env python3
"""
Hook Stop de Claude Code: reporta tokens consumidos en CADA solicitud
(no acumulado de toda la sesion), y cuantas cuentas se generaron en esa
misma solicitud, si aplica.

Lee transcript_path (el .jsonl que Claude Code ya escribe, con el 'usage'
exacto que se factura por mensaje), calcula el delta desde la ultima vez
que se reporto en esta sesion, lo muestra en el chat (systemMessage) y lo
anota en memoria/tokens/reporte-tokens.csv.

COMO SE CUENTA:
- Claude Code escribe una linea del transcript por cada bloque de un mismo
  mensaje (thinking, text, tool_use), y todas repiten el mismo 'usage'.
  Por eso se cuenta una sola vez cada message.id (si no, se infla ~2-3x).
- Las cuentas generadas se cuentan solo en el resultado de una llamada que
  ejecuto generar_cuenta_xml.py (no en texto del chat ni en archivos leidos).

LIMITACIONES CONOCIDAS (leer antes de confiar ciegamente en el numero):
- La deteccion de "cuentas generadas" depende de que generar_cuenta_xml.py
  siga imprimiendo exactamente "N/N cuentas generadas correctamente". Si
  ese texto cambia, el contador de cuentas queda en 0 silenciosamente.
- Los subagentes (herramienta Agent) escriben su propio transcript; su
  consumo no se incluye aqui.
- Esta cifra sale del transcript local que escribe Claude Code, que deberia
  coincidir con lo facturado, pero el dato oficial de facturacion sigue
  siendo Settings -> Usage en claude.ai (o la Console, si se usa API).
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MARCA_PATH = REPO_ROOT / ".claude" / "tokens_ultima_linea.local.json"
REPORTE_CSV = REPO_ROOT / "memoria" / "tokens" / "reporte-tokens.csv"

PATRON_CUENTAS = re.compile(r"^(\d+)/\d+ cuentas generadas correctamente", re.MULTILINE)
HERRAMIENTA_CUENTAS = "generar_cuenta_xml.py"


def leer_transcript(ruta):
    lineas = []
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            try:
                lineas.append(json.loads(linea))
            except json.JSONDecodeError:
                continue
    return lineas


def bloques(entrada):
    mensaje = entrada.get("message")
    if not isinstance(mensaje, dict):
        return []
    contenido = mensaje.get("content")
    return contenido if isinstance(contenido, list) else []


def texto_de_resultado(bloque):
    contenido = bloque.get("content")
    if isinstance(contenido, str):
        return contenido
    if isinstance(contenido, list):
        return "\n".join(c.get("text", "") for c in contenido if isinstance(c, dict))
    return ""


def sumar_uso(lineas):
    """Suma el usage una vez por message.id (la ultima linea de cada mensaje)."""
    por_mensaje = {}
    for i, entrada in enumerate(lineas):
        mensaje = entrada.get("message")
        if not isinstance(mensaje, dict) or not mensaje.get("usage"):
            continue
        clave = mensaje.get("id") or f"sin-id-{i}"
        por_mensaje[clave] = mensaje

    totales = {"entrada": 0, "salida": 0, "cache_creado": 0, "cache_leido": 0}
    modelos = set()
    for mensaje in por_mensaje.values():
        usage = mensaje["usage"]
        totales["entrada"] += usage.get("input_tokens", 0) or 0
        totales["salida"] += usage.get("output_tokens", 0) or 0
        totales["cache_creado"] += usage.get("cache_creation_input_tokens", 0) or 0
        totales["cache_leido"] += usage.get("cache_read_input_tokens", 0) or 0
        if mensaje.get("model"):
            modelos.add(mensaje["model"])
    return totales, len(por_mensaje), sorted(modelos)


def extraer_cuentas_generadas(lineas):
    llamadas_herramienta = set()
    for entrada in lineas:
        for bloque in bloques(entrada):
            if isinstance(bloque, dict) and bloque.get("type") == "tool_use":
                if HERRAMIENTA_CUENTAS in json.dumps(bloque.get("input", {}), ensure_ascii=False):
                    llamadas_herramienta.add(bloque.get("id"))

    total = 0
    for entrada in lineas:
        for bloque in bloques(entrada):
            if (
                isinstance(bloque, dict)
                and bloque.get("type") == "tool_result"
                and bloque.get("tool_use_id") in llamadas_herramienta
            ):
                for m in PATRON_CUENTAS.finditer(texto_de_resultado(bloque)):
                    total += int(m.group(1))
    return total


def main():
    datos = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
    transcript_path = datos.get("transcript_path", "")
    session_id = datos.get("session_id", "desconocida")

    if not transcript_path or not os.path.exists(transcript_path):
        sys.exit(0)

    lineas = leer_transcript(transcript_path)

    marca = {}
    if MARCA_PATH.exists():
        try:
            marca = json.loads(MARCA_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            marca = {}
    desde = marca.get(session_id, 0)
    nuevas = lineas[desde:]

    t, llamadas, modelos = sumar_uso(nuevas)
    cuentas_generadas = extraer_cuentas_generadas(nuevas)
    total_tokens = t["entrada"] + t["salida"] + t["cache_creado"] + t["cache_leido"]

    reporte = (
        f"[REPORTE DE TOKENS - esta solicitud] "
        f"Entrada: {t['entrada']:,} | Salida: {t['salida']:,} | "
        f"Cache creado: {t['cache_creado']:,} | Cache leido: {t['cache_leido']:,} | "
        f"TOTAL: {total_tokens:,} | Llamadas al modelo: {llamadas} "
        f"({', '.join(modelos) or 'sin modelo'}) | "
        f"Cuentas generadas: {cuentas_generadas}"
    )
    # systemMessage es lo que Claude Code muestra al usuario; stderr con exit 0 no se ve.
    print(json.dumps({"systemMessage": reporte}, ensure_ascii=False))

    REPORTE_CSV.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not REPORTE_CSV.exists()
    with open(REPORTE_CSV, "a", encoding="utf-8") as f:
        if nuevo:
            f.write("fecha_hora,session_id,llamadas_modelo,entrada_tokens,salida_tokens,cache_creado,cache_leido,total_tokens,cuentas_generadas\n")
        f.write(
            f"{datetime.now().isoformat(timespec='seconds')},{session_id},{llamadas},"
            f"{t['entrada']},{t['salida']},{t['cache_creado']},{t['cache_leido']},{total_tokens},{cuentas_generadas}\n"
        )

    marca[session_id] = len(lineas)
    MARCA_PATH.parent.mkdir(parents=True, exist_ok=True)
    MARCA_PATH.write_text(json.dumps(marca), encoding="utf-8")

    sys.exit(0)


if __name__ == "__main__":
    main()
