# TCM Contabilidad IA

Las instrucciones del proyecto estan en AGENTS.md (se importa abajo).

@AGENTS.md

## Como ejecutar Python en este equipo

El comando `python` no siempre esta en el PATH en Windows (puede chocar
con el alias de la Microsoft Store). Si `python --version` no funciona:

1. Prueba `py --version` (el lanzador alternativo de Windows).
2. Si tampoco funciona:
   - Desactiva el alias de la Microsoft Store: Configuracion > Aplicaciones >
     Configuracion avanzada de aplicaciones > Alias de ejecucion de aplicaciones,
     y apaga `python.exe` y `python3.exe`.
   - Si Python no esta instalado: `winget install Python.Python.3.12`, cierra y
     abre la terminal, y confirma con `python --version`.
   - Si sigue sin aparecer, agrega al PATH de usuario la carpeta de instalacion
     (y su subcarpeta `Scripts`) que muestra `py -0p`.
   - Luego instala dependencias: `python -m pip install -r requirements.txt`.
   Ver tambien memoria/lecciones.md (alias de la Microsoft Store, BOM en JSON).
3. Como ultimo recurso, usa la ruta completa al ejecutable de Python de
   tu propia maquina (no la copies de otra persona - cada equipo tiene
   la suya).