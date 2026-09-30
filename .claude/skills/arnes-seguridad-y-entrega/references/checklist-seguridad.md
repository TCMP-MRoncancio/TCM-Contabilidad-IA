# Checklist de seguridad del arnés

Marcar cada punto con: **cumple** (con evidencia), **no aplica** (con motivo) o **riesgo aceptado** (con decisión Dxx).

## Ambiente
- [ ] Ningún agente tiene forma de escribir en un ambiente: no hay cliente de consola ni cliente HTTP de escritura permitido (`deny`) ni conexión con permisos de escritura.
- [ ] La conexión de lectura usa un usuario o token **solo de lectura** creado para eso, no el de la aplicación.
- [ ] AGENTS.md dice que el humano aplica y que las lecturas van solo por la conexión de solo lectura.
- [ ] Hay una regla dura sobre los objetos nativos del sistema que no se tocan, y el revisor la verifica.
- [ ] Las consultas que se dan al humano son de solo lectura y completas.

## Credenciales y datos
- [ ] Ninguna credencial en archivos del arnés ni de los vaults (buscar: `password`, `pwd`, `secret`, `token`, cadenas de conexión).
- [ ] Las contraseñas van en variables de entorno; su **nombre** puede estar documentado, su valor no.
- [ ] Se advierte que los hooks copian las conversaciones al vault: nunca pegar credenciales en el chat.
- [ ] Las copias crudas de conversaciones están ignoradas: `memoria/sesiones/raw/` en el arnés y `tickets/*/sesiones/raw/` en cada vault.
- [ ] Decisión registrada sobre `contexto/`: se versiona en el repo del arnés o no (material de clientes o de terceros).
- [ ] El repo del arnés es privado si contiene cualquier material interno.

## Repos y publicación
- [ ] `git push`, `git clone` y la creación de repos están en `deny`.
- [ ] Los vaults son repos propios y el `.gitignore` del arnés los excluye.
- [ ] Los agentes no corren git en los repos del humano (ni siquiera comandos de lectura, que pueden dejar archivos de bloqueo).

## El arnés sobre sí mismo
- [ ] `.claude/`, `herramientas/` y `vault-patrones/` en `ask`.
- [ ] Cada agente con herramientas mínimas; el revisor sin Write ni Edit; el diseñador sin Bash.
- [ ] Ninguna definición de agente le permite editar el seguimiento del ticket.
- [ ] Los cambios al arnés se registran en `memoria/decisiones.md`.

## Entrega
- [ ] El entregable en modo `nuevo` lleva guarda al principio y la guarda se probó.
- [ ] Las correcciones de desarrollo se generan aparte, rotuladas "NO PROMOVER".
- [ ] Se promueve la salida generada, no extracciones de desarrollo.
- [ ] Si se modifica algo existente, hay reverso escrito y probado.
- [ ] Las defensas contra la herramienta de aplicación están dentro del entregable y se verificaron midiendo lo guardado.

## Organización
- [ ] Las restricciones de la organización (modelos deshabilitados, conectores prohibidos) están escritas en AGENTS.md.
