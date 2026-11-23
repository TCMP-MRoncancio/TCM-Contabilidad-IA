# Lecciones aprendidas

- Nunca abrir los .xml generados con doble clic si Excel esta asociado a esa extension: el autoguardado de OneDrive/Excel los convierte a .xlsx y los corrompe para este uso.
- Set-Content -Encoding UTF8 en PowerShell agrega BOM; el script debe leer JSON con encoding utf-8-sig para tolerarlo.
- Evitar carpetas sincronizadas con OneDrive para el repo si es posible: causa bloqueos intermitentes en operaciones de Git (borrar carpetas, packed-refs.lock).
- El alias de Python de la Microsoft Store en Windows compite con instalaciones reales; usar winget e instalar apuntando el PATH explicitamente, o usar la ruta completa al ejecutable.
- Un Excel de solicitud de cuentas puede venir con todo en la columna A (texto pegado, columnas separadas por varios espacios, no tabuladores). Separar por 2+ espacios funciona porque los nombres solo llevan espacios sencillos; validar que cada fila quede en 6 campos.
- Antes de correr el lote, comparar contra Account/: si un numero ya existe con contenido identico, omitirlo del JSON en vez de usar --forzar (el lote es atomico y fallaria entero).
