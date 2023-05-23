from .excel_processor import SheetSchema, ColumnSchema

itemizado_schema = SheetSchema(
    sheet_name="Itemizado",
    columns=[
        ColumnSchema(old_name="Ítem", new_name="item_id", dtype=str, is_pk=True , trim_spaces=True, to_uppercase=True),
        ColumnSchema(old_name="Tag Number", new_name="tag_id", dtype=object, trim_spaces=True),
        ColumnSchema(old_name="Nombre Partida", new_name="name_item", dtype=str,trim_spaces=True),
        ColumnSchema(old_name="BMP", new_name="bmp", dtype=object,trim_spaces=True),
        ColumnSchema(old_name="Cantidad", new_name="qty_item", dtype=float,decimal_places=2),
        ColumnSchema(old_name="Unidad", new_name="unit_item", dtype=object,trim_spaces=True),
        ColumnSchema(old_name="Cantidad HH", new_name="laborunits_item", dtype=float,decimal_places=2),
        ColumnSchema(old_name="Mano de Obra (CLP)", new_name="laborunits_cost_clp", dtype=float),
        ColumnSchema(old_name="Materiales e Insumos (CLP)", new_name="material_cost_clp", dtype=float),
        ColumnSchema(old_name="Equipos y Maquinarias (CLP)", new_name="equip_maq_cost_clp", dtype=float),
        ColumnSchema(old_name="Subcontratos (CLP)", new_name="sub_contractor_cost_clp", dtype=float),
        ColumnSchema(old_name="Otros (CLP)", new_name="others", dtype=float),
        ColumnSchema(old_name="Disciplina", new_name="discipline", dtype=object, trim_spaces=True),
        ColumnSchema(old_name="Rend", new_name="performance", dtype=float),
    ]
)

activity_schema = SheetSchema(
    sheet_name="Matriz Conversión P6 vs It",
    columns=[
        ColumnSchema(old_name="ID Ítem", new_name="item_id", dtype=str,trim_spaces=True, to_uppercase=True),
        ColumnSchema(old_name="ID Actividad", new_name="activity_code", dtype=str, trim_spaces=True),
        ColumnSchema(old_name="Actividad", new_name="activity_name", dtype=str, trim_spaces=True, unique_with="activity_code"),  # Actualizado
        ColumnSchema(old_name="Unidad", new_name="activity_unit", dtype=str, trim_spaces=True, to_uppercase=True, unique_with="activity_code"),  # Actualizado
        ColumnSchema(old_name="Cantidad", new_name="qty_activity", dtype=float, disallow_zero=True,decimal_places=2),
        ColumnSchema(old_name="HH Actividad", new_name="activity_laborunits", dtype=float, disallow_zero=True,decimal_places=2)
    ]
)
