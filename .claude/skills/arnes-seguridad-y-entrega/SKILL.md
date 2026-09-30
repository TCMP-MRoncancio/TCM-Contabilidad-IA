---
name: arnes-seguridad-y-entrega
description: "Paso 8 de construir un arnes: checklist de seguridad (permisos, credenciales, conexiones de solo lectura, git, datos sensibles) y diseno de la entrega (paquete de promocion, guardas de idempotencia, correcciones de desarrollo aparte, defensas contra herramientas que alteran el entregable, retiro). Usar al cerrar la construccion de un arnes, al auditar su seguridad, al definir como se promueve un entregable o al corregir algo ya instalado en desarrollo. No usar para aplicar nada en un ambiente: eso lo hace el humano."
---

# Seguridad y entrega (paso 8)

**Objetivo:** que el arnés no pueda dañar un ambiente ni filtrar datos por error, y que lo que se promueve sea exactamente lo
que se generó y revisó.
**Entrada:** el arnés de los pasos 2 a 7.
**Salida:** checklist de seguridad sin puntos abiertos (`references/checklist-seguridad.md`); plantilla de promoción en el generador
(`references/promocion-plantilla.md`); guardas y defensas del entregable (`references/guardas-y-defensas.md`).

## Parte A · Seguridad

### Principio
**Lo que se puede bloquear se bloquea; lo que no, se escribe como regla y se revisa.** Una regla escrita se puede saltar sin
querer (en el piloto, dos veces); un permiso denegado no.

### Capas de protección
| Capa | Protege de | Cómo |
|---|---|---|
| Permisos `deny` | Escritura en el ambiente, en `contexto/`, publicación remota | `.claude/settings.json` |
| Permisos `ask` | Que el arnés se modifique a sí mismo | `.claude/settings.json` sobre `.claude/`, `herramientas/`, `vault-patrones/` |
| Herramientas de cada agente | Que un agente haga lo que no le toca | Frontmatter `tools:` mínimo |
| Conexión de solo lectura | Escrituras accidentales al consultar | Un MCP o usuario con permisos solo de lectura; nunca el usuario de la aplicación |
| Credenciales fuera de archivos | Filtraciones por git o por conversaciones copiadas | Variables de entorno; los hooks copian conversaciones al vault, así que una clave pegada en el chat termina en un archivo |
| Repos separados y `.gitignore` | Que datos de un cliente lleguen a otro repo | Vaults propios; `contexto/` excluido si es confidencial |
| El humano aplica | Que un error llegue al ambiente sin un par de ojos | Regla dura y ausencia de clientes que escriban |
| El humano publica | Que algo salga del equipo sin revisión | `deny` sobre `git push`, `git clone`, creación de repos |

### Pasos
1. Recorrer `references/checklist-seguridad.md` punto por punto con el humano.
2. Cada punto abierto: se cierra, o se registra como riesgo aceptado en `memoria/decisiones.md` con motivo y quién.
3. Probar los `deny` en una sesión nueva (ver `arnes-estructura`, paso 6).

**Termina cuando:** el checklist no tiene puntos abiertos sin decisión.

## Parte B · Entrega

### Qué se promueve
**Lo generado y revisado** (`salida/` del ticket), nunca una extracción manual del ambiente de desarrollo. La extracción de desarrollo
arrastra cambios manuales no revisados y pierde las guardas y defensas del generador.

Si alguien cambió el objeto en la interfaz de desarrollo, ese cambio **vuelve a la ficha** (con `desde-extraccion`), se regenera la
salida, se revisa y recién entonces se promueve.

### Modos del entregable
| Modo | Cuándo | Guarda | Dónde queda | Se promueve |
|---|---|---|---|---|
| `nuevo` | El objeto no existe en el ambiente destino | Sí: falla si ya existe | `salida/` | Sí |
| `existente` | Se modifica algo instalado, de forma planificada | No | `salida/` | Sí, con reverso escrito y probado |
| Corrección de desarrollo | Corregir en desarrollo algo ya instalado durante las pruebas | No | `entrega/<objeto>-CORRECCION-DEV.<ext>`, con "NO PROMOVER" en la primera línea | **Nunca** |

La corrección de desarrollo se genera con una opción del generador (`--correccion-dev`) **sin cambiar el modo de la ficha**:
cambiar el modo para corregir y volver a cambiarlo después es la forma más fácil de promover por error la versión sin guarda.

### Guardas de idempotencia
El entregable en modo `nuevo` empieza con una guarda que **detiene la instalación si el objeto ya existe**, antes de crear o
modificar nada. Ejemplos por tecnología en `references/guardas-y-defensas.md`.

- Va **al principio** de la instalación: el orden de las piezas se decide para que la guarda frene antes que cualquier otra pieza.
  En el piloto, alguien propuso instalar primero las tablas y procedimientos (para evitar avisos del editor) y eso habría dejado la
  guarda sin efecto; se mantuvo el objeto con guarda primero.
- Si el formato del entregable **no admite** una guarda dentro (por ejemplo, un archivo de datos que se importa tal cual), la guarda
  pasa a ser el **primer paso obligatorio** de `promocion.md` (una consulta de solo lectura que el humano corre antes de aplicar, con
  el resultado que obliga a detenerse) y se registra como riesgo aceptado en `memoria/decisiones.md`.
- Se **prueba**: aplicar dos veces en desarrollo. La segunda vez debe detenerse sin modificar nada. El resultado esperado se escribe
  exacto en `promocion.md`, incluidas las líneas que parecen error y no lo son.

### Defensas contra la herramienta de aplicación
Si la herramienta que aplica el entregable puede alterarlo (finales de línea, codificación, espacios), la defensa va **dentro del
entregable**, no en el archivo ni en git. En el piloto, el editor convertía los saltos de línea al ejecutar aunque el archivo
estuviera correcto; la solución fue que el propio script eliminara el carácter sobrante al insertar. El archivo con el final de línea
correcto, el `.gitattributes` y una regla del validador quedan como defensas adicionales. Ver `references/guardas-y-defensas.md`.

Verificar la defensa **midiendo lo guardado** (longitudes en bytes, conteo del carácter), no solo mirando la interfaz.

### El paquete de promoción
Lo genera el generador en `entrega/promocion.md` (plantilla en `references/promocion-plantilla.md`). Contiene:
1. Qué archivos se aplican, en qué orden y en qué base o ambiente.
2. Dependencias entre piezas y con objetos del ambiente.
3. La prueba de la guarda, con su resultado esperado exacto y la consulta de verificación.
4. Verificaciones después de aplicar (consultas de solo lectura, qué deben devolver).
5. **Pasos fuera del script**: lo que el humano hace a mano en el sistema (reiniciar, recargar, habilitar).
6. Modo de tablas o datos y respaldo, si se modifican datos existentes.
7. Reverso (rollback) si se modifica algo existente, escrito y probado antes de aplicar (lección M06 del piloto).
8. Cómo retirar el objeto.
9. Lo que es solo de desarrollo y no se promueve.

### Retiro del ticket piloto
El ticket piloto de calibración se retira del ambiente al terminar, con el plan de retiro de la ficha del arnés. El retiro lo aplica
el humano; se registra en la bitácora con la verificación de que ya no existe.

## Control de salida
- [ ] Checklist de seguridad sin puntos abiertos sin decisión.
- [ ] `deny` probados.
- [ ] Generador con modos `nuevo`, `existente` y `--correccion-dev`.
- [ ] Guarda al principio de la instalación, probada dos veces en desarrollo.
- [ ] Defensas contra la herramienta de aplicación dentro del entregable, verificadas midiendo lo guardado.
- [ ] `promocion.md` generado con las nueve secciones.
- [ ] Regla escrita: se promueve `salida/`, no una extracción de desarrollo.

## Errores que ya cometimos (piloto de referencia)
- **Suponer que el archivo correcto basta.** El editor lo alteraba al ejecutar; recién una consulta de longitud lo mostró.
- **Proponer un orden que anulaba la guarda** (ver arriba).
- **Cambiar el modo de la ficha para corregir desarrollo** y tener que acordarse de volverlo: se reemplazó por una opción del generador.
- **Consultas abreviadas** en las instrucciones al humano ("GROUP BY ...") que dieron error de sintaxis: las consultas van completas.
- **Material confidencial a punto de versionarse** en un repo compartido: se decide antes del primer push (checklist).

## Después de este paso
El arnés está listo para el **ticket piloto de calibración** (`arnes-guia`, paso 9). Recorrerlo de punta a punta, registrar cada error
del arnés como incidencia y lección, corregir herramientas, agentes o skills con aprobación, y cerrarlo con `/cierre`.
