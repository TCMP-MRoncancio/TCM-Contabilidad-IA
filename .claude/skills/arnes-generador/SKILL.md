---
name: arnes-generador
description: "Paso 5 de construir un arnes: disenar la ficha declarativa del diseno y las herramientas deterministas (lector, validador del entregable, desde-extraccion, generador, validador de ficha, comparador de ida y vuelta, lint, cobertura) con trazabilidad y prueba de regresion sobre el corpus. Usar cuando haya que decidir como se produce el entregable sin que el LLM lo escriba a mano, especificar o revisar herramientas del arnes, o medir su exactitud. No usar para generar el entregable de un ticket (eso lo hace la herramienta del arnes)."
---

# Ficha y generador (paso 5)

**Objetivo:** que el entregable salga siempre de un script determinista a partir de una ficha declarativa, con trazabilidad
de cada elemento y una prueba de regresión que demuestre que el script reproduce los ejemplos reales.
**Entrada:** diccionario, fragmentos y cobertura (paso 3); tabla de variabilidad de la ficha del arnés; tabla de fases (paso 4).
**Salida:** formato de la ficha documentado con una plantilla; herramientas en `herramientas/` con su README; prueba de regresión
pasando sobre el corpus.
**Especificación de cada herramienta:** `references/especificacion-herramientas.md`.

## Por qué

Un LLM que escribe el entregable a mano varía entre sesiones, se salta detalles de formato y no deja rastro de por qué cada línea
es como es. Un script repite siempre lo mismo, se prueba contra el corpus y se corrige una vez para todos los tickets.
El LLM hace lo que hace bien: entender el pedido, llenar la ficha, preguntar lo que falta, revisar.

## Las piezas

| Pieza | Qué hace | Entrada → salida |
|---|---|---|
| **Lector** | Entiende el formato del entregable: lo separa en secciones y elementos | Archivo del sistema → estructura en memoria o JSON |
| **Validador del entregable** | Revisa un entregable (generado o extraído) contra reglas numeradas (V01, V02…) | Archivo → lista de errores y avisos |
| **Cobertura y fragmentos** | Recorre el corpus, clasifica variantes, cuenta y extrae fragmentos | `contexto/` → `vault-patrones/<dominio>/cobertura.md` y `fragmentos/` |
| **Desde-extracción** | Arma una ficha a partir de un entregable existente | Archivo → `ficha.yaml` |
| **Generador** | Produce el entregable, la trazabilidad, el documento de diseño y la entrega | `ficha.yaml` → `salida/`, `trazabilidad.md`, `diseno.md`, `entrega/` |
| **Validador de ficha** | Revisa que la ficha esté completa y respete los límites del sistema | `ficha.yaml` → errores |
| **Comparador** | Compara dos entregables elemento por elemento, con normalizaciones declaradas | Generado + extraído → diferencias |
| **Lint** | Revisa el código auxiliar (scripts, procedimientos) contra el estándar interno | Archivos → errores y avisos |
| **Editor visual (opcional)** | Réplica de la interfaz del sistema que produce la ficha | Navegador → `ficha.yaml` |

## La ficha

La ficha dice **qué** se quiere; el generador decide **cómo** se escribe. Plantilla genérica: `references/ficha-plantilla.yaml`.

Reglas de diseño de la ficha:
1. **Cada campo de la ficha corresponde a uno o más elementos del entregable**, documentado en el diccionario ("ajustar desde la
   ficha: `<campo>`"). Un campo sin destino es ruido; un elemento variable sin campo es una brecha.
2. Lo **variable de negocio** va en la ficha; lo **variable de ambiente** se lee de `cliente.md`; lo **fijo conocido** es regla
   del generador; lo **fijo desconocido** se copia del fragmento.
3. **Modo explícito:** `modo: nuevo` (el objeto no debe existir; el entregable lleva guarda) o `modo: existente` (se modifica
   algo instalado). `desde-extracción` pone `existente`.
4. Lo que no se puede expresar lo declara **el diseñador** como **bloque manual** dentro de la ficha (por ejemplo, `codigo_manual:` con el código
   y el motivo). Así queda en la trazabilidad y lo revisa el revisor. Nunca se edita la salida a mano.
5. La ficha lleva `estado: borrador | aprobada`. El diseñador la escribe en `borrador`. **El orquestador** la pasa a `aprobada`
   después de la aprobación escrita del humano (y la cita en `ESTADO.md`). Con la ficha en borrador, el generador solo escribe
   `diseno/diseno.md` o una vista previa fuera del vault.
6. Incluye los **casos de prueba** y los **pasos fuera del script** (lo que el humano hace a mano en el sistema); el generador
   los lleva a `diseno.md` y a `promocion.md`.
7. Los límites del sistema (largos, tipos, rangos) se validan en la ficha, no se descubren al aplicar.

## Pasos

Construir en este orden. Cada herramienta se apoya en las anteriores (el generador usa el validador de ficha; la regresión usa
desde-extracción, generador y comparador).

### 1. Lector y validador del entregable
Primero entender el formato: el lector separa el entregable en secciones y elementos; el validador aplica reglas numeradas.
Cada regla tiene id, severidad (error, aviso) y **mensaje con el remedio** ("V20: el texto trae CR; envolver con …").

**Termina cuando:** el validador corre sobre todo el corpus y cada error encontrado se explica (es un error real del ejemplo o
una regla mal escrita).

### 2. Cobertura y fragmentos
La herramienta de cobertura clasifica variantes y extrae fragmentos (paso 4 de `arnes-conocimiento`). Se regenera, no se edita.

**Termina cuando:** `cobertura.md` y `fragmentos/` salen de la herramienta.

### 3. Comparador
Compara elemento por elemento. Declara en código, una sola vez, las normalizaciones (finales de línea, valores que el sistema
recalcula siempre) y las justifica en el README. Devuelve código 1 si hay diferencias.

**Termina cuando:** comparar un ejemplo consigo mismo da 0 diferencias y un ejemplo alterado a propósito da la diferencia esperada.

### 4. Desde-extracción
Convierte un entregable real en ficha. Es la mitad de la prueba de regresión y la forma de modificar algo que ya está instalado.
Todo elemento del entregable tiene que ir a un campo de la ficha o a un contenedor explícito de "extras" que el generador
reproduce tal cual (así ninguna clave se pierde).

**Termina cuando:** convierte todo el corpus sin excepciones.

### 5. Validador de ficha
Revisa la ficha: campos obligatorios, límites del sistema, referencias entre elementos (que lo referenciado exista), variantes
con fragmento (si no hay, error "brecha"), modo coherente con el objeto.

**Termina cuando:** una ficha con cada tipo de error conocido da el error esperado.

### 6. Generador
Produce desde la ficha: el entregable en `salida/`, `trazabilidad.md`, `diseno/diseno.md` y `entrega/`. Usa el validador de ficha
(paso 5): con errores se niega a generar, salvo `--forzar`.

Con la ficha en `estado: borrador` escribe **solo** `diseno/diseno.md` (para que el humano lo apruebe) o una vista previa completa
en una carpeta fuera del vault; `salida/` y `entrega/` se escriben solo con la ficha `aprobada`.

Propiedades obligatorias:
- **Determinista:** misma ficha, misma salida, byte a byte.
- **Sin dependencias** fuera de la biblioteca estándar del lenguaje, salvo decisión registrada.
- **Final de línea y codificación explícitos** al escribir.
- **No reescribe** una pieza cuya única diferencia sería la fecha del encabezado.
- **Nunca se conecta a un ambiente.**
- **Trazabilidad:** cada elemento del entregable con su origen: `ficha` (campo), `regla` (id), `fragmento` (nombre) o `extra`.
- **Modos:** `nuevo` escribe la guarda; `existente`, no; `--correccion-dev` escribe solo una corrección para desarrollo en
  `entrega/`, rotulada "no promover", sin tocar la ficha ni `salida/`.
- `--forzar` permite generar con errores de validación **solo** para la prueba de regresión.

**Termina cuando:** genera una ficha de ejemplo y el validador del entregable da 0 errores.

### 7. Prueba de regresión (ida y vuelta sobre el corpus)
Para cada ejemplo del corpus: desde-extracción → ficha → generar `--forzar` → comparar con el original. Procedimiento y script
de referencia en `references/prueba-regresion.md`.

- Meta: **100 % sin diferencias**. Cada diferencia es un error del generador o del lector, o una normalización que se declara.
- Se corre **antes y después** de cualquier cambio a las herramientas, y el resultado se escribe en la decisión que registra el cambio.
- Se reporta siempre con el mismo método (mismas opciones, mismo conjunto). En el piloto, un script de medición mal armado
  reportó 75 de 85 cuando el generador daba 86 de 86: faltaba una opción, se comparaba un archivo equivocado y se descartaba un duplicado.

**Termina cuando:** 100 % del corpus sin diferencias y el método de medición documentado en el README de herramientas.

### 8. Lint del código auxiliar
Si el entregable incluye código (procedimientos, scripts), un lint lo revisa contra el estándar interno, con reglas numeradas.

### 9. Editor visual (opcional)
Si el diseño es visual (pantallas, formularios), un HTML que replique la interfaz real del sistema acelera el diseño.
Reglas del piloto: cada control con una marca de madurez (verificado, inferido, hipótesis, brecha); los controles sin elemento
conocido se muestran como brecha y el validador de ficha los rechaza; lo que no es del sistema (lógica agregada) se distingue
visualmente; no guarda en el navegador (la ficha descargada es el único estado).

## Contrato común de las herramientas
- Se ejecutan desde la raíz del arnés: `python herramientas/<herramienta>.py <comando> …`.
- Código de salida 0 si no hay errores, 1 si hay errores o diferencias (sirven como control automático).
- Mensajes en el idioma del equipo, con ruta y línea del problema.
- Documentadas en `herramientas/README.md` con un ejemplo por comando y la sección "Garantías" (qué prueba de regresión pasan).

## Control de salida
- [ ] Plantilla de ficha con modo, estado, casos de prueba, pasos fuera del script y bloques manuales.
- [ ] Cada campo de la ficha con destino en el diccionario.
- [ ] Lector, validador del entregable, cobertura, comparador, desde-extracción, validador de ficha, generador (y lint si aplica).
- [ ] Prueba de regresión al 100 % con método documentado.
- [ ] `herramientas/README.md` con comandos, garantías y códigos de salida.
- [ ] Sección "Herramientas" de AGENTS.md completa.

## Errores que ya cometimos (piloto de referencia)
- **Copiar un valor que era una referencia** (ver `arnes-conocimiento`). El validador de ficha ahora rechaza referencias fuera de rango.
- **Generar con CRLF por diseño** porque los ejemplos del sistema venían así; la herramienta de aplicación agregaba otro problema
  encima. La defensa terminó dentro del entregable (`arnes-seguridad-y-entrega`).
- **Medición de regresión mal armada** (ver paso 7).
- **Un documento generado que nadie usaba** (una guía de configuración manual) mientras todo se hacía por script: se quitó del
  generador y sus pasos pasaron a `promocion.md`. Lo que se genera se usa, o no se genera.

## Siguiente paso
`arnes-agentes-y-skills`.
