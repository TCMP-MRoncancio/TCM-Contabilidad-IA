# Los diez principios del arnés, con su origen

Cada principio dice **qué** se hace, **por qué** (el problema que evita) y **cómo se comprueba** que un arnés lo cumple.
El origen remite al piloto de referencia (arnés de Custom Windows de Kondor+, TCM Partners, 2026-09). Los identificadores
D.. y M.. son decisiones y lecciones de ese piloto; sirven para entender el motivo, no para copiar el dominio.

---

## 1. Roles separados

**Qué.** Tres tipos de actor con límites claros:

| Actor | Hace | No hace |
|---|---|---|
| Humano (consultor, desarrollador) | Decide, aprueba, aplica en el ambiente, opera git remoto y sistemas externos (Jira, correo) | No delega la aprobación |
| Orquestador (sesión principal) | Conduce las fases, pregunta, lanza agentes, corre herramientas, actualiza el seguimiento | No construye el entregable a mano |
| Agentes especializados | Una tarea acotada (diseñar, construir, revisar) con las herramientas mínimas | No delegan en otros agentes, no editan el seguimiento, no marcan controles |

**Por qué.** Un solo actor que diseña, construye, revisa y aprueba no detecta sus propios errores y termina marcando como
hecho lo que no está hecho.

**Origen.** En el piloto, el agente constructor marcó el control de fase 3 sin la revisión independiente; el diseñador usó
Bash para editar archivos por fuera de su herramienta. Se corrigió quitándole herramientas, no con más texto (M02, incidencias
del ticket piloto).

**Se comprueba.** Cada agente tiene en su frontmatter solo las herramientas que necesita; ninguna definición de agente
menciona editar el estado del ticket; el control del diseño exige una aprobación escrita por el humano.

## 2. Ficha declarativa más generador determinista

**Qué.** El diseño se expresa en una **ficha** (YAML) que dice *qué* se quiere. Un **script** determinista produce el entregable,
la trazabilidad y el documento de diseño a partir de la ficha. El entregable generado no se edita a mano: si algo no se
puede expresar, se agrega a la ficha (por ejemplo, un bloque de código manual declarado) y se regenera.

**Por qué.** Un LLM que escribe el entregable a mano varía entre sesiones, se salta detalles de formato y no deja rastro de
por qué cada línea es como es. Un script repite siempre lo mismo y se puede probar contra ejemplos reales.

**Origen.** D15, D16: la ficha mapea cada atributo a una clave del formato de salida; `ficha_a_cw.py` genera todo.
El generador reproduce exactamente 86 exports reales de referencia (ida y vuelta sobre el corpus).

**Se comprueba.** Existe una herramienta `generar`; existe `validar` para la ficha; existe una prueba de regresión sobre el
corpus; el entregable trae una trazabilidad que dice de dónde salió cada elemento.

## 3. Conocimiento con nivel de madurez

**Qué.** El material crudo (documentación, ejemplos reales) vive en `contexto/` y es de solo lectura. El conocimiento curado
vive en `vault-patrones/` y **cada elemento declara cuánto se puede confiar en él**: desconocido, hipótesis, inferido,
verificado por captura, verificado por ida y vuelta, obsoleto. Lo nuevo entra por `candidatos/` y se integra con aprobación.

**Por qué.** Sin niveles, una suposición se vuelve "dato" después de dos sesiones y nadie sabe de dónde salió.

**Regla central.** Un elemento `desconocido` se copia tal cual de un ejemplo real; nunca se deduce. Si el diseño necesita algo
que ningún ejemplo cubre, es una **brecha**: se detiene, se resuelve una vez en el sistema real y se registra.

**Origen.** D07, D08. Lección M12: una clave marcada "desconocido, copiar" resultó ser una referencia a otra sección; copiada
a un contexto distinto hizo caer la aplicación. La regla se refinó: antes de copiar un valor numérico sin significado, cruzarlo
con el corpus para ver si es una referencia.

**Se comprueba.** Cada nota del vault tiene `estado:` en su frontmatter o columna de madurez; existe `candidatos/README.md`
con plantilla; las skills de dominio dicen qué hacer según cada nivel.

## 4. Verificación empírica

**Qué.** Todo lo que se afirma sobre el sistema destino tiene fuente (archivo, captura, consulta) o se marca como hipótesis.
Los métodos, de menor a mayor fuerza: cruce con el corpus de ejemplos, captura de la interfaz contra su export, aplicación
y extracción de vuelta (ida y vuelta).

**Por qué.** La documentación del fabricante y la intuición fallan en los detalles. En el piloto, tres supuestos razonables
resultaron falsos al aplicar.

**Origen.** M10, M11, M13, M14. Casos: una bandera que significaba lo contrario de lo supuesto (`Display`); una regla sacada
de una captura que el corpus contradecía (369 contra 43); un editor (SSMS) que modificaba el texto al ejecutar aunque el
archivo estuviera correcto.

**Se comprueba.** Existe una herramienta `comparar`; la fase de aplicación exige "ninguna diferencia sin explicar"; las
lecciones citan la evidencia.

## 5. Fases con controles

**Qué.** El trabajo de cada ticket avanza por fases numeradas. Cada fase tiene un **control** verificable. La revisión va
**antes** de aplicar; la ida y vuelta, después. El diseño necesita aprobación explícita del humano.

**Por qué.** Sin controles, las fases se solapan y los errores llegan al ambiente.

**Origen.** D12, M05. Tabla de fases 0 a 7 del piloto (alta, requerimiento, diseño, construcción, aplicación, pruebas,
entrega, cierre).

**Se comprueba.** `ESTADO.md` de cada ticket trae la lista de controles y solo se marcan con evidencia.

## 6. Memoria en archivos

**Qué.** El estado de cada ticket vive en archivos del vault del cliente: `ESTADO.md` (dónde estamos), `bitacora.md` (qué se hizo),
`decisiones.md`, `preguntas.md`, `incidencias.md` y `evidencias/`. Los hooks cargan el estado al iniciar y copian la
conversación al cerrar o compactar. `/cierre` deja todo al día; `/recuperar-contexto` busca de lo resumido a lo crudo.

**Por qué.** La conversación se compacta, se corta o la retoma otra persona. Lo que no está en un archivo se pierde.

**Origen.** D04, D11, M04. En el piloto, una sesión de más de 460.000 tokens se cortó con un error del proceso; el trabajo se
retomó desde los archivos sin pérdida.

**Se comprueba.** El hook de inicio imprime fase, control pendiente y próximo paso del ticket activo; existe `/cierre`.

## 7. Seguridad por configuración

**Qué.** Las acciones peligrosas se bloquean en `.claude/settings.json` (`deny`) o piden confirmación (`ask`). Los agentes no
ejecutan nada que escriba en el ambiente; las lecturas van por una conexión de solo lectura; las credenciales viven en
variables de entorno; git remoto y sistemas externos los opera el humano.

**Por qué.** Una regla escrita se puede saltar sin querer; un permiso denegado no.

**Origen.** D09, D10, M03. Lista `deny` del piloto: editar `contexto/`, clientes de base de datos por consola, `git push`,
`git clone`, crear repos. Lista `ask`: editar el vault de patrones, `.claude/` y las herramientas.

**Se comprueba.** Intentar una acción denegada en una sesión de prueba y ver que se bloquea.

## 8. Repos separados

**Qué.** El arnés (reglas, agentes, skills, herramientas) es un repo. El conocimiento reutilizable (`vault-patrones`) es otro.
Cada cliente tiene su vault propio. Los vaults se clonan **dentro** de la carpeta del arnés y el `.gitignore` del arnés los excluye.

**Por qué.** El arnés y los patrones se comparten con todos; los datos de un cliente, solo con su equipo.

**Origen.** D05.

**Se comprueba.** `git status` del arnés no lista archivos de ningún vault.

## 9. Entrega segura

**Qué.** Se promueve a los ambientes superiores **lo generado y revisado**, nunca una extracción manual de un ambiente de
desarrollo. Las correcciones sobre algo ya instalado en desarrollo van en un archivo aparte, rotulado "no promover".
Las instalaciones llevan guardas de idempotencia (fallar si ya existe lo que se va a crear). Los finales de línea y la
codificación se controlan porque las herramientas de ejecución los alteran.

**Por qué.** Una extracción de desarrollo arrastra cambios manuales no revisados y pierde las protecciones del generador.

**Origen.** D21 (guarda que detiene la instalación si el identificador ya existe), D24, D25 (el editor agregaba un carácter
de fin de línea al ejecutar; se neutralizó dentro del propio script).

**Se comprueba.** La plantilla de promoción dice qué archivo se promueve, en qué orden, qué prueba confirma la guarda y qué
pasos quedan fuera del script.

## 10. Colaboración explícita

**Qué.** Claude Code es el único que escribe en la carpeta del arnés. Un revisor (Claude en Cowork u otra sesión) revisa los
reportes, verifica contra los archivos en modo lectura y prepara los mensajes. El humano hace de puente: aplica, trae
resultados y aprueba **con sus propias palabras**.

**Por qué.** Un segundo par de ojos encontró en el piloto errores reales que el ejecutor había dado por buenos (una cifra mal
reportada, una regla que el corpus contradecía, una causa mal atribuida).

**Se comprueba.** Las aprobaciones de fase quedan escritas por el humano en `ESTADO.md` o en la bitácora.
