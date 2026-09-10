# Instrucciones para Claude Code en este repositorio

Este repositorio es la fuente de verdad para la creación de cuentas contables (chart of accounts) de [NOMBRE DE LA EMPRESA]. Sigue estas reglas siempre que el usuario pida crear, revisar o validar una cuenta.

## Antes de generar cualquier cuenta

Lee, en este orden:
1. `docs/estructura-cuenta.md` — qué campos lleva la cuenta y en qué formato
2. `docs/naturaleza-cuentas.md` — para determinar si la cuenta es deudora o acreedora según su tipo
3. `docs/catalogo-paises-bonos.md` — para validar que los valores de país/bono/moneda que use el usuario existen en el catálogo permitido

No inventes campos ni valores que no estén en estos documentos. Si el usuario da un valor que no aparece en el catálogo permitido, pregúntale antes de continuar — no asumas ni corrijas en silencio.

## Qué preguntar si falta información

Si el usuario no da todos los campos obligatorios definidos en `docs/estructura-cuenta.md`, pregunta uno por uno los que falten. No generes el archivo con campos vacíos o inventados.

**Pregunta siempre primero a qué proyecto/entidad pertenece la cuenta** (`ChartOfAccount_Id` — ej. Scotia, Alpha, RD_UNICA). Nunca asumas un proyecto por defecto: es un campo que varía por definición. Valídalo contra `docs/catalogo-proyectos.md`; si el proyecto no está confirmado ahí, dile al usuario que primero hay que agregarlo al catálogo vía Pull Request — no generes la cuenta con un proyecto sin confirmar, aunque suene plausible.

## Al generar el archivo de salida

1. Arma el registro con las 6 claves exactas de `schemas/cuenta.schema.json` (`Account_ShortName`, `Account_Name`, `ChartOfAccount_Id`, `AccountType`, `ValuationType`, `InputMode`).
2. Escribe esos datos a un `.json` temporal y ejecuta `scripts/generar_cuenta_xml.py` sobre ese archivo — el script valida contra el schema (incluye los valores de enum confirmados) y, si pasa, genera el XML.
3. El script ya replica el formato exacto que producía la macro `Accounts()` del Excel original (`Cargador_Datos_v21.xlsm`) — no reformatees ni reordenes el XML manualmente.
4. El resultado queda en `salidas/[Account_ShortName].xml`.
5. Muestra al usuario un resumen de la cuenta creada (no solo "listo", sino los valores que quedaron), y si el script rechazó algún valor de enum por no estar confirmado, explícaselo con claridad — no reintentes forzando el valor.

## Qué NO hacer

- No modifiques `docs/`, `schemas/` ni `CLAUDE.md` a menos que el usuario lo pida explícitamente y confirme que quiere proponer un cambio al estándar (en ese caso, sugiere hacerlo vía Pull Request, no directo en `main`).
- No generes cuentas duplicadas sin avisar si detectas que ya existe una similar en `salidas/`.
- No calcules ni asumas tasas, montos o cualquier dato de un movimiento financiero — este repositorio es solo para datos estáticos (la cuenta en sí), no para transacciones.
