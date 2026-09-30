---
name: arnes-guia
description: "Punto de entrada para construir un arnes (harness) de Claude Code para un caso de uso de desarrollo o configuracion. Usar cuando alguien quiera armar un arnes nuevo, pregunte por donde empezar, que es un arnes, en que orden se construye o que skill arnes-* usar. No usar para trabajar dentro de un arnes ya construido (ahi mandan su AGENTS.md y sus skills de dominio)."
---

# Guía para construir un arnés

Un **arnés** es la estructura que rodea a Claude Code para que un tipo de trabajo repetitivo y delicado se haga siempre igual,
con control humano y sin perder memoria entre sesiones. No es un prompt largo: son carpetas, reglas, agentes, skills,
herramientas deterministas, hooks y permisos que trabajan juntos.

Esta skill es el mapa. No construye nada por sí sola: dice qué skill usar en cada momento y en qué orden.

## Cuándo conviene un arnés (y cuándo no)

Conviene cuando se cumplen **al menos tres** de estas condiciones:

| # | Condición | Pregunta para comprobarla |
|---|---|---|
| 1 | El trabajo se repite (tickets, casos, clientes) | ¿Vamos a hacer esto más de cinco veces? |
| 2 | El entregable tiene un formato estricto que una máquina lee | ¿Un error de una coma rompe algo? |
| 3 | Hay un ambiente real donde se aplica y se puede comprobar | ¿Podemos aplicar, extraer de vuelta y comparar? |
| 4 | Equivocarse es caro o riesgoso | ¿Un error llega a un cliente, a producción o a datos? |
| 5 | El conocimiento está disperso o incompleto | ¿Hay ejemplos reales pero nadie sabe qué significa cada parte? |
| 6 | Varias personas o sesiones van a trabajar en lo mismo | ¿Alguien más va a retomar esto? |

**No conviene** para una tarea única, para exploración libre o cuando no existe forma de verificar el resultado.
En esos casos basta con una conversación o una skill simple.

## Los diez principios (resumen)

El detalle y su origen están en `references/principios.md`. Toda decisión del arnés debe poder justificarse con alguno.

1. **Roles separados.** El humano decide y aplica; el orquestador conduce; los agentes hacen una tarea con las herramientas mínimas.
2. **Ficha declarativa más generador determinista.** El LLM llena una ficha; un script produce el entregable. Lo generado no se edita a mano.
3. **Conocimiento con nivel de madurez.** Nada se inventa: lo desconocido se copia tal cual o se abre una brecha.
4. **Verificación empírica.** Se aplica, se extrae de vuelta y se compara. Lo que no se verificó se dice.
5. **Fases con controles.** Ninguna fase avanza sin evidencia; el diseño lo aprueba el humano, explícitamente.
6. **Memoria en archivos, no en la conversación.** Estado, bitácora y decisiones por ticket; hooks que cargan y guardan.
7. **Seguridad por configuración.** Permisos que bloquean, no solo reglas escritas.
8. **Repos separados** para el arnés, el conocimiento reutilizable y los datos de cada cliente.
9. **Entrega segura.** Se promueve lo generado y revisado; las correcciones de un ambiente van aparte.
10. **Colaboración explícita.** Claude Code ejecuta, un revisor (Cowork u otra sesión) revisa, el humano hace de puente y aprueba.

## Orden de construcción

Seguir este orden. Cada paso produce un archivo que el siguiente necesita.

| Paso | Skill | Produce | No avanzar sin |
|---|---|---|---|
| 1 | `arnes-concepcion` | `ficha-arnes.md` aprobada | Las 12 preguntas respondidas o marcadas como brecha |
| 2 | `arnes-estructura` | Esqueleto: carpetas, AGENTS.md, CLAUDE.md, settings.json, .gitignore | Permisos `deny` probados |
| 3 | `arnes-conocimiento` | `contexto/` con el material crudo y `vault-patrones/` inicial | Diccionario con nivel de madurez por elemento |
| 4 | `arnes-fases-y-tickets` | Tabla de fases, plantillas de seguimiento, herramienta de tickets | Un ticket de prueba creado con la herramienta |
| 5 | `arnes-generador` | Formato de la ficha, generador, validador, comparador, lint | Ida y vuelta sobre el corpus sin diferencias |
| 6 | `arnes-agentes-y-skills` | Agentes y skills de dominio | Cada agente con herramientas mínimas y formato de retorno |
| 7 | `arnes-memoria-y-sesiones` | Hooks instalados, `/cierre`, `/recuperar-contexto` | El hook de inicio muestra el ticket de prueba |
| 8 | `arnes-seguridad-y-entrega` | Checklist de seguridad cumplido y plantilla de promoción | Checklist sin puntos abiertos |
| 9 | (uso) | **Ticket piloto de calibración** recorrido de punta a punta | Lecciones registradas y herramientas corregidas |

El paso 9 no es opcional. El primer ticket real siempre encuentra errores del arnés (en el piloto de referencia aparecieron
al menos seis que ningún análisis previo había detectado). Por eso el primer ticket debe ser **chico, de bajo riesgo y diseñado para
cerrar dudas**, no para entregar valor de negocio.

Se puede volver a un paso anterior cuando el piloto lo pida: es lo normal. Cada vuelta se registra como decisión.

## Qué pedirle a Claude en cada momento

- "Quiero armar un arnés para X" → empezar por `arnes-concepcion`.
- "Ya tengo la ficha del arnés aprobada" → `arnes-estructura`.
- "Tengo ejemplos reales pero no sé qué significa cada parte" → `arnes-conocimiento`.
- "¿Cómo defino las fases?" → `arnes-fases-y-tickets`.
- "¿Cómo evito que Claude escriba el entregable a mano?" → `arnes-generador`.
- "¿Qué agentes necesito?" → `arnes-agentes-y-skills`.
- "Se pierde lo que hablamos entre sesiones" → `arnes-memoria-y-sesiones`.
- "¿Cómo lo protejo? ¿Cómo entrego?" → `arnes-seguridad-y-entrega`.

## Reglas para quien construye el arnés

1. **Si falta un dato, se pregunta.** Nunca se completa con una suposición razonable. Una suposición razonable es exactamente
   el tipo de error que el arnés existe para evitar.
2. **Nada específico de otro dominio.** Las skills `arnes-*` traen ejemplos del piloto de referencia (Custom Windows de Kondor+);
   son ilustraciones marcadas como tales. No se copia su vocabulario ni sus reglas a otro caso sin comprobar que aplican.
3. **Un solo lugar para cada cosa.** Si un dato vive en dos archivos, uno queda viejo. Las skills apuntan a los archivos; no los copian.
4. **Todo cambio al arnés se registra** en `memoria/decisiones.md` con fecha, motivo y quién lo decidió.
5. **Sesiones cortas.** Una conversación que crece sin límite termina cortándose y se pierde. Cerrar con `/cierre` al terminar
   cada bloque grande y abrir una sesión nueva.

## Glosario mínimo

El glosario completo está en `references/glosario.md`. Lo indispensable:

- **Orquestador**: la sesión principal de Claude Code. Conduce, pregunta, delega y cuida la memoria.
- **Agente (subagente)**: definición en `.claude/agents/` que hace una tarea acotada y devuelve un resultado.
- **Skill**: instrucciones en `.claude/skills/<nombre>/SKILL.md` que se cargan cuando la tarea coincide con su `description`.
- **Ficha**: documento declarativo (YAML) que describe *qué* se quiere; el generador decide *cómo* se escribe.
- **Ida y vuelta**: generar, aplicar en el ambiente, extraer de vuelta y comparar con lo generado.
- **Brecha**: algo que el diseño necesita y que el conocimiento verificado no cubre. Se resuelve una vez y se registra.
- **Candidato**: propuesta de conocimiento nuevo, pendiente de aprobación humana.
- **Ticket**: una unidad de trabajo con su propio seguimiento (estado, bitácora, decisiones, preguntas, incidencias, evidencias).

## Siguiente paso

Cargar `arnes-concepcion` y responder sus preguntas antes de crear cualquier carpeta.
