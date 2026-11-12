"""Genera los datos sintéticos de NexaTech (nov-2025 a oct-2026)."""
import numpy as np, pandas as pd, math, datetime as dt
from pathlib import Path

rng = np.random.default_rng(2026)
OUT = Path(__file__).resolve().parent.parent / "Datos"

# ---------------- Productos ----------------
# (id, nombre, categoria, subcategoria, precio, stock_actual, lead_time_dias, origen)
P = [
 ("P01","Procesador AMD Ryzen 3 (3.ª gen.)","Componentes","Procesadores",410000,8,12,"Catálogo"),
 ("P02","Fuente de poder para PC","Componentes","Fuentes de poder",62540,12,10,"Catálogo"),
 ("P03","Tarjeta madre ASUS PRIME A520M-K","Componentes","Tarjetas madre",350000,6,12,"Catálogo"),
 ("P04","Procesador Intel Core i9 12.ª gen. (serie K)","Componentes","Procesadores",2150000,4,15,"Catálogo"),
 ("P05","Tarjeta madre ASUS TUF Gaming B650E-E WIFI","Componentes","Tarjetas madre",1250000,5,15,"Catálogo"),
 ("P06","Tarjeta madre ASRock B650M-H/M.2+","Componentes","Tarjetas madre",420000,9,12,"Catálogo"),
 ("P07","Procesador Intel Core i5-12400F","Componentes","Procesadores",914000,7,12,"Página web"),
 ("P08","Tarjeta gráfica NVIDIA GeForce RTX 3050 6GB OC","Componentes","Tarjetas gráficas",1390000,0,15,"Página web"),
 ("P09","Gabinete gamer Eva Cosmic 11M","Componentes","Gabinetes",200000,6,10,"Página web"),
 ("P10","Disipador líquido Corsair iCUE Titan 360 mm RGB","Componentes","Refrigeración",802946,2,15,"Página web"),
 ("P11","Teclado USB Multilaser","Periféricos","Teclados",35000,20,7,"Catálogo"),
 ("P12","Mouse gamer RGB","Periféricos","Mouse",45000,18,7,"Catálogo y página"),
 ("P13","Diadema gamer con micrófono RGB","Periféricos","Audio",75000,10,7,"Catálogo"),
 ("P14","Memoria RAM Corsair Vengeance RGB Pro","Memoria y almacenamiento","Memoria RAM",280000,7,10,"Catálogo"),
 ("P15","Unidad SSD ADATA SU650","Memoria y almacenamiento","Almacenamiento",160000,15,10,"Catálogo"),
 ("P16","Memoria RAM Crucial para portátil","Memoria y almacenamiento","Memoria RAM",95000,12,10,"Catálogo"),
 ("P17","Cámara web USB","Accesorios","Video",65000,10,7,"Catálogo y página"),
 ("P18","Hub USB 3.0 de cuatro puertos","Accesorios","Conectividad",30000,16,7,"Catálogo"),
 ("P19","Parlantes compactos RGB","Accesorios","Audio",45000,11,7,"Catálogo"),
 ("P20","Computador HP Pro Tower 290 G9 Core i3","Computadores","Escritorio oficina",1650000,6,15,"Catálogo"),
 ("P21","Computador de escritorio Acer Core i5","Computadores","Escritorio hogar",1900000,5,15,"Catálogo"),
]
CORTO = {"P01":"Ryzen 3 (3.ª gen.)","P02":"Fuente de poder","P03":"ASUS PRIME A520M-K","P04":"Core i9 12.ª gen. K",
 "P05":"ASUS TUF B650E-E WIFI","P06":"ASRock B650M-H/M.2+","P07":"Core i5-12400F","P08":"RTX 3050 6GB OC",
 "P09":"Gabinete Eva Cosmic 11M","P10":"Corsair iCUE Titan 360","P11":"Teclado Multilaser","P12":"Mouse gamer RGB",
 "P13":"Diadema gamer RGB","P14":"RAM Corsair Vengeance","P15":"SSD ADATA SU650","P16":"RAM Crucial portátil",
 "P17":"Cámara web USB","P18":"Hub USB 3.0 x4","P19":"Parlantes RGB","P20":"HP Pro Tower 290 G9","P21":"Acer Core i5"}
prod = pd.DataFrame(P, columns=["ID_Producto","Producto","Categoria","Subcategoria","Precio_Lista","Stock_Actual","Lead_Time_Dias","Origen"])
prod["Nombre_Corto"] = prod.ID_Producto.map(CORTO)
price = dict(zip(prod.ID_Producto, prod.Precio_Lista))

# ---------------- Ciudades ----------------
C = [("Bogotá","Cundinamarca","Andina",4.7110,-74.0721,0.36),
     ("Medellín","Antioquia","Andina",6.2442,-75.5812,0.20),
     ("Cali","Valle del Cauca","Pacífica",3.4516,-76.5320,0.13),
     ("Barranquilla","Atlántico","Caribe",10.9685,-74.7813,0.10),
     ("Bucaramanga","Santander","Andina",7.1193,-73.1227,0.08),
     ("Cartagena","Bolívar","Caribe",10.3910,-75.4794,0.07),
     ("Pereira","Risaralda","Andina",4.8133,-75.6961,0.06)]
ciud = pd.DataFrame(C, columns=["Ciudad","Departamento","Region","Latitud","Longitud","peso"])

# ---------------- Tipos de canasta ----------------
def pick(items, p=None): return items[rng.choice(len(items), p=p)]

def basket(tipo):
    L = []  # list of (prod, qty)
    if tipo == "periferico":
        main = pick(["P12","P11","P13","P19","P18"], [0.32,0.22,0.22,0.14,0.10])
        q = 1 if rng.random() < 0.85 else int(rng.choice([2,3]))
        if main == "P11" and rng.random() < 0.06: q = int(rng.choice([4,5,6]))  # compra de oficina
        L.append((main, q))
        if rng.random() < 0.35:
            extra = pick([x for x in ["P12","P11","P13","P19","P18"] if x != main])
            L.append((extra, 1))
    elif tipo == "upgrade":
        main = pick(["P14","P15","P16","P02"], [0.30,0.36,0.22,0.12])
        q = 1 if main in ("P15","P02") else int(rng.choice([1,2],p=[0.6,0.4]))
        L.append((main, q))
        if rng.random() < 0.30:
            extra = pick([x for x in ["P14","P15","P16","P18"] if x != main])
            L.append((extra, 1))
    elif tipo == "componente":
        main = pick(["P07","P08","P09","P01","P06","P05","P04","P10","P03"],
                    [0.19,0.18,0.15,0.11,0.10,0.08,0.06,0.07,0.06])
        L.append((main, 1))
        if main == "P08" and rng.random() < 0.45: L.append(("P02",1))
        if main == "P04" and rng.random() < 0.55: L.append(("P10",1))
        if main == "P07" and rng.random() < 0.30: L.append(("P14",1))
        if main == "P09" and rng.random() < 0.25: L.append(("P02",1))
    elif tipo == "armado":  # PC de entrada AM4 compatible
        L += [("P01",1),("P03",1),("P14",1),("P15",1)]
        if rng.random() < 0.7: L.append(("P02",1))
        if rng.random() < 0.6: L.append(("P09",1))
        if rng.random() < 0.3: L.append(("P12",1))
    elif tipo == "pc":
        main = pick(["P20","P21"], [0.52,0.48])
        q = 1 if rng.random() < 0.9 else 2
        L.append((main, q))
        if rng.random() < 0.40: L.append(("P17",1))
        if rng.random() < 0.25: L.append(("P13",1))
    elif tipo == "estudio":
        L.append(("P17", 1 if rng.random() < 0.9 else 2))
        for x, pr in [("P13",0.40),("P18",0.35),("P19",0.25)]:
            if rng.random() < pr: L.append((x,1))
    return L

TIPOS = ["periferico","upgrade","componente","armado","pc","estudio"]
BASE = np.array([0.38,0.19,0.17,0.05,0.08,0.13])
# multiplicadores estacionales por tipo (mes -> vector)
SEAS = {
 11: [1.0,1.0,1.45,1.3,1.2,0.8],   # Black Friday: tickets altos
 12: [1.35,0.9,1.25,1.1,1.0,0.8],  # Navidad: gamer/regalos
 1:  [0.9,1.0,0.8,0.9,1.4,1.7],    # regreso a clases
 2:  [0.9,1.0,0.8,0.9,1.3,1.6],
 6:  [1.0,1.1,1.1,1.1,1.2,0.9],    # prima
 7:  [1.0,1.1,1.0,1.0,1.1,1.0],
}
# volumen relativo de pedidos por mes (estacionalidad + crecimiento)
MESES = [(2025,11),(2025,12)] + [(2026,m) for m in range(1,11)]
VOL = {11:1.30,12:1.40,1:0.95,2:1.00,3:0.82,4:0.78,5:0.88,6:1.12,7:1.00,8:0.92,9:0.88,10:1.00}
N_PED = 760
w = np.array([VOL[m]*(1+0.025*i) for i,(y,m) in enumerate(MESES)])
counts = rng.multinomial(N_PED, w/w.sum())

# ---------------- Clientes ----------------
clientes = []  # ciudad de cada cliente

rows = []
oid = 0
used_first = {}
def black_friday(d): return dt.date(2025,11,27) <= d <= dt.date(2025,11,30)
for (y,m), n in zip(MESES, counts):
    ndays = (dt.date(y+(m==12), m%12+1, 1) - dt.date(y,m,1)).days
    # peso diario: fines de semana un poco más, Black Friday pico, quincenas
    dw = []
    for d in range(1, ndays+1):
        day = dt.date(y,m,d)
        x = 1.0 + (0.18 if day.weekday() >= 5 else 0) + (0.25 if d in (15,16,30,31,1) else 0)
        if black_friday(day): x *= 4.5
        if m == 12 and 15 <= d <= 23: x *= 1.6
        dw.append(x)
    dw = np.array(dw)/sum(dw)
    pt = BASE * np.array(SEAS.get(m,[1]*6)); pt /= pt.sum()
    for _ in range(n):
        oid += 1
        day = dt.date(y,m,int(rng.choice(np.arange(1,ndays+1), p=dw)))
        # 78 % de los pedidos vienen de clientes nuevos; el resto, de clientes que ya compraron
        if not clientes or rng.random() < 0.78:
            ccity = rng.choice(ciud.Ciudad, p=ciud.peso/ciud.peso.sum())
            clientes.append(ccity); cid = len(clientes)-1
        else:
            cid = int(rng.integers(len(clientes)))
        tipo = rng.choice(TIPOS, p=pt)
        items = {}
        for pid,q in basket(tipo):
            items[pid] = items.get(pid,0)+q
        ticket = sum(price[p]*q for p,q in items.items())
        p_cred = 0.85 if ticket >= 1_000_000 else (0.65 if ticket >= 300_000 else 0.40)
        pago = "Tarjeta de crédito" if rng.random() < p_cred else "Tarjeta débito"
        desc = 0.10 if black_friday(day) else 0.0
        for pid,q in items.items():
            rows.append(dict(ID_Pedido=f"NX-{oid:05d}", Fecha=day.isoformat(),
                             ID_Cliente=f"CL-{cid+1:04d}", ID_Producto=pid,
                             Ciudad=clientes[cid], Cantidad=q,
                             Precio_Unitario=int(round(price[pid]*(1-desc), -2)) if desc else price[pid],
                             Metodo_Pago=pago))

ped = pd.DataFrame(rows)
# reordenar cronológicamente y renumerar pedidos
first = ped.groupby("ID_Pedido").Fecha.first().sort_values(kind="stable")
mapid = {o:f"NX-{i+1:05d}" for i,o in enumerate(first.index)}
ped["ID_Pedido"] = ped.ID_Pedido.map(mapid)
ped = ped.sort_values(["Fecha","ID_Pedido","ID_Producto"]).reset_index(drop=True)
# clientes renumerados por orden de primera compra
fc = ped.drop_duplicates("ID_Cliente").ID_Cliente.tolist()
cmap = {c:f"CL-{i+1:04d}" for i,c in enumerate(fc)}
ped["ID_Cliente"] = ped.ID_Cliente.map(cmap)
# añadir Producto y Categoria (campos mínimos del docente en la tabla de pedidos)
ped = ped.merge(prod[["ID_Producto","Producto","Categoria"]], on="ID_Producto", how="left")
ped = ped[["ID_Pedido","Fecha","ID_Cliente","Ciudad","ID_Producto","Producto","Categoria",
           "Cantidad","Precio_Unitario","Metodo_Pago"]]

# ---------------- Inventario ----------------
corte = pd.to_datetime(ped.Fecha).max()
ult90 = ped[pd.to_datetime(ped.Fecha) > corte - pd.Timedelta(days=90)]
dd = ult90.groupby("ID_Producto").Cantidad.sum()/90
inv = prod[["ID_Producto","Stock_Actual","Lead_Time_Dias"]].copy()
inv["Demanda_Diaria"] = inv.ID_Producto.map(dd).fillna(0)
# punto de reorden (revisión quincenal) = demanda diaria x (lead time + 15 días de revisión) + stock de seguridad
# stock de seguridad = 50 % de la demanda durante el lead time (mínimo 1 unidad)
inv["Stock_Seguridad"] = inv.apply(lambda r: max(1, math.ceil(r.Demanda_Diaria*r.Lead_Time_Dias*0.5)), axis=1)
inv["Punto_Reorden"] = inv.apply(lambda r: math.ceil(r.Demanda_Diaria*(r.Lead_Time_Dias+15)) + r.Stock_Seguridad, axis=1)
inv["Fecha_Corte"] = corte.date().isoformat()
inv = inv[["ID_Producto","Stock_Actual","Punto_Reorden","Stock_Seguridad","Lead_Time_Dias","Fecha_Corte"]]

# ---------------- Metas ----------------
# meta comercial planeada: crecimiento lineal de 2,5 % mensual sobre una base, con ajuste de temporada
base = 26_500_000
ajuste = {11:1.25,12:1.50,1:1.05,2:0.95,3:0.88,4:0.88,5:0.92,6:1.30}
metas = []
for i,(y,m) in enumerate(MESES):
    v = base*(1+0.025*i)*ajuste.get(m,1.0)
    metas.append(dict(Mes=dt.date(y,m,1).isoformat(), Meta_Ventas=int(round(v,-6))))
metas = pd.DataFrame(metas)

prod_out = prod[["ID_Producto","Producto","Nombre_Corto","Categoria","Subcategoria","Precio_Lista","Origen"]]
ciud_out = ciud.drop(columns="peso")

OUT.mkdir(exist_ok=True)
for name, df in [("Pedidos",ped),("Productos",prod_out),("Inventario",inv),("Ciudades",ciud_out),("Metas",metas)]:
    df.to_csv(OUT/f"{name}.csv", index=False, encoding="utf-8")
print(ped.shape, ped.ID_Pedido.nunique(), "pedidos")

# ---------------- Excel con todas las tablas ----------------
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
xl = OUT/"NexaTech_Datos.xlsx"
tabs = [("Pedidos",ped),("Productos",prod_out),("Inventario",inv),("Ciudades",ciud_out),("Metas",metas)]
with pd.ExcelWriter(xl, engine="openpyxl") as w:
    for name, df in tabs:
        d = df.copy()
        for c in ("Fecha","Fecha_Corte","Mes"):
            if c in d: d[c] = pd.to_datetime(d[c])
        d.to_excel(w, sheet_name=name, index=False)
        ws = w.sheets[name]
        ref = f"A1:{get_column_letter(d.shape[1])}{d.shape[0]+1}"
        t = Table(displayName=f"t{name}", ref=ref)
        t.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
        ws.add_table(t)
        for i,c in enumerate(d.columns,1):
            ws.column_dimensions[get_column_letter(i)].width = max(12, min(48, int(d[c].astype(str).str.len().max())+3))
            fmt = None
            if c in ("Fecha","Fecha_Corte","Mes"): fmt = "dd/mm/yyyy"
            elif c in ("Precio_Unitario","Precio_Lista","Meta_Ventas"): fmt = '"$"#,##0'
            if fmt:
                for cell in ws[get_column_letter(i)][1:]: cell.number_format = fmt
        ws.freeze_panes = "A2"
print("xlsx ok")
