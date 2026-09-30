---
name: arnes-fases-y-tickets
description: "Paso 4 de construir un arnes: definir las fases y sus controles, el formato de ESTADO.md y del seguimiento por ticket (bitacora, decisiones, preguntas, incidencias, evidencias), el vault del cliente y la herramienta ticket.py. Usar al disenar el ciclo de vida de los tickets de un arnes, al adaptar la tabla de fases o al instalar la gestion de tickets. No usar para mover de fase un ticket concreto de un arnes ya construido (eso lo hace su skill /ticket)."
---

# Fases y tickets (paso 4)

**Objetivo:** que cada unidad de trabajo avance por fases con un control verificable, y que su estado viva en archivos que
cualquier persona o sesión pueda leer sin la conversación.
**Entrada:** `ficha-arnes.md` (preguntas 3, 4, 7, 11 y 12) y la estructura del paso 2.
**Salida:** tabla de fases en AGENTS.md; plantillas de cliente y de ticket en `herramientas/plantillas/`; `herramientas/ticket.py`;
`.claude/arnes.json`; un ticket de prueba creado con la herramienta.
**Archivos listos para copiar:** `references/herramientas/` (ticket.py y plantillas) y `references/arnes-plantilla.json`.

## Las fases estándar

Punto de partida probado en el piloto de referencia. Se adaptan al caso, pero **tres reglas no se tocan**:
la revisión va antes de aplicar; la aplicación la hace el humano; el diseño lo aprueba el humano por escrito.

| Fase | Qué se hace | Control para avanzar | Quién marca el control |
|---|---|---|---|
| 0 Alta | Crear el ticket, confirmar el ambiente | Versión y formato del ambiente confirmados; identificador del objeto sin colisión (consulta de solo lectura) | Orquestador, con la evidencia |
| 1 Requerimiento | Entender la necesidad, proponer arquetipo, preguntar | Sin preguntas críticas abiertas; arquetipo aceptado | Orquestador |
| 2 Diseño | Escribir la ficha (diseñador) y generar `diseno.md` (orquestador) | Ficha validada sin errores y diseño **aprobado por escrito** por el humano; el orquestador pasa la ficha a `estado: aprobada` | Orquestador, con la aprobación del humano citada |
| 3 Construcción | Generar el entregable y revisarlo | Validador, lint y revisión independiente sin errores, **antes** de aplicar | Orquestador, con el informe del revisor |
| 4 Aplicación e ida y vuelta | El humano aplica en desarrollo y extrae de vuelta | Comparación sin diferencias no explicadas | Orquestador, con la comparación |
| 5 Pruebas | Casos de prueba en desarrollo | Casos ejecutados con evidencia y aprobados | Orquestador, con la aprobación |
| 6 Entrega | Paquete de promoción | Paquete completo (orden, dependencias, pasos fuera del script, verificación, retiro) | Orquestador |
| 7 Cierre | Bitácora final, candidatos | Conocimiento verificado y candidatos registrados | Orquestador |

**Cómo adaptar:**
- Si el caso **no permite extraer de vuelta**, la fase 4 se reduce a "aplicado y verificado por consulta de solo lectura o captura"
  y el riesgo se escribe en la ficha del arnés.
- Si no hay identificador que pueda colisionar, el control de la fase 0 queda solo en el ambiente.
- No se fusionan fases 3 y 4: la revisión antes de aplicar es un control distinto de la ida y vuelta después (lección M05 del piloto).
- Una fase nueva se agrega con su control y su responsable; nunca una fase sin control.

## El seguimiento de un ticket

Cada ticket tiene su carpeta en el vault de su cliente. **Un solo lugar para cada cosa:**

| Archivo | Qué guarda | Cuándo se escribe | Quién |
|---|---|---|---|
| `ESTADO.md` | Dónde estamos: fase, control pendiente, próximo paso, bloqueos, preguntas abiertas, hecho, controles | Al cumplir cada control y en `/cierre` | Orquestador |
| `bitacora.md` | Qué se hizo en cada sesión y por qué (una entrada por sesión, al final) | En `/cierre` | Orquestador |
| `decisiones.md` | Decisiones del ticket con motivo y quién | En el momento | Orquestador |
| `preguntas.md` | Preguntas numeradas con su respuesta y fuente | En el momento | Orquestador |
| `incidencias.md` | Qué pasó, cómo se detectó, causa, resolución, lección | En el momento | Orquestador |
| `evidencias/` | Capturas, extracciones, consultas, informes de revisión | Cuando llegan | Humano (deja) y orquestador (registra) |
| `diseno/` | `ficha.yaml` y `diseno.md` | Fase 2 | Agente diseñador |
| `salida/` | Entregable generado | Fase 3 | Generador |
| `entrega/` | Promoción y correcciones de desarrollo | Fases 4 a 6 | Generador y orquestador |
| `sesiones/` | Copias de conversaciones | Automático | Hooks |

### El formato de `ESTADO.md` es un contrato

El hook de inicio y `ticket.py` lo leen. Respetar:
- Frontmatter YAML plano (una línea `clave: valor` por campo) con al menos: `ticket`, `cliente`, `titulo`, `fase`,
  `control_pendiente`, `actualizado`. `fase` empieza con el número (`0-alta`, `3-construccion`): el hook usa el prefijo para saber
  si el ticket está cerrado.
- Secciones de nivel 2 con estos títulos exactos: `## Próximo paso`, `## En curso`, `## Bloqueos`, `## Preguntas abiertas`,
  `## Hecho`, `## Controles por fase`.
- "Próximo paso" se entiende **sin la conversación**: qué, quién, con qué archivo.
- Los controles se marcan `[x]` **solo con evidencia** citada en la misma línea o en "Hecho".

Si se cambian los títulos, se cambian también en `.claude/arnes.json` (`secciones_estado`).

## Pasos

### 1. Escribir la tabla de fases en AGENTS.md
Adaptar la tabla estándar con las respuestas de la ficha del arnés. Cada control debe poder comprobarse leyendo un archivo.

**Termina cuando:** ninguna fase tiene un control del tipo "está bien" o "se revisó": todos citan una herramienta, un archivo o una aprobación.

### 2. Instalar las plantillas y la herramienta
1. Copiar `references/herramientas/ticket.py` a `herramientas/ticket.py`.
2. Copiar `references/herramientas/plantillas/` a `herramientas/plantillas/` (incluidos los archivos ocultos `.gitignore` y
   `.gitattributes` de `vault-cliente/`: cada vault nuevo los recibe).
3. Copiar `references/arnes-plantilla.json` a `.claude/arnes.json` y ajustar `nombre` y, si cambiaron, las rutas.
4. Adaptar `plantillas/ticket/ESTADO.md` a la tabla de fases del paso 1 (lista de controles y `control_pendiente` inicial).
5. Si el caso necesita otros datos en el alta (un identificador del objeto, un código de proyecto), agregarlos como
   marcadores `{{CLAVE}}` en la plantilla; `ticket.py crear` los recibe con `--dato CLAVE=valor` y avisa los que queden sin valor.

**Termina cuando:** `python herramientas/ticket.py listar` corre sin error.

### 3. Crear un cliente y un ticket de prueba
```
python herramientas/ticket.py nuevo-cliente prueba
python herramientas/ticket.py crear prueba T-000 --titulo "Ticket de prueba del arnés"
python herramientas/ticket.py estado
```
Comprobar que existen todos los archivos del seguimiento y que `estado` muestra el ESTADO del ticket.
El ticket de prueba se borra después (lo hace el humano) o se deja con fase `7-cierre`.

**Termina cuando:** el ticket de prueba tiene toda su estructura y queda activo.

### 4. Escribir la skill `/ticket` del arnés
Crear `.claude/skills/ticket/SKILL.md` a partir de `references/skill-ticket-plantilla.md`. Es la que usa el orquestador para
listar, activar, crear y pasar de fase.

**Termina cuando:** la skill existe y su descripción está en ASCII entre comillas (lección M01 del piloto).

## Cómo se pasa de fase (regla que va en la skill `/ticket`)

1. Leer el control de la fase actual en AGENTS.md y en la lista de `ESTADO.md`.
2. Si se cumple, **con la evidencia a la vista**: marcar el control, cambiar `fase` y `control_pendiente` en el frontmatter,
   actualizar "Próximo paso" y `actualizado`, agregar una línea en "Hecho" con la evidencia.
3. Si no se cumple, decir qué falta. Nunca marcar sin evidencia.
4. El control del diseño (fase 2) exige una aprobación **escrita por el humano**, con fecha. Se cita textual en "Hecho".

## El ticket piloto de calibración

El primer ticket real del arnés es el que definió `arnes-concepcion` (paso 6). Durante ese ticket:
- Se espera encontrar errores del arnés. Cada uno va a `incidencias.md` del ticket y, si aplica a todos, a `memoria/lecciones.md`.
- Cada corrección a herramientas, agentes o skills se registra en `memoria/decisiones.md` con el ticket como motivo.
- Se prueba a propósito lo `desconocido` e `inferido` que más importa.
- Al terminar, se retira del ambiente (plan de retiro) y se cierra con `/cierre`.

## Control de salida

- [ ] Tabla de fases en AGENTS.md, con control y responsable por fase.
- [ ] `herramientas/ticket.py`, plantillas y `.claude/arnes.json` instalados.
- [ ] `ESTADO.md` de la plantilla coincide con la tabla de fases.
- [ ] Ticket de prueba creado y mostrado por `ticket.py estado`.
- [ ] Skill `/ticket` escrita.

## Errores que ya cometimos (piloto de referencia)

- **Un agente marcó un control.** El constructor marcó la fase 3 como cumplida sin la revisión independiente. Regla: solo el
  orquestador edita el seguimiento; los agentes devuelven, no marcan.
- **Un caso de prueba necesitaba un estado previo que nadie guardó.** Una prueba pedía una línea base anterior a la instalación
  y no figuraba como paso previo de la entrega; al aplicar, la línea base se perdió. Regla: los casos que exigen una línea base
  salen como paso 0 de la aplicación.
- **Rol "por definir".** Nadie estaba asignado a aplicar y extraer de vuelta. Regla: la fase 2 no se aprueba con roles abiertos
  en `cliente.md`.

## Siguiente paso

`arnes-generador`.
