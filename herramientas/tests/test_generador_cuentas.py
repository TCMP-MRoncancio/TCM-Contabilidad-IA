#!/usr/bin/env python3
"""
Pruebas de regresion para herramientas/generar_cuenta_xml.py.

Corre en cada Pull Request via .github/workflows/validar-generador-cuentas.yml.
Si algo aqui falla, el PR no se puede fusionar - esto es justo lo que hubiera
atrapado la regresion del 29/09/2026 donde se perdio la validacion de
duplicados durante una reestructuracion de carpetas.

Usa numeros de cuenta reservados para pruebas (empiezan en 9999999999) que
nunca deberian colisionar con datos reales, y limpia los archivos que genera
al terminar, sin importar si las pruebas pasan o fallan.
"""

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