# vault-patrones

Conocimiento reutilizable para construir <tipo de entregable> sobre <sistema destino>.
Es un repo propio que se clona **dentro** de la carpeta del arnés. El arnés lo ignora en su propio git.
Se puede abrir en Obsidian (frontmatter, enlaces).

## Qué hay
| Ruta | Qué guarda |
|---|---|
| `inventario-contexto.md` | Qué hay en `contexto/`: cantidades, origen, versión, confidencialidad |
| `<dominio>/modelo.md` | Qué es el objeto, qué partes tiene, dónde se guarda |
| `<dominio>/diccionario/` | Una nota por sección del formato, con la madurez de cada elemento |
| `<dominio>/fragmentos/` | Trozos reales por variante (generados; los aprobados desde tickets llevan otro nombre) |
| `<dominio>/cobertura.md` | Variantes, ocurrencias y fragmento (generado) |
| `<dominio>/arquetipos/` | Tipos de pedido, con sus preguntas |
| `<dominio>/anti-patrones.md` | Lo que no se copia del corpus, y por qué |
| `<dominio>/plantillas-curadas.md` | Ejemplos de referencia |
| `lecciones/` | Lecciones del dominio, con enlace al ticket de origen |
| `candidatos/` | Bandeja de entrada: propuestas nacidas en los tickets, pendientes de aprobación |

## Nivel de madurez
| Estado | Significa | Cómo se usa |
|---|---|---|
| `desconocido` | Existe, pero no sabemos qué hace | Se copia tal cual del fragmento; nunca se cambia |
| `hipotesis` | Idea con poca evidencia | Se pregunta o se verifica antes de depender de ella |
| `inferido` | Evidencia consistente en el corpus o la documentación | Se usa, avisando que no está confirmado |
| `verificado-captura` | Confirmado cruzando la interfaz con el archivo | Se usa |
| `verificado-ida-y-vuelta` | Aplicado y extraído de vuelta igual | Se usa |
| `extraido-de-ejemplo` | (fragmentos) Copia literal de un ejemplo real | Se usa como base |
| `obsoleto` | Contradicho por evidencia nueva | No se usa; queda como historia |

## Cómo crece
1. Un ticket descubre algo reutilizable (un elemento confirmado, un fragmento nuevo, una trampa).
2. Lo propone en `candidatos/` con su evidencia (plantilla en `candidatos/README.md`).
3. El humano aprueba; se integra en la nota que corresponde y sube su estado.
4. Si una ida y vuelta contradice algo, la nota pasa a `obsoleto` y se registra la lección.

Nadie escribe directo fuera de `candidatos/`: en el arnés, editar este vault pide aprobación.

## Lo generado automáticamente
<Comandos exactos que regeneran cobertura, fragmentos y catálogo desde `contexto/`.>

## Inicializar como repo (lo hace el humano)
```
git init -b main
git add .
git commit -m "vault-patrones: estructura inicial"
git remote add origin <url>
git push -u origin main
```
