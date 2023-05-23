# Excel Processor

Este módulo proporciona una manera de procesar archivos Excel con un esquema predefinido. Las clases y funciones en este módulo permiten leer hojas de Excel, validar y transformar datos en función del esquema proporcionado.

## Clases

### ExcelProcessor

La clase principal para procesar archivos Excel. Requiere un `file_path` y un objeto `SheetSchema` para su inicialización.

Métodos:

* `__init__(self, file_path: str, schema: SheetSchema)`: Inicializa la instancia de ExcelProcessor.
* `_rename_columns(self) -> None`: Cambia los nombres de las columnas en el dataframe de acuerdo con el esquema proporcionado.
* `_validate_columns_exist(self) -> None`: Verifica si todas las columnas definidas en el esquema están presentes en la hoja de Excel.
* `_validate_column_types(self) -> None`: Comprueba si todos los datos en las columnas tienen el tipo correcto según el esquema proporcionado.
* `_validate_no_formulas(self) -> None`: Verifica si no hay fórmulas en ninguna de las celdas del dataframe.
* `_validate_primary_key(self) -> None`: Valida que la columna definida como PK no tenga valores duplicados.
* `_validate_item_starts_with_letter(self, column_name: str) -> None`: Verifica que la columna proporcionada comience con una letra (solo para la hoja "Itemizado").
* `_validate_no_zero_values(self) -> None`: Verifica que las columnas marcadas para no contener ceros no tengan ningún valor igual a cero.
* `_validate_unique_values(self) -> None`: Verifica que las columnas que se deben ser únicas con respecto a otra columna cumplan esta condición.
* `process(self) -> ExcelProcessorResult`: Procesa el archivo Excel y devuelve un objeto ExcelProcessorResult que contiene el dataframe procesado o un mensaje de error.

### SheetSchema

Una clase para definir el esquema de una hoja de Excel, que incluye el nombre de la hoja y las columnas.

### ColumnSchema

Una clase para definir el esquema de una columna, que incluye el nombre antiguo, el nombre nuevo, el tipo de datos y si es la columna PK. También permite especificar si una columna no debe contener valores en cero o si debe ser única respecto a otra columna.

### ExcelProcessorResult

Una clase para almacenar el resultado del procesamiento del archivo Excel, incluyendo el dataframe y cualquier mensaje de error que pueda ocurrir durante el procesamiento.

## Uso

1. Importa las clases necesarias:

```python
from excel_processor import ExcelProcessor, SheetSchema, ColumnSchema

```

1. Define el esquema para la hoja y las columnas:

```python
schema = SheetSchema(
    sheet_name="Itemizado",
    columns=[
        ColumnSchema(old_name="Ítem", new_name="item_id", dtype=str, is_pk=True),
        ColumnSchema(old_name="Nombre Partida", new_name="name_item", dtype=str, is_pk=False),
        ColumnSchema(old_name="Cantidad", new_name="qty_item", dtype=float, is_pk=False, disallow_zero=True),
        ColumnSchema(old_name="Unidad", new_name="unit_item", dtype=str, is_pk=False),
        ColumnSchema(old_name="Cantidad HH", new_name="laborunits_item", dtype=float, is_pk=False),
    ]
)
```

3. Procesa el archivo Excel:

```python
processor = ExcelProcessor("Matriz de Conversion Clarificador Rev.B1.xlsx", schema)
result = processor.process()
```

Hint: La limpieza de los datos (eliminación de espacios y conversión a mayúsculas) se realiza después de renombrar las columnas y antes de validar los tipos de datos. Este es un orden lógico para estas operaciones, pero si necesitas que se realicen en un orden diferente, puedes ajustar el orden de las llamadas a métodos en `process()`.
