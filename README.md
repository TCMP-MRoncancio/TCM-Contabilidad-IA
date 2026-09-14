# Repositorio de Estándares — Creación de Cuentas (Chart of Accounts)

## Qué es esto

Fuente única de verdad para la creación de **datos estáticos financieros** (cuentas contables y, a futuro, breakdowns y otros apartados). Contiene los estándares que Claude usa para generar archivos de salida validados a partir de una solicitud en lenguaje natural.

Una cuenta es un dato maestro: no cambia con cada movimiento financiero. Un movimiento (transaccional) siempre apunta a una cuenta que ya existe en el catálogo, con un sentido (débito/crédito) definido por la naturaleza de esa cuenta. Este repositorio gobierna la creación de esas cuentas — no los movimientos.

## Estructura

```
docs/                       Estándares en lenguaje natural (fuente de verdad para Claude)
  estructura-cuenta.md        Campos, formato y XML de salida — basado en la macro Accounts() del Excel original
  naturaleza-cuentas.md       Reglas de naturaleza deudora/acreedora por tipo de cuenta (movimientos, no cuentas)
  catalogo-paises-bonos.md    Valores permitidos (países, tipos de bono, etc.) — pendiente de uso futuro
schemas/
  cuenta.schema.json          Mismo estándar de estructura-cuenta.md, en JSON Schema (para validación dura)
scripts/
  generar_cuenta_xml.py       Valida un borrador de cuenta y genera el XML — replica byte a byte la macro Accounts() del Excel original
salidas/                     Carpeta donde caen los .xml generados (no versionar los resultados finales)
CLAUDE.md                    Instrucciones que Claude Code carga automáticamente al abrir este repo
```

## Origen de este estándar

La estructura de `docs/estructura-cuenta.md` y `schemas/cuenta.schema.json` se extrajo directamente de la macro VBA `Accounts()` del archivo `Cargador_Datos_v21.xlsm` (Cargador de Datos K+TP & K+), que hasta ahora era la forma manual de generar estas cuentas. `scripts/generar_cuenta_xml.py` fue probado y produce un XML **idéntico** al que generaba esa macro. El Excel original queda como referencia histórica, no como la fuente de verdad — a partir de ahora, `docs/` y `schemas/` lo son.

**Pendiente:** los enums `AccountType`, `ValuationType`, `ChartOfAccount_Id` e `InputMode` solo tienen un valor confirmado cada uno (el que aparece en los datos de ejemplo del Excel). Antes de usar esto en producción con cuentas de otros tipos, el equipo debe completar el dominio real de valores válidos en `docs/estructura-cuenta.md`.

## Cómo se usa (piloto actual)

1. Clona el repo y ábrelo en VS Code con la extensión de Claude Code.
2. Pídele a Claude, en lenguaje natural, que cree una cuenta (ej. *"crea la cuenta para cliente corporativo, tipo activo, país Colombia"*).
3. Claude lee `docs/*.md`, arma el archivo siguiendo el estándar, y opcionalmente corre `scripts/validar_cuenta.py` para validarlo.
4. El archivo generado queda en `Account/`.

## Gobernanza

- **Solo lectura / clonación** para el resto de la organización.
- Cambios a `docs/` o `schemas/` **solo vía Pull Request**, revisados por el equipo dueño del estándar (ver `CODEOWNERS`).
- Nadie edita estos archivos directamente en `main`.

## Roadmap

- [x] Fase 0 — Piloto local: Claude Code + `.md` + validación manual (donde estamos ahora)
- [ ] Fase 1 — Formalizar `docs/` en Skills (`SKILL.md` con frontmatter YAML)
- [ ] Fase 2 — Backend vía API + validación automática dura antes de cada salida
- [ ] Fase 3 — Interfaz accesible para toda la organización (chatbot conectado, sin necesidad de VS Code)

## Nota de gobernanza pendiente

Actualmente el �nico CODEOWNER es \@TCMP-MRoncancio\, lo que significa que la misma persona que propone un cambio tambi�n lo aprueba � v�lido para el arranque del piloto en solitario, pero elimina el prop�sito real de la revisi�n. **Antes de usar este repositorio para generar cuentas que se carguen a producci�n**, sumar al menos un segundo revisor a \CODEOWNERS\, para que ning�n cambio a los est�ndares se apruebe sin una segunda persona.


