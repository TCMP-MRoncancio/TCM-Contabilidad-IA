#!/usr/bin/env python3
"""Hook Stop (opcional): recuerda actualizar ESTADO.md antes de terminar.

Si en alguna de las carpetas de "vigilar_cambios_en" (.claude/arnes.json) del ticket activo hay archivos
mas nuevos que su ESTADO.md, bloquea UNA sola vez por sesion (codigo 2) y pide actualizar el estado o
ejecutar /cierre. La marca de "ya avisado" queda en .claude/.marcas/ (ignorada por git).
Ante cualquier error, deja terminar (codigo 0).
"""
import json
import os
import sys
from pathlib import Path

RAIZ = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
DEFECTOS = {
    "puntero_activo": ".claude/activo.local.json",
    "dir_ticket": "vault-cliente-{cliente}/tickets/{ticket}",
    "dir_diseno": "vault-cliente-{cliente}/tickets/{ticket}/diseno",
    "archivo_estado": "ESTADO.md",
    "vigilar_cambios_en": ["{dir_diseno}", "{dir_ticket}/salida", "{dir_ticket}/entrega"],
}


def config():
    cfg = dict(DEFECTOS)
    ruta = RAIZ / ".claude" / "arnes.json"
    if ruta.exists():
        cfg.update(json.loads(ruta.read_text(encoding="utf-8")))
    return cfg


def main():
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8")
        except Exception:
            pass
    datos = sys.stdin.read()
    entrada = json.loads(datos) if datos.strip() else {}
    if entrada.get("stop_hook_active"):
        return 0
    cfg = config()
    try:
        activo = json.loads((RAIZ / cfg["puntero_activo"]).read_text(encoding="utf-8"))
    except Exception:
        return 0
    valores = {"cliente": activo["cliente"], "ticket": activo["ticket"]}
    valores["dir_ticket"] = cfg["dir_ticket"].format(**valores)
    valores["dir_diseno"] = cfg["dir_diseno"].format(**valores)
    estado = RAIZ / valores["dir_ticket"] / cfg["archivo_estado"]
    if not estado.exists():
        return 0
    marca = RAIZ / ".claude" / ".marcas" / f"cierre-{entrada.get('session_id', 'x')}"
    if marca.exists():
        return 0
    ultimo = 0
    for plantilla in cfg["vigilar_cambios_en"]:
        carpeta = RAIZ / plantilla.format(**valores)
        if carpeta.exists():
            ultimo = max([ultimo] + [p.stat().st_mtime for p in carpeta.rglob("*") if p.is_file()])
    if ultimo > estado.stat().st_mtime:
        marca.parent.mkdir(parents=True, exist_ok=True)
        marca.write_text("1", encoding="utf-8")
        print("Hay cambios en el ticket que no están en ESTADO.md. "
              "Actualiza ESTADO.md (o ejecuta /cierre) antes de terminar.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    try:
        codigo = main()
    except Exception:
        codigo = 0
    sys.exit(codigo)
