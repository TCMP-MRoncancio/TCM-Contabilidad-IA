# Lecciones sobre cómo trabajamos

Lecciones sobre Claude Code, agentes y proceso. Las lecciones sobre el dominio van en `vault-patrones/lecciones/`.
Cada lección con id correlativo (M01, M02…) que no se reutiliza.

## Mxx · <título corto>
<Qué pasó, con evidencia (ticket, fecha, archivo).>
Se aplica: <qué hace distinto el arnés desde ahora: regla, permiso, validación, cambio de herramienta>.

---

Lecciones heredadas del piloto de referencia que conviene copiar tal cual en un arnés nuevo. Se renumeran en este arnés:
las skills `arnes-*` citan las del piloto con su número original ("M15 del piloto"), que no coincide con esta numeración.

## M01 · Descripciones de agentes y skills en ASCII y entre comillas
El frontmatter YAML se rompe con tildes mal codificadas o con `: ` sin comillas dentro de la descripción, y el agente o la skill
deja de cargarse sin un error visible. Se aplica: descripciones ASCII entre comillas dobles.

## M02 · Los subagentes no delegan
Un subagente no puede lanzar otro. Se aplica: la sesión principal es el orquestador; los agentes hacen una tarea y devuelven el resultado.

## M03 · Claude no reescribe sus propios agentes ni skills
Si puede, las definiciones cambian solas durante el trabajo y el comportamiento deriva. Se aplica: editar `.claude/` pide aprobación
(permiso `ask`) y los cambios se registran en `memoria/decisiones.md`.

## M04 · Desconfiar de una sesión retomada
Una sesión retomada o compactada puede recordar un estado viejo. Se aplica: el hook de inicio inyecta `ESTADO.md` actual en
inicio, retomar, limpiar y compactar; ante diferencias, `/recuperar-contexto`.

## M05 · La revisión va antes de aplicar
Revisar después de aplicar obliga a corregir en el ambiente. Se aplica: la revisión es el control de la fase de construcción;
la ida y vuelta es un control distinto, después.

## M06 · El reverso es obligatorio al modificar algo existente
Para objetos nuevos, el reverso es borrar lo creado; para cambios sobre objetos o datos existentes, el reverso tiene que estar
escrito y probado antes de aplicar.

## M07 · Un solo lugar para cada cosa
Cuando el mismo dato vive en dos archivos, uno queda viejo. Se aplica: tabla "Dónde se anota qué" de AGENTS.md; las skills
apuntan a los archivos en lugar de copiarlos.

## M08 · Escribir archivos con final de línea explícito
En Windows, abrir un archivo en modo texto para escribir convierte `\n` en `\r\n`. Se aplica: `newline="\n"` al escribir
(o trabajar en bytes); después de una tanda de ediciones, revisar los finales de línea.

## M09 · Sesiones cortas
Una conversación de cientos de miles de tokens termina cortándose. Se aplica: `/cierre` y sesión nueva al terminar cada bloque grande.
