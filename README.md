# Demo: Modelado Dimensional + Dashboard de Gestión

**Caso completo de ingeniería y análisis de datos** para una distribuidora mayorista ficticia ("Distribuidora del Centro S.A."), desde la generación del dato crudo hasta el tablero de gestión — con el modelado dimensional como pieza central.

`Python` · `Power BI` · `DAX` · `Modelado dimensional (esquema estrella)`

> 🧪 **Todos los datos son sintéticos**, generados por código. No corresponden a ninguna empresa real.

---

## Qué demuestra este proyecto

La tesis de [Vektia](https://vektia.com.ar): **un análisis solo es tan bueno como la estructura de datos que lo sostiene.** Este repo recorre las cuatro capas:

1. **Datos de origen** — 5 entidades relacionales con integridad referencial validada (`data/`)
2. **Generación reproducible** — script Python que produce el dataset con realismo de negocio (`scripts/`)
3. **Modelado dimensional** — esquema estrella + capa de medidas DAX documentada (`powerbi/`)
4. **Análisis** — dashboard de gestión de 3 páginas (`img/`)

## El dataset

| Archivo | Contenido |
|---|---|
| `data/clientes.csv` | 80 clientes con segmento, localidad, vendedor y condición de pago |
| `data/productos.csv` | 47 artículos en 5 categorías, con costo y precio |
| `data/vendedores.csv` | 5 vendedores con zona |
| `data/ventas.csv` | ~40.000 líneas de factura (24 meses: jul-2024 a jun-2026) |
| `data/cobranzas.csv` | ~7.700 recibos, con demoras según perfil de pago del cliente |

**Realismo incorporado por diseño:** estacionalidad (pico +35% en diciembre, valle en enero-febrero), tendencia de crecimiento, ajuste inflacionario de precios (~2% mensual), perfiles de morosidad (55% puntuales / 30% demora leve / 15% morosos), pagos parciales, y ~10% de la facturación pendiente de cobro a la fecha de corte — para que el análisis de cuentas por cobrar tenga sustancia.

Regenerar el dataset:

```bash
python scripts/generar_demo.py
```

(Determinístico: semilla fija, mismo resultado en cada corrida.)

## El modelo

Esquema estrella con dimensión de calendario, tabla de hechos de ventas a grano de línea de factura, y tabla auxiliar de facturas para el análisis de cobranzas:

```
Vendedores 1─* Clientes 1─* Ventas *─1 Productos
                   │            │
                   └─* Cobranzas│
                        │       │
              Calendario 1──────┴─ (fechas de venta y de cobro)
```

La capa de medidas completa está en [`powerbi/medidas_DAX.txt`](powerbi/medidas_DAX.txt), documentada y organizada en 5 bloques:

1. **Ventas y rentabilidad** — ventas, costo, margen, ticket promedio
2. **Comparativas temporales** — YoY, MoM, acumulados YTD
3. **Cuentas por cobrar** — saldos con **fecha de corte dinámica** (patrón `REMOVEFILTERS` + `MAX(Calendario[Date])`: el saldo se recalcula a cualquier fecha seleccionada)
4. **Aging de deuda** — antigüedad de saldos en tramos 0-30 / 31-60 / 61-90 / +90 días
5. **Indicadores de cobranza** — % cobrado, DSO (días promedio de cobro)

## El dashboard

*(Capturas en `img/` — 3 páginas: Visión General · Ventas y Rentabilidad · Cuentas por Cobrar)*

La página de **Cuentas por Cobrar** es la demostración central: saldos por cliente con aging, calculados a fecha de corte seleccionable — el tipo de análisis que solo funciona cuando el modelado de fondo es correcto.

## Estructura del repo

```
├── data/         # Dataset sintético (5 CSV, delimitador ;, decimal coma)
├── scripts/      # Generador reproducible del dataset
├── powerbi/      # Medidas DAX documentadas + guía de armado
└── img/          # Capturas del dashboard
```

---

**[Vektia](https://vektia.com.ar)** — Ingeniería y Análisis de Datos · Córdoba, Argentina
*La arquitectura de datos es la base. El análisis certero es la consecuencia.*
