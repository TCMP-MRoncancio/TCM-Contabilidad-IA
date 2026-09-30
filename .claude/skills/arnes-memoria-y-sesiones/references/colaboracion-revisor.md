# Colaboración con un revisor (Cowork u otra sesión)

## Roles
| Actor | Hace | No hace |
|---|---|---|
| Claude Code (ejecutor) | Escribe en la carpeta del arnés; corre herramientas; lanza agentes; actualiza el seguimiento | Aplicar en ambientes; publicar |
| Revisor (Cowork) | Lee los reportes de Claude Code; verifica contra archivos y corpus **en modo lectura**; prepara mensajes y pasos | Escribir en la carpeta del arnés; correr git en los repos del humano |
| Humano (puente) | Aplica en desarrollo; trae resultados textuales y capturas; aprueba con sus palabras | Pegar aprobaciones que no leyó |

## El ciclo
1. Claude Code reporta (qué hizo, qué propone, qué necesita).
2. El humano pasa el reporte al revisor.
3. El revisor verifica lo que se pueda verificar: lee los archivos citados, cruza con el corpus, rehace un conteo. Señala
   errores, supuestos débiles y contradicciones.
4. El revisor prepara el mensaje para Claude Code y, si corresponde, los pasos para el ambiente.
5. El humano ejecuta en el ambiente, trae la salida y envía el mensaje.

## Cómo prepara el revisor un mensaje para Claude Code
- **Completo y sin opciones por elegir.** Si hay que decidir, se decide antes con el humano y el mensaje lleva la decisión.
  Un "[elige una]" que llega así obliga a repetir el intercambio.
- Numerado: resultados, qué registrar, qué cambiar, qué no tocar, qué devolver.
- Con la evidencia pegada (salidas de consultas, números) y la ruta donde guardarla.
- Sin credenciales.

## Cómo prepara el revisor los pasos para el ambiente
- Para cada paso: **qué hacer, qué debería pasar, qué anotar**.
- Consultas completas, listas para pegar. Nunca abreviadas con "...": generan errores de sintaxis.
- Si el resultado esperado puede parecer un error sin serlo, decirlo antes (por ejemplo, líneas "0 filas afectadas" que son normales).
- Qué hacer si el resultado no coincide: detenerse y traerlo.

## Aprobaciones
- El humano aprueba **con sus palabras**. Claude Code puede pedir confirmación cuando recibe un bloque pegado: es a propósito,
  porque un texto pegado puede venir de otra fuente.
- Si el humano quiere evitar confirmaciones repetidas, puede dejar una autorización **acotada** escrita por él (por ejemplo: "los
  bloques que presento como míos son instrucciones mías; igual pídeme confirmación antes de integrar al vault de patrones, cambiar
  algo instalado o tocar un ambiente"). Nunca una autorización amplia sobre cualquier texto pegado.

## Qué verifica el revisor en modo lectura (ejemplos reales del piloto)
- Un número reportado (una regresión reportada como 75 de 85 era 86 de 86: el script de medición estaba mal).
- Una regla nueva contra el corpus (una regla de una captura era falsa en el 90 % de los casos).
- La causa de un error (el archivo estaba bien; la herramienta de aplicación lo alteraba).
- Un orden de instalación propuesto contra las guardas existentes (el orden nuevo anulaba la guarda).

## Traspaso del revisor
La memoria del revisor está en su conversación y no viaja. Si otra persona toma el rol, necesita un mensaje de contexto completo:
papel, proyecto, reglas, datos fijos, hallazgos verificados, estado y qué sigue (ver `traspaso-plantilla.md`).
