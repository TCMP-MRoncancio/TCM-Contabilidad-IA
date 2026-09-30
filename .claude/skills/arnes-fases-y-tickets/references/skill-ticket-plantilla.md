---
name: ticket
description: "Gestion de tickets del arnes. Usar con /ticket o cuando se pida ver el estado, listar, activar o crear un ticket o un cliente, o pasar un ticket de fase."
---

# /ticket

Cada ticket vive en `<dir_ticket>` (ver `.claude/arnes.json`): seguimiento, `diseno/`, `salida/`, `entrega/`, `evidencias/`, `sesiones/`.
El ticket activo es personal (`.claude/activo.local.json`) y el hook de inicio inyecta su estado.

## Qué hacer según el pedido
| Pedido | Acción |
|---|---|
| Ver en qué estamos | `python herramientas/ticket.py estado` y resumir: fase, control pendiente, próximo paso, bloqueos, preguntas |
| Ver los tickets | `python herramientas/ticket.py listar` |
| Cambiar de ticket | `python herramientas/ticket.py activar <cliente> <ticket>` y mostrar su estado |
| Crear un ticket | Pedir (si faltan) cliente, identificador, título y los datos que pida la plantilla; luego `python herramientas/ticket.py crear <cliente> <ticket> --titulo "<título>" [--jira <clave>] [--dato CLAVE=valor]` |
| Crear un cliente | `python herramientas/ticket.py nuevo-cliente <cliente>`; completar `cliente.md` con el humano |
| Pasar de fase | Ver abajo |

## Pasar de fase
1. Revisar el control de la fase actual (tabla de fases de AGENTS.md y lista de `ESTADO.md`).
2. Si se cumple, con la evidencia: marcar el control, cambiar `fase` y `control_pendiente` en el frontmatter, actualizar
   "Próximo paso" y `actualizado`, y agregar una línea en "Hecho" con la evidencia.
3. Si no se cumple, decir qué falta. Nunca marcar un control sin evidencia; la aprobación del diseño la da el humano, por escrito.

## Reglas
- `ESTADO.md` es la fuente de verdad del avance: se actualiza en el momento, no al final.
- No crear carpetas a mano: usar `ticket.py` para que las plantillas queden completas.
- Git remoto y sistemas externos los opera el humano.
