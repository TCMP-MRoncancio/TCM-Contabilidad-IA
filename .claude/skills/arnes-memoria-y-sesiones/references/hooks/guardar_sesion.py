#!/usr/bin/env python3
"""Hook PreCompact / SessionEnd: guarda la conversacion en el vault.

Recibe por stdin el JSON del hook (session_id, transcript_path, hook_event_name).
Escribe un extracto legible en <destino>/sesiones/AAAA-MM-DD_<id8>.md, una copia cruda comprimida
en <destino>/sesiones/raw/<id>.jsonl.gz y regenera <destino>/sesiones/INDICE.md.
Destino: la carpeta del ticket activo (segun .claude/arnes.json) o la memoria del sistema si no hay ticket.
Es idempotente (cada ejecucion regenera el extracto completo) y nunca bloquea (codigo 0 siempre).
El formato de la transcripcion es interno de Claude Code y puede cambiar: se lee con tolerancia.
"""
import datetime as dt
import gzip
import json
import os
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
DEFECTOS = {
    "puntero_activo": ".claude/activo.local.json",
    "dir_ticket": "vault-cliente-{cliente}/tickets/{ticket}",
    "dir_memoria": "memoria",
    "max_chars_mensaje_sesion": 4000,
}
CLAVES_RUTA = ("file_path", "path", "notebook_path")
HERRAMIENTAS_QUE_ESCRIBEN = ("Edit", "Write", "MultiEdit", "NotebookEdit")


def config():
    cfg = dict(DEFECTOS)
    ruta = RAIZ / ".claude" / "arnes.json"
    if ruta.exists():
        cfg.update(json.loads(ruta.read_text(encoding="utf-8")))
    return cfg


def escribir(destino, texto):
    with open(destino, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)


def destino(cfg):
    try:
        activo = json.loads((RAIZ / cfg["puntero_activo"]).read_text(encoding="utf-8"))
        tdir = RAIZ / cfg["dir_ticket"].format(cliente=activo["cliente"], ticket=activo["ticket"])
        if tdir.exists():
            return tdir, f"{activo['cliente']}/{activo['ticket']}"
    except Exception:
        pass
    return RAIZ / cfg["dir_memoria"], "sin ticket"


def contenido_a_texto(contenido):
    """Devuelve (texto, herramientas, rutas, solo_resultados_de_herramientas)."""
    if isinstance(contenido, str):
        return contenido, [], [], False
    textos, herramientas, rutas = [], [], []
    hubo_algo_distinto = False
    for bloque in contenido or []:
        if not isinstance(bloque, dict):
            continue
        tipo = bloque.get("type")
        if tipo == "tool_result":
            continue
        hubo_algo_distinto = True
        if tipo == "text":
            textos.append(bloque.get("text", ""))
        elif tipo == "tool_use":
            nombre = bloque.get("name", "?")
            herramientas.append(nombre)
            entrada = bloque.get("input") or {}
            for clave in CLAVES_RUTA:
                if isinstance(entrada.get(clave), str):
                    rutas.append((nombre, entrada[clave]))
    return "\n".join(t for t in textos if t), herramientas, rutas, not hubo_algo_distinto


def extraer(transcripcion):
    turnos, rutas, primera, ultima = [], [], None, None
    with open(transcripcion, encoding="utf-8", errors="replace") as fh:
        for linea in fh:
            linea = linea.strip()
            if not linea:
                continue
            try:
                obj = json.loads(linea)
            except Exception:
                continue
            marca = obj.get("timestamp")
            if isinstance(marca, str):
                primera = primera or marca
                ultima = marca
            mensaje = obj.get("message") if isinstance(obj.get("message"), dict) else None
            if mensaje is None:
                continue
            rol = mensaje.get("role") or obj.get("type")
            if rol not in ("user", "assistant"):
                continue
            texto, herramientas, rs, solo_resultados = contenido_a_texto(mensaje.get("content"))
            rutas.extend(rs)
            if rol == "user" and solo_resultados:
                continue
            if not texto and not herramientas:
                continue
            turnos.append((rol, texto, herramientas))
    return turnos, rutas, primera, ultima


def recortar(texto, maximo):
    if len(texto) <= maximo:
        return texto
    return texto[:maximo] + f"\n\n[… recortado: {len(texto) - maximo} caracteres más en la copia cruda]"


def escribir_extracto(ses_dir, sesion, evento, ticket, transcripcion, turnos, rutas, primera, ultima, maximo):
    fecha = (primera or dt.datetime.now().isoformat())[:10]
    lineas = [
        "---",
        f"sesion: {sesion}",
        f"ticket: {ticket}",
        f"evento: {evento}",
        f"inicio: {primera or '?'}",
        f"ultimo_mensaje: {ultima or '?'}",
        f"guardado: {dt.datetime.now().isoformat(timespec='seconds')}",
        f"copia_cruda: raw/{sesion}.jsonl.gz",
        "---",
        f"# Sesión {fecha} · {sesion[:8]}",
        "",
        "Extracto automático (hooks PreCompact/SessionEnd). La interpretación de lo ocurrido va en la bitácora.",
        "",
    ]
    cambios, vistos = [], set()
    for herramienta, ruta in rutas:
        if herramienta in HERRAMIENTAS_QUE_ESCRIBEN and ruta not in vistos:
            vistos.add(ruta)
            cambios.append(f"- `{ruta}` ({herramienta})")
    if cambios:
        lineas += ["## Archivos modificados", *cambios, ""]
    lineas.append("## Conversación")
    for rol, texto, herramientas in turnos:
        quien = "Humano" if rol == "user" else "Claude"
        if texto:
            lineas.append(f"**{quien}:** {recortar(texto, maximo)}")
        if herramientas:
            conteo = Counter(herramientas)
            lineas.append("_(herramientas: " + ", ".join(f"{n} ×{c}" if c > 1 else n for n, c in conteo.items()) + ")_")
        lineas.append("")
    escribir(ses_dir / f"{fecha}_{sesion[:8]}.md", "\n".join(lineas))


def regenerar_indice(ses_dir):
    filas = ["# Índice de sesiones", "", "| Archivo | Evento | Inicio |", "|---|---|---|"]
    for md in sorted(ses_dir.glob("*.md")):
        if md.name == "INDICE.md":
            continue
        cabecera = md.read_text(encoding="utf-8", errors="replace")[:800]
        evento = re.search(r"(?m)^evento: (.*)$", cabecera)
        inicio = re.search(r"(?m)^inicio: (.*)$", cabecera)
        filas.append(f"| [[{md.stem}]] | {evento.group(1) if evento else '?'} | {inicio.group(1) if inicio else '?'} |")
    escribir(ses_dir / "INDICE.md", "\n".join(filas) + "\n")


def main():
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8")
        except Exception:
            pass
    cfg = config()
    datos = sys.stdin.read()
    entrada = json.loads(datos) if datos.strip() else {}
    transcripcion = entrada.get("transcript_path")
    sesion = re.sub(r"[^A-Za-z0-9_-]", "_", entrada.get("session_id") or "sin-id")
    evento = entrada.get("hook_event_name", "?")
    if not transcripcion or not Path(transcripcion).exists():
        print(f"guardar_sesion: no hay transcripción ({transcripcion})", file=sys.stderr)
        return
    base, ticket = destino(cfg)
    ses_dir = base / "sesiones"
    (ses_dir / "raw").mkdir(parents=True, exist_ok=True)
    turnos, rutas, primera, ultima = extraer(transcripcion)
    escribir_extracto(ses_dir, sesion, evento, ticket, transcripcion, turnos, rutas, primera, ultima,
                      int(cfg["max_chars_mensaje_sesion"]))
    with open(transcripcion, "rb") as origen, gzip.open(ses_dir / "raw" / f"{sesion}.jsonl.gz", "wb") as copia:
        shutil.copyfileobj(origen, copia)
    regenerar_indice(ses_dir)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"guardar_sesion: {exc}", file=sys.stderr)
    sys.exit(0)
