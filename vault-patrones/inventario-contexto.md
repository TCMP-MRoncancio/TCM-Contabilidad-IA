# Inventario de `contexto/`

> Generado como parte del Bloque 3 (evidencia contra la macro). Documenta que hay en `contexto/`, de donde sale y que prueba respalda cada afirmacion. `contexto/` es solo lectura; este inventario vive en `vault-patrones/` porque es conocimiento curado, no material crudo.

## Fuente original

**Archivo:** `Cargador_Datos_v21.xlsm` ("Cargador de Datos K+TP & K+")
**Hoja relevante:** `Account`
**Macro relevante:** `Accounts()`, modulo `Modulo2`
**Registros de ejemplo:** 621 cuentas reales, columnas `ShortName`, `Name`, `ChartOfAccount`, `AccountType`, `ValuationType`, `ImputMode`

Este archivo contiene otras 7 hojas/macros (SSI_Cpty, SSI_Entity, BIC, BankAccount, BankAccount_LBTR, Corresp, CustAccounts) que generan otros tipos de archivo para Kondor -- fuera del alcance de este repositorio, que solo cubre `Account` (chart of accounts).

**Advertencia de contenido sensible:** la hoja `Manual` y otras hojas del Excel contienen datos reales de produccion (numeros de cuenta bancaria, codigos SWIFT, identificadores de contrapartes). Si se coloca el Excel completo en `contexto/`, confirmar que el repositorio es privado y que nadie con acceso no autorizado puede verlo.

## Primera prueba -- 621 registros de ejemplo (contra RECONSTRUCCION del formato, no evidencia valida por si sola)

| Metrica | Resultado |
|---|---|
| Total de cuentas de la muestra | 621 |
| Coinciden byte a byte | 621 |
| Rechazadas indebidamente por el validador | 0 |
| Con diferencias reales | 0 |
| **Porcentaje de coincidencia** | **100.00%** |

## Segunda prueba -- 11 casos reales exportados por la macro (EVIDENCIA VALIDA, versionada como fixture automatizado)

Esta es la evidencia que respalda la afirmacion de equivalencia con la macro. Los 11 casos quedaron anonimizados en herramientas/tests/fixtures/macro/ y se verifican automaticamente en cada corrida de test_generador_cuentas.py -- no es solo un analisis puntual, es una prueba de regresion permanente.

El consultor aporto 11 archivos `.xml` reales, generados por la macro `Accounts()` en uso productivo (nombres de cuenta como "CONTINGENCIA DERECHO 208" a "218", proyecto `RD_UNICA`). Se parsearon, se pasaron por `validar_estructural` + `validar_reglas_negocio`, y se comparo el XML que produce `generar_xml()` contra el contenido real, byte a byte.

| Metrica | Resultado |
|---|---|
| Casos reales analizados | 11 |
| Pasan la validacion sin errores | 11/11 |
| Contenido identico (ignorando fin de linea) | 11/11 |
| **Hallazgo:** fin de linea real de la macro | **CRLF** (`\r\n`), no LF |

**Decision tomada con esta evidencia:** el script se actualizo para escribir con `newline="\r\n"` (antes usaba `"\n"`, marcado explicitamente como pendiente de confirmar en el Bloque 2). Con el cambio aplicado, el script reproduce los 11 casos reales **byte a byte, de forma exacta**, no solo en contenido.

## Que NO cubre esta prueba (limites honestos)

- Los 621 registros de ejemplo y los 11 casos reales usan **un unico valor** para `ChartOfAccount_Id` (`RD_UNICA`), `AccountType` (`B`), `ValuationType` (`N`) e `InputMode` (`C`). La prueba confirma que el generador reproduce fielmente estos valores -- **no** confirma el comportamiento con otros proyectos (Scotia, Alpha) ni otros valores de enum, porque esos casos no existen en la muestra.
- No hay evidencia de que Kondor efectivamente acepte el XML generado -- esta prueba compara contra la macro (la herramienta anterior), no contra una carga real en Kondor. Eso es Bloque 4.
- Los 11 archivos reales no se incorporaron al repositorio ni a la suite de pruebas automatizadas, porque contienen nombres de cuenta de produccion -- decision pendiente del consultor sobre si deben anonimizarse antes de versionarse como fixture de prueba permanente.

## Pendiente de tu parte (Bloque 3, segun tu instruccion original)

1. Decide si el Excel completo va a `contexto/Cargador_Datos_v21.xlsm` (tiene datos sensibles de otras hojas) o si prefieres mantenerlo solo local, fuera de git.
2. Decide si los 11 XML reales se anonimizan para quedar como fixture de prueba permanente, o se mantienen fuera del repositorio.