# Plantillas de traspaso

## 1. Pedido a Claude Code para el documento de traspaso

> Prepara un traspaso para <persona>, que retoma <ticket o arnés>. Crea `memoria/traspaso-AAAA-MM-DD.md` con:
> estado de fases; qué está verificado en el ambiente de desarrollo; qué falta (checklist y fases siguientes);
> decisiones vigentes y lecciones, en una línea cada una; reglas de seguridad de AGENTS.md; datos fijos del ambiente;
> pendientes que requieren aprobación humana. No ejecutes nada contra un ambiente.

## 2. Estructura del documento de traspaso

```
# Traspaso · <arnés o ticket> · AAAA-MM-DD

## Estado
| Ticket | Fase | Control pendiente | Próximo paso |

## Verificado en desarrollo
- <hallazgo> (evidencia: <archivo>)

## Pendiente
- <tarea> (dónde está el detalle)

## Decisiones vigentes
- Dxx · <una línea>

## Lecciones
- Mxx · <una línea>

## Reglas de seguridad
- <de AGENTS.md>

## Datos fijos del ambiente
- <identificadores, versiones, particularidades> (sin credenciales)

## Requiere aprobación humana
- <qué y por qué>

## Accesos que se entregan aparte (canal seguro)
- Conexión de solo lectura, usuario del ambiente, variable de entorno de la contraseña.
```

## 3. Primer mensaje de la persona nueva a Claude Code

> Soy <nombre>. Retomo <arnés o ticket>. Antes de hacer nada:
> 1. Lee AGENTS.md, `memoria/` (decisiones, lecciones, la sesión más reciente y el traspaso) y el ESTADO, la bitácora, las decisiones
>    y las incidencias del ticket.
> 2. Explícame en pocas líneas cómo está organizado el proyecto, en qué fase estamos, qué está verificado y qué falta.
> 3. Dime con tus palabras las reglas de seguridad: quién ejecuta, qué conexión se usa para leer, qué no se versiona, qué aprobaciones doy yo.
> 4. Dime qué necesitas de mí (accesos, variables de entorno, conexión de solo lectura) y qué no puedes verificar por tu cuenta.
> Reglas: no ejecutes nada contra un ambiente; si falta un dato, pregunta; pídeme confirmación antes de cambiar herramientas,
> integrar al vault de patrones o generar cambios sobre algo instalado; sesiones cortas con `/cierre`.

## 4. Si la persona saliente guardó preferencias en su perfil
Preguntarle a su Claude Code: "¿qué preferencias mías tienes guardadas y dónde?". Las que estén fuera de la carpeta no viajan;
la persona nueva define las suyas.
