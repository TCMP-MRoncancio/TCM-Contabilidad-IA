---
name: arnes-memoria-y-sesiones
description: "Paso 7 de construir un arnes: memoria por capas en archivos, hooks que cargan el estado al iniciar y guardan la conversacion al compactar o cerrar, skills /cierre y /recuperar-contexto, sesiones cortas, traspaso a otra persona y colaboracion con un revisor (Cowork). Usar al instalar o reparar la memoria de un arnes, cuando se pierde lo hablado entre sesiones, cuando una sesion se corta o cuando hay que entregar el trabajo a otra persona. No usar para el conocimiento del dominio (eso es arnes-conocimiento)."
---

# Memoria y sesiones (paso 7)

**Objetivo:** que cualquier sesión nueva, o cualquier persona nueva, sepa dónde está cada ticket, qué se hizo y por qué, sin
leer conversaciones anteriores. La memoria es **automática** (hooks) y **disciplinada** (`/cierre`).
**Entrada:** estructura (paso 2), seguimiento por ticket y `.claude/arnes.json` (paso 4).
**Salida:** hooks instalados y probados; skills `/cierre` y `/recuperar-contexto`; protocolo de sesión en AGENTS.md.
**Archivos listos para copiar:** `references/hooks/` (tres scripts en Python con biblioteca estándar y el bloque de `settings.json`),
`references/skill-cierre-plantilla.md`, `references/skill-recuperar-contexto-plantilla.md`.

## Las capas de memoria

De lo más resumido a lo más crudo. Se lee en este orden y se para cuando la pregunta queda respondida.

| # | Capa | Qué da | Quién la escribe | Cuándo |
|---|---|---|---|---|
| 1 | `ESTADO.md` del ticket | Fase, control pendiente, próximo paso, bloqueos | Orquestador | Al cumplir cada control y en `/cierre` |
| 2 | `bitacora.md`, `decisiones.md`, `preguntas.md`, `incidencias.md` | Qué se hizo, por qué, qué se preguntó, qué pasó | Orquestador | En el momento y en `/cierre` |
| 3 | `evidencias/` | Lo que se vio: capturas, extracciones, consultas, informes | Humano y orquestador | Cuando llega |
| 4 | `sesiones/*.md` e `INDICE.md` | Extracto de cada conversación | Hook `guardar_sesion.py` | Al compactar y al cerrar |
| 5 | `sesiones/raw/*.jsonl.gz` | La conversación completa comprimida (no se versiona) | Hook `guardar_sesion.py` | Al compactar y al cerrar |
| 6 | Conversaciones de Claude Code en el perfil del usuario | Retomar con `claude --resume` | Claude Code | Según `cleanupPeriodDays` |
| 7 | `memoria/` | Decisiones y lecciones del arnés, sesiones sin ticket | Orquestador | Cuando algo vale para todos los tickets |

La **memoria automática de Claude Code** (la que guarda preferencias en el perfil) **no** se usa para el estado de los tickets:
no viaja con la carpeta, no la ve otra persona y no se versiona.

## Los hooks

| Script | Evento | Qué hace | Si no está |
|---|---|---|---|
| `cargar_estado.py` | `SessionStart`: startup, resume, clear, compact | Imprime el estado del ticket activo y las dos últimas entradas de la bitácora; Claude Code lo agrega al contexto. Sin ticket activo, lista los abiertos | Claude empieza sin saber en qué fase está el ticket; una sesión retomada recuerda un estado viejo (lección M04 del piloto) |
| `guardar_sesion.py` | `PreCompact` y `SessionEnd` | Copia la conversación al ticket activo: extracto legible, copia cruda comprimida e índice | Lo hablado se pierde al compactar o si la sesión se corta |
| `verificar_cierre.py` (opcional) | `Stop` | Si hay archivos más nuevos que `ESTADO.md` en las carpetas de `vigilar_cambios_en` (por defecto `diseno/`, `salida/` y `entrega/`), bloquea una vez y pide actualizarlo | Se termina sin dejar el estado al día |

Propiedades de los tres: solo biblioteca estándar de Python; leen las rutas de `.claude/arnes.json`; **nunca fallan** (ante
cualquier error terminan con código 0, salvo el aviso deliberado del opcional); escriben con final de línea LF.

## Pasos

### 1. Instalar los hooks
1. Copiar `references/hooks/cargar_estado.py`, `guardar_sesion.py` y (si se quiere) `verificar_cierre.py` a `.claude/hooks/`.
2. Agregar a `.claude/settings.json` el bloque `hooks` de `references/hooks/settings-hooks.json`. Si se quiere el opcional,
   copiar la clave `Stop` (el contenido de `_opcional_Stop`) dentro de `hooks`; `_opcional_Stop` no se copia.
3. En Windows, si `python` no está en el PATH, cambiar el comando por `py`.
4. Confirmar en la documentación oficial de Claude Code que los nombres de eventos y el formato no cambiaron.

**Termina cuando:** los scripts están en `.claude/hooks/` y `settings.json` los referencia.

### 2. Probar los hooks
1. Con el ticket de prueba activo (paso 3 de `arnes-fases-y-tickets`), abrir una sesión nueva: el primer mensaje del contexto
   debe mostrar el ticket, su fase y su próximo paso.
2. Correrlo a mano para ver la salida: `python .claude/hooks/cargar_estado.py < /dev/null` (en Windows: `echo {} | python .claude\hooks\cargar_estado.py`).
3. Cerrar la sesión y comprobar que apareció `sesiones/<fecha>_<id>.md` en la carpeta del ticket, con su `INDICE.md`.

**Termina cuando:** las dos comprobaciones dan lo esperado.

### 3. Escribir `/cierre` y `/recuperar-contexto`
Crear `.claude/skills/cierre/SKILL.md` y `.claude/skills/recuperar-contexto/SKILL.md` desde las plantillas de `references/`.

- `/cierre` deja: una entrada nueva al final de la bitácora (breve: el hook muestra ~900 caracteres), `ESTADO.md` al día,
  decisiones, preguntas e incidencias registradas, candidatos creados, y verifica que "Próximo paso" se entiende sin contexto.
- `/recuperar-contexto` busca en el orden de la tabla de capas y responde con la fuente.

**Termina cuando:** `/cierre` corrido sobre el ticket de prueba deja la bitácora y el estado como se espera.

### 4. Escribir el protocolo de sesión en AGENTS.md
Inicio (confirmar con el humano en qué seguimos), durante (registrar en el momento), cierre (`/cierre`), si algo se perdió
(`/recuperar-contexto`), **sesiones cortas**.

## Sesiones cortas

Una conversación que crece sin límite termina cortándose: en el piloto, una sesión de más de 460.000 tokens terminó con un error
del proceso. Regla:
- Al terminar cada **bloque grande** (una fase, un grupo de pruebas), ejecutar `/cierre` y abrir una sesión nueva.
- La sesión nueva no retoma la anterior con `--resume` si era muy larga: empieza limpia y el hook carga el estado.
- Si una sesión se corta: abrir una nueva, pedir un resumen del estado desde los archivos, verificar si quedó algo a medias
  (archivos modificados en el extracto de la sesión) y registrar el corte en la bitácora.

## Traspaso a otra persona

Lo que **viaja con la carpeta**: todo lo que está en archivos (estado, bitácora, decisiones, lecciones, sesiones).
Lo que **no viaja**: la memoria automática del perfil de cada uno, las preferencias guardadas en Claude Code, los accesos
(ambiente, conexión de solo lectura, credenciales) y lo que sepa un revisor en su propia conversación.

Pasos del traspaso (plantilla en `references/traspaso-plantilla.md`):
1. Cerrar la sesión actual con `/cierre`; si alguna se cortó, reconstruirla primero.
2. Pedir a Claude Code un `memoria/traspaso-AAAA-MM-DD.md` con: estado de fases, lo verificado, lo que falta, decisiones y lecciones
   en una línea cada una, reglas de seguridad, datos fijos del ambiente y pendientes que requieren aprobación.
3. Entregar los accesos por un canal seguro, **nunca** en archivos.
4. La persona nueva abre una sesión nueva con el mensaje de arranque de la plantilla.
5. Si usaba un revisor (Cowork), la persona nueva le pasa el contexto con la plantilla de revisor (`references/colaboracion-revisor.md`).

## Colaboración con un revisor

Ver `references/colaboracion-revisor.md`: roles, cómo se preparan los mensajes para Claude Code, cómo se aprueba y qué
verificaciones hace el revisor en modo lectura.

## Control de salida
- [ ] Hooks copiados, referenciados en `settings.json` y probados (inicio muestra el ticket; cierre deja el extracto).
- [ ] `/cierre` y `/recuperar-contexto` escritos y probados.
- [ ] Protocolo de sesión en AGENTS.md, incluida la regla de sesiones cortas.
- [ ] `memoria/sesiones/raw/` en el `.gitignore` del arnés y `tickets/*/sesiones/raw/` en el de cada vault de cliente.

## Errores que ya cometimos (piloto de referencia)
- **Sesión retomada con estado viejo** (M04 del piloto): por eso el hook corre también en resume, clear y compact.
- **Sesión que creció hasta cortarse**: el trabajo se recuperó desde los archivos; la regla de sesiones cortas vino después.
- **Un traspaso que asumía que la memoria del revisor viajaba**: no viaja; hubo que escribir un mensaje de contexto completo para el revisor nuevo.
- **Un mensaje con plantilla abierta** (`[elige una]`) llegó así a Claude Code y hubo que repetir el intercambio: los mensajes
  para Claude Code van completos, sin opciones por elegir.

## Siguiente paso
`arnes-seguridad-y-entrega`.
