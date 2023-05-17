# Proyecto de Análisis de Datos con Python

Este proyecto tiene como objetivo analizar un archivo Excel proporcionado por el cliente y compararlo con datos provenientes de Primavera P6. Utiliza Python y Jupyter Notebook para implementar el flujo de trabajo.

## Estructura del directorio

El proyecto está organizado de la siguiente manera:

- `main.ipynb`: Archivo principal de Jupyter Notebook que contiene el flujo principal del proyecto.
- `excel_processor/`: Directorio que contiene el módulo `excel_processor.py` encargado de procesar archivos Excel según un esquema predefinido.
- `data/`: Directorio que almacena los datos de entrada y salida.

  - `input/`: Carpeta donde se coloca el archivo Excel proporcionado por el cliente (`cliente.xlsx`).
  - `output/`: Carpeta donde se guarda el resultado del análisis, como el archivo Excel resultante (`resultado.xlsx`).
- `p6_data/`: Directorio que contiene el módulo `import_data_to_p6.py` utilizado para importar datos desde la base de datos Primavera P6.
- `utils/`: Directorio que alberga el módulo `add_columns_to_dataframe.py` y otros archivos de utilidad.

## Requisitos

Para ejecutar este proyecto, se requiere tener instalados los siguientes paquetes de Python:

- pandas
- openpyxl
- sqlalchemy

Puedes instalar estos paquetes ejecutando el siguiente comando: 

pip install -r requirements.txt

## Uso

1. Coloca el archivo Excel proporcionado por el cliente en la carpeta `data/input/`.
2. Ejecuta el archivo `main.ipynb` en Jupyter Notebook para iniciar el análisis.
3. El resultado del análisis se guardará en la carpeta `data/output/` como `resultado.xlsx`.
