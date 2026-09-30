# Niveles de madurez: definición y transiciones

## Definición

| Nivel | Evidencia mínima para asignarlo | Cómo se escribe |
|---|---|---|
| `desconocido` | El elemento aparece en al menos un ejemplo real | `estado: desconocido` y "Evidencia: aparece en N ejemplos, valores observados: …" |
| `hipotesis` | Una idea plausible, sin conteo | "Hipótesis: … Cómo probarla: …" |
| `inferido` | Cruce con el corpus sin excepciones sin explicar, o documentación coherente con el corpus | "Inferido: N de N ejemplos … (herramienta y fecha)" |
| `verificado-captura` | Captura de la interfaz y archivo del mismo objeto, misma versión, coinciden | "Verificado: captura X y archivo Y (fecha, quién)" |
| `verificado-ida-y-vuelta` | Se aplicó en un ambiente, se extrajo de vuelta y el comparador no dio diferencias sin explicar | "Verificado ida y vuelta: ticket T, fecha, archivo de evidencia" |
| `extraido-de-ejemplo` | Solo para fragmentos: copia literal de un ejemplo real | "Origen: archivo, objeto, ocurrencias" |
| `obsoleto` | Evidencia nueva que contradice el nivel anterior | "Obsoleto desde AAAA-MM-DD: … (evidencia)". No se borra |

## Transiciones permitidas

```
desconocido ──► hipotesis ──► inferido ──► verificado-captura ──► verificado-ida-y-vuelta
     │              │             │                 │
     └──────────────┴─────────────┴─────────────────┴──► obsoleto (cuando la evidencia contradice)
```

- Se puede saltar niveles si la evidencia es del nivel de destino (por ejemplo, de `desconocido` a `verificado-ida-y-vuelta`).
- **Bajar** de nivel solo pasando por `obsoleto` y registrando una lección: una contradicción siempre enseña algo.
- Subir de nivel en el vault requiere un **candidato aprobado**. En un ticket, el hallazgo se anota en `incidencias.md` o
  `bitacora.md` y se propone como candidato en `/cierre`.

## Qué hace cada agente según el nivel

| Nivel | Diseñador | Constructor / generador | Revisor |
|---|---|---|---|
| `desconocido` | No lo diseña: lo deja con el valor del fragmento | Copia el valor del fragmento | Marca como error cualquier valor distinto al del fragmento |
| `hipotesis` | Pregunta o propone una prueba | No construye sobre él | Marca como bloqueante si el entregable depende de él |
| `inferido` | Lo usa y lo anota como supuesto | Lo usa | Lo lista como "a confirmar en la ida y vuelta" |
| `verificado-*` | Lo usa | Lo usa | Comprueba que se usó bien |
| `obsoleto` | No lo usa | No lo usa | Marca como error si aparece |
| (sin nota) | Pregunta o abre una brecha | Se detiene | Marca como bloqueante |
