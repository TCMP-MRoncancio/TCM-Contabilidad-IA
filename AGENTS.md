# TCM Contabilidad IA

Proyecto de TCM Partners para generar cuentas contables (chart of accounts) de Kondor K+/K+TP mediante Claude Code, con memoria persistente y estandares versionados.
El consultor decide y aplica en el servidor; el agente pregunta, valida y genera.

## Reglas duras

1. **Si falta un dato, pregunta en vez de inventar.** Vale para numero de cuenta, proyecto, tipo de cuenta y cualquier valor de catalogo. Todo lo que afirmes sobre el estandar lleva fuente (vault-patrones/) o se marca como candidato sin confirmar.
2. **Apunta por tu cuenta lo que convenga recordar**, en el lugar que corresponde (ver "Donde se anota que").
3. **Nunca sobrescribes un .xml existente sin --forzar explicito**, y nunca uses --forzar por iniciativa propia: avisa primero que la cuenta ya existe y pregunta si de verdad se quiere reemplazar.
4. **`contexto/` es solo lectura.** Es la fuente cruda de documentacion de Kondor/Finastra; lo curado y confirmado vive en `vault-patrones/`.
5. **Una cuenta se genera solo con datos validados**: proyecto confirmado en el catalogo, formato de nombre sin tildes/especiales, numero de cuenta del largo esperado, y enums (AccountType/ValuationType/InputMode) dentro de los valores confirmados. Un valor sin confirmar se detiene y se documenta en `vault-patrones/candidatos/`, nunca se inventa ni se fuerza.
6. **Nombres en ASCII.** `Account_Name` solo letras sin acento, numeros y espacios.
7. **No se generan cuentas de un proyecto no confirmado.** Si el proyecto no esta en `vault-patrones/kondor/cuentas/catalogo-proyectos.md`, se detiene y se propone agregarlo (via Pull Request) antes de continuar.
8. **No se tocan cuentas ya cargadas a Kondor.** Este repositorio solo genera archivos nuevos para carga; no modifica ni elimina nada dentro de Kondor.
9. **Git remoto lo opera el consultor**: crear ramas, hacer push, abrir y aprobar Pull Requests.
10. **Los permisos de `.claude/settings.json` no se modifican sin aprobacion escrita del consultor.**

## Mapa del proyecto

| Carpeta | Que es | Quien escribe |
|---|---|---|
| `contexto/` | Documentacion Kondor/Finastra, manuales y ejemplos de referencia | Nadie (solo lectura) |
| `vault-patrones/` | Estandar de creacion de cuentas, con nivel de madurez | Solo via Pull Request; propuestas van a `candidatos/` |
| `vault-proyecto-<proyecto>/` | Datos de cada proyecto/entidad (RD_UNICA, y a futuro otros) | Se actualiza al confirmar un proyecto nuevo |
| `herramientas/` | `generar_cuenta_xml.py`: valida y genera los XML | Solo con aprobacion |
| `schemas/` | JSON Schema y catalogo de proyectos que usa la herramienta | Solo via Pull Request |
| `Account/` | Archivos .xml generados, listos para cargar a Kondor | Generado por la herramienta, no se edita a mano |
| `reportes/` | Reporte Excel consolidado de todas las cuentas en `Account/` | Generado por la herramienta |
| `memoria/` | Decisiones y lecciones del proyecto | Se actualiza durante el trabajo |
| `.claude/` | Permisos y configuracion de Claude Code | Solo con aprobacion |

## Donde se anota que

| Que | Donde |
|---|---|
| Estandar de campos y formato de una cuenta | `vault-patrones/kondor/cuentas/estructura-cuenta.md` |
| Naturaleza deudora/acreedora por tipo | `vault-patrones/kondor/cuentas/naturaleza-cuentas.md` |
| Proyectos/entidades confirmados | `vault-patrones/kondor/cuentas/catalogo-proyectos.md` |
| Valores de enum aun sin confirmar | `vault-patrones/candidatos/enums-pendientes.md` |
| Datos de un proyecto especifico | `vault-proyecto-<proyecto>/proyecto.md` |
| Decisiones de como trabajamos | `memoria/decisiones.md` |
| Problemas y su solucion | `memoria/lecciones.md` |

## Herramientas

- `python herramientas/generar_cuenta_xml.py <archivo.json> [--forzar]`

## Flujo de trabajo actual (sin tickets todavia)

1. El consultor pide, en lenguaje natural, crear una o varias cuentas.
2. Claude lee `vault-patrones/kondor/cuentas/` para conocer el estandar vigente.
3. Claude arma el JSON con los datos, corre la herramienta, y reporta el resultado (generadas, rechazadas y por que).
4. El consultor copia los `.xml` de `Account/` a la ruta real de Kondor y confirma la carga.
5. Si algo nuevo se confirma (un proyecto, un valor de enum), se propone el cambio a `vault-patrones/` via Pull Request, nunca se asume sobre la marcha.