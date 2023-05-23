import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Aggregation:
    column: str
    agg_func: str
    output_name: str

@dataclass
class GroupingParameters:
    df: pd.DataFrame
    groupby_columns: List[str]
    aggregations: List[Aggregation]

@dataclass
class GroupedDataResult:
    dataframe: Optional[pd.DataFrame]
    error_message: Optional[str]

def group_dataframe(grouping_parameters: GroupingParameters) -> GroupedDataResult:
    try:
        # Crear un diccionario para mapear las columnas a sus respectivas funciones de agregación
        agg_dict = {agg.column: agg.agg_func for agg in grouping_parameters.aggregations}

        # Crear un diccionario para mapear las funciones de agregación a los nombres de columnas de salida
        rename_dict = {(agg.column, agg.agg_func): agg.output_name for agg in grouping_parameters.aggregations}

        # Realizar la operación de agrupación, reiniciar el índice y devolver el resultado
        grouped_df = (grouping_parameters.df.groupby(grouping_parameters.groupby_columns)
                        .agg(agg_dict)
                        .rename(columns=rename_dict)
                        .reset_index())
        return GroupedDataResult(dataframe=grouped_df, error_message=None)

    except Exception as e:
        return GroupedDataResult(dataframe=None, error_message=str(e))

