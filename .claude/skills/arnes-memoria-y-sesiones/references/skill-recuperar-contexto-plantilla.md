---
name: recuperar-contexto
description: "Recuperar contexto perdido. Usar con /recuperar-contexto o cuando no se sepa como seguir, que paso con alguna cuestion, por que se decidio algo, cuando una sesion se corto o cuando la sesion parezca desactualizada respecto de los archivos."
---

# /recuperar-contexto

Buscar de lo más resumido a lo más crudo y parar cuando la pregunta quede respondida **con fuente**.

## Orden de búsqueda (ticket activo; si no hay, preguntar cuál o empezar por `memoria/`)
| # | Dónde | Qué da |
|---|---|---|
| 1 | `ESTADO.md` del ticket | Fase, control pendiente, próximo paso, bloqueos |
| 2 | `bitacora.md` | Qué se hizo en cada sesión y qué quedó pendiente |
| 3 | `decisiones.md`, `preguntas.md`, `incidencias.md` | Por qué se decidió algo, qué se preguntó, qué pasó con un problema |
| 4 | `evidencias/` | Extracciones de vuelta, capturas, resultados de consultas, informes de revisión |
| 5 | `sesiones/INDICE.md` y `sesiones/*.md` | Conversaciones resumidas por los hooks (buscar con Grep por palabra clave) |
| 6 | `sesiones/raw/*.jsonl.gz` | Conversación completa, comprimida (comando abajo) |
| 7 | `claude --resume` | Retomar una conversación de Claude Code |
| 8 | `memoria/` | Decisiones y lecciones del arnés, sesiones sin ticket |
| 9 | `git log` de los repos de los vaults (lo corre el humano y pega el resultado: los agentes no corren git) | Cuándo cambió un archivo y con qué mensaje |

Buscar en una conversación comprimida (paso 6):
```
python -c "import gzip,sys; [print(l.rstrip()) for l in gzip.open(sys.argv[1],'rt',encoding='utf-8') if sys.argv[2].lower() in l.lower()]" <archivo.jsonl.gz> <palabra>
```

## Si la sesión se cortó
1. Leer el extracto de la última sesión (`sesiones/`) y su lista de archivos modificados.
2. Revisar si alguno de esos archivos quedó a medias (comparar con lo que dice la bitácora).
3. Registrar el corte en la bitácora y seguir desde "Próximo paso".

## Respuesta
Lo encontrado, con la ruta del archivo y la fecha. Si no se encontró, decirlo y preguntar al humano; no reconstruir de memoria.
