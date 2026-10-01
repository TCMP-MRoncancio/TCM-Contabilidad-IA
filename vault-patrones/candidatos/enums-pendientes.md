# Candidatos pendientes de confirmar

## Enums de estructura-cuenta.md

`AccountType`, `ValuationType` e `InputMode` solo tienen UN valor confirmado cada uno (B / N / C), tomado de los 621 registros de ejemplo del Excel original (`Cargador_Datos_v21.xlsm`). No se conoce el dominio completo.

**No promover a vault-patrones/kondor/cuentas/estructura-cuenta.md hasta confirmar con alguien que conozca la parametrizacion real de Kondor.**

## Proyectos (ChartOfAccount_Id)

Scotia y Alpha fueron mencionados como proyectos existentes, pero no se ha confirmado el codigo exacto que usan en Kondor. Ver `vault-patrones/kondor/cuentas/catalogo-proyectos.md`.
## Espacios al inicio/fin de Account_Name (pendiente, 2026-10-01)

No se sabe si la macro original recorta (trim), rechaza, o conserva espacios al inicio o al final de `Account_Name`. Hasta confirmarlo, `herramientas/generar_cuenta_xml.py` **rechaza** estos casos explicando el motivo (no asume ningun comportamiento).

**Pregunta para el consultor:** ¿la macro recorta, rechaza o conserva los espacios al inicio/fin del nombre?

Cuando se confirme, actualizar `validar_reglas_negocio()` en el script y esta nota.