---
nota: diccionario
seccion: <nombre de la sección del formato>
dominio: <dominio>
actualizado: AAAA-MM-DD
---
# Diccionario · <sección>

<Qué es esta sección del entregable, cuántas veces aparece por objeto, en qué orden va, cómo se relaciona con las demás.>

| Elemento | Significado | Valores observados | Madurez | Evidencia | Qué hacer |
|---|---|---|---|---|---|
| `<clave>` | <qué hace, o "sin significado identificado"> | `0` (N), `1` (M) | desconocido | Aparece en N ejemplos | copiar del fragmento |
| `<clave>` | <…> | <…> | inferido | N de N ejemplos (herramienta, fecha) | ajustar desde la ficha: `<campo de la ficha>` |
| `<clave>` | <…> | <…> | verificado-captura | Captura X + archivo Y (fecha, quién) | regla fija del generador |
| `<clave>` | Índice de <otra sección> (0 = ninguno) | 0..N | verificado-ida-y-vuelta | Ticket T, evidencia E | calcular: <cómo> |

Valores posibles de "Qué hacer":
- **copiar del fragmento**: el generador toma el valor del fragmento; el diseño no lo toca.
- **ajustar desde la ficha: `<campo>`**: el valor sale de la ficha del ticket.
- **regla fija del generador**: siempre el mismo valor, con motivo conocido.
- **calcular: <cómo>**: el valor depende de otras partes del objeto (referencias, conteos, posiciones).

## Contradicciones con la documentación
- <La documentación dice X; el corpus muestra Y en N de M casos.>

## Historia
- AAAA-MM-DD · `<clave>` de `inferido` a `verificado-captura` (candidato C, ticket T).
