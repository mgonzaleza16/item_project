import pandas as pd
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Tuple, Optional
import re

class ColumnSchema(BaseModel):
    old_name: str
    new_name: str
    dtype: Any
    is_pk: bool = False
    trim_spaces: bool = False
    to_uppercase: bool = False
    is_composite_pk: Optional[List[str]] = None
    unique_with: Optional[str] = None
    disallow_zero: bool = False  # Nuevo parámetro


class SheetSchema(BaseModel):
    sheet_name: str
    columns: List[ColumnSchema]

class ExcelProcessorResult:
    def __init__(self, dataframe: Optional[pd.DataFrame] = None, error_message: Optional[str] = None):
        self.dataframe = dataframe
        self.error_message = error_message


class ExcelProcessor:
    def __init__(self, file_path: str, schema: SheetSchema):
        self.file_path = file_path
        self.schema = schema
        self.df = None

    def _rename_columns(self) -> None:
        rename_dict = {column.old_name: column.new_name for column in self.schema.columns}
        self.df.rename(columns=rename_dict, inplace=True)

    def _validate_column_types(self) -> None:
        for column in self.schema.columns:
            invalid_cells = self.df.loc[
                ~self.df[column.new_name].apply(
                    lambda x: pd.isna(x) or isinstance(x, column.dtype)
                )
            ]
            if not invalid_cells.empty:
                invalid_cells_info = ', '.join(
                    [f"{column.new_name}{index + 2}" for index in invalid_cells.index]
                )
                raise ValueError(
                    f"La columna {column.new_name} contiene valores de diferentes tipos en las celdas: {invalid_cells_info}"
                )

    def _validate_no_formulas(self) -> None:
        for column in self.schema.columns:
            formula_cells = self.df.loc[self.df[column.new_name].apply(lambda x: isinstance(x, str) and x.startswith('='))]
            if not formula_cells.empty:
                formula_cells_info = ', '.join([f"{column.new_name}{index + 2}" for index in formula_cells.index])
                raise ValueError(f"La columna {column.new_name} contiene fórmulas en las celdas: {formula_cells_info}")

    def _validate_primary_key(self) -> None:
        pk_columns = [col.new_name for col in self.schema.columns if col.is_pk]

        if pk_columns:
            duplicated = self.df.duplicated(subset=pk_columns)
            if duplicated.any():
                raise ValueError(f"Clave primaria duplicada en las filas: {duplicated[duplicated].index.tolist()}")

    def _validate_item_starts_with_letter(self, column_name: str) -> None:
        non_letter_cells = self.df.loc[~self.df[column_name].apply(lambda x: bool(re.match("^[A-Za-z]", x)))]
        if not non_letter_cells.empty:
            non_letter_cells_info = ', '.join([f"{column_name}{index + 2}" for index in non_letter_cells.index])
            raise ValueError(f"La columna {column_name} debe comenzar con una letra en las celdas: {non_letter_cells_info}")

    def _validate_columns_exist(self) -> None:
        missing_columns = [column.old_name for column in self.schema.columns if column.old_name not in self.df.columns]
        if missing_columns:
            raise ValueError(f"Las siguientes columnas no se encuentran en la hoja de Excel: {', '.join(missing_columns)}")

    def _clean_columns(self) -> None:
        for column in self.schema.columns:
            if column.dtype == str:  # Solo realiza operaciones de cadena en columnas que se supone que son de texto
                if self.df[column.new_name].apply(type).eq(str).all():  # Verifica si todos los datos son de tipo cadena
                    if column.trim_spaces:
                        self.df[column.new_name] = self.df[column.new_name].str.strip()
                    if column.to_uppercase:
                        self.df[column.new_name] = self.df[column.new_name].str.upper()
                else:
                    raise ValueError(f"Column {column.new_name} is expected to be of type str, but contains non-str data.")

    def _validate_unique_values(self) -> None:
        for column in self.schema.columns:
            if column.unique_with is not None:
                df_grouped = self.df.groupby(column.unique_with)[column.new_name].nunique()
                non_unique_values = df_grouped[df_grouped > 1]

                if not non_unique_values.empty:
                    raise ValueError(f"Column '{column.new_name}' has multiple values for the same '{column.unique_with}': {non_unique_values.index.tolist()}")

    def _validate_no_zero_values(self) -> None:
        for column in self.schema.columns:
            if column.disallow_zero:
                zero_cells = self.df.loc[self.df[column.new_name] == 0]
                if not zero_cells.empty:
                    zero_cells_info = ', '.join([f"{column.new_name}{index + 2}" for index in zero_cells.index])
                    raise ValueError(f"La columna {column.new_name} contiene valores 0 en las celdas: {zero_cells_info}")


    def process(self) -> ExcelProcessorResult:
        try:
            self.df = pd.read_excel(self.file_path, sheet_name=self.schema.sheet_name)
            self._validate_columns_exist()
            self._rename_columns()
            self._clean_columns()
            self._validate_column_types()
            self._validate_no_formulas()
            self._validate_primary_key()  # aquí es donde se produjo el error
            self._validate_no_zero_values()
            self._validate_unique_values()
            if self.schema.sheet_name == "Itemizado":
                self._validate_item_starts_with_letter("item_id")
            self.df = self.df[[column.new_name for column in self.schema.columns]]
            self.df.fillna(value=pd.NA, inplace=True)
            return ExcelProcessorResult(dataframe=self.df)
        except Exception as e:
            return ExcelProcessorResult(error_message=str(e))

