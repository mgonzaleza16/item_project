from typing import Dict, Any
import pandas as pd
from pydantic import BaseModel, Field

class AddColumnsToDataFrame(BaseModel):
    dataframe: pd.DataFrame = Field(..., description="Pandas DataFrame")
    parameters: Dict[str, Any] = Field(..., description="Dictionary with new column names and values")

    class Config:
        arbitrary_types_allowed = True

    def add_columns(self) -> pd.DataFrame:
        try:
            new_columns = {k: v for k, v in self.parameters.items() if k not in self.dataframe.columns}
            return self.dataframe.assign(**new_columns)
        except Exception as e:
            print(f"Error al agregar columnas al DataFrame: {e}")
            return self.dataframe
