# -*- coding: utf-8 -*-
"""
Generador de dataset sintético para el dashboard demo de Vektia.
Empresa ficticia: "Distribuidora del Centro S.A." — distribuidora mayorista
de consumo masivo del interior de Córdoba.
Período: julio 2024 a junio 2026 (24 meses).
Salidas: clientes.csv, productos.csv, vendedores.csv, ventas.csv, cobranzas.csv
"""
import csv
import random
from datetime import date, timedelta

random.seed(42)

OUT = "/home/claude/vektia_demo/"
import os
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------
# 1. VENDEDORES
# ------------------------------------------------------------------
vendedores = [
    (1, "Marcos Ferreyra", "Zona Este"),
    (2, "Lucía Benítez",   "Zona Norte"),
    (3, "Diego Sosa",      "Zona Sur"),
    (4, "Carla Moyano",    "Zona Oeste"),
    (5, "Javier Ríos",     "Grandes Cuentas"),
]

with open(OUT + "vendedores.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["VendedorID", "Vendedor", "Zona"])
    w.writerows(vendedores)

# ------------------------------------------------------------------
# 2. CLIENTES
# ------------------------------------------------------------------
localidades = [
    ("Villa María", "Córdoba"), ("Bell Ville", "Córdoba"), ("Marcos Juárez", "Córdoba"),
    ("San Francisco", "Córdoba"), ("Río Cuarto", "Córdoba"), ("Córdoba Capital", "Córdoba"),
    ("Villa Nueva", "Córdoba"), ("Las Varillas", "Córdoba"), ("Leones", "Córdoba"),
    ("Corral de Bustos", "Córdoba"), ("Arroyito", "Córdoba"), ("Oncativo", "Córdoba"),
    ("Rafaela", "Santa Fe"), ("Venado Tuerto", "Santa Fe"), ("Casilda", "Santa Fe"),
]
segmentos = [
    ("Almacén", 0.38), ("Autoservicio", 0.25), ("Kiosco", 0.15),
    ("Supermercado", 0.12), ("Mayorista", 0.10),
]
nombres_fantasia = [
    "El Progreso", "La Esquina", "Don Pedro", "San Cayetano", "La Familia", "El Trébol",
    "Los Hermanos", "La Central", "Del Pueblo", "Santa Rita", "El Amanecer", "La Estrella",
    "Mi Barrio", "El Cruce", "La Nueva", "Los Amigos", "San Martín", "El Fortín",
    "La Victoria", "Del Parque", "El Sol", "La Perla", "Don Julio", "La Colonia",
    "El Águila", "Los Alamos", "La Terminal", "El Recreo", "Santa Ana", "La Plaza",
]
tipos = ["Almacén", "Despensa", "Autoservicio", "Kiosco", "Súper", "Distribuidora", "Maxikiosco"]
cond_pago = [("Contado", 0.20), ("Cta Cte 15 días", 0.25), ("Cta Cte 30 días", 0.40), ("Cta Cte 60 días", 0.15)]

def eleccion_ponderada(items):
    r = random.random()
    acc = 0
    for val, p in items:
        acc += p
        if r <= acc:
            return val
    return items[-1][0]

clientes = []
for i in range(1, 81):
    seg = eleccion_ponderada(segmentos)
    loc, prov = random.choice(localidades)
    nombre = f"{random.choice(tipos)} {random.choice(nombres_fantasia)}"
    vend = random.choice(vendedores)[0] if seg != "Mayorista" else 5
    cp = "Cta Cte 30 días" if seg in ("Supermercado", "Mayorista") else eleccion_ponderada(cond_pago)
    alta = date(2018, 1, 1) + timedelta(days=random.randint(0, 2700))
    # perfil de pago: 0=puntual, 1=demora leve, 2=moroso
    perfil = random.choices([0, 1, 2], weights=[55, 30, 15])[0]
    clientes.append([i, nombre, seg, loc, prov, vend, cp, alta.isoformat(), perfil])

with open(OUT + "clientes.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["ClienteID", "Cliente", "Segmento", "Localidad", "Provincia",
                "VendedorID", "CondicionPago", "FechaAlta", "_PerfilPago"])
    w.writerows(clientes)

# ------------------------------------------------------------------
# 3. PRODUCTOS
# ------------------------------------------------------------------
catalogo = {
    "Bebidas": [
        ("Gaseosa Cola 2.25L", 1450), ("Gaseosa Lima 2.25L", 1380), ("Agua Mineral 2L", 780),
        ("Agua Saborizada 1.5L", 950), ("Jugo en Polvo x20", 2100), ("Cerveza Rubia 1L Ret", 1850),
        ("Vino Tinto Tetra 1L", 1600), ("Energizante 500ml", 1750), ("Soda Sifón 1.5L", 690),
        ("Jugo Exprimido 1L", 1980),
    ],
    "Almacén": [
        ("Aceite Girasol 1.5L", 2900), ("Arroz Largo Fino 1kg", 1350), ("Fideos Guiseros 500g", 890),
        ("Harina 000 1kg", 750), ("Azúcar 1kg", 1100), ("Yerba Mate 1kg", 4200),
        ("Café Torrado 500g", 5600), ("Puré de Tomate 520g", 720), ("Atún al Natural 170g", 2350),
        ("Galletitas Surtidas 400g", 1650), ("Mermelada Durazno 454g", 1480), ("Sal Fina 500g", 520),
    ],
    "Limpieza": [
        ("Detergente 750ml", 1250), ("Lavandina 1L", 680), ("Jabón en Polvo 800g", 2450),
        ("Suavizante 900ml", 1580), ("Limpiador Piso 900ml", 1150), ("Esponja Multiuso x3", 890),
        ("Papel Higiénico x4", 2100), ("Rollo Cocina x2", 1350), ("Desodorante Ambiente 360ml", 1690),
    ],
    "Perfumería": [
        ("Shampoo Familiar 930ml", 2950), ("Jabón Tocador x3", 1450), ("Pasta Dental 90g", 1380),
        ("Desodorante Aerosol 150ml", 2250), ("Máquina Afeitar x2", 1150), ("Toallas Femeninas x8", 1580),
        ("Pañales M x30", 6900), ("Alcohol en Gel 250ml", 980),
    ],
    "Golosinas": [
        ("Alfajor Triple x6", 2700), ("Chocolate Tableta 100g", 1850), ("Caramelos Surtidos 500g", 1950),
        ("Chicles Menta x20", 1450), ("Turrón x10", 1250), ("Papas Fritas 200g", 1980),
        ("Maní Salado 400g", 1550), ("Galletita Rellena x3", 1350),
    ],
}

productos = []
pid = 100
for cat, items in catalogo.items():
    for desc, precio_base in items:
        pid += 1
        margen = random.uniform(0.22, 0.38)          # margen bruto objetivo
        costo = round(precio_base * (1 - margen), 2)
        rotacion = random.uniform(0.5, 2.0)           # popularidad relativa
        productos.append([pid, desc, cat, costo, precio_base, rotacion])

with open(OUT + "productos.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["ProductoID", "Producto", "Categoria", "CostoBase", "PrecioBase", "_Rotacion"])
    for p in productos:
        w.writerow(p[:3] + [str(p[3]).replace(".", ","), str(p[4]).replace(".", ","), str(round(p[5], 3)).replace(".", ",")])

# ------------------------------------------------------------------
# 4. VENTAS (jul-2024 a jun-2026)
# ------------------------------------------------------------------
# Estacionalidad mensual (dic pico, ene-feb valle) + tendencia de crecimiento
# + ajuste de precios mensual (~2.2% prom, estilo inflación moderada)
estacionalidad = {1: 0.82, 2: 0.85, 3: 0.98, 4: 1.00, 5: 1.02, 6: 0.97,
                  7: 1.00, 8: 1.01, 9: 1.03, 10: 1.06, 11: 1.10, 12: 1.35}

inicio = date(2024, 7, 1)
fin = date(2026, 6, 30)

# índice de precios acumulado por mes
indice = {}
acum = 1.0
d = inicio
while d <= fin:
    key = (d.year, d.month)
    if key not in indice:
        indice[key] = acum
        acum *= 1 + random.uniform(0.015, 0.030)
    d += timedelta(days=32)
    d = d.replace(day=1)

# actividad relativa por cliente (tamaño)
peso_segmento = {"Kiosco": 0.5, "Almacén": 1.0, "Autoservicio": 1.8, "Supermercado": 3.5, "Mayorista": 5.0}

ventas = []
factura_num = 20000
facturas_totales = {}   # factura -> (fecha, cliente, total)

d = inicio
while d <= fin:
    if d.weekday() < 6:  # lunes a sábado
        mes_factor = estacionalidad[d.month]
        # tendencia: crecimiento real leve a lo largo de 24 meses
        meses_transc = (d.year - 2024) * 12 + d.month - 7
        tendencia = 1 + 0.012 * meses_transc
        n_facturas = max(3, int(random.gauss(11 * mes_factor * tendencia, 2.5)))
        for _ in range(n_facturas):
            cli = random.choice(clientes)
            peso = peso_segmento[cli[2]]
            factura_num += 1
            n_lineas = max(1, int(random.gauss(4 + peso, 2)))
            total_fac = 0.0
            for _ in range(n_lineas):
                prod = random.choices(productos, weights=[p[5] for p in productos])[0]
                idx = indice[(d.year, d.month)]
                precio = round(prod[4] * idx * random.uniform(0.97, 1.03), 2)
                costo = round(prod[3] * idx * random.uniform(0.98, 1.02), 2)
                cant = max(1, int(random.gauss(6 * peso, 3)))
                ventas.append([factura_num, d.isoformat(), cli[0], prod[0], cant,
                               precio, costo])
                total_fac += cant * precio
            facturas_totales[factura_num] = (d, cli, round(total_fac, 2))
    d += timedelta(days=1)

with open(OUT + "ventas.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["FacturaID", "Fecha", "ClienteID", "ProductoID", "Cantidad",
                "PrecioUnitario", "CostoUnitario"])
    for v in ventas:
        w.writerow(v[:5] + [str(v[5]).replace(".", ","), str(v[6]).replace(".", ",")])

# ------------------------------------------------------------------
# 5. COBRANZAS
# ------------------------------------------------------------------
# Según condición de pago y perfil del cliente, se genera el pago
# (a veces parcial, a veces aún impago si es reciente o moroso).
plazos = {"Contado": 0, "Cta Cte 15 días": 15, "Cta Cte 30 días": 30, "Cta Cte 60 días": 60}
hoy = date(2026, 6, 30)

cobranzas = []
recibo = 50000
for fac, (fecha, cli, total) in facturas_totales.items():
    plazo = plazos[cli[6]]
    perfil = cli[8]
    if perfil == 0:
        demora = random.randint(-3, 5)
        prob_impago = 0.01
    elif perfil == 1:
        demora = random.randint(5, 25)
        prob_impago = 0.04
    else:
        demora = random.randint(20, 90)
        prob_impago = 0.18

    vence = fecha + timedelta(days=plazo)
    fecha_pago = vence + timedelta(days=demora)

    if fecha_pago > hoy or random.random() < prob_impago:
        continue  # factura impaga a la fecha de corte

    recibo += 1
    if random.random() < 0.12:  # pago parcial en dos veces
        parte = round(total * random.uniform(0.4, 0.7), 2)
        cobranzas.append([recibo, fecha_pago.isoformat(), cli[0], fac, parte])
        f2 = fecha_pago + timedelta(days=random.randint(7, 30))
        if f2 <= hoy:
            recibo += 1
            cobranzas.append([recibo, f2.isoformat(), cli[0], fac, round(total - parte, 2)])
    else:
        cobranzas.append([recibo, fecha_pago.isoformat(), cli[0], fac, total])

with open(OUT + "cobranzas.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["ReciboID", "FechaPago", "ClienteID", "FacturaID", "Importe"])
    for c in cobranzas:
        w.writerow(c[:4] + [str(c[4]).replace(".", ",")])

# ------------------------------------------------------------------
# Resumen
# ------------------------------------------------------------------
tot_ventas = sum(v[4] * v[5] for v in ventas)
tot_cobrado = sum(c[4] for c in cobranzas)
print(f"Facturas:  {len(facturas_totales):,}")
print(f"Líneas:    {len(ventas):,}")
print(f"Cobranzas: {len(cobranzas):,}")
print(f"Facturado: $ {tot_ventas:,.0f}")
print(f"Cobrado:   $ {tot_cobrado:,.0f}")
print(f"Saldo:     $ {tot_ventas - tot_cobrado:,.0f}  ({(tot_ventas-tot_cobrado)/tot_ventas*100:.1f}% de la facturación)")
