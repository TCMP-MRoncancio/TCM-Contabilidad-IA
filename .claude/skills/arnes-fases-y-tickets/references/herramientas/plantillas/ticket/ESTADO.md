---
ticket: {{TICKET}}
jira: {{JIRA}}
cliente: {{CLIENTE}}
titulo: {{TITULO}}
arquetipo: por definir
fase: 0-alta
control_pendiente: ambiente confirmado e identificador sin colision
dir_diseno: {{DIR_DISENO}}
actualizado: {{FECHA}}
---
# {{TICKET}} · {{TITULO}}

## Próximo paso
- Confirmar el ambiente (versión y formato del sistema destino) y que el identificador del objeto no existe.

## En curso
- (nada)

## Bloqueos
- (ninguno)

## Preguntas abiertas
- Ver `preguntas.md`.

## Hecho
- {{FECHA}} · alta del ticket.

## Controles por fase
- [ ] **0 Alta**: versión y formato del ambiente confirmados; identificador sin colisión (consulta de solo lectura).
- [ ] **1 Requerimiento**: necesidad entendida, arquetipo propuesto, sin preguntas críticas abiertas.
- [ ] **2 Diseño**: ficha validada sin errores y documento de diseño aprobados explícitamente por el humano (fecha y quién).
- [ ] **3 Construcción**: entregable generado; validador, lint y revisión independiente sin errores, antes de aplicar.
- [ ] **4 Aplicación e ida y vuelta**: aplicado en desarrollo por el humano; extracción de vuelta comparada sin diferencias no explicadas.
- [ ] **5 Pruebas**: casos de prueba ejecutados con evidencia y aprobados.
- [ ] **6 Entrega**: paquete de promoción completo.
- [ ] **7 Cierre**: bitácora final, conocimiento verificado y candidatos registrados.
