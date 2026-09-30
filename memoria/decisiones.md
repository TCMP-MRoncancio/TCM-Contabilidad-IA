# Decisiones

- 2026-09: se descarta el nucleo generico multi-area (registro/organizacion.yaml) como base de este proyecto. Se adopta en su lugar el patron de vault-patrones / vault-proyecto-* / contexto / memoria, adaptado de un piloto de Custom Windows (CW), pero sin el concepto de tickets por ahora.
- 2026-09: las cuentas se generan siempre validadas contra schema + catalogo de proyectos + catalogo de enums; nunca se sobrescribe un .xml existente sin --forzar explicito.
- 2026-09: se adopta el plan de adecuacion al estandar de arnes TCM segun memoria/revision-arnes-2026-09-30.md; se ejecuta por bloques con aprobacion del consultor.
- 2026-09: se agregan denies de Bash (redireccion de shell) contra contexto/, ademas de Edit/Write. RIESGO ACEPTADO: no cubre toda forma posible de escritura por shell (ej. python -c, tee, cp); la defensa robusta seria restringir Bash a lista blanca estricta, pendiente de evaluar en un bloque posterior.