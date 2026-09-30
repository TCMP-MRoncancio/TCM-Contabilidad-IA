# AGENTS.md — <nombre del arnés>

<Una línea: qué desarrolla o configura este arnés y para quién.>
El humano decide y aplica; los agentes analizan, diseñan, generan y revisan.

## Reglas duras
1. **Si te falta un dato, pregunta en vez de inventar.** Todo lo que afirmes lleva fuente (archivo, captura, consulta) o se marca como hipótesis.
2. **Apunta por tu cuenta lo que convenga recordar**, en el lugar que corresponde (ver "Dónde se anota qué").
3. **Nunca ejecutas nada que escriba en un ambiente.** El humano aplica en desarrollo. Las lecturas se hacen solo por la conexión de solo lectura.
4. **`contexto/` es solo lectura.** Es la fuente cruda; lo curado vive en `vault-patrones/`.
5. **El entregable se compone con conocimiento verificado.** Un elemento sin significado confirmado se copia tal cual del fragmento; nunca se deduce. Si el diseño pide algo sin fragmento, te detienes y abres una brecha.
6. **El entregable lo produce el generador.** No se edita a mano; si algo no se puede expresar en la ficha, se agrega a la ficha y se regenera.
7. **No se avanza de fase sin su control.** El diseño necesita aprobación explícita del humano. La revisión va antes de aplicar, nunca después.
8. <Prohibición del dominio, por ejemplo: "No se tocan objetos nativos del sistema destino".>
9. **El estado de los tickets vive en el vault del cliente**, no en la memoria automática de Claude Code.
10. **Git remoto y sistemas externos los opera el humano**: clonar, publicar, crear repos, mover tickets.

## Mapa del proyecto
| Carpeta | Qué es | Quién escribe |
|---|---|---|
| `contexto/` | Documentación y ejemplos reales | El humano (Claude solo lee) |
| `vault-patrones/` | Conocimiento reutilizable con nivel de madurez (repo propio) | Solo con aprobación; las propuestas van a `candidatos/` |
| `vault-cliente-<c>/` | Cliente, ambiente, inventario y seguimiento por ticket (repo propio) | Orquestador y agentes, dentro de su ticket |
| `vault-cliente-<c>/tickets/<t>/diseno/` | `ficha.yaml` (diseñador) y `diseno.md` (generador) | Diseñador y generador |
| `vault-cliente-<c>/tickets/<t>/salida/` | Entregable generado | Generador (lo corre el constructor u orquestador) |
| `memoria/` | Decisiones, lecciones y sesiones del sistema | Orquestador |
| `herramientas/` | Generador, validador, comparador, lint, tickets | Solo con aprobación |
| `.claude/` | Agentes, skills, hooks y permisos | Solo con aprobación |

## Protocolo de sesión
- **Al iniciar:** el hook de inicio muestra el estado del ticket activo (o la lista de tickets abiertos). Confirma con el humano en qué seguimos. Si no hay ticket activo, usa `/ticket`.
- **Durante:** actualiza `ESTADO.md` al cumplir cada control. Registra decisiones, preguntas e incidencias en el momento, no al final.
- **Al cerrar:** ejecuta `/cierre`. Las conversaciones se copian solas al vault con los hooks.
- **Si no sabemos cómo seguir o qué pasó con algo:** `/recuperar-contexto`.
- **Sesiones cortas:** al terminar un bloque grande, `/cierre` y sesión nueva.

## Dónde se anota qué
| Qué | Dónde |
|---|---|
| Avance, bloqueos y próximo paso del ticket | `vault-cliente-<c>/tickets/<t>/ESTADO.md` |
| Qué se hizo en cada sesión y por qué | `…/tickets/<t>/bitacora.md` |
| Decisiones del ticket | `…/tickets/<t>/decisiones.md` |
| Preguntas abiertas y sus respuestas | `…/tickets/<t>/preguntas.md` |
| Problemas y su resolución | `…/tickets/<t>/incidencias.md` |
| Capturas, pruebas y extracciones de vuelta | `…/tickets/<t>/evidencias/` |
| Datos del cliente y de su ambiente | `vault-cliente-<c>/cliente.md` y `ambiente/` |
| Algo que sirve para otros clientes | `vault-patrones/candidatos/` (se integra con aprobación) |
| Decisiones y lecciones sobre cómo trabajamos | `memoria/decisiones.md` y `memoria/lecciones.md` |

## Fases y controles
<Se completa con la skill arnes-fases-y-tickets.>

## Agentes
<Se completa con la skill arnes-agentes-y-skills.>
Los agentes no delegan entre sí: el orquestador los lanza, les pasa el ticket y guarda lo que devuelven.
Los agentes y skills los cambia el humano o se cambian con su aprobación; un agente no reescribe su propia definición.

## Skills
<Lista de skills de dominio y de sesión.>

## Herramientas
<Se completa con la skill arnes-generador: un comando por línea con su uso.>
