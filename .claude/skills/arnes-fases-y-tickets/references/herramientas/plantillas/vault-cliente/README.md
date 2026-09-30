# vault-cliente-{{CLIENTE}}

Memoria del cliente **{{CLIENTE}}**: su ambiente, lo que ya está construido para él y el seguimiento de cada ticket.
Es un repo propio (acceso restringido al equipo del cliente) que se clona **dentro** de la carpeta del arnés. El arnés lo ignora en su git.

## Estructura
| Ruta | Qué guarda |
|---|---|
| `cliente.md` | Ambientes, convenciones de nombres, restricciones y roles |
| `ambiente/` | Lo verificado del ambiente; cada dato con fuente y fecha |
| `inventario/` | Una nota por objeto instalado, obtenida del ambiente (nunca de `contexto/`) |
| `tablero.md` | Tickets y su fase |
| `tickets/<ticket>/` | Seguimiento, diseño, salida, entrega, evidencias y sesiones |

## Reglas
- Nunca anotar credenciales ni cadenas de conexión con clave.
- `tickets/*/sesiones/raw/` no se versiona.

## Inicializar como repo (lo hace el humano)
```
git init -b main
git add .
git commit -m "vault-cliente-{{CLIENTE}}: estructura inicial"
git remote add origin <url>
git push -u origin main
```
