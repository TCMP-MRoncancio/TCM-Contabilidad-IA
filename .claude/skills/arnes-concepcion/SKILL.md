---
name: arnes-concepcion
description: "Paso 1 de construir un arnes: analizar el caso de uso antes de crear carpetas. Usar cuando se pida disenar un arnes nuevo, definir que va a resolver, evaluar si un caso de uso sirve para un arnes o completar la ficha del arnes. Produce ficha-arnes.md aprobada por el humano. No usar para disenar un ticket dentro de un arnes ya construido."
---

# Concepción del arnés (paso 1)

**Objetivo:** entender el caso de uso lo suficiente para que todas las decisiones de estructura, conocimiento, fases, generador
y agentes tengan un motivo escrito. El resultado es `ficha-arnes.md`, aprobada por el humano.

**Entrada:** una descripción del caso de uso (aunque sea de una línea) y acceso al material que exista (documentación, ejemplos).
**Salida:** `ficha-arnes.md` con las 12 respuestas, la clasificación de variabilidad, los métodos de verificación, los riesgos,
el ticket piloto de calibración y la aprobación.
**Plantilla:** `references/ficha-arnes-plantilla.md`. Ejemplo completo del piloto de referencia: `references/ejemplo-piloto.md`.

Mientras se trabaja, la ficha vive en la carpeta raíz del arnés como `memoria/ficha-arnes.md`: es lo único que se crea antes de
la aprobación. El resto de la estructura espera a que esté aprobada.

## Pasos

### 1. Entrevista inicial

Hacer al humano las **12 preguntas** de la tabla. Reglas:

- Una pregunta sin respuesta **no se completa con una suposición**. Se escribe "BRECHA: <qué falta y a quién preguntar>".
- Cada respuesta lleva su fuente: "lo dijo <persona> el <fecha>", "archivo X", "captura Y".
- Si la respuesta abre una duda nueva, se agrega como pregunta derivada (12.a, 12.b…).
- Preguntar de a pocas (tres o cuatro por mensaje), empezando por 1, 2, 3 y 4, porque las demás dependen de ellas.

| # | Pregunta | Por qué importa | Qué decide |
|---|---|---|---|
| 1 | ¿Qué es exactamente el entregable? Formato, extensión, quién o qué lo lee | Si una máquina lo lee, el formato es estricto y conviene un generador | Si hace falta generador (principio 2) |
| 2 | ¿En qué sistema se aplica? Versión, ambientes (desarrollo, QA, producción) y si el formato cambia entre ambientes o versiones | Un formato que varía por ambiente obliga a fragmentos por variante | Variantes del diccionario y de los fragmentos |
| 3 | ¿Cómo se aplica y quién lo aplica? ¿Con qué herramienta? | La herramienta que aplica puede alterar el entregable (codificación, finales de línea, orden) | Rol del humano; defensas en el generador |
| 4 | ¿Se puede extraer de vuelta lo aplicado? ¿Con qué herramienta y en qué formato? | Sin extracción no hay ida y vuelta: la verificación queda más débil | Fase de aplicación y comparador |
| 5 | ¿Qué ejemplos reales hay? Cantidad, de qué clientes, de qué versiones, confidencialidad | El corpus es la base del conocimiento y de la prueba de regresión | Contenido de `contexto/` y política de versionado |
| 6 | ¿Qué documentación hay? Manual del fabricante, estándares internos, guías de estilo | Define reglas fijas del generador y del lint | Reglas de validación y lint |
| 7 | ¿Qué es una unidad de trabajo (ticket)? ¿Qué identificador tiene y quién lo crea? | El seguimiento se organiza por ticket | Herramienta de tickets y plantillas |
| 8 | ¿Qué se puede leer del ambiente, cómo y con qué permisos? | Las lecturas confirman datos; nunca deben poder escribir | Conexión de solo lectura (MCP) y permisos |
| 9 | ¿Qué es irreversible o riesgoso? Datos sensibles, objetos nativos del sistema que no se pueden tocar | Define las prohibiciones duras | Lista `deny` y reglas duras de AGENTS.md |
| 10 | ¿Qué cambia de un caso a otro y qué es siempre igual? | Lo variable va a la ficha; lo fijo, al generador | Formato de la ficha |
| 11 | ¿Quién diseña, quién aplica, quién aprueba, quién revisa? | Separación de roles | Agentes y controles de fase |
| 12 | ¿Cuál sería un primer caso chico, de bajo riesgo, que recorra todo el flujo? | El primer ticket siempre encuentra errores del arnés | Ticket piloto de calibración |

**Termina cuando:** las 12 tienen respuesta con fuente o están marcadas como brecha con responsable.

### 2. Inspección del corpus y la documentación

Antes de diseñar nada, mirar el material real. Claude lo hace en modo lectura y anota números, no impresiones:

1. Contar ejemplos por tipo, versión y origen. Anotar cuántos hay de cada variante.
2. Abrir tres ejemplos de tipos distintos y describir su estructura: secciones, elementos, cómo se referencian entre sí.
3. Buscar elementos cuyo significado **no** se entiende. Listarlos: serán `desconocido` en el diccionario.
4. Buscar señales de que el formato varía (encabezados distintos, claves que aparecen solo en algunos ejemplos).
5. Revisar la documentación: ¿explica el formato? ¿Coincide con los ejemplos? Anotar contradicciones.

Registrar en la ficha del arnés la sección "Inventario del material" con los conteos.

**Termina cuando:** hay conteos reales y una lista de elementos no entendidos.

### 3. Clasificación de variabilidad

Con la respuesta 10 y la inspección, armar la tabla de variabilidad. Cada aspecto del entregable va a una de cuatro columnas:

| Tipo | Significa | Dónde irá en el arnés |
|---|---|---|
| Variable de negocio | Lo decide el caso (nombres, campos, reglas) | Ficha del ticket |
| Variable de ambiente | Depende del cliente o del ambiente (versión, formato, prefijos) | `vault-cliente-<c>/cliente.md` |
| Fija conocida | Siempre igual y se sabe por qué | Regla del generador |
| Fija desconocida | Siempre igual en los ejemplos, pero no se sabe qué hace | Se copia del fragmento; nunca se cambia |

Un aspecto que no entra en ninguna columna es una pregunta pendiente.

**Termina cuando:** todo aspecto visto en la inspección está clasificado o marcado como pregunta.

### 4. Métodos de verificación

Para cada tipo de afirmación que el arnés va a hacer, definir cómo se comprueba. Usar los métodos disponibles de la respuesta 4:

| Método | Fuerza | Requiere |
|---|---|---|
| Cruce con el corpus (cuántos ejemplos lo cumplen y cuántos no) | Media | Corpus de más de 20 ejemplos |
| Captura de la interfaz contra el archivo del mismo objeto | Alta para lo visible | Acceso a la interfaz y a la extracción del mismo objeto, en la misma versión |
| Ida y vuelta (aplicar, extraer, comparar) | La más alta | Ambiente de desarrollo y herramienta de extracción |
| Consulta de solo lectura al ambiente | Alta para datos | Conexión de solo lectura |
| Documentación del fabricante | Baja si no se contrasta | — |

Si el caso no permite ida y vuelta, se escribe en la ficha como riesgo alto y se compensa con más cruce de corpus y revisión.

**Termina cuando:** cada tipo de afirmación tiene al menos un método.

### 5. Riesgos y prohibiciones

Con la respuesta 9, escribir la lista de acciones que **nunca** hará un agente. Cada una se convertirá en una regla dura de
AGENTS.md y, si se puede, en un permiso `deny`. Ejemplos de categorías:

- Escribir en el ambiente (cualquier sentencia que modifique datos u objetos).
- Tocar objetos nativos del sistema destino.
- Guardar credenciales en archivos.
- Publicar en repositorios remotos o sistemas externos.
- Editar el material crudo.

**Termina cuando:** cada riesgo tiene su prohibición y, si aplica, su permiso.

### 6. Ticket piloto de calibración

Definir el primer ticket con la respuesta 12. Debe cumplir todo esto:

- Recorre **todas** las fases, incluida la aplicación y la extracción de vuelta.
- Toca a propósito los elementos marcados `desconocido` o `inferido` que más importan, para confirmarlos.
- Es de bajo riesgo: se aplica solo en desarrollo, no afecta a otros usuarios, se puede retirar.
- Es chico: se diseña en una sesión.
- Tiene un plan de retiro (cómo se borra al terminar).

**Termina cuando:** el ticket piloto está descrito con lo que pretende confirmar.

### 7. Aprobación

Presentar la ficha al humano. La aprobación la escribe **él**, con sus palabras, en la sección "Aprobación" (fecha y nombre).
Un "ok" en la conversación no alcanza: tiene que quedar en el archivo.

## Control de salida

- [ ] Las 12 preguntas con respuesta y fuente, o marcadas como brecha con responsable.
- [ ] Inventario del material con conteos reales.
- [ ] Tabla de variabilidad completa.
- [ ] Método de verificación por tipo de afirmación.
- [ ] Lista de prohibiciones.
- [ ] Ticket piloto definido, con plan de retiro.
- [ ] Aprobación escrita por el humano.

## Errores que ya cometimos (piloto de referencia)

- **Aceptar la documentación como verdad.** El manual del fabricante traía ejemplos en un dialecto distinto al del ambiente
  (M08 del piloto). Toda regla de la documentación se contrasta con el corpus.
- **Suponer que un ejemplo del corpus es lo que está instalado.** Un objeto del corpus tenía otro tamaño que el instalado (M11 del piloto).
  Antes de deducir algo de una captura, confirmar que es la misma versión.
- **No preguntar por la herramienta de aplicación.** El editor con el que se ejecutaba el entregable modificaba los finales de
  línea al ejecutar (M14 del piloto). La pregunta 3 existe por eso.
- **Dejar un rol "por definir".** La revisión detectó que nadie estaba asignado a aplicar y extraer de vuelta. La pregunta 11
  no se deja abierta.

## Siguiente paso

Con la ficha aprobada: `arnes-estructura`.
