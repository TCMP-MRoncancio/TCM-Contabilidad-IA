# Ejemplo: ficha del arnés del piloto de referencia (resumida)

> **Ilustración.** Este es el caso real que originó estas skills: un arnés para desarrollar Custom Windows (CW) de Kondor+,
> un sistema de tesorería. Sirve para ver cómo quedan las respuestas; no copiar su vocabulario a otro caso.

| # | Pregunta | Respuesta del piloto |
|---|---|---|
| 1 | Entregable | Script SQL que inserta la configuración de la ventana (un texto de líneas `Clave:Valor` dentro de un literal) más procedimientos y tablas SQL. Lo lee Kondor al abrir la ventana |
| 2 | Sistema y ambientes | Kondor+ 3.5.7, base SQL Server. Hay tres formatos de exportación según la versión y el tipo de base; el ambiente del piloto usa uno |
| 3 | Cómo se aplica | El consultor lo ejecuta en SSMS en desarrollo. **Hallazgo tardío:** SSMS convertía los saltos de línea al ejecutar y dejaba un carácter extra en la configuración |
| 4 | Extracción de vuelta | Sí: la función "Distribution" de Kondor exporta la ventana instalada en el mismo formato |
| 5 | Ejemplos | 85 exportaciones con 181 ventanas de varios clientes; 407 archivos de procedimientos; 32 capturas de la interfaz. Confidencial: código de clientes |
| 6 | Documentación | Guía de personalización del fabricante y manual interno de desarrollo SQL (31 reglas) |
| 7 | Ticket | Un ticket por ventana, con clave de Jira; lo crea el desarrollador |
| 8 | Lecturas | Consultas SQL de solo lectura a la base de desarrollo, por un MCP con usuario de lectura |
| 9 | Riesgos | Escribir en tablas nativas de Kondor; pisar la ventana de otro desarrollo con el mismo identificador; credenciales |
| 10 | Variabilidad | Variable: campos, posiciones, eventos, procedimientos. Ambiente: formato de exportación, prefijos. Fijo: orden de las ocho secciones. Fijo desconocido: varias claves sin significado documentado |
| 11 | Roles | Consultor aplica y aprueba; Claude diseña, genera y revisa con agentes separados; Cowork revisa los reportes |
| 12 | Piloto | Una ventana mínima sobre dos tipos de operación, con un campo de cada tipo, una coherencia de prueba y registros de cada evento en una tabla de log |

Lo que confirmó el ticket piloto que ningún análisis previo había visto:

1. Una clave numérica "desconocida" era una referencia a otra sección: copiada fuera de contexto, la ventana dejaba de abrir.
2. Una bandera significaba lo contrario de lo inferido del corpus.
3. Una regla sacada de una sola captura era falsa en el 90 % del corpus.
4. El editor que aplicaba el script alteraba el texto; hubo que neutralizarlo dentro del propio script.
5. Un agente con más herramientas de las necesarias las usó fuera de su tarea.
6. Un agente marcó como cumplido un control que exigía una revisión independiente.
