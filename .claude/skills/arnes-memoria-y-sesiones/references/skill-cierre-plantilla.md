---
name: cierre
description: "Cierre de sesion. Usar con /cierre, cuando el humano diga que termina por hoy, al terminar un bloque grande de trabajo o antes de cambiar de ticket, para dejar la bitacora, el estado y los candidatos al dia."
---

# /cierre

Objetivo: que la próxima sesión (o cualquier persona) sepa qué se hizo, qué falta y por qué, sin leer la conversación.

## Pasos (sobre el ticket activo)
Sin ticket activo solo se hacen los pasos 4, 5 y 7 (candidatos, memoria del sistema e informe); la conversación la guarda el hook
en `memoria/sesiones/`.

1. **Bitácora**: una entrada nueva **al final** (el hook muestra las dos últimas, hasta ~900 caracteres: ser breve):
   ```
   ## AAAA-MM-DD · <tema de la sesión> · fase <n>
   **Hecho:** <qué se hizo, con rutas de archivos>
   **Decidido:** <decisiones y por qué, o "nada"> (detalle en decisiones.md)
   **Aprendido:** <lo nuevo sobre el sistema o el cliente, con evidencia> (omitir si no hubo)
   **Pendiente:** <qué quedó a medias y dónde>
   ```
2. **ESTADO.md**: frontmatter (`fase`, `control_pendiente`, `actualizado`) y secciones "Próximo paso", "En curso", "Bloqueos",
   "Preguntas abiertas" y "Hecho". Controles marcados solo con evidencia.
3. **decisiones.md**, **preguntas.md**, **incidencias.md**: lo que haya surgido y no esté registrado (con fecha).
4. **Candidatos**: si se confirmó un elemento, se consiguió un fragmento nuevo, apareció una trampa o una lección del dominio,
   crear el candidato en `vault-patrones/candidatos/` y mencionarlo en la bitácora.
5. **Memoria del sistema**: solo si surgió algo sobre cómo trabajamos que vale para todos los tickets (`memoria/decisiones.md`
   o `memoria/lecciones.md`). Si fue un error de un agente o skill, agregarlo a su sección "Errores que ya cometimos" (con aprobación).
6. **Verificar**: releer `ESTADO.md` y confirmar que "Próximo paso" se entiende sin contexto. Correr
   `python .claude/hooks/cargar_estado.py < /dev/null` (en Windows: `echo {} | python .claude\hooks\cargar_estado.py`) para ver
   exactamente lo que inyectará el hook la próxima vez.
7. Decir al humano en dos o tres líneas qué quedó registrado y cuál es el próximo paso. Si el bloque fue grande, recomendar
   abrir una sesión nueva.

## Notas
- La conversación se copia sola a `sesiones/` con los hooks; la bitácora es el resumen que se lee primero.
- Si el humano va a aplicar algo en un ambiente, dejar escrito exactamente qué archivo, en qué orden y qué debe devolver.
