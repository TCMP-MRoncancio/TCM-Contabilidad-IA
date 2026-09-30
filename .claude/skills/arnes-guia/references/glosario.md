# Glosario del arnés

Términos en el orden en que aparecen al construir un arnés.

| Término | Definición | Dónde vive |
|---|---|---|
| Arnés (harness) | Estructura de carpetas, reglas, agentes, skills, herramientas, hooks y permisos que rodea a Claude Code para un caso de uso | Repo del arnés |
| Caso de uso | El tipo de trabajo que el arnés resuelve (por ejemplo: configurar ventanas en un sistema, generar interfaces, parametrizar reglas) | `ficha-arnes.md` |
| Entregable | Lo que se aplica en el sistema destino (un script, un archivo de configuración, un paquete) | Vault del cliente, carpeta del ticket |
| Sistema destino | Donde se aplica el entregable y de donde se puede extraer de vuelta | `vault-cliente-<c>/ambiente/` |
| Ambiente | Una instancia del sistema destino (desarrollo, QA, producción) | `vault-cliente-<c>/cliente.md` |
| Humano / consultor | La persona que decide, aprueba y aplica | — |
| Orquestador | La sesión principal de Claude Code; conduce el ticket y delega | `AGENTS.md` |
| Agente (subagente) | Definición que hace una tarea acotada con herramientas limitadas | `.claude/agents/<nombre>.md` |
| Skill | Instrucciones que se cargan cuando la tarea coincide con su descripción | `.claude/skills/<nombre>/SKILL.md` |
| Skill de dominio | Skill que sabe del caso de uso concreto (fundamentos, diseño, construcción, revisión) | `.claude/skills/` del arnés |
| Skill de sesión | Skill que maneja el ciclo de trabajo (`/ticket`, `/cierre`, `/recuperar-contexto`) | `.claude/skills/` del arnés |
| Hook | Script que Claude Code ejecuta solo en un evento (inicio, compactación, fin de sesión) | `.claude/hooks/` y `settings.json` |
| Permiso `deny` / `ask` | Regla de `settings.json` que bloquea una acción o pide confirmación | `.claude/settings.json` |
| `AGENTS.md` | Reglas del proyecto; `CLAUDE.md` lo importa | Raíz del arnés |
| `contexto/` | Material crudo: documentación, manuales, ejemplos reales. Solo lectura (lo carga el humano) | Raíz del arnés |
| `vault-patrones/` | Conocimiento curado y reutilizable, con nivel de madurez | Repo propio, clonado dentro del arnés |
| Vault del cliente | Datos del cliente, su ambiente y el seguimiento de cada ticket | `vault-cliente-<c>/`, repo propio |
| Nivel de madurez | Cuánto se puede confiar en un elemento del conocimiento | Frontmatter o columna de cada nota |
| Diccionario | Significado de cada elemento del formato del entregable, con su madurez | `vault-patrones/<dominio>/diccionario/` |
| Fragmento | Trozo real de un entregable, copiado tal cual de un ejemplo, que se usa como base para componer | `vault-patrones/<dominio>/fragmentos/` |
| Cobertura | Tabla de qué variantes tienen fragmento y cuántas veces aparecen en el corpus | `vault-patrones/<dominio>/cobertura.md` |
| Corpus | El conjunto de ejemplos reales disponibles | `contexto/` |
| Brecha | Algo que el diseño necesita y el conocimiento verificado no cubre | `preguntas.md` o `incidencias.md` del ticket |
| Candidato | Propuesta de conocimiento nuevo, pendiente de aprobación | `vault-patrones/candidatos/` |
| Lección | Algo que salió mal o casi, generalizado para no repetirlo | `memoria/lecciones.md` (sobre el método) o `vault-patrones/lecciones/` (sobre el dominio) |
| Decisión | Elección de diseño con fecha, motivo y quién | `memoria/decisiones.md` o `decisiones.md` del ticket |
| Ticket | Unidad de trabajo con su propio seguimiento | `vault-cliente-<c>/tickets/<t>/` |
| Ticket activo | El ticket en el que trabaja cada persona; es personal | `.claude/activo.local.json` |
| Ficha | Documento declarativo (YAML) del diseño de un ticket | `vault-cliente-<c>/tickets/<t>/diseno/ficha.yaml` |
| Documento de diseño | Versión legible de la ficha que aprueba el humano (lo escribe el generador) | `vault-cliente-<c>/tickets/<t>/diseno/diseno.md` |
| Generador | Script que produce el entregable desde la ficha | `herramientas/` |
| Validador | Script que revisa la ficha o el entregable contra reglas | `herramientas/` |
| Comparador | Script que compara lo generado con lo extraído del ambiente | `herramientas/` |
| Trazabilidad | Registro de dónde salió cada elemento del entregable (ficha, regla fija, fragmento) | Carpeta del ticket |
| Ida y vuelta | Generar, aplicar, extraer de vuelta y comparar | Fase de aplicación |
| Guarda | Bloque al inicio de un script de instalación que se detiene si lo que se va a crear ya existe | Entregable |
| Corrección de desarrollo | Script que corrige algo ya instalado en desarrollo; nunca se promueve | `entrega/` del ticket |
| Promoción | Paso del entregable a ambientes superiores | `entrega/promocion.md` |
| Ticket piloto de calibración | Primer ticket, chico y de bajo riesgo, pensado para recorrer todo el flujo y cerrar dudas | — |
| `/cierre` | Skill que deja la bitácora, el estado y los candidatos al día al terminar | `.claude/skills/cierre/` |
| `/recuperar-contexto` | Skill que busca información perdida de lo resumido a lo crudo | `.claude/skills/recuperar-contexto/` |
