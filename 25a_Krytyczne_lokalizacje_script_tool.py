import arcpy

# Ustaw ścieżkę do źródłowej tabeli
input_table = r"D:\ArcGIS\2024_02_27_Critical_location\2024_02_27_Critical_location.gdb\loc_critical_GIS_ExportTable"

# Ustaw ścieżkę do wynikowej tabeli (w tym przypadku folder wyjściowy i nazwa pliku wynikowego)
output_gdb = r"D:\ArcGIS\2024_02_27_Critical_location\2024_02_27_Critical_location.gdb"
output_table_name = "e1_loc_critical_Clear"
arcpy.env.overwriteOutput = True

# Lista kolumn do wyodrębnienia
fields = [
    "RISK_STATUS",
    "REGION",
    "PROJECT",
    "LOC_OBJ",
    "LOC_NAME_OPL",
    "FINAL_REMARKS",
    "DESC_INV",
    "CEASE_DATE_PLAN",
    "DISCONNECT_DATE",
    "SOLUTION_DATE",
    "BEST_SOLUTION_PLAN_DATE"
]

# Klauzula WHERE, która filtruje rekordy


# Utwórz mapowanie pól
field_mappings = arcpy.FieldMappings()
for field in fields:
    field_map = arcpy.FieldMap()
    field_map.addInputField(input_table, field)
    field_mappings.addFieldMap(field_map)

where_clause = "RISK_STATUS IN ('BLACK', 'RED', 'YELLOW')"
# Użyj funkcji TableToTable_conversion do skopiowania wybranych kolumn
arcpy.conversion.TableToTable(input_table, output_gdb, output_table_name, field_mapping=field_mappings,
                              where_clause=where_clause)
