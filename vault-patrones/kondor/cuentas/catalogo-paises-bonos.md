# Catálogo de Valores Permitidos

> **Nota:** tabla de ejemplo. El equipo financiero debe reemplazarla con los valores reales que maneja la empresa. Mientras un valor no esté en esta lista, Claude debe rechazarlo y preguntar, no aceptarlo "porque suena razonable".

## Países habilitados

| Código ISO | País | Moneda por defecto |
|---|---|---|
| CO | Colombia | COP |
| MX | México | MXN |
| US | Estados Unidos | USD |
| [AGREGAR] | | |

## Tipos de bono habilitados

| Código | Nombre | Notas |
|---|---|---|
| [DEFINIR] | [DEFINIR] | [DEFINIR] |

## Tipos de cuenta habilitados

| Código | Nombre |
|---|---|
| ACT | Activo |
| PAS | Pasivo |
| PAT | Patrimonio |
| ING | Ingreso |
| GAS | Gasto |

## Cómo actualizar este catálogo

Cualquier valor nuevo (un país, un tipo de bono) se agrega vía Pull Request a este archivo, revisado por el equipo encargado — nunca se le pide a Claude que "acepte" un valor nuevo sobre la marcha en una conversación.
