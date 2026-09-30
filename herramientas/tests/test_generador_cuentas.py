#!/usr/bin/env python3
"""
Pruebas de regresion para herramientas/generar_cuenta_xml.py.

Corre en cada Pull Request via .github/workflows/validar-generador-cuentas.yml.
Si algo aqui falla, el PR no se puede fusionar.

Cubre dos cosas:
1. El comportamiento del generador (duplicados, formato, catalogos) - PASS 1-7.
2. Que los ".md" de vault-patrones/ y el codigo (VALORES_CONFIRMADOS,
   catalogo_proyectos.json) no se hayan desincronizado - PASS 8-9. Esto es
   justo lo que fallo el 29/09/2026: una reestructuracion dejo el codigo y
   la documentacion diciendo cosas distintas, y nadie lo noto hasta que
   Claude Code lo leyo con cuidado despues del hecho.
"""

import re
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import generar_cuenta_xml as gen

CUENTA_BASE = {
    "Account_ShortName": "9999999999990001",
    "Account_Name": "Cuenta de prueba ci",
    "ChartOfAccount_Id": "RD_UNICA",
    "AccountType": "B",
    "ValuationType": "N",
    "InputMode": "C",
}

ESTRUCTURA_MD = gen.REPO_ROOT / "vault-patrones" / "kondor" / "cuentas" / "estructura-cuenta.md"
CATALOGO_PROYECTOS_MD = gen.REPO_ROOT / "vault-patrones" / "kondor" / "cuentas" / "catalogo-proyectos.md"

fallos = []
archivos_generados = []


def check(nombre, condicion, detalle=""):
    estado = "PASS" if condicion else "FAIL"
    print(f"[{estado}] {nombre}" + (f" - {detalle}" if detalle and not condicion else ""))
    if not condicion:
        fallos.append(nombre)


def limpiar():
    for ruta in archivos_generados:
        ruta.unlink(missing_ok=True)


def extraer_valores_confirmados_md() -> dict:
    """Lee la tabla 'Valores validos confirmados' de estructura-cuenta.md.
    Solo cuenta una fila si el nombre del enum esta en backticks como
    PRIMERA columna (asi no se confunde con la tabla de campos, donde el
    enum aparece en la segunda columna)."""
    texto = ESTRUCTURA_MD.read_text(encoding="utf-8-sig")
    resultado = {}
    for linea in texto.splitlines():
        m = re.match(r"^\|\s*`(\w+)`\s*\|\s*(.+?)\s*\|\s*.*\|\s*$", linea)
        if not m:
            continue
        enum_nombre, celda_valores = m.groups()
        valores = {v for v in re.findall(r"`([^`]+)`", celda_valores)}
        if valores:
            resultado[enum_nombre] = valores
    return resultado


def extraer_proyectos_confirmados_md() -> set:
    """Lee la tabla de catalogo-proyectos.md. Solo cuenta una fila si la
    PRIMERA columna es un codigo entre backticks (las filas con [AGREGAR]
    como primera columna son proyectos aun sin confirmar, se ignoran)."""
    texto = CATALOGO_PROYECTOS_MD.read_text(encoding="utf-8-sig")
    codigos = set()
    for linea in texto.splitlines():
        m = re.match(r"^\|\s*`([^`]+)`\s*\|", linea)
        if m:
            codigos.add(m.group(1))
    return codigos


def main():
    schema = gen.cargar_schema()

    # --- 1. Cuenta valida se genera ---
    cuenta = dict(CUENTA_BASE)
    ok = gen.procesar_cuenta(cuenta, schema)
    ruta = gen.SALIDAS_DIR / f"{cuenta['Account_ShortName']}.xml"
    archivos_generados.append(ruta)
    check("Cuenta valida se genera", ok and ruta.exists())

    # --- 2. Duplicado sin --forzar se rechaza ---
    errores = gen.validar(cuenta, schema, permitir_duplicados=False)
    check(
        "Duplicado sin --forzar se rechaza",
        any("duplicados" in e for e in errores),
        f"errores: {errores}",
    )

    # --- 3. Duplicado CON --forzar se permite ---
    ok_forzado = gen.procesar_cuenta(cuenta, schema, permitir_duplicados=True)
    check("Duplicado con --forzar se sobrescribe", ok_forzado)

    # --- 4. AccountType no confirmado se rechaza ---
    cuenta_tipo_malo = dict(CUENTA_BASE, Account_ShortName="9999999999990002", AccountType="Z")
    errores = gen.validar(cuenta_tipo_malo, schema)
    check(
        "AccountType no confirmado se rechaza",
        any("valores confirmados" in e for e in errores),
        f"errores: {errores}",
    )

    # --- 5. Nombre con caracteres especiales se rechaza ---
    cuenta_nombre_malo = dict(CUENTA_BASE, Account_ShortName="9999999999990003", Account_Name="Cuenta Ñoña #1")
    errores = gen.validar(cuenta_nombre_malo, schema)
    check(
        "Nombre con tildes/especiales se rechaza",
        any("tildes" in e for e in errores),
        f"errores: {errores}",
    )

    # --- 6. Numero de cuenta de largo incorrecto se rechaza ---
    cuenta_largo_malo = dict(CUENTA_BASE, Account_ShortName="12345")
    errores = gen.validar(cuenta_largo_malo, schema)
    check(
        "Numero de cuenta de largo incorrecto se rechaza",
        any("digitos" in e for e in errores),
        f"errores: {errores}",
    )

    # --- 7. Proyecto no confirmado se rechaza ---
    cuenta_proyecto_malo = dict(CUENTA_BASE, Account_ShortName="9999999999990004", ChartOfAccount_Id="PROYECTO_INVENTADO")
    errores = gen.validar(cuenta_proyecto_malo, schema)
    check(
        "Proyecto no confirmado se rechaza",
        any("catalogo de proyectos" in e for e in errores),
        f"errores: {errores}",
    )

    limpiar()

    # --- 8. VALORES_CONFIRMADOS del script coincide con estructura-cuenta.md ---
    valores_md = extraer_valores_confirmados_md()
    for enum_nombre, valores_script in gen.VALORES_CONFIRMADOS.items():
        valores_doc = valores_md.get(enum_nombre)
        check(
            f"'{enum_nombre}' en el script coincide con estructura-cuenta.md",
            valores_doc is not None and valores_doc == valores_script,
            f"script={valores_script} vs md={valores_doc}",
        )
    for enum_nombre in valores_md:
        check(
            f"'{enum_nombre}' documentado en el .md tambien existe en el script",
            enum_nombre in gen.VALORES_CONFIRMADOS,
            f"'{enum_nombre}' esta en estructura-cuenta.md pero no en VALORES_CONFIRMADOS del script",
        )

    # --- 9. catalogo_proyectos.json coincide con catalogo-proyectos.md ---
    proyectos_json = gen.cargar_proyectos_validos()
    proyectos_doc = extraer_proyectos_confirmados_md()
    check(
        "catalogo_proyectos.json coincide con catalogo-proyectos.md",
        proyectos_json == proyectos_doc,
        f"json={proyectos_json} vs md={proyectos_doc}",
    )

    print()
    if fallos:
        print(f"RESULTADO: {len(fallos)} prueba(s) fallaron: {fallos}")
        sys.exit(1)
    else:
        print("RESULTADO: todas las pruebas pasaron.")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        limpiar()
        print("ERROR INESPERADO durante las pruebas:")
        traceback.print_exc()
        sys.exit(1)