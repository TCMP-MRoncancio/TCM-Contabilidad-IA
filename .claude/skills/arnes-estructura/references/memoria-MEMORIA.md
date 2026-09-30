# Memoria del sistema

Memoria del arnés: lo que vale para **todos** los tickets y clientes sobre cómo trabajamos.
El estado de cada ticket no va aquí: vive en su vault de cliente. El conocimiento del dominio tampoco: vive en `vault-patrones/`.

| Archivo | Qué guarda |
|---|---|
| [[decisiones]] | Decisiones de diseño del arnés, con fecha y motivo (D01, D02…) |
| [[lecciones]] | Lecciones sobre cómo trabajar con Claude Code y con los agentes (M01, M02…) |
| `sesiones/` | Conversaciones sin ticket activo (las copian los hooks) y resúmenes de sesiones de diseño |

## Capas de memoria (de lo más resumido a lo más crudo)
1. `ESTADO.md` del ticket: lo inyecta el hook de inicio.
2. `bitacora.md`, `decisiones.md`, `preguntas.md` e `incidencias.md` del ticket: se escriben durante la sesión y en `/cierre`.
3. `sesiones/*.md` del ticket (o de aquí): extracto de cada conversación, escrito por los hooks.
4. `sesiones/raw/*.jsonl.gz`: la conversación completa comprimida (no se versiona).
5. Las conversaciones de Claude Code en el perfil del usuario: se conservan según `cleanupPeriodDays` y se retoman con `claude --resume`.

Para buscar algo perdido: `/recuperar-contexto`.
