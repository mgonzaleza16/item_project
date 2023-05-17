# AddColumnsToDataFrame

Este módulo contiene la clase `AddColumnsToDataFrame`, que permite agregar nuevas columnas a un DataFrame de Pandas a partir de un diccionario de parámetros.

## Uso

Para utilizar esta clase, importe el módulo y cree una instancia de `AddColumnsToDataFrame`, proporcionando un DataFrame de Pandas y un diccionario de parámetros. Luego, utilice el método `add_columns` para agregar las nuevas columnas al DataFrame.

```python
from add_columns_to_dataframe import AddColumnsToDataFrame

# DataFrame de ejemplo y diccionario de parámetros
df = pd.DataFrame(...)
params = {"columna1": "valor1", "columna2": "valor2"}

# Crear instancia de la clase e ingresar el dataframe y el diccionario de parámetros
add_columns_to_df = AddColumnsToDataFrame(dataframe=df, parameters=params)

# Agregar columnas al dataframe
df_with_columns = add_columns_to_df.add_columns()

```

# DataFrame de ejemplo y diccionario de parámetros

df = pd.DataFrame(...)
params = {"columna1": "valor1", "columna2": "valor2"}

# Crear instancia de la clase e ingresar el dataframe y el diccionario de parámetros

add_columns_to_df = AddColumnsToDataFrame(dataframe=df, parameters=params)

# Agregar columnas al dataframe

df_with_columns = add_columns_to_df.add_columns()
`</code></div>``</div></pre>`

## Validaciones

La clase `AddColumnsToDataFrame` realiza las siguientes validaciones:

* Verifica que el argumento `dataframe` sea un DataFrame de Pandas.
* Verifica que el argumento `parameters` sea un diccionario.
* Solo agrega las columnas que no existan actualmente en el DataFrame. Si una columna ya está presente en el DataFrame, no se modifica.
* Captura cualquier error que ocurra durante la adición de las nuevas columnas y evita que el error detenga la ejecución del programa. En caso de error, devuelve el DataFrame original sin modificar.
