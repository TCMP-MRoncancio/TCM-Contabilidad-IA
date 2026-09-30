---
name: arnes-agentes-y-skills
description: "Paso 6 de construir un arnes: disenar el orquestador y los subagentes (disenador, constructor, revisor) con herramientas minimas, modelo y formato de retorno, y escribir las skills de dominio (fundamentos, diseno, construccion, revision, estandar de codigo) con descripciones que se activen bien. Usar al crear o revisar agentes o skills de un arnes, cuando un agente usa herramientas fuera de su tarea o cuando una skill no se activa. No usar para las skills de sesion (/cierre, /recuperar-contexto): estan en arnes-memoria-y-sesiones."
---

# Agentes y skills (paso 6)

**Objetivo:** que cada tarea la haga un actor con **solo** las herramientas que necesita, que sepa qué leer antes de empezar,
qué producir, qué no tocar y cómo devolver el resultado.
**Entrada:** AGENTS.md con fases (paso 4), herramientas (paso 5), vault de patrones (paso 3).
**Salida:** `.claude/agents/*.md`, `.claude/skills/<dominio>-*/SKILL.md`, secciones "Agentes" y "Skills" de AGENTS.md.
**Plantillas:** `references/agentes-plantilla.md`, `references/skills-dominio-plantilla.md`, `references/informe-revision-plantilla.md`.

## Quién hace qué

| Actor | Herramientas | Escribe en | Nunca |
|---|---|---|---|
| **Orquestador** (sesión principal) | Todas las que permita `settings.json` | Seguimiento del ticket, `memoria/`, candidatos; corre `validar` y `generar` para el diseñador; pasa la ficha a `aprobada` tras la aprobación escrita | Construir el entregable a mano; marcar controles sin evidencia |
| **Diseñador** | Read, Grep, Glob, Write, Edit (**sin Bash**) | `diseno/ficha.yaml` del ticket (incluido `codigo_manual`) | Ejecutar nada; escribir código del entregable; editar el seguimiento |
| **Constructor** | Read, Grep, Glob, Write, Edit, Bash (solo las herramientas del arnés) | `salida/`, `entrega/`, `trazabilidad.md` y `diseno/diseno.md`, siempre vía el generador | Cambiar la ficha; editar el seguimiento; marcar controles; conectarse a un ambiente |
| **Revisor** | Read, Grep, Glob, Bash de solo lectura (**sin Write ni Edit**) | Nada: devuelve el informe | Corregir; escribir; conectarse a un ambiente |

Reglas comunes:
1. **Los agentes no delegan** en otros agentes (un subagente no puede lanzar otro). El orquestador los lanza, les pasa el ticket
   y guarda lo que devuelven.
2. **Solo el orquestador edita el seguimiento** (`ESTADO.md`, bitácora, decisiones, preguntas, incidencias).
3. **Un agente no reescribe su propia definición.** Editar `.claude/` pide aprobación (permiso `ask`) y se registra en `memoria/decisiones.md`.
4. **Si una restricción de herramientas empuja a saltársela, se quita la herramienta.** Si el diseñador "necesita" correr el
   validador, lo corre el orquestador y le devuelve los errores. La definición dice qué hacer en ese caso: detenerse y pedirlo.

### Por qué tres agentes y no uno
El que diseña no revisa su diseño; el que construye no aprueba su construcción. La revisión independiente encontró en el piloto
problemas que el constructor había dado por buenos. Si el caso es muy chico, se puede prescindir del constructor (lo hace el
orquestador corriendo el generador), **nunca del revisor**.

### Modelos
Diseño y revisión con el modelo más capaz disponible; construcción (que es correr el generador y revisar su salida) con uno más
económico. Respetar las restricciones de la organización (por ejemplo, un modelo deshabilitado por costo). El modelo se fija en
el frontmatter del agente; si la organización lo restringe, se escribe en AGENTS.md.

## Anatomía de una definición de agente

```
---
name: <nombre-en-kebab>
description: "<Qué hace y cuándo usarlo, en ASCII, entre comillas dobles, sin ': ' sin escapar>"
tools: <lista mínima>
model: <modelo>
---
<Rol en una línea. Trabajas sobre un solo ticket, que te indica el orquestador.>

## Antes de empezar
<Skills a leer, en orden. Archivos del ticket a leer. Condición de entrada: si no se cumple, te detienes y lo informas.>

## Qué produces
<Archivos, con ruta exacta. "Solo escribes dentro de <carpeta>.">

## Reglas
<No ejecutas / no delegas / no editas el seguimiento / si falta un dato, lo devuelves como pregunta. Qué hacer en el caso que empuja a romper la regla.>

## Antes de devolver
<Comandos de verificación que corresponden a su tarea, si tiene Bash.>

## Qué devuelves
<Formato numerado y fijo: resumen corto, archivos escritos, preguntas, supuestos, brechas, si está listo para el siguiente control.>
```

La descripción es lo que Claude lee para decidir cuándo usar el agente: en ASCII y entre comillas (lección M01 del piloto: una tilde mal
codificada o un `: ` sin comillas rompe el frontmatter y el agente deja de cargarse sin aviso).

## Skills de dominio

| Skill | Cuándo se carga | Qué contiene | Qué no contiene |
|---|---|---|---|
| `<dominio>-fundamentos` | Antes de cualquier tarea del dominio | Mapa "pregunta → nota del vault"; tabla "nivel de madurez → qué hacer"; datos que no se olvidan; fuera de alcance | El conocimiento en sí (apunta al vault) |
| `<dominio>-diseno` | Fases 1 y 2 | Cómo pasar de requerimiento a ficha: arquetipo, preguntas, reglas de la ficha, qué devuelve | Código del entregable |
| `<dominio>-construccion` | Fase 3 | Cómo correr el generador, qué revisar en la trazabilidad, qué hacer si algo no se puede expresar | Edición manual de la salida |
| `<dominio>-revision` | Fases 3 (antes de aplicar) y 4 (ida y vuelta) | Checklist, severidades, formato del informe, cómo clasificar diferencias | Correcciones |
| `<estandar>-codigo` | Al escribir o revisar código auxiliar | Cómo se escribe una pieza, qué no puede faltar, cómo correr el lint | Reglas duplicadas del vault (apunta a ellas) |

### Cómo escribir la `description` de una skill
- **Qué hace** en una frase, **cuándo usarla** con las frases que diría el usuario, y **cuándo no**.
- ASCII, entre comillas dobles, sin saltos de línea.
- Específica del arnés: dos skills con descripciones parecidas compiten y se carga la equivocada.
- Probar: en una sesión nueva, pedir la tarea con palabras distintas y ver si la skill se carga.

### Cómo escribir el cuerpo
- Objetivo, entrada, salida.
- Pasos numerados, cada uno con su criterio de término.
- Checklist de control.
- Apunta a los archivos del vault; **no copia** su contenido (un dato en dos lugares, uno queda viejo).
- "Errores que ya cometimos" con los casos reales del arnés, y se actualiza en cada `/cierre` que encuentre uno nuevo.

## Pasos

1. Escribir la sección "Agentes" de AGENTS.md con la tabla de arriba adaptada.
2. Crear los tres agentes desde `references/agentes-plantilla.md`, ajustando rutas, skills y comandos.
3. Crear las skills de dominio desde `references/skills-dominio-plantilla.md`.
4. Escribir la sección "Skills" de AGENTS.md con la lista.
5. **Probar cada agente** con una tarea chica del ticket de prueba y comprobar: que lee lo que debe antes de empezar, que no usa
   herramientas fuera de su tarea, que escribe solo en su carpeta y que devuelve en el formato fijado. Registrar el resultado.
6. Registrar en `memoria/decisiones.md` los agentes, sus herramientas y sus modelos.

## Control de salida
- [ ] Tres agentes con herramientas mínimas, carpeta de escritura y formato de retorno.
- [ ] Ninguna definición permite editar el seguimiento a un agente.
- [ ] Descripciones en ASCII entre comillas.
- [ ] Skills de dominio que apuntan al vault sin copiarlo.
- [ ] Cada agente probado con una tarea chica.
- [ ] AGENTS.md con las secciones "Agentes" y "Skills".

## Errores que ya cometimos (piloto de referencia)
- **"Usa Bash solo para X"** no alcanzó: el diseñador usó Bash para copiar y editar archivos, y después para leer. Se le quitó Bash.
- **El revisor usó comandos de lectura** que su definición no nombraba. Se aceptó y se escribió en su definición: "Bash solo de
  lectura (ls, cat, grep, diff); nada que escriba, mueva o borre".
- **El constructor marcó un control** de fase. Ahora su definición dice que no edita el seguimiento.
- **Definiciones que cambiaban solas** en un piloto anterior. Ahora `.claude/` pide aprobación.

## Siguiente paso
`arnes-memoria-y-sesiones`.
