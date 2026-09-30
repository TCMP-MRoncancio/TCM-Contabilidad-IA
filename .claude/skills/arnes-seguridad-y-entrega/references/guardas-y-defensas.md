# Guardas y defensas, con ejemplos

Los ejemplos son ilustraciones por tecnología. Adaptar al sistema destino y **probarlos en desarrollo** antes de adoptarlos.

## Guarda de idempotencia

### SQL Server (T-SQL), script con varios lotes separados por `go`
```sql
IF EXISTS (SELECT 1 FROM <base>..<tabla_de_objetos> WITH (NOLOCK) WHERE <columna_nombre> = '<IDENTIFICADOR>')
BEGIN
    RAISERROR('El objeto <IDENTIFICADOR> ya existe. Instalación detenida: elegir otro identificador o usar modo existente.', 16, 1)
    SET NOEXEC ON
END
go

-- … resto de la instalación …

SET NOEXEC OFF
go
```
- `RAISERROR` solo no alcanza en un script con varios lotes: los lotes siguientes se ejecutarían igual. `SET NOEXEC ON` hace que
  el resto se compile sin ejecutarse, y `SET NOEXEC OFF` al final restituye la sesión.
- **Resultado esperado de la prueba** (segunda aplicación): el mensaje del `RAISERROR` y líneas "(0 filas afectadas)", que son normales
  bajo `NOEXEC` porque las sentencias se compilan sin ejecutarse. Lo que **no** debe aparecer: "(1 fila afectada)".
- Verificar con una consulta de solo lectura que el objeto sigue igual (misma fecha de modificación, mismo contenido).

### Archivos de configuración o despliegue por script (bash, PowerShell)
```bash
if [ -e "<ruta del objeto en destino>" ]; then
  echo "El objeto ya existe. Instalación detenida." >&2
  exit 1
fi
```

### API o sistema con endpoint de consulta
Consultar primero si el objeto existe; si existe, detener antes de cualquier creación. Registrar la consulta y su respuesta.

## Defensa contra la herramienta de aplicación

### Caso real del piloto: finales de línea dentro de un literal
El entregable insertaba un texto de varias líneas (`Clave:Valor` por línea) dentro de un literal SQL. El editor que ejecutaba el
script convertía los saltos de línea a CRLF **al ejecutar**, aunque el archivo tuviera LF, y el carácter CR quedaba guardado al final
de cada línea del texto. La interfaz del sistema mostraba un carácter extraño en algunos valores; peor, cualquier comparación contra
esos valores habría fallado.

Defensa dentro del propio script:
```sql
INSERT <tabla> VALUES ( …, REPLACE('<texto de varias líneas>', CHAR(13), ''), … )
```
- Un literal de más de 8000 bytes se trata como `varchar(max)` y `REPLACE` no lo trunca (verificado con un texto de 25.888 caracteres).
- Verificación midiendo lo guardado: `DATALENGTH` del texto guardado igual al largo sin CR; conteo de `CHAR(13)` igual a cero.
- Defensas adicionales (no suficientes solas): archivo con LF, `.gitattributes` con `eol=lf`, regla del validador que marca un literal
  con CR que no esté envuelto.

### Principio general
1. Identificar qué altera la herramienta de aplicación (finales de línea, codificación, espacios finales, orden, comillas).
2. Neutralizarlo **en el contenido que se aplica**, no en el archivo.
3. Medirlo en lo que quedó guardado, en bytes, no a ojo.
4. Documentar la alteración en `promocion.md` ("Notas de la herramienta de aplicación").

## Corrección de desarrollo
- Mismo contenido que la salida, en modo `existente`, sin guarda.
- Primera línea: `-- CORRECCION DE OBJETO INSTALADO EN DESARROLLO. NO PROMOVER A QA NI PRODUCCION.` (o el comentario equivalente).
- Nombre: `entrega/<objeto>-CORRECCION-DEV.<ext>`.
- Antes de aplicarla: confirmar que nadie cambió el objeto instalado desde la interfaz (comparar fecha de modificación y largo con
  lo aplicado); si cambió, extraerlo primero y llevar el cambio a la ficha.
