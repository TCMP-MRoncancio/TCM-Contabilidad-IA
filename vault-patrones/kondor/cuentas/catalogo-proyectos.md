# Catálogo de Proyectos (ChartOfAccount_Id)

`ChartOfAccount_Id` identifica **el proyecto/entidad** al que pertenece la cuenta — no es un valor fijo del estándar, varía según para quién se está creando la cuenta (ej. Scotia, Alpha, RD_UNICA...).

Claude **siempre debe preguntar** a qué proyecto pertenece la cuenta — nunca asumir un default. Si el usuario da un código que no está en esta lista, Claude debe detenerse y preguntar si es un proyecto nuevo (y en ese caso, indicarle que debe agregarse aquí vía Pull Request antes de generar la cuenta) o si fue un error de escritura.

## Proyectos confirmados

| Código (`ChartOfAccount_Id`) | Nombre / Entidad | Notas |
|---|---|---|
| `RD_UNICA` | [CONFIRMAR nombre de entidad] | Único proyecto visto hasta ahora en los datos de ejemplo del Excel original |
| [AGREGAR] | Scotia | Mencionado como proyecto existente — pendiente de confirmar el código exacto que usa en Kondor |
| [AGREGAR] | Alpha | Mencionado como proyecto existente — pendiente de confirmar el código exacto que usa en Kondor |

## Cómo agregar un proyecto nuevo

1. Confirmar el código exacto (`ChartOfAccount_Id`) tal como está parametrizado en Kondor para ese proyecto — no inventarlo ni derivarlo del nombre comercial.
2. Agregar la fila a la tabla de arriba vía Pull Request, revisado por el equipo encargado (ver `CODEOWNERS`).
3. Agregar el mismo código a `schemas/catalogo_proyectos.json`, en el mismo Pull Request — es la copia que lee `scripts/generar_cuenta_xml.py` para validar.

Mantener ambos archivos sincronizados: esta tabla es para que las personas lean el catálogo, `catalogo_proyectos.json` es para que el script lo valide automáticamente.
