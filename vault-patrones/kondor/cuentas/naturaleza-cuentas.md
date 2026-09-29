# Naturaleza de las Cuentas (Deudora / Acreedora)

> **Nota:** regla contable estándar incluida como punto de partida. El equipo financiero debe confirmar que aplica sin excepciones al estándar de la empresa.

La naturaleza de una cuenta determina si un movimiento la incrementa por el débito o por el crédito. Se asigna automáticamente según el tipo de cuenta — Claude no debe preguntarle esto al usuario, debe derivarlo de esta tabla.

| Tipo de cuenta | Naturaleza | Se incrementa con | Se disminuye con |
|---|---|---|---|
| Activo | Deudora | Débito | Crédito |
| Gasto | Deudora | Débito | Crédito |
| Pasivo | Acreedora | Crédito | Débito |
| Patrimonio | Acreedora | Crédito | Débito |
| Ingreso | Acreedora | Crédito | Débito |

## Regla de validación

Si el usuario indica explícitamente una naturaleza que contradice el tipo de cuenta (ej. pide una cuenta de "Pasivo" con naturaleza "Deudora"), Claude debe **detenerse y preguntar** en vez de generar la cuenta — probablemente hay un malentendido sobre el tipo de cuenta que realmente se necesita.

## Cuentas de naturaleza mixta o especial

> **[DEFINIR]** — si en el catálogo real existen cuentas de naturaleza contraria a su tipo (cuentas correctoras, de valuación, etc.), documentarlas aquí explícitamente con su regla particular. Mientras no se documenten, Claude debe asumir la tabla estándar de arriba.
