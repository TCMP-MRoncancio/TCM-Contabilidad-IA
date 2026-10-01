# Contexto (no se versiona)

Esta carpeta es solo lectura y **no se sube al repositorio** (ver `.gitignore`): contiene material crudo con datos de produccion, como `Cargador_Datos_v21.xlsm` (la macro original) y cualquier exportacion real que se use como referencia.

## Por que no se versiona

El Excel y sus exportaciones contienen datos reales de produccion (numeros de cuenta, nombres reales, y en otras hojas del mismo archivo, informacion sensible de contrapartes bancarias). Mantenerlo fuera de git evita que esos datos queden en el historial del repositorio, incluso si despues se borra el archivo.

## Donde esta el conocimiento curado sobre este material

El inventario y la evidencia de regresion contra la macro (que prueba que el generador reproduce fielmente su salida) viven en `vault-patrones/inventario-contexto.md` -- ese si esta versionado, porque es el resultado curado, no el dato crudo.

## Que hacer si necesitas el material original

Pidele al consultor que te comparta el Excel o las muestras directamente; no deberian llegar por este repositorio.