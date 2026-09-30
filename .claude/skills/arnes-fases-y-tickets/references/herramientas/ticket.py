#!/usr/bin/env python3
"""Gestion de clientes y tickets de un arnes.

Uso (desde la raiz del arnes):
  python herramientas/ticket.py listar
  python herramientas/ticket.py estado
  python herramientas/ticket.py activar <cliente> <ticket>
  python herramientas/ticket.py crear <cliente> <ticket> --titulo "..." [--jira CLAVE] [--dato clave=valor ...]
  python herramientas/ticket.py nuevo-cliente <cliente>

Lee las rutas de .claude/arnes.json (ver arnes-plantilla.json). Solo usa la biblioteca estandar.
Escribe siempre con final de linea LF. Nunca borra ni sobrescribe un archivo existente.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

DEFECTOS = {
    "puntero_activo": ".claude/activo.local.json",
    "dir_cliente": "vault-cliente-{cliente}",
    "dir_tickets": "vault-cliente-{cliente}/tickets",
    "dir_ticket": "vault-cliente-{cliente}/tickets/{ticket}",
    "dir_diseno": "vault-cliente-{cliente}/tickets/{ticket}/diseno",
    "archivo_estado": "ESTADO.md",
    "archivo_bitacora": "bitacora.md",
    "plantilla_cliente": "herramientas/plantillas/vault-cliente",
    "plantilla_ticket": "herramientas/plantillas/ticket",
    "prefijo_fase_cerrada": "7",
}
NOMBRE_VALIDO = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


def config():
    cfg = dict(DEFECTOS)
    ruta = RAIZ / ".claude" / "arnes.json"
    if ruta.exists():
        cfg.update(json.loads(ruta.read_text(encoding="utf-8")))
    return cfg


def ruta(cfg, clave, **valores):
    return RAIZ / cfg[clave].format(**valores)


def escribir(destino, texto):
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)


def leer_frontmatter(texto):
    meta = {}
    m = re.match(r"^---\s*\n(.*?)\n---", texto, re.S)
    if m:
        for linea in m.group(1).splitlines():
            if ":" in linea and not linea.strip().startswith("#"):
                clave, valor = linea.split(":", 1)
                meta[clave.strip()] = valor.strip().strip('"').strip("'")
    return meta


def validar_nombre(tipo, nombre):
    if not NOMBRE_VALIDO.match(nombre):
        sys.exit(f"Error: {tipo} '{nombre}' no es valido (ASCII, sin espacios, hasta 64 caracteres).")


def copiar_plantilla(origen, destino, valores):
    """Copia la plantilla reemplazando {{CLAVE}}. No pisa archivos que ya existen."""
    if not origen.exists():
        sys.exit(f"Error: no existe la plantilla {origen.relative_to(RAIZ)}")
    creados = []
    for archivo in sorted(origen.rglob("*")):
        rel = archivo.relative_to(origen)
        objetivo = destino / rel
        if archivo.is_dir():
            objetivo.mkdir(parents=True, exist_ok=True)
            continue
        if objetivo.exists():
            continue
        texto = archivo.read_text(encoding="utf-8")
        for clave, valor in valores.items():
            texto = texto.replace("{{" + clave + "}}", valor)
        escribir(objetivo, texto)
        creados.append(objetivo)
    return creados


def listar_clientes(cfg):
    patron = cfg["dir_cliente"]
    regex = re.compile("^" + re.escape(patron).replace(re.escape("{cliente}"), "(?P<c>[^/]+)") + "$")
    clientes = []
    for d in sorted(RAIZ.glob(patron.replace("{cliente}", "*"))):
        m = regex.match(d.relative_to(RAIZ).as_posix())
        if d.is_dir() and m:
            clientes.append(m.group("c"))
    return clientes


def tickets(cfg, incluir_cerrados=True):
    filas = []
    for cliente in listar_clientes(cfg):
        dt_dir = ruta(cfg, "dir_tickets", cliente=cliente)
        for estado in sorted(dt_dir.glob("*/" + cfg["archivo_estado"])):
            ticket = estado.parent.name
            if ticket.startswith("_"):
                continue
            meta = leer_frontmatter(estado.read_text(encoding="utf-8", errors="replace"))
            cerrado = meta.get("fase", "").startswith(cfg["prefijo_fase_cerrada"])
            if cerrado and not incluir_cerrados:
                continue
            filas.append((cliente, ticket, meta))
    return filas


def activo(cfg):
    p = RAIZ / cfg["puntero_activo"]
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def cmd_listar(cfg, _args):
    filas = tickets(cfg)
    if not filas:
        print("No hay tickets. Crear uno con: python herramientas/ticket.py crear <cliente> <ticket> --titulo \"...\"")
        return
    act = activo(cfg) or {}
    for cliente, ticket, meta in filas:
        marca = "*" if (act.get("cliente"), act.get("ticket")) == (cliente, ticket) else " "
        print(f"{marca} {cliente} / {ticket} · fase {meta.get('fase', '?')} · {meta.get('titulo', '')}")


def cmd_estado(cfg, _args):
    act = activo(cfg)
    if not act:
        print("No hay ticket activo. Usar: python herramientas/ticket.py activar <cliente> <ticket>")
        return
    estado = ruta(cfg, "dir_ticket", **act) / cfg["archivo_estado"]
    if not estado.exists():
        print(f"El ticket activo {act['cliente']}/{act['ticket']} no tiene {cfg['archivo_estado']}.")
        return
    print(estado.read_text(encoding="utf-8", errors="replace"))


def cmd_activar(cfg, args):
    tdir = ruta(cfg, "dir_ticket", cliente=args.cliente, ticket=args.ticket)
    if not (tdir / cfg["archivo_estado"]).exists():
        sys.exit(f"Error: no existe {tdir.relative_to(RAIZ)}/{cfg['archivo_estado']}")
    escribir(RAIZ / cfg["puntero_activo"],
             json.dumps({"cliente": args.cliente, "ticket": args.ticket}, ensure_ascii=False) + "\n")
    print(f"Ticket activo: {args.cliente} / {args.ticket}")


def cmd_nuevo_cliente(cfg, args):
    validar_nombre("cliente", args.cliente)
    destino = ruta(cfg, "dir_cliente", cliente=args.cliente)
    creados = copiar_plantilla(RAIZ / cfg["plantilla_cliente"], destino,
                               {"CLIENTE": args.cliente, "FECHA": dt.date.today().isoformat()})
    ruta(cfg, "dir_tickets", cliente=args.cliente).mkdir(parents=True, exist_ok=True)
    print(f"Cliente {args.cliente}: {len(creados)} archivos creados en {destino.relative_to(RAIZ)}")
    print("Completar cliente.md con el humano y crear el repo del vault (lo hace el humano).")


def cmd_crear(cfg, args):
    validar_nombre("cliente", args.cliente)
    validar_nombre("ticket", args.ticket)
    if not ruta(cfg, "dir_cliente", cliente=args.cliente).exists():
        sys.exit(f"Error: no existe el cliente {args.cliente}. Crearlo con: nuevo-cliente {args.cliente}")
    tdir = ruta(cfg, "dir_ticket", cliente=args.cliente, ticket=args.ticket)
    if (tdir / cfg["archivo_estado"]).exists():
        sys.exit(f"Error: el ticket {args.ticket} ya existe en {tdir.relative_to(RAIZ)}")
    diseno = ruta(cfg, "dir_diseno", cliente=args.cliente, ticket=args.ticket)
    valores = {
        "CLIENTE": args.cliente,
        "TICKET": args.ticket,
        "TITULO": args.titulo,
        "JIRA": args.jira or "por definir",
        "FECHA": dt.date.today().isoformat(),
        "DIR_TICKET": tdir.relative_to(RAIZ).as_posix(),
        "DIR_DISENO": diseno.relative_to(RAIZ).as_posix(),
    }
    for par in args.dato or []:
        if "=" not in par:
            sys.exit(f"Error: --dato espera clave=valor (recibido: {par})")
        clave, valor = par.split("=", 1)
        valores[clave.strip().upper()] = valor.strip()
    creados = copiar_plantilla(RAIZ / cfg["plantilla_ticket"], tdir, valores)
    diseno.mkdir(parents=True, exist_ok=True)
    estado = tdir / cfg["archivo_estado"]
    if estado.exists():
        os.utime(estado)  # ESTADO queda como el archivo mas nuevo del alta (lo usa el hook de cierre)
    pendientes = set()
    for archivo in creados:
        pendientes.update(re.findall(r"\{\{([A-Z0-9_]+)\}\}", archivo.read_text(encoding="utf-8")))
    print(f"Ticket {args.ticket} creado en {tdir.relative_to(RAIZ)} ({len(creados)} archivos).")
    if pendientes:
        print("Marcadores sin valor (pasarlos con --dato CLAVE=valor o completarlos a mano): " + ", ".join(sorted(pendientes)))
    cmd_activar(cfg, args)


def main():
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8")
        except Exception:
            pass
    p = argparse.ArgumentParser(description="Clientes y tickets del arnes")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("listar")
    sub.add_parser("estado")
    a = sub.add_parser("activar")
    a.add_argument("cliente")
    a.add_argument("ticket")
    n = sub.add_parser("nuevo-cliente")
    n.add_argument("cliente")
    c = sub.add_parser("crear")
    c.add_argument("cliente")
    c.add_argument("ticket")
    c.add_argument("--titulo", required=True)
    c.add_argument("--jira")
    c.add_argument("--dato", action="append", help="clave=valor para un marcador {{CLAVE}} de las plantillas")
    args = p.parse_args()
    cfg = config()
    {"listar": cmd_listar, "estado": cmd_estado, "activar": cmd_activar,
     "nuevo-cliente": cmd_nuevo_cliente, "crear": cmd_crear}[args.cmd](cfg, args)


if __name__ == "__main__":
    main()
