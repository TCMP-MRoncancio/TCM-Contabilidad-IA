# Plantillas de las skills de dominio

Copiar cada bloque a `.claude/skills/<nombre>/SKILL.md`. Reemplazar `<dominio>` y completar con las rutas reales del vault.

---

## `<dominio>-fundamentos`

~~~~markdown
---
name: <dominio>-fundamentos
description: "Modelo mental de <objetos del dominio> y mapa del vault de patrones. Usar antes de cualquier tarea sobre <objetos> (analizar, disenar, construir, revisar o responder preguntas) y cuando haya dudas sobre que significa un elemento del formato."
---

# Fundamentos de <dominio>

Esta skill no repite el conocimiento: dice dónde está y cómo usarlo según su nivel de confianza.

## Dónde está cada cosa
| Pregunta | Nota |
|---|---|
| ¿Qué es, qué piezas tiene, dónde se guarda? | `vault-patrones/<dominio>/modelo.md` |
| ¿Qué significa este elemento? | `vault-patrones/<dominio>/diccionario/` |
| ¿Qué tipo de pedido es? | `vault-patrones/<dominio>/arquetipos/README.md` |
| ¿Hay fragmento para esta variante? | `vault-patrones/<dominio>/cobertura.md` |
| ¿Qué ejemplo mirar? ¿Qué no copiar? | `plantillas-curadas.md`, `anti-patrones.md` |
| ¿Qué formato usa el ambiente? | `vault-cliente-<c>/cliente.md` |

## Cómo actuar según el estado de madurez
| Estado | Qué hacer |
|---|---|
| `verificado-ida-y-vuelta`, `verificado-captura`, `extraido-de-ejemplo` | Usar |
| `inferido` | Usar y decirlo |
| `hipotesis` | No depender: preguntar o proponer una prueba |
| `desconocido` | Copiar el valor del fragmento tal cual |
| `obsoleto` | No usar |
| Sin nota | Es una pregunta o una brecha, nunca una suposición |

## Datos que no se olvidan
- <Cinco a diez hechos del dominio que, si se olvidan, rompen el entregable. Cada uno con su nota de origen.>

## Consultas al ambiente
- Solo lectura y solo por la conexión de solo lectura. Nunca un cliente de consola que escriba.
- Lo consultado y su resultado se anotan en el ticket con fecha.

## Fuera de alcance
- <Lo que el arnés no cubre todavía. Si un pedido lo necesita, es una brecha: se avisa al humano.>
~~~~

---

## `<dominio>-diseno`

~~~~markdown
---
name: <dominio>-diseno
description: "Fases 1 y 2 de un ticket de <dominio>. Convierte un requerimiento en ficha.yaml lista para aprobar. Usar cuando se pida analizar un requerimiento, proponer un arquetipo o disenar o modificar un <objeto>."
---

# Diseño (fases 1 y 2)

Resultado: `diseno/ficha.yaml` (plantilla en `references/`). Desde ella el generador produce `diseno.md`, que aprueba el humano.

## Antes de empezar
1. Leer `ESTADO.md`, `preguntas.md` y `decisiones.md` del ticket; `cliente.md` y `ambiente/` del cliente.
2. Si es una modificación: pedir al humano la extracción actual del objeto **desde el ambiente** (no usar la de `contexto/`),
   y convertirla con `desde-extraccion`.

## Fase 1 · Requerimiento
1. Entender el para qué de negocio. Proponer el arquetipo.
2. Hacer las preguntas del arquetipo que falten. Una pregunta sin respuesta no se completa con una suposición: va a `preguntas.md`.
3. Control: sin preguntas críticas abiertas y arquetipo aceptado.

## Fase 2 · Diseño
1. Escribir la ficha: cada elemento con una variante que tenga fragmento; cada propiedad con destino en el diccionario.
2. Casos de prueba, incluidos los que exigen una línea base previa (`previo: true`).
3. Pasos fuera del script.
4. Supuestos y brechas.
5. Devolver al orquestador, que corre `validar` y `generar` (con la ficha en borrador solo sale `diseno/diseno.md`), pide la
   aprobación **escrita** del humano y, con ella, pasa la ficha a `estado: aprobada`.
~~~~

---

## `<dominio>-construccion`

~~~~markdown
---
name: <dominio>-construccion
description: "Fase 3 de un ticket de <dominio>. Genera el entregable desde una ficha aprobada con el generador del arnes. Usar cuando haya que generar o corregir la salida de un ticket."
---

# Construcción (fase 3)

Entrada: ficha con `estado: aprobada` y la aprobación registrada en `ESTADO.md`. Sin eso, no se construye.
**Nunca se ejecuta nada contra un ambiente**: el humano aplica después de la revisión.

## Camino normal
```
python herramientas/ficha.py validar <ficha>
python herramientas/ficha.py generar <ficha>
python herramientas/leer.py validar <salida>
```
Si algo no se puede expresar, vuelve al diseño: el diseñador lo agrega a la ficha como `codigo_manual`, el humano lo aprueba y se
regenera. **No se edita la salida a mano.**

## Qué revisar en la trazabilidad
- Elementos con origen `fragmento` o `extra`: ¿corresponde copiarlos en este contexto? (¿alguno es una referencia?)
- Elementos `inferido`: listarlos para confirmarlos en la ida y vuelta.
~~~~

---

## `<dominio>-revision`

~~~~markdown
---
name: <dominio>-revision
description: "Revision independiente de un <objeto> antes de aplicarlo (fase 3) y comparacion de ida y vuelta despues de aplicarlo (fase 4). Usar para revisar ficha y salida de un ticket o para analizar diferencias entre lo generado y lo extraido."
---

# Revisión

Solo lectura: se informa, no se corrige. El informe va a `evidencias/revision-AAAA-MM-DD.md`; los hallazgos abiertos, a `incidencias.md`.

## A. Antes de aplicar (fase 3)
1. Herramientas sin errores: validador de la ficha, validador del entregable, lint.
2. Ficha contra salida: cada elemento de la ficha está en la salida y viceversa; `desconocido` con el valor del fragmento;
   referencias dentro de rango.
3. Seguridad: nada que escriba sobre objetos nativos; nada que pierda datos; controles que fallan cerrados.
4. Anti-patrones ausentes.
5. Informe (plantilla en `references/informe-revision-plantilla.md`).

## B. Después de aplicar (fase 4)
1. El humano aplica en desarrollo y extrae de vuelta; deja el archivo en `evidencias/` sin editar.
2. `python herramientas/leer.py comparar <salida> <evidencias/extraido>`.
3. Cada diferencia se clasifica: el sistema normalizó (conocimiento nuevo → candidato), la ficha no se tradujo (error → incidencia),
   la interfaz la cambió (manual → decisión).
4. Control: ninguna diferencia sin explicar.
~~~~
