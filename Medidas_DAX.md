# Modelo de datos NexaTech — documentación técnica

## Modelo estrella

- **Hechos:** `Pedidos` (una fila por línea de pedido: un pedido puede tener varios productos).
- **Dimensiones:** `Productos`, `Ciudades`, `Calendario` (tabla de fechas DAX).
- **Tablas de apoyo:** `Inventario` (foto del stock al 31/10/2026) y `Metas` (meta mensual de ventas).
- **Medidas:** tabla `_Medidas` (solo contiene medidas, para tenerlas ordenadas en carpetas).

| Desde (muchos) | Hacia (uno) | Para qué |
|---|---|---|
| Pedidos[ID_Producto] | Productos[ID_Producto] | Analizar ventas por producto y categoría |
| Pedidos[Ciudad] | Ciudades[Ciudad] | Analizar ventas por ciudad/región |
| Pedidos[Fecha] | Calendario[Fecha] | Análisis por mes, trimestre y día de la semana |
| Metas[Mes] | Calendario[Fecha] | Comparar ventas vs. meta mensual |
| Inventario[ID_Producto] | Productos[ID_Producto] | Cruzar stock con la demanda de cada producto |

Todas las relaciones tienen filtro en una sola dirección (de la dimensión hacia la tabla de hechos).

## Power Query

Parámetro `RutaDatos` = carpeta de los CSV. Cada tabla: *Csv.Document → Promover encabezados → Tipos de dato (cultura en-US para leer bien decimales y fechas) → Renombrar columnas*. En `Pedidos` además se quitan `Producto` y `Categoria` (ya viven en la dimensión `Productos`; el docente las pidió en el archivo, pero en el modelo se evitan duplicados) y se agrega la columna `Importe = Cantidad × Precio Unitario`.

### Pedidos
```m
let
    Origen = Csv.Document(File.Contents(RutaDatos & "Pedidos.csv"), [Delimiter = ",", Columns = 10, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    QuitarDescriptivas = Table.RemoveColumns(Encabezados, {"Producto", "Categoria"}),
    Tipos = Table.TransformColumnTypes(QuitarDescriptivas, {{"ID_Pedido", type text}, {"Fecha", type date}, {"ID_Cliente", type text}, {"Ciudad", type text}, {"ID_Producto", type text}, {"Cantidad", Int64.Type}, {"Precio_Unitario", Int64.Type}, {"Metodo_Pago", type text}}, "en-US"),
    Renombradas = Table.RenameColumns(Tipos, {{"Precio_Unitario", "Precio Unitario"}, {"Metodo_Pago", "Método de Pago"}}),
    ConImporte = Table.AddColumn(Renombradas, "Importe", each [Cantidad] * [Precio Unitario], Int64.Type)
in
    ConImporte
```

### Productos
```m
let
    Origen = Csv.Document(File.Contents(RutaDatos & "Productos.csv"), [Delimiter = ",", Columns = 7, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"ID_Producto", type text}, {"Producto", type text}, {"Nombre_Corto", type text}, {"Categoria", type text}, {"Subcategoria", type text}, {"Precio_Lista", Int64.Type}, {"Origen", type text}}, "en-US"),
    Renombradas = Table.RenameColumns(Tipos, {{"Nombre_Corto", "Nombre Corto"}, {"Categoria", "Categoría"}, {"Subcategoria", "Subcategoría"}, {"Precio_Lista", "Precio Lista"}, {"Origen", "Fuente del Producto"}})
in
    Renombradas
```

### Inventario
```m
let
    Origen = Csv.Document(File.Contents(RutaDatos & "Inventario.csv"), [Delimiter = ",", Columns = 6, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"ID_Producto", type text}, {"Stock_Actual", Int64.Type}, {"Punto_Reorden", Int64.Type}, {"Stock_Seguridad", Int64.Type}, {"Lead_Time_Dias", Int64.Type}, {"Fecha_Corte", type date}}, "en-US")
in
    Tipos
```

### Ciudades
```m
let
    Origen = Csv.Document(File.Contents(RutaDatos & "Ciudades.csv"), [Delimiter = ",", Columns = 5, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"Ciudad", type text}, {"Departamento", type text}, {"Region", type text}, {"Latitud", type number}, {"Longitud", type number}}, "en-US"),
    Renombradas = Table.RenameColumns(Tipos, {{"Region", "Región"}})
in
    Renombradas
```

### Metas
```m
let
    Origen = Csv.Document(File.Contents(RutaDatos & "Metas.csv"), [Delimiter = ",", Columns = 2, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"Mes", type date}, {"Meta_Ventas", Int64.Type}}, "en-US")
in
    Tipos
```

## Tabla Calendario (DAX)

*Modelado → Nueva tabla*. Después: marcarla como tabla de fechas (columna `Fecha`) y ordenar `Mes` por `Orden Mes`, `Nombre Mes` por `Mes Num` y `Día Semana` por `Num Día Semana`.

```dax
Calendario =
VAR Inicio = DATE ( YEAR ( MIN ( Pedidos[Fecha] ) ), MONTH ( MIN ( Pedidos[Fecha] ) ), 1 )
VAR Fin = EOMONTH ( MAX ( Pedidos[Fecha] ), 0 )
RETURN
    SELECTCOLUMNS (
        CALENDAR ( Inicio, Fin ),
        "Fecha", [Date],
        "Año", YEAR ( [Date] ),
        "Mes Num", MONTH ( [Date] ),
        "Nombre Mes", SWITCH ( MONTH ( [Date] ), 1, "Ene", 2, "Feb", 3, "Mar", 4, "Abr", 5, "May", 6, "Jun", 7, "Jul", 8, "Ago", 9, "Sep", 10, "Oct", 11, "Nov", 12, "Dic" ),
        "Mes", SWITCH ( MONTH ( [Date] ), 1, "Ene", 2, "Feb", 3, "Mar", 4, "Abr", 5, "May", 6, "Jun", 7, "Jul", 8, "Ago", 9, "Sep", 10, "Oct", 11, "Nov", 12, "Dic" ) & " " & RIGHT ( YEAR ( [Date] ), 2 ),
        "Orden Mes", YEAR ( [Date] ) * 100 + MONTH ( [Date] ),
        "Trimestre", "T" & ROUNDUP ( MONTH ( [Date] ) / 3, 0 ),
        "Día Semana", SWITCH ( WEEKDAY ( [Date], 2 ), 1, "Lun", 2, "Mar", 3, "Mié", 4, "Jue", 5, "Vie", 6, "Sáb", 7, "Dom" ),
        "Num Día Semana", WEEKDAY ( [Date], 2 )
    )
```

## Medidas

### 1. Ventas

**Ventas Totales** — Ingresos = Σ Cantidad × Precio unitario. Formato: `\$#,0`.
```dax
Ventas Totales =
SUM ( Pedidos[Importe] )
```

**Unidades Vendidas** — Unidades vendidas. Formato: `#,0`.
```dax
Unidades Vendidas =
SUM ( Pedidos[Cantidad] )
```

**Total Pedidos** — Pedidos distintos (un pedido puede tener varias líneas). Formato: `#,0`.
```dax
Total Pedidos =
DISTINCTCOUNT ( Pedidos[ID_Pedido] )
```

**Ticket Promedio** — Valor promedio por pedido. Formato: `\$#,0`.
```dax
Ticket Promedio =
DIVIDE ( [Ventas Totales], [Total Pedidos] )
```

**Meta Ventas** — Meta mensual de ventas definida por la tienda. Formato: `\$#,0`.
```dax
Meta Ventas =
-- La meta es global: solo se muestra si no hay filtros de producto/categoría o ciudad
IF (
    ISFILTERED ( Productos ) || ISFILTERED ( Ciudades ),
    BLANK (),
    SUM ( Metas[Meta_Ventas] )
)
```

**% Cumplimiento Meta** — Ventas / Meta. Formato: `0%`.
```dax
% Cumplimiento Meta =
DIVIDE ( [Ventas Totales], [Meta Ventas] )
```

**% Participación** — Peso de cada categoría, producto o ciudad sobre el total visible. Formato: `0.0%`.
```dax
% Participación =
DIVIDE (
    [Ventas Totales],
    CALCULATE ( [Ventas Totales], ALLSELECTED ( Productos ), ALLSELECTED ( Ciudades ) )
)
```

**Ventas Top 8** — Ventas solo de los 8 productos con más ingresos (para el ranking). Formato: `\$#,0`.
```dax
Ventas Top 8 =
VAR Ventas = [Ventas Totales]
VAR Posicion = RANKX ( ALLSELECTED ( Productos[Nombre Corto] ), [Ventas Totales], , DESC )
RETURN
    IF ( NOT ISBLANK ( Ventas ) && Posicion <= 8, Ventas )
```

### 2. Clientes

**Clientes Únicos** — Clientes distintos que compraron. Formato: `#,0`.
```dax
Clientes Únicos =
DISTINCTCOUNT ( Pedidos[ID_Cliente] )
```

**Clientes Recurrentes** — Clientes con 2 o más pedidos en el periodo seleccionado. Formato: `#,0`.
```dax
Clientes Recurrentes =
COUNTROWS (
    FILTER (
        VALUES ( Pedidos[ID_Cliente] ),
        CALCULATE ( DISTINCTCOUNT ( Pedidos[ID_Pedido] ) ) > 1
    )
)
```

**% Recompra** — Clientes recurrentes / clientes únicos. Formato: `0%`.
```dax
% Recompra =
DIVIDE ( [Clientes Recurrentes], [Clientes Únicos] )
```

### 3. Inventario

**Stock Actual** — Unidades disponibles a la fecha de corte. Formato: `#,0`.
```dax
Stock Actual =
SUM ( Inventario[Stock_Actual] )
```

**Punto de Reorden** — Nivel de stock en el que se debe pedir al proveedor. Formato: `#,0`.
```dax
Punto de Reorden =
SUM ( Inventario[Punto_Reorden] )
```

**Demanda Diaria 90d** — Unidades promedio por día en los últimos 90 días (no depende de los filtros de fecha ni ciudad). Formato: `0.00`.
```dax
Demanda Diaria 90d =
VAR Corte = CALCULATE ( MAX ( Inventario[Fecha_Corte] ), REMOVEFILTERS () )
VAR Unidades90 =
    CALCULATE (
        [Unidades Vendidas],
        REMOVEFILTERS ( Calendario ),
        REMOVEFILTERS ( Ciudades ),
        FILTER ( ALL ( Calendario[Fecha] ), Calendario[Fecha] > Corte - 90 && Calendario[Fecha] <= Corte )
    )
RETURN
    DIVIDE ( Unidades90, 90 )
```

**Días de Cobertura** — Días que alcanza el stock al ritmo de venta actual. Formato: `#,0`.
```dax
Días de Cobertura =
DIVIDE ( [Stock Actual], [Demanda Diaria 90d] )
```

**Estado Inventario** — Agotado = 0 · Reponer ≤ punto de reorden · Vigilar ≤ 1,5 × punto de reorden.
```dax
Estado Inventario =
VAR Stock = [Stock Actual]
VAR Reorden = [Punto de Reorden]
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( Stock ), BLANK (),
        Stock = 0, "🔴 Agotado",
        Stock <= Reorden, "🟠 Reponer",
        Stock <= Reorden * 1.5, "🟡 Vigilar",
        "🟢 Suficiente"
    )
```

**Productos a Reponer** — Productos agotados o por debajo del punto de reorden. Formato: `#,0`.
```dax
Productos a Reponer =
COUNTROWS (
    FILTER ( VALUES ( Productos[ID_Producto] ), [Stock Actual] <= [Punto de Reorden] )
) + 0
```

**Productos Agotados** — Productos con stock 0. Formato: `#,0`.
```dax
Productos Agotados =
COUNTROWS (
    FILTER ( VALUES ( Productos[ID_Producto] ), [Stock Actual] = 0 )
) + 0
```

### 4. Textos KPI

**Texto Meta** — Subtítulo de la tarjeta de ventas.
```dax
Texto Meta =
VAR Cumplimiento = [% Cumplimiento Meta]
RETURN
    IF (
        ISBLANK ( Cumplimiento ),
        "Meta: ver sin filtros",
        IF ( Cumplimiento >= 1, "▲ ", "▼ " ) & FORMAT ( Cumplimiento, "0%" ) & " de la meta"
    )
```

**Texto Pedidos** — Subtítulo de la tarjeta de pedidos.
```dax
Texto Pedidos =
FORMAT ( [Unidades Vendidas], "#,0" ) & " unidades"
```

**Texto Ticket** — Subtítulo de la tarjeta de ticket.
```dax
Texto Ticket =
FORMAT ( DIVIDE ( [Unidades Vendidas], [Total Pedidos] ), "0.0" ) & " unid. por pedido"
```

**Texto Clientes** — Subtítulo de la tarjeta de clientes.
```dax
Texto Clientes =
FORMAT ( [% Recompra], "0%" ) & " volvió a comprar"
```

**Texto Inventario** — Subtítulo de la tarjeta de inventario.
```dax
Texto Inventario =
[Productos Agotados] & " agotado · " & ( [Productos a Reponer] - [Productos Agotados] ) & " por reponer"
```
