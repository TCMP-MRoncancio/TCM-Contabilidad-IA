---
name: arnes-conocimiento
description: "Paso 3 de construir un arnes: organizar el material crudo en contexto/ y construir vault-patrones con diccionario, fragmentos, cobertura, arquetipos, candidatos y niveles de madurez; y verificar conocimiento con metodos empiricos (cruce de corpus, captura contra export, ida y vuelta). Usar al armar o ampliar el conocimiento de un arnes, al preguntar que significa un elemento del formato o al decidir si algo esta verificado. No usar para disenar un ticket concreto."
---

# Conocimiento del arnés (paso 3)

**Objetivo:** que el arnés sepa qué significa cada parte del entregable **y cuánto se puede confiar en cada cosa que sabe**.
**Entrada:** `ficha-arnes.md` aprobada (inventario del material, lista de elementos no entendidos) y la estructura del paso 2.
**Salida:** `contexto/` organizado (por el humano) e inventariado (`vault-patrones/inventario-contexto.md`); `vault-patrones/` con modelo, diccionario, fragmentos, cobertura, arquetipos,
anti-patrones, lecciones y candidatos, cada elemento con su nivel de madurez.
**Plantillas:** `references/`.

## Las dos capas

| Capa | Qué contiene | Quién escribe | Regla |
|---|---|---|---|
| `contexto/` | El material tal como llegó: documentación, manuales, ejemplos reales, capturas | Nadie después de cargarlo | Solo lectura (permiso `deny`). Nunca se corrige: si tiene errores, se anotan en el vault |
| `vault-patrones/` | Lo curado: qué significa cada cosa, con evidencia y nivel de madurez | Solo con aprobación; lo nuevo entra por `candidatos/` | Cada elemento declara su madurez. Lo generable se genera con una herramienta |

## Niveles de madurez

Todo elemento del vault lleva uno. El detalle y las reglas de transición están en `references/niveles-madurez.md`.

| Nivel | Significa | Qué hace el arnés con él |
|---|---|---|
| `desconocido` | Existe, pero no se sabe qué hace | Se copia tal cual del fragmento. Nunca se cambia ni se deduce |
| `hipotesis` | Idea con poca evidencia | No se depende de él: se pregunta o se propone una prueba |
| `inferido` | Evidencia consistente en el corpus o la documentación | Se usa, diciendo que no está confirmado |
| `verificado-captura` | Confirmado cruzando la interfaz con el archivo del mismo objeto | Se usa |
| `verificado-ida-y-vuelta` | Aplicado en un ambiente y extraído de vuelta igual | Se usa |
| `extraido-de-ejemplo` | (fragmentos) Sintaxis copiada tal cual de un ejemplo real | Base para componer; el significado está en el diccionario |
| `obsoleto` | Contradicho por evidencia nueva | No se usa; queda como historia |
| (sin nota) | No hay nada escrito | Es una pregunta o una brecha, nunca una suposición |

## Pasos

### 1. Organizar `contexto/` e inventariarlo

`contexto/` está protegido con `deny` desde el paso 2: **Claude no puede escribir ahí**. Por eso:
1. El **humano** carga el material y lo ordena en subcarpetas por tipo: `documentacion/`, `estandares/`, `ejemplos/<origen>/`,
   `capturas/<objeto>/`. Claude puede proponerle la distribución, pero no mueve archivos.
2. No se renombran ni editan los archivos originales. Si un nombre es ambiguo, se explica en el inventario, no se cambia.
3. Claude escribe el inventario **fuera** de `contexto/`, en `vault-patrones/inventario-contexto.md`: qué hay, cuántos, de dónde,
   de qué versión y si es confidencial.
4. Pedir al humano la confirmación de confidencialidad antes de versionar (skill `arnes-estructura`, paso 4).

**Termina cuando:** el inventario coincide con los conteos de la ficha del arnés.

### 2. Escribir el modelo del dominio

`vault-patrones/<dominio>/modelo.md`: una página que explica qué es el objeto que se construye, qué partes tiene, cómo se
relacionan y dónde se guarda en el sistema destino. Cada afirmación con su fuente (documento y página, o ejemplo).

**Termina cuando:** alguien que no conoce el sistema entiende de qué piezas se compone un entregable.

### 3. Construir el diccionario

`vault-patrones/<dominio>/diccionario/`: **una nota por sección** del formato del entregable (plantilla en
`references/nota-diccionario-plantilla.md`). Cada elemento en una fila con: nombre, significado, valores observados,
nivel de madurez, evidencia y qué hacer (ajustar desde la ficha, regla fija, copiar).

Reglas:
- Empezar todo en `desconocido` salvo que haya evidencia. Subir el nivel solo con la evidencia escrita en la fila.
- Si la documentación dice una cosa y el corpus otra, gana el corpus y se anota la contradicción.
- **Antes de marcar un elemento numérico como "copiar"**, comprobar si es una referencia a otra parte del mismo objeto:
  ¿todos sus valores caben dentro del conteo de alguna otra sección? Si sí, es una referencia y se **calcula**, no se copia
  (lección del piloto: una clave "copiar" resultó ser el índice de un contenedor; copiada a un objeto sin contenedores lo rompió).

**Termina cuando:** cada elemento visto en el corpus tiene fila, aunque sea `desconocido`.

### 4. Extraer fragmentos y generar la cobertura

Un **fragmento** es un trozo real del entregable copiado tal cual de un ejemplo (plantilla en `references/fragmento-plantilla.md`).
Es la unidad con la que el generador compone.

1. Escribir (o pedir que se escriba) una herramienta que recorra el corpus, clasifique cada elemento por **variante**
   (combinación de tipo y opciones que cambia la sintaxis) y cuente ocurrencias. Ver `arnes-generador`.
2. Por cada variante, elegir el ejemplo más representativo (de la versión del ambiente destino, de un origen confiable) y
   copiarlo tal cual como fragmento, con: origen exacto, ocurrencias, claves que se ajustan desde la ficha y claves que se copian.
3. Generar `cobertura.md`: tabla de variantes, ocurrencias, archivos y fragmento. **Una variante sin fila no tiene fragmento:
   si un diseño la necesita, es una brecha.**
4. Los fragmentos generados y la cobertura se **regeneran** con la herramienta; no se editan a mano. Los fragmentos que se
   agregan desde un ticket llevan otro nombre para que la regeneración no los pise.

**Termina cuando:** la cobertura está generada y cada variante frecuente tiene fragmento.

### 5. Arquetipos, anti-patrones y plantillas curadas

- `arquetipos/`: los tipos de pedido que llegan, un archivo por arquetipo (plantilla en `references/arquetipo-plantilla.md`) y un
  `arquetipos/README.md` con la tabla de arquetipos y cómo elegir uno. Cada arquetipo dice para qué
  sirve, qué piezas usa y **qué preguntas hay que hacer** antes de diseñar.
- `anti-patrones.md`: lo que aparece en el corpus y no se debe copiar, con el motivo.
- `plantillas-curadas.md`: los ejemplos del corpus que sirven de referencia, y por qué.

**Termina cuando:** cada pedido esperado cae en un arquetipo o se anota como arquetipo pendiente.

### 6. Bandeja de candidatos y lecciones

- `candidatos/README.md` con la plantilla (`references/candidato-plantilla.md`) y las subcarpetas `integrados/` y `descartados/`.
- `lecciones/README.md` con el formato de lección del dominio (`references/leccion-dominio-plantilla.md`).
- `vault-patrones/README.md` con la tabla de madurez, cómo crece y cómo se regenera lo generado
  (`references/vault-patrones-README-plantilla.md`).

**Termina cuando:** existe el circuito ticket → candidato → aprobación → integración.

## Cómo se verifica conocimiento

El procedimiento detallado de cada método está en `references/metodos-verificacion.md`. En resumen:

| Método | Cuándo usarlo | Sube a |
|---|---|---|
| **Cruce con el corpus** (contar cuántos ejemplos cumplen una regla y cuántos no) | Siempre, antes de cualquier otro | `inferido` si la regla se cumple sin excepciones o con excepciones explicadas |
| **Captura contra archivo** (la interfaz de un objeto y su extracción, misma versión) | Para lo que se ve en la interfaz | `verificado-captura` |
| **Ida y vuelta** (aplicar, extraer, comparar) | Para todo lo que se aplica | `verificado-ida-y-vuelta` |
| **Consulta de solo lectura** al ambiente | Para datos del ambiente (tipos, tablas, identificadores) | `verificado-captura` para datos del ambiente, con la consulta como evidencia |

Reglas que salieron del piloto:
- **Una regla sacada de pocas capturas no se lleva al generador** hasta cruzarla con el corpus. En el piloto, una regla de una
  captura resultó falsa en 369 de 412 casos.
- **Captura y archivo tienen que ser de la misma versión** del objeto. Comparar primero algún valor que ambos muestran
  (por ejemplo, un tamaño); si difiere, pedir una extracción nueva.
- **Una bandera "inferida" que decide qué se guarda o qué se bloquea** se confirma con captura antes de construir pruebas sobre ella.
- **La comparación del mismo objeto con todo desmarcado y con una opción marcada** identifica qué elemento corresponde a cada
  opción de la interfaz. Es la forma más barata de confirmar banderas.

## Control de salida

- [ ] `vault-patrones/inventario-contexto.md` con inventario y confidencialidad confirmada.
- [ ] `modelo.md` con fuentes.
- [ ] Diccionario: cada elemento del corpus con fila y madurez.
- [ ] Elementos numéricos "copiar" revisados como posibles referencias.
- [ ] Fragmentos por variante frecuente y `cobertura.md` generada por herramienta.
- [ ] Arquetipos con sus preguntas.
- [ ] Candidatos, lecciones y README del vault.

## Errores que ya cometimos (piloto de referencia)

- **"Desconocido, copiar" sin revisar si era una referencia** (ver paso 3). Rompió la aplicación en desarrollo.
- **Inferir una bandera al revés.** El corpus sugería un significado; la captura mostró el contrario. Tres campos de prueba se
  diseñaron sobre la suposición equivocada.
- **Sembrar el vault con conocimiento de un piloto anterior sin evidencia.** Se decidió partir de cero desde `contexto/`
  (decisión D06 del piloto): el conocimiento heredado sin evidencia es una hipótesis, no un dato.

## Siguiente paso

`arnes-fases-y-tickets`.
