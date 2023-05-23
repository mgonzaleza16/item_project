from enum import Enum
from pydantic import BaseModel
from typing import Dict, Any, Optional
import pandas as pd

class ComparisonType(str, Enum):
    EQUALITY = "equality"
    INCLUSION = "inclusion"

class ComparisonResult(BaseModel):
    has_error: bool = False
    error_message: Optional[str] = None

class ComparisonSchema(BaseModel):
    comparison_type: ComparisonType = ComparisonType.EQUALITY
    columns_dict: Dict[str, str]

class DataFrameComparator:
    def __init__(self, df1: pd.DataFrame, df2: pd.DataFrame, df1_name: str, df2_name: str):
        self.df1 = df1
        self.df2 = df2
        self.df1_name = df1_name
        self.df2_name = df2_name

    def validate_columns(self, comparison_schema: ComparisonSchema) -> ComparisonResult:
        for df1_column, df2_column in comparison_schema.columns_dict.items():
            if df1_column not in self.df1.columns:
                return ComparisonResult(has_error=True, error_message=f"La columna {df1_column} no se encuentra en el dataframe {self.df1_name}.")
            if df2_column not in self.df2.columns:
                return ComparisonResult(has_error=True, error_message=f"La columna {df2_column} no se encuentra en el dataframe {self.df2_name}.")
        return ComparisonResult()

    def validate_values(self, comparison_schema: ComparisonSchema) -> ComparisonResult:
        for df1_column, df2_column in comparison_schema.columns_dict.items():
            if comparison_schema.comparison_type == ComparisonType.EQUALITY:
                unequal_values = self.df1[df1_column] != self.df2[df2_column]
                if unequal_values.any():
                    return ComparisonResult(has_error=True, error_message=f"Los valores de la columna {df1_column} en el dataframe {self.df1_name} no son iguales a los de la columna {df2_column} en el dataframe {self.df2_name} en las filas: {unequal_values[unequal_values].index.tolist()}")
            elif comparison_schema.comparison_type == ComparisonType.INCLUSION:
                not_included_values = ~self.df1[df1_column].isin(self.df2[df2_column])
                if not_included_values.any():
                    return ComparisonResult(has_error=True, error_message=f"Los valores de la columna {df1_column} en el dataframe {self.df1_name} no se encuentran en la columna {df2_column} del dataframe {self.df2_name}: {self.df1[df1_column][not_included_values].tolist()}")
        return ComparisonResult()
