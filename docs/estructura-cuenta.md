# Estructura de una Cuenta (Chart of Accounts) — Kondor K+ / K+TP

> Reemplaza al XML generado por la macro `Accounts()` del archivo
> `Cargador_Datos_v21.xlsm` (hoja `Account`, módulo `Modulo2`). Este documento
> es la versión "traducida a texto" de esa lógica, para que Claude la use como
> referencia en vez del Excel.

## Campos (en el orden exacto que exige el XML de salida)

| # | Campo | Columna en el Excel original | Tipo XML | Obligatorio | Formato / Reglas |
|---|---|---|---|---|---|
| 1 | `Account_ShortName` | `ShortName` | string | Sí | Numérico, **16 dígitos** (según los 621 registros de ejemplo del Excel original) |
| 2 | `Account_Name` | `Name` | string | Sí | Texto libre, descriptivo |
| 3 | `ChartOfAccount_Id` | `ChartOfAccount` | string | Sí | **Identifica el proyecto/entidad** al que pertenece la cuenta (ej. Scotia, Alpha, RD_UNICA...). No tiene un valor por defecto — varía según el proyecto, y siempre debe preguntarse. Ver `docs/catalogo-proyectos.md` para la lista de proyectos confirmados |
| 4 | `AccountType` | `AccountType` | enum | Sí | En el Excel original, todas las filas usan `B`. **[CONFIRMAR]** el significado y los demás valores válidos de este enum con la documentación de Kondor o el equipo que mantiene el Excel — no está documentado dentro del propio archivo |
| 5 | `ValuationType` | `ValuationType` | enum | Sí | En el Excel original, todas las filas usan `N`. **[CONFIRMAR]** significado y valores válidos |
| 6 | `InputMode` | `ImputMode` (sic, así está escrito en el Excel) | enum | Sí | En el Excel original, todas las filas usan `C`. **[CONFIRMAR]** significado y valores válidos |

## Por qué hay campos marcados [CONFIRMAR]

El archivo Excel original (`Cargador_Datos_v21.xlsm`) solo contiene **un** valor para `AccountType`, `ValuationType` e `InputMode` en las 621 cuentas de ejemplo — es decir, nunca se ve variación real en los datos, así que no se puede inferir el dominio completo de valores válidos solo mirando el Excel. La pestaña `Manual` del archivo tampoco los documenta (solo contiene un catálogo de bancos/BIC, no de estos enums).

`ChartOfAccount_Id` es un caso distinto: **no es un enum de valor casi-fijo, es el identificador del proyecto/entidad** (Scotia, Alpha, RD_UNICA, etc.) y varía legítimamente cuenta por cuenta. Su catálogo vive aparte, en `docs/catalogo-proyectos.md` (y su copia para validación automática en `schemas/catalogo_proyectos.json`), porque se espera que crezca con el tiempo a medida que se confirmen más proyectos.

**Antes de usar este estándar en producción**, alguien del equipo que sabe cómo se parametrizó Kondor debe completar la tabla de valores válidos abajo para `AccountType`, `ValuationType` e `InputMode`. Mientras tanto, Claude debe usar por defecto los mismos valores que aparecen en el Excel (`B` / `N` / `C`) y **preguntar explícitamente** si el usuario pide algo distinto — nunca inventar un valor de enum que no esté confirmado aquí. Para `ChartOfAccount_Id`, Claude nunca debe asumir un default — siempre debe preguntar a qué proyecto pertenece la cuenta (ver `docs/catalogo-proyectos.md`).

### Valores válidos confirmados (completar)

| Enum | Valores válidos | Significado |
|---|---|---|
| `AccountType` | `B`, [AGREGAR] | [DEFINIR] |
| `ValuationType` | `N`, [AGREGAR] | [DEFINIR] |
| `InputMode` | `C`, [AGREGAR] | [DEFINIR] |

> `ChartOfAccount_Id` (proyecto) tiene su propio catálogo en `docs/catalogo-proyectos.md` — no se lista aquí porque se espera que crezca con más frecuencia que estos tres.

## Preguntas que Claude debe hacer, en este orden

1. **¿Para qué proyecto/entidad es esta cuenta?** (`ChartOfAccount_Id`) — obligatorio, sin default. Validar contra `docs/catalogo-proyectos.md`; si no está en el catálogo, avisar que hay que confirmarlo/agregarlo antes de continuar, no generar la cuenta con un código no confirmado.
2. Nombre descriptivo de la cuenta (`Account_Name`)
3. Número de cuenta (`Account_ShortName`) — si el usuario no lo da, **no lo inventes ni lo autonumeres** salvo que el estándar real de la empresa defina una regla de numeración (no documentada todavía en este repo)
4. Tipo de cuenta, tipo de valoración y modo de entrada — usar los defaults de la tabla de arriba y confirmar con el usuario si aplica un valor distinto

## Formato exacto del archivo de salida

Un archivo `.xml` por cuenta, nombrado `[Account_ShortName].xml`, con este formato (sin indentación, tal como lo genera la macro original):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Account>
<Account_ShortName type="string">2310101000006001</Account_ShortName>
<Account_Name type="string">Cuentas CAD 01</Account_Name>
<ChartOfAccount_Id type="string">RD_UNICA</ChartOfAccount_Id>
<AccountType type="enum">B</AccountType>
<ValuationType type="enum">N</ValuationType>
<InputMode type="enum">C</InputMode>
</Account>
```

## Nota sobre el resto del Excel

`Cargador_Datos_v21.xlsm` genera, además de cuentas, otros 7 tipos de archivo (SSI_Cpty, SSI_Entity, BIC, BankAccount, BankAccount_LBTR, Corresp, CustAccounts) — cada uno con su propia pestaña y su propia macro. Este repositorio, por ahora, solo cubre `Account` (chart of accounts). Si más adelante se necesita replicar los otros generadores, aplica el mismo proceso: documentar la pestaña + macro correspondiente en un nuevo archivo `docs/estructura-[tipo].md`.
