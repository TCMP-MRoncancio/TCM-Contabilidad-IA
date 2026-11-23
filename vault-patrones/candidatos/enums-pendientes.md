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

## Proyecto Banistmo (pendiente, 2026-11-11)

El consultor reporto un proyecto llamado Banistmo con este ejemplo (fila copiada del Excel de carga):

| ShortName | Name | ChartOfAccount | AccountType | ValuationType | ImputMode |
|---|---|---|---|---|---|
| '707201020201020101 | CControlDivExt-RepoAbtoPJ_Corden | Banistmo | B | N | C |

Choca con el estandar vigente en tres puntos:

1. **Proyecto**: `Banistmo` no esta en `catalogo-proyectos.md` ni en `schemas/catalogo_proyectos.json`. Falta confirmar el codigo exacto en Kondor (mayusculas/minusculas, `Banistmo` vs `BANISTMO`).
2. **Largo del ShortName**: el ejemplo tiene **18 digitos**; el schema exige exactamente 16 (`^[0-9]{16}$`). Pendiente: ¿el largo es fijo por proyecto (16 RD_UNICA, 18 Banistmo) o variable? El apostrofo inicial (`'`) parece ser solo el marcador de texto de Excel, no parte del valor - confirmar.
3. **Caracteres en Account_Name**: el ejemplo usa `-` y `_`; la regla actual (AGENTS.md regla 6 y schema `^[A-Za-z0-9 ]+$`) solo permite letras, numeros y espacios. Pendiente: ¿Kondor acepta `-` y `_` en el nombre?

Los enums (B / N / C) coinciden con los ya confirmados.

**Confirmado por el consultor (2026-11-11):**
- Codigo de proyecto: `Banistmo` (exacto, con esa capitalizacion).
- ShortName de Banistmo: entre **18 y 20 digitos**. Es el **unico** proyecto con ese largo; el resto sigue en 16.
- El apostrofo inicial es solo el marcador de texto de Excel; **no** forma parte del valor.
- Account_Name: se permite **guion bajo (`_`)** como separador alternativo; el **guion medio (`-`) no** se permite (confirmado 2026-11-11). El ejemplo `CControlDivExt-RepoAbtoPJ_Corden` debe reescribirse sin `-` antes de cargarse.

**Resuelto.** Aplicado en: catalogo (md + json), `largo_short_name` en `schemas/catalogo_proyectos.json` + validacion en el script, schema (`^[0-9]{16,20}$` y `^[A-Za-z0-9 _]+$`), `estructura-cuenta.md` y AGENTS.md regla 6. Pruebas en `herramientas/tests/test_generador_cuentas.py`.
