#!/usr/bin/env python3
"""
Pruebas de regresion para herramientas/generar_cuenta_xml.py.
Corre en cada Pull Request via .github/workflows/validar-generador-cuentas.yml.
Usa una carpeta TEMPORAL (no Account/ real).
"""

import json
import re
import shutil
import sys
import tempfile
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
_tmpdir = None


def check(nombre, condicion, detalle=""):
    estado = "PASS" if condicion else "FAIL"
    print(f"[{estado}] {nombre}" + (f" - {detalle}" if detalle and not condicion else ""))
    if not condicion:
        fallos.append(nombre)


def usar_carpeta_temporal():
    global _tmpdir
    _tmpdir = Path(tempfile.mkdtemp(prefix="test_generador_cuentas_"))
    gen.SALIDAS_DIR = _tmpdir / "Account"
    gen.REPORTES_DIR = _tmpdir / "reportes"
    gen.REPORTE_PATH = gen.REPORTES_DIR / "reporte_cuentas.xlsx"


def limpiar():
    if _tmpdir and _tmpdir.exists():
        shutil.rmtree(_tmpdir, ignore_errors=True)


def extraer_valores_confirmados_md() -> dict:
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
    texto = CATALOGO_PROYECTOS_MD.read_text(encoding="utf-8-sig")
    codigos = set()
    for linea in texto.splitlines():
        m = re.match(r"^\|\s*`([^`]+)`\s*\|", linea)
        if m:
            codigos.add(m.group(1))
    return codigos


def main():
    usar_carpeta_temporal()
    schema = gen.cargar_schema()

    cuenta = dict(CUENTA_BASE)
    errores = gen.validar_estructural(cuenta, schema)
    ok = len(errores) == 0
    if ok:
        gen.escribir_cuenta(cuenta, permitir_duplicados=False)
    ruta = gen.SALIDAS_DIR / f"{cuenta['Account_ShortName']}.xml"
    check("Cuenta valida se genera", ok and ruta.exists())

    errores = gen.validar_reglas_negocio(cuenta, permitir_duplicados=False, nombres_vistos_en_lote=set())
    check(
        "Duplicado sin --forzar se rechaza",
        any("duplicados" in e for e in errores),
        f"errores: {errores}",
    )

    contenido_original = ruta.read_text(encoding="utf-8")
    gen.escribir_cuenta(cuenta, permitir_duplicados=True)
    ruta_bak = ruta.with_suffix(ruta.suffix + ".bak")
    check(
        "Duplicado con --forzar se sobrescribe y crea .bak",
        ruta.exists() and ruta_bak.exists() and ruta_bak.read_text(encoding="utf-8") == contenido_original,
    )

    cuenta_tipo_malo = dict(CUENTA_BASE, Account_ShortName="9999999999990002", AccountType="Z")
    errores = gen.validar_reglas_negocio(cuenta_tipo_malo, False, set())
    check(
        "AccountType no confirmado se rechaza",
        any("valores confirmados" in e for e in errores),
        f"errores: {errores}",
    )

    cuenta_nombre_malo = dict(CUENTA_BASE, Account_ShortName="9999999999990003", Account_Name="Cuenta Ñoña #1")
    errores = gen.validar_estructural(cuenta_nombre_malo, schema)
    check(
        "Nombre con tildes/especiales se rechaza (estructural)",
        len(errores) > 0,
        f"errores: {errores}",
    )

    cuenta_nombre_vacio = dict(CUENTA_BASE, Account_ShortName="9999999999990004", Account_Name="   ")
    errores = gen.validar_reglas_negocio(cuenta_nombre_vacio, False, set())
    check(
        "Nombre solo espacios se rechaza",
        any("vacio" in e or "espacios" in e for e in errores),
        f"errores: {errores}",
    )

    cuenta_largo_malo = dict(CUENTA_BASE, Account_ShortName="12345")
    errores = gen.validar_estructural(cuenta_largo_malo, schema)
    check(
        "Numero de cuenta de largo incorrecto se rechaza (estructural)",
        len(errores) > 0,
        f"errores: {errores}",
    )

    cuenta_shortname_numerico = dict(CUENTA_BASE, Account_ShortName=9999999999990005, Account_Name="Cuenta numerica")
    try:
        errores = gen.validar_estructural(cuenta_shortname_numerico, schema)
        check(
            "Account_ShortName no-texto da error claro (sin excepcion)",
            len(errores) > 0,
            f"errores: {errores}",
        )
    except Exception as e:
        check("Account_ShortName no-texto da error claro (sin excepcion)", False, f"lanzo excepcion: {e!r}")

    cuenta_proyecto_malo = dict(CUENTA_BASE, Account_ShortName="9999999999990006", ChartOfAccount_Id="PROYECTO_INVENTADO")
    errores = gen.validar_reglas_negocio(cuenta_proyecto_malo, False, set())
    check(
        "Proyecto no confirmado se rechaza",
        any("catalogo de proyectos" in e for e in errores),
        f"errores: {errores}",
    )

    cuenta_campo_extra = dict(CUENTA_BASE, Account_ShortName="9999999999990007", campo_inventado="algo")
    errores = gen.validar_estructural(cuenta_campo_extra, schema)
    check(
        "Campo adicional no declarado se rechaza (additionalProperties)",
        len(errores) > 0,
        f"errores: {errores}",
    )

    lote_mixto = [
        dict(CUENTA_BASE, Account_ShortName="9999999999990010", Account_Name="Cuenta lote valida"),
        dict(CUENTA_BASE, Account_ShortName="123", Account_Name="Cuenta lote invalida"),
    ]
    entrada_lote = _tmpdir / "lote_mixto.json"
    entrada_lote.write_text(json.dumps(lote_mixto), encoding="utf-8")
    codigo_salida = _correr_main_como_subproceso_simulado(entrada_lote)
    archivo_deberia_no_existir = gen.SALIDAS_DIR / "9999999999990010.xml"
    check(
        "Lote con una cuenta invalida no genera NINGUN archivo (atomico)",
        codigo_salida != 0 and not archivo_deberia_no_existir.exists(),
    )

    lote_duplicado_interno = [
        dict(CUENTA_BASE, Account_ShortName="9999999999990011", Account_Name="Cuenta lote uno"),
        dict(CUENTA_BASE, Account_ShortName="9999999999990011", Account_Name="Cuenta lote dos repetida"),
    ]
    entrada_lote2 = _tmpdir / "lote_dup_interno.json"
    entrada_lote2.write_text(json.dumps(lote_duplicado_interno), encoding="utf-8")
    codigo_salida2 = _correr_main_como_subproceso_simulado(entrada_lote2)
    check(
        "Duplicado dentro del mismo lote rechaza el lote completo",
        codigo_salida2 != 0,
    )

    cuenta_newline = dict(CUENTA_BASE, Account_ShortName="9999999999990012")
    ruta_nl = gen.escribir_cuenta(cuenta_newline, permitir_duplicados=False)
    contenido_bytes = ruta_nl.read_bytes()
    check(
        "Archivo generado usa CRLF (coincide con la macro original)",
        contenido_bytes.count(b"\n") == contenido_bytes.count(b"\r\n") and b"\r\n" in contenido_bytes,
    )

    cuenta_peligrosa = {
        "Account_ShortName": "9999999999990013",
        "Account_Name": "Cuenta con amp",
        "ChartOfAccount_Id": "RD_UNICA & Co <script>",
        "AccountType": "B",
        "ValuationType": "N",
        "InputMode": "C",
    }
    xml_generado = gen.generar_xml(cuenta_peligrosa)
    check(
        "Valores se escapan en el XML (sin '<' ni '&' crudos del dato)",
        "<script>" not in xml_generado and "RD_UNICA & Co" not in xml_generado,
        f"xml: {xml_generado}",
    )

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

    proyectos_json = gen.cargar_proyectos_validos()
    proyectos_doc = extraer_proyectos_confirmados_md()
    check(
        "catalogo_proyectos.json coincide con catalogo-proyectos.md",
        proyectos_json == proyectos_doc,
        f"json={proyectos_json} vs md={proyectos_doc}",
    )

    limpiar()

    print()
    if fallos:
        print(f"RESULTADO: {len(fallos)} prueba(s) fallaron: {fallos}")
        sys.exit(1)
    else:
        print("RESULTADO: todas las pruebas pasaron.")
        sys.exit(0)


def _correr_main_como_subproceso_simulado(archivo_entrada: Path) -> int:
    argv_original = sys.argv
    sys.argv = ["generar_cuenta_xml.py", str(archivo_entrada)]
    try:
        gen.main()
        return 0
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    finally:
        sys.argv = argv_original


if __name__ == "__main__":
    try:
        main()
    except Exception:
        limpiar()
        print("ERROR INESPERADO durante las pruebas:")
        traceback.print_exc()
        sys.exit(1)