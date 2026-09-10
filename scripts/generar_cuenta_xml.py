#!/usr/bin/env python3
"""
Genera archivos XML de cuentas (chart of accounts) para Kondor K+/K+TP,
replicando EXACTAMENTE la salida de la macro `Accounts()` del archivo
`Cargador_Datos_v21.xlsm` (hoja "Account", modulo "Modulo2").

Uso:
    python scripts/generar_cuenta_xml.py cuentas.json

El JSON de entrada puede ser un solo objeto o una lista de objetos, cada
uno con las claves de schemas/cuenta.schema.json, por ejemplo:

{
  "Account_ShortName": "2310101000006001",
  "Account_Name": "Cuentas CAD 01",
  "ChartOfAccount_Id": "RD_UNICA",
  "AccountType": "B",
  "ValuationType": "N",
  "InputMode": "C"
}

Cada cuenta genera un archivo <Account_ShortName>.xml en /salidas,
igual que la macro original generaba uno junto al Excel. Además, genera un
<Account_ShortName>.xlsx con los mismos datos, solo para revisión humana
(Kondor K+/K+TP sigue consumiendo el .xml; el .xlsx no lo reemplaza).
"""

import json
import sys
from pathlib import Path

from openpyxl import Workbook

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "cuenta.schema.json"
CATALOGO_PROYECTOS_PATH = REPO_ROOT / "schemas" / "catalogo_proyectos.json"
SALIDAS_DIR = REPO_ROOT / "salidas"

# Valores confirmados para los enums de estructura fija (no varían por proyecto).
# Actualizar esta lista cuando el equipo confirme el dominio real de cada uno.
VALORES_CONFIRMADOS = {
    "AccountType": {"B"},
    "ValuationType": {"N"},
    "InputMode": {"C"},
}


def cargar_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def cargar_proyectos_validos() -> set:
    """ChartOfAccount_Id identifica un proyecto/entidad (Scotia, Alpha, RD_UNICA...)
    y crece con el tiempo, por eso vive en su propio catalogo JSON en vez de
    estar hardcodeado junto a los demas enums."""
    with open(CATALOGO_PROYECTOS_PATH, "r", encoding="utf-8") as f:
        datos = json.load(f)
    return set(datos.get("proyectos_validos", []))


def validar(cuenta: dict, schema: dict) -> list:
    errores = []

    for campo in schema["required"]:
        if campo not in cuenta or cuenta[campo] in (None, ""):
            errores.append(f"Falta el campo obligatorio: {campo}")

    short_name = cuenta.get("Account_ShortName", "")
    if short_name and not (short_name.isdigit() and len(short_name) == 16):
        errores.append(
            f"Account_ShortName debe ser numérico de 16 dígitos, se recibió: "
            f"'{short_name}' ({len(short_name)} caracteres)"
        )

    for campo, valores_ok in VALORES_CONFIRMADOS.items():
        valor = cuenta.get(campo)
        if valor and valor not in valores_ok:
            errores.append(
                f"'{campo}' = '{valor}' no está en la lista de valores confirmados "
                f"{sorted(valores_ok)}. Si es un valor nuevo y válido, agrégalo a "
                f"docs/estructura-cuenta.md y a VALORES_CONFIRMADOS en este script "
                f"antes de usarlo (no generar el archivo con un valor sin confirmar)."
            )

    proyecto = cuenta.get("ChartOfAccount_Id")
    if proyecto:
        proyectos_validos = cargar_proyectos_validos()
        if proyecto not in proyectos_validos:
            errores.append(
                f"ChartOfAccount_Id = '{proyecto}' no está en el catálogo de proyectos "
                f"confirmados {sorted(proyectos_validos)}. Si es un proyecto nuevo y "
                f"real (ej. Scotia, Alpha), agrégalo primero a docs/catalogo-proyectos.md "
                f"y a schemas/catalogo_proyectos.json vía Pull Request — no generar la "
                f"cuenta con un proyecto sin confirmar."
            )

    return errores


def generar_xml(cuenta: dict) -> str:
    """Reproduce carácter por carácter el formato que escribía la macro VBA
    (mismo orden de tags, mismos atributos type, sin indentación)."""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<Account>\n"
        f'<Account_ShortName type="string">{cuenta["Account_ShortName"]}</Account_ShortName>\n'
        f'<Account_Name type="string">{cuenta["Account_Name"]}</Account_Name>\n'
        f'<ChartOfAccount_Id type="string">{cuenta["ChartOfAccount_Id"]}</ChartOfAccount_Id>\n'
        f'<AccountType type="enum">{cuenta["AccountType"]}</AccountType>\n'
        f'<ValuationType type="enum">{cuenta["ValuationType"]}</ValuationType>\n'
        f'<InputMode type="enum">{cuenta["InputMode"]}</InputMode>\n'
        "</Account>\n"
    )


def generar_xlsx(cuenta: dict, ruta: Path) -> None:
    """Copia de solo lectura humana de la cuenta, en formato Excel real.
    No es el archivo que consume Kondor — ese sigue siendo el .xml."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Account"
    campos = [
        "Account_ShortName",
        "Account_Name",
        "ChartOfAccount_Id",
        "AccountType",
        "ValuationType",
        "InputMode",
    ]
    ws.append(campos)
    ws.append([cuenta[campo] for campo in campos])
    wb.save(ruta)


def procesar_cuenta(cuenta: dict, schema: dict) -> bool:
    errores = validar(cuenta, schema)
    if errores:
        print(f"❌ Cuenta '{cuenta.get('Account_ShortName', '?')}' NO pasó la validación:")
        for e in errores:
            print(f"   - {e}")
        return False

    SALIDAS_DIR.mkdir(exist_ok=True)
    ruta_xml = SALIDAS_DIR / f"{cuenta['Account_ShortName']}.xml"
    ruta_xml.write_text(generar_xml(cuenta), encoding="utf-8")
    print(f"✅ Generado: {ruta_xml}")

    ruta_xlsx = SALIDAS_DIR / f"{cuenta['Account_ShortName']}.xlsx"
    generar_xlsx(cuenta, ruta_xlsx)
    print(f"✅ Generado (revisión humana): {ruta_xlsx}")
    return True


def main():
    if len(sys.argv) != 2:
        print("Uso: python scripts/generar_cuenta_xml.py cuentas.json")
        sys.exit(1)

    entrada = Path(sys.argv[1])
    if not entrada.exists():
        print(f"No se encontró el archivo: {entrada}")
        sys.exit(1)

    with open(entrada, "r", encoding="utf-8") as f:
        datos = json.load(f)

    cuentas = datos if isinstance(datos, list) else [datos]
    schema = cargar_schema()

    ok = sum(procesar_cuenta(c, schema) for c in cuentas)
    print(f"\n{ok}/{len(cuentas)} cuentas generadas correctamente.")
    sys.exit(0 if ok == len(cuentas) else 1)


if __name__ == "__main__":
    main()
