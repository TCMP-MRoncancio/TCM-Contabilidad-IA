# Métodos de verificación, paso a paso

## 1. Cruce con el corpus

**Sirve para:** confirmar o descartar una regla ("todo X tiene Y", "el valor de Z siempre cabe en W").

1. Escribir la regla como una condición que se pueda contar: "para todo elemento con A, se cumple B".
2. Escribir un script de solo lectura que recorra `contexto/`, cuente cuántos casos cumplen y cuántos no, y liste las excepciones
   con su archivo. El script va en el scratchpad o en `herramientas/` si se va a repetir; nunca escribe en `contexto/`.
3. Mirar **todas** las excepciones. Una excepción explicada (otra versión, otro tipo) se documenta; una sin explicar impide pasar a `inferido`.
4. Anotar en la fila del diccionario: "N de M casos (script, fecha)". Guardar el script si otro lo va a repetir.

**Prueba de referencia (elemento numérico sin significado):** para cada valor distinto de cero, comprobar si es menor o igual que
el conteo de alguna otra sección del mismo objeto. Si 100 % de los casos caben, es casi seguro una referencia. En el piloto,
253 de 253 valores cabían en el conteo de contenedores: la clave era el índice del contenedor.

**Limitación:** el corpus muestra qué es habitual, no qué es obligatorio ni qué hace. Un cruce perfecto da `inferido`, no más.

## 2. Captura contra archivo

**Sirve para:** saber qué elemento del archivo corresponde a cada opción de la interfaz.

1. Elegir un objeto que exista **en la interfaz y en el corpus en la misma versión**. Confirmarlo comparando un valor que ambos
   muestran (un tamaño, un nombre, una cantidad). Si difiere, pedir una extracción nueva de ese objeto.
2. Pedir al humano capturas de las pantallas donde se ven las opciones que interesan.
3. Comparar opción por opción con el archivo. El atajo más eficaz: un objeto con **todo desmarcado** contra el mismo objeto con
   **una sola opción marcada**; la única diferencia en el archivo es el elemento de esa opción.
4. Anotar en el diccionario: "Verificado: captura <archivo> y extracción <archivo> (fecha, quién)".

**Trampas conocidas:** una bandera puede estar invertida (marcado = 0); una regla sacada de una sola captura puede no valer en general
(cruzarla con el corpus antes de llevarla al generador); seleccionar un elemento en la interfaz puede moverlo sin querer.

## 3. Ida y vuelta

**Sirve para:** la verificación más fuerte de todo lo que se aplica.

1. Generar el entregable desde la ficha.
2. El humano lo aplica en desarrollo con la herramienta real de aplicación.
3. El humano extrae de vuelta el mismo objeto con la herramienta real de extracción y deja el archivo en `evidencias/`, sin editarlo.
4. Correr el comparador entre lo generado y lo extraído.
5. **Cada diferencia se explica** en una de tres categorías:
   - el sistema normalizó un valor → conocimiento nuevo (candidato);
   - la ficha no se tradujo bien → error del generador (incidencia);
   - alguien cambió algo en la interfaz → cambio manual (se decide si vuelve a la ficha).
6. Ninguna diferencia sin explicar. Los valores que el sistema recalcula siempre (tamaños de vista, fechas) se declaran una vez
   como "no cuentan" en la herramienta.

**Además:** verificar lo que la extracción no muestra. En el piloto, la herramienta de aplicación agregaba un carácter invisible
que la extracción normalizaba; solo una consulta directa al dato guardado (longitud del texto) lo reveló.

## 4. Consulta de solo lectura

**Sirve para:** datos del ambiente (tipos de columnas, identificadores, existencia de objetos, contenido guardado).

1. La consulta la corre el humano o un MCP de **solo lectura**. Nunca una conexión con permisos de escritura.
2. Se escribe completa, sin abreviaciones (una consulta con "..." genera errores de sintaxis), con bloqueo de lectura mínimo si el motor lo permite.
3. El resultado se copia a `evidencias/` o a `ambiente/` con fecha.
4. Medir en bytes o longitudes cuando el problema puede ser invisible (espacios, finales de línea, codificación).

## 5. Qué método elegir

| Pregunta | Método |
|---|---|
| ¿Esta regla vale siempre? | Cruce con el corpus |
| ¿Qué hace esta opción de la interfaz? | Captura contra archivo |
| ¿Lo que generamos funciona igual en el sistema? | Ida y vuelta |
| ¿Qué hay guardado de verdad? | Consulta de solo lectura |
| ¿Por qué falló? | Los cuatro, en ese orden, hasta encontrar la causa |
