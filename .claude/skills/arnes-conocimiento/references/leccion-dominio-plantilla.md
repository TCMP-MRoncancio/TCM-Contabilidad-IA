# Formato de una lección del dominio

Una lección es algo que salió mal o casi, generalizado para que no se repita en otro ticket o cliente.
Nace en un ticket (`incidencias.md` o `bitacora.md`), se propone en `candidatos/` y, aprobada, se escribe en `vault-patrones/lecciones/`.

- Un archivo por sesión o ticket de origen: `AAAA-MM-DD-<tema>.md`.
- Id correlativo (`L01`, `L02`…) que no se reutiliza aunque la lección quede obsoleta.

```
## Lxx · <título corto>
- Origen: <ticket o sesión> (<fecha>)
- Qué pasó: <hechos, con evidencia>
- Lección: <la regla general>
- Cómo se aplica: <qué hace distinto el arnés: regla, validación, nota del vault, herramienta>
- Estado: vigente | obsoleta (<por qué>)
```

Diferencia con `memoria/lecciones.md`: allí van las lecciones sobre **cómo trabajamos** (agentes, Claude Code, proceso);
aquí, las lecciones sobre **el sistema destino**.
