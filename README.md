# Guía de armado — Dashboard NexaTech en Power BI

## Qué hay en esta carpeta

| Elemento | Para qué sirve |
|---|---|
| `NexaTech_Dashboard.pbip` | **Proyecto completo**: modelo, Power Query, medidas DAX, tema y las 2 páginas con sus visuales. Ábrelo primero. |
| `NexaTech_ModeloBase.pbip` | Respaldo: el mismo modelo y las mismas medidas, con una página vacía. Úsalo solo si el anterior no abre. |
| `Datos/` | Los 5 CSV que lee el modelo y un Excel (`NexaTech_Datos.xlsx`).|
| `Recursos/` | Tema de colores (`NexaTech_tema.json`), fondos de página y logo, para el armado manual. |
| `Medidas_DAX.md` | Todo el modelo documentado: tablas, relaciones, pasos de Power Query y código de cada medida.

## Paso a paso (Windows)

1. **Descomprime la carpeta en `C:\`**, de modo que quede `C:\NexaTech_PowerBI\`. Esa es la ruta que el modelo espera para los CSV.
2. Ten **Power BI Desktop actualizado**. Si al abrir el `.pbip` aparece un aviso sobre proyectos, ve a *Archivo → Opciones y configuración → Opciones → Características en versión preliminar*, activa la opción de **proyectos de Power BI (.pbip)** y reinicia Power BI. Si Power BI ofrece "actualizar" el proyecto a un formato más nuevo, acepta: no afecta nada.
3. Doble clic en **`NexaTech_Dashboard.pbip`**.
4. Si descomprimiste en otra ruta: *Inicio → Transformar datos → Editar parámetros → `RutaDatos`* y escribe la carpeta `Datos` (debe terminar en `\`).
5. **Inicio → Actualizar.** El proyecto se entrega sin datos cargados: hasta que actualices, los visuales se verán vacíos.
