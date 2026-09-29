# Lecciones aprendidas

- Nunca abrir los .xml generados con doble clic si Excel esta asociado a esa extension: el autoguardado de OneDrive/Excel los convierte a .xlsx y los corrompe para este uso.
- Set-Content -Encoding UTF8 en PowerShell agrega BOM; el script debe leer JSON con encoding utf-8-sig para tolerarlo.
- Evitar carpetas sincronizadas con OneDrive para el repo si es posible: causa bloqueos intermitentes en operaciones de Git (borrar carpetas, packed-refs.lock).
- El alias de Python de la Microsoft Store en Windows compite con instalaciones reales; usar winget e instalar apuntando el PATH explicitamente, o usar la ruta completa al ejecutable.
