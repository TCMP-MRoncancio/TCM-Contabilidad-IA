# Instrucciones para Claude Code en este repositorio

Este repositorio es la fuente de verdad para la creación de cuentas contables (chart of accounts) de Kondor K+/K+TP. Sigue estas reglas siempre que el usuario pida crear, revisar o validar una cuenta.

## Antes de generar cualquier cuenta

Lee, en este orden:
1. `docs/estructura-cuenta.md` — qué campos lleva la cuenta y en qué formato
2. `docs/naturaleza-cuentas.md` — para determinar si la cuenta es deudora o acreedora según su tipo
3. `docs/catalogo-proyectos.md` — para validar el proyecto/entidad (ChartOfAccount_Id)
4. `docs/catalogo-paises-bonos.md` — para validar valores de país/bono/moneda si aplica

No inventes campos ni valores que no estén en estos documentos. Si el usuario da un valor que no aparece en el catálogo permitido, pregúntale antes de continuar — no asumas ni corrijas en silencio.

## Qué preguntar si falta información

Si el usuario no da todos los campos obligatorios definidos en `docs/estructura-cuenta.md`, pregunta uno por uno los que falten. No generes el archivo con campos vacíos o inventados.

**Pregunta siempre primero a qué proyecto/entidad pertenece la cuenta** (`ChartOfAccount_Id` — ej. Scotia, Alpha, RD_UNICA). Nunca asumas un proyecto por defecto: es un campo que varía por definición. Valídalo contra `docs/catalogo-proyectos.md`; si el proyecto no está confirmado ahí, dile al usuario que primero hay que agregarlo al catálogo vía Pull Request — no generes la cuenta con un proyecto sin confirmar, aunque suene plausible.

## Reglas de formato obligatorias

- **`Account_Name` no puede contener tildes ni caracteres especiales** — solo letras sin acento (A-Z), números y espacios. Si el usuario da un nombre con tildes o símbolos, corrígelo tú mismo a la versión sin tildes/símbolos y avísale del cambio (no se lo preguntes como si fuera opcional, es una regla fija del estándar).
- **`Account_ShortName` debe tener el mismo largo que las demás cuentas del catálogo** — actualmente 16 dígitos numéricos, según los 621 registros de ejemplo del Excel original. Si el usuario da un número con otra cantidad de dígitos, no lo generes: avísale del largo esperado y pídele que lo corrija.

## Al generar el archivo de salida

1. Arma el registro con las 6 claves exactas de `schemas/cuenta.schema.json` (`Account_ShortName`, `Account_Name`, `ChartOfAccount_Id`, `AccountType`, `ValuationType`, `InputMode`).
2. Escribe esos datos a un `.json` temporal y ejecuta `scripts/generar_cuenta_xml.py` sobre ese archivo — el script valida contra el schema (incluye los valores de enum confirmados, el catálogo de proyectos, el formato de nombre y el largo del número de cuenta) y, si pasa, genera el XML.
3. El script ya replica el formato exacto que producía la macro `Accounts()` del Excel original (`Cargador_Datos_v21.xlsm`) — no reformatees ni reordenes el XML manualmente.
4. El resultado queda en `Account/[Account_ShortName].xml`.
5. Muestra al usuario un resumen de la cuenta creada (no solo "listo", sino los valores que quedaron), y si el script rechazó algún valor por no estar confirmado o no cumplir el formato, explícaselo con claridad — no reintentes forzando el valor.

## Qué NO hacer

- No modifiques `docs/`, `schemas/` ni `CLAUDE.md` a menos que el usuario lo pida explícitamente y confirme que quiere proponer un cambio al estándar (en ese caso, sugiere hacerlo vía Pull Request, no directo en `main`).
- No generes cuentas duplicadas sin avisar si detectas que ya existe una similar en `Account/`.
- No calcules ni asumas tasas, montos o cualquier dato de un movimiento financiero — este repositorio es solo para datos estáticos (la cuenta en sí), no para transacciones.

## Cómo ejecutar Python en este equipo

En esta máquina, el comando `python` no está disponible de forma confiable en el PATH. Usa siempre la ruta completa al ejecutable en vez de `python` o `python3`:

C:\Users\JoséMateoRoncancioMa\AppData\Local\Programs\Python\Python312\python.exe scripts\generar_cuenta_xml.py <archivo>

