#!/usr/bin/env python3
"""Hook SessionStart: inyecta en el contexto el estado del ticket activo.

Se configura en .claude/settings.json para los eventos startup, resume, clear y compact.
Lee .claude/arnes.json (rutas) y .claude/activo.local.json ({"cliente": "...", "ticket": "..."}).
Imprime por stdout un resumen corto del ESTADO.md del ticket activo y las ultimas entradas de su
bitacora; Claude Code agrega ese texto al contexto. Si no hay ticket activo, lista los abiertos.
Nunca falla: ante cualquier error imprime un aviso y termina con codigo 0.
"""
import json
import os
import re
import sys
from pathlib import Path

RAIZ = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
DEFECTOS = {
    "puntero_activo": ".claude/activo.local.json",
    "dir_cliente": "vault-cliente-{cliente}",
    "dir_tickets": "vault-cliente-{cliente}/tickets",
    "dir_ticket": "vault-cliente-{cliente}/tickets/{ticket}",
    "dir_diseno": "vault-cliente-{cliente}/tickets/{ticket}/diseno",
    "archivo_estado": "ESTADO.md",
    "archivo_bitacora": "bitacora.md",
    "campos_cabecera": ["titulo", "fase", "control_pendiente", "actualizado"],
    "secciones_estado": ["Próximo paso", "Bloqueos", "Preguntas abiertas", "En curso"],
    "prefijo_fase_cerrada": "7",
    "max_lineas_seccion": 12,
    "max_entradas_bitacora": 2,
    "max_chars_entrada": 900,
}


def config():
    cfg = dict(DEFECTOS)
    ruta = RAIZ / ".claude" / "arnes.json"
    if ruta.exists():
        cfg.update(json.loads(ruta.read_text(encoding="utf-8")))
    return cfg


def salida_utf8():
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8")
        except Exception:
            pass


def leer_entrada():
    try:
        datos = sys.stdin.read()
        return json.loads(datos) if datos.strip() else {}
    except Exception:
        return {}


def leer_frontmatter(texto):
    meta, cuerpo = {}, texto
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", texto, re.S)
    if m:
        for linea in m.group(1).splitlines():
            if ":" in linea and not linea.strip().startswith("#"):
                clave, valor = linea.split(":", 1)
                meta[clave.strip()] = valor.strip().strip('"').strip("'")
        cuerpo = m.group(2)
    return meta, cuerpo


def normalizar(texto):
    return texto.strip().lower().translate(str.maketrans("áéíóúñÁÉÍÓÚÑ", "aeiounAEIOUN"))


def secciones(cuerpo):
    res, actual, buf = {}, None, []
    for linea in cuerpo.splitlines():
        if linea.startswith("## "):
            if actual is not None:
                res[actual] = "\n".join(buf).strip()
            actual, buf = normalizar(linea[3:]), []
        elif actual is not None:
            buf.append(linea)
    if actual is not None:
        res[actual] = "\n".join(buf).strip()
    return res


def recortar(texto, max_lineas):
    lineas = [l for l in texto.splitlines() if l.strip()]
    if not lineas:
        return "(vacío)"
    if len(lineas) > max_lineas:
        resto = len(lineas) - max_lineas
        lineas = lineas[:max_lineas] + [f"… ({resto} líneas más en el archivo)"]
    return "\n".join(lineas)


def ultimas_entradas(ruta, cantidad, max_chars):
    if not ruta.exists():
        return "(sin bitácora)"
    texto = ruta.read_text(encoding="utf-8", errors="replace")
    partes = re.split(r"(?m)^## ", texto)
    entradas = ["## " + p.strip() for p in partes[1:] if p.strip()]
    if not entradas:
        return "(sin entradas todavía)"
    salida = []
    for entrada in entradas[-cantidad:]:
        salida.append(entrada if len(entrada) <= max_chars else entrada[:max_chars] + " …")
    return "\n\n".join(salida)


def clientes(cfg):
    patron = cfg["dir_cliente"]
    regex = re.compile("^" + re.escape(patron).replace(re.escape("{cliente}"), "(?P<c>[^/]+)") + "$")
    res = []
    for d in sorted(RAIZ.glob(patron.replace("{cliente}", "*"))):
        m = regex.match(d.relative_to(RAIZ).as_posix())
        if d.is_dir() and m:
            res.append(m.group("c"))
    return res


def tickets_abiertos(cfg):
    filas = []
    for cliente in clientes(cfg):
        base = RAIZ / cfg["dir_tickets"].format(cliente=cliente)
        for estado in sorted(base.glob("*/" + cfg["archivo_estado"])):
            ticket = estado.parent.name
            if ticket.startswith("_"):
                continue
            meta, _ = leer_frontmatter(estado.read_text(encoding="utf-8", errors="replace"))
            if meta.get("fase", "").startswith(cfg["prefijo_fase_cerrada"]):
                continue
            filas.append(f"- {cliente} / {ticket} · fase {meta.get('fase', '?')} · {meta.get('titulo', '')}")
    return filas


def main():
    salida_utf8()
    cfg = config()
    origen = leer_entrada().get("source", "inicio")
    print(f"# Contexto del proyecto (cargado automáticamente · {origen})")
    activo = None
    puntero = RAIZ / cfg["puntero_activo"]
    if puntero.exists():
        try:
            activo = json.loads(puntero.read_text(encoding="utf-8"))
        except Exception:
            activo = None
    if activo and activo.get("cliente") and activo.get("ticket"):
        cliente, ticket = activo["cliente"], activo["ticket"]
        tdir = RAIZ / cfg["dir_ticket"].format(cliente=cliente, ticket=ticket)
        estado = tdir / cfg["archivo_estado"]
        if estado.exists():
            meta, cuerpo = leer_frontmatter(estado.read_text(encoding="utf-8", errors="replace"))
            sec = secciones(cuerpo)
            print(f"Ticket activo: **{ticket}** · cliente **{cliente}**")
            for campo in cfg["campos_cabecera"]:
                print(f"{campo}: {meta.get(campo, '?')}")
            print(f"Carpeta del ticket: {tdir.relative_to(RAIZ).as_posix()}/ · "
                  f"Diseño: {cfg['dir_diseno'].format(cliente=cliente, ticket=ticket)}/")
            for titulo in cfg["secciones_estado"]:
                clave = normalizar(titulo)
                if clave in sec:
                    print(f"\n## {titulo}\n{recortar(sec[clave], cfg['max_lineas_seccion'])}")
            print("\n## Últimas entradas de la bitácora")
            print(ultimas_entradas(tdir / cfg["archivo_bitacora"], cfg["max_entradas_bitacora"], cfg["max_chars_entrada"]))
            print("\n---\nProtocolo: confirma con el humano en qué seguimos; actualiza ESTADO.md en cada control "
                  "y ejecuta /cierre antes de terminar.")
            return
        print(f"El puntero apunta a {cliente}/{ticket}, pero no existe {tdir.relative_to(RAIZ).as_posix()}/{cfg['archivo_estado']}.")
    else:
        print("No hay ticket activo.")
    filas = tickets_abiertos(cfg)
    if filas:
        print("\nTickets abiertos:")
        print("\n".join(filas))
    else:
        print("No se encontraron tickets abiertos (¿están clonados los vaults de cliente?).")
    print("\nPregunta al humano en qué ticket trabajar y usa /ticket para activarlo o crearlo.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"(Aviso: no se pudo cargar el estado del ticket: {exc})")
    sys.exit(0)
