# Promoción · <ticket> · <objeto>

> Generado por `herramientas/<generador>` desde la ficha aprobada el AAAA-MM-DD. No editar a mano.
> **Se promueve el contenido de `salida/`.** Lo que está en `entrega/*-CORRECCION-DEV*` es solo de desarrollo.

## 1. Qué se aplica y en qué orden
| Orden | Archivo | Ambiente / base | Qué crea o modifica |
|---|---|---|---|
| 1 | `salida/<objeto>.<ext>` (con guarda) | | |
| 2 | | | |

El objeto con guarda va primero: si ya existe, la instalación se detiene antes de crear cualquier otra pieza.

## 2. Dependencias
- <Pieza A necesita B.> <Objetos del ambiente que deben existir.>

## 3. Prueba de la guarda (solo en desarrollo)
1. Aplicar el archivo 1 **por segunda vez**.
2. Resultado esperado exacto: <mensaje de error de la guarda>. <Líneas que parecen error y son normales, si las hay.>
   Lo que **no** debe aparecer: <indicio de que se modificó algo>.
3. Verificación (solo lectura):
   ```
   <consulta completa>
   ```
   Debe devolver: <resultado>.

## 4. Verificaciones después de aplicar
| # | Qué | Consulta de solo lectura (completa) | Debe devolver |
|---|---|---|---|
| 1 | | | |

## 5. Pasos fuera del script
- <Reiniciar, recargar, habilitar: lo que el humano hace a mano en el sistema.>

## 6. Datos existentes y respaldo
- <No aplica: solo se crean objetos nuevos.> | <Qué se modifica, cómo se respalda antes.>

## 7. Reverso
- <Solo si se modifica algo existente: script de reverso, probado en desarrollo el AAAA-MM-DD.>

## 8. Retiro
- <Cómo se elimina el objeto si hay que retirarlo.>

## 9. Solo desarrollo (no se promueve)
- <Correcciones de desarrollo, elementos de calibración.>

## Notas de la herramienta de aplicación
- <Por ejemplo: ejecutar el archivo sin editarlo ni guardarlo; si el editor ofrece convertir los finales de línea, no convertir.
  Alternativa por consola, si existe.>
