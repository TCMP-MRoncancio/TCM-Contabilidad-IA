# Decisiones

- 2026-09: se descarta el nucleo generico multi-area (registro/organizacion.yaml) como base de este proyecto. Se adopta en su lugar el patron de vault-patrones / vault-proyecto-* / contexto / memoria, adaptado de un piloto de Custom Windows (CW), pero sin el concepto de tickets por ahora.
- 2026-09: las cuentas se generan siempre validadas contra schema + catalogo de proyectos + catalogo de enums; nunca se sobrescribe un .xml existente sin --forzar explicito.
