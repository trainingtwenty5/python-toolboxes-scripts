import arcpy
import os
import time

print('----------------------------------- T-MOBILE ----------------------------------- ')

# Ustaw ścieżkę do źródłowej tabeli
input_table = r"D:\projekty_aprx\orange_projekty_aprx\2024_02_27_Critical_location\Dane\16_09_2024\16_09_2024.gdb\loc_critical___TMPL_16_09_2024csv"

# Ustaw ścieżkę do wynikowej tabeli
output_gdb = r"D:\projekty_aprx\orange_projekty_aprx\2024_02_27_Critical_location\Dane\16_09_2024\16_09_2024.gdb"

arcpy.management.AddField(input_table, "AKTUALIZACJA", "DATE")
arcpy.management.CalculateField(input_table, "AKTUALIZACJA", "time.strftime('%d/%m/%Y')")

output_table_name = "e1_loc_critical_Clear"
arcpy.env.overwriteOutput = True

# Lista kolumn do wyodrębnienia
fields = [
    "MNO_NAME", "PROJECT", "REGION", "LOC_NAME_OPL", "LOC_NETWORKS_NAME", "LOC_NETWORKS_CODE",
    "CEASE_DATE_PLAN", "DISCONNECT_DATE", "SOLUTION_DATE", "SOLUTION_DATE_PLAN", 
    "BEST_SOLUTION_PLAN_DATE", "CROSS_TYPE", "AKTUALIZACJA", "LOC_XPOS", "LOC_YPOS", 
    "LOC_LON84", "LOC_LAT84"
]

# Klauzula WHERE, która filtruje rekordy
where_clause = "RISK_STATUS IN ('BLACK', 'RED', 'YELLOW')"

# Utwórz mapowanie pól
field_mappings = arcpy.FieldMappings()
for field in fields:
    field_map = arcpy.FieldMap()
    field_map.addInputField(input_table, field)
    field_mappings.addFieldMap(field_map)

# Użyj funkcji TableToTable_conversion do skopiowania wybranych kolumn
arcpy.conversion.TableToTable(input_table, output_gdb, output_table_name, field_mapping=field_mappings, where_clause=where_clause)

# Utworzenie punktów w układzie WGS 1984
Critical_location_pkt = arcpy.management.XYTableToPoint(
    in_table=output_table_name,
    out_feature_class=output_gdb + r"\Critical_location",
    x_field="LOC_LON84",
    y_field="LOC_LAT84",
    coordinate_system=arcpy.SpatialReference(4326)  # WGS 1984
)

# Podział na warstwy
arcpy.analysis.SplitByAttributes(Critical_location_pkt, output_gdb, "CROSS_TYPE")

# Przekształcenie współrzędnych do układu WGS 1984 Web Mercator (auxiliary sphere)
coordinate_system_3857 = arcpy.SpatialReference(3857)  # WGS 1984 Web Mercator (auxiliary sphere)
suffixes = ["DISCONNECTED", "OFF_in_3"]
layers_3857 = []

for suffix in suffixes:
    in_feature_class = os.path.join(output_gdb, suffix)
    out_feature_class = os.path.join(output_gdb, suffix + "_3857")
    arcpy.management.Project(
        in_dataset=in_feature_class,
        out_dataset=out_feature_class,
        out_coor_system=coordinate_system_3857
    )
    layers_3857.append(out_feature_class)

print('----------------------------------- Zamiana nazw i stosowanie stylu ----------------------------------- ')
aprx = arcpy.mp.ArcGISProject("current")
map_obj = aprx.listMaps('T-MOBILE')[0]

# Usuń wszystkie warstwy z mapy
for lyr in map_obj.listLayers():
    map_obj.removeLayer(lyr)

# Dodaj nowe warstwy z 3857, zmień ich nazwy i zastosuj symbolizację
base_symbology_path = r"D:\projekty_aprx\orange_projekty_aprx\2024_02_27_Critical_location"
for lyr_path in layers_3857:
    lyr = map_obj.addDataFromPath(lyr_path)
    if "OFF_in_3_3857" in lyr.name:
        lyr.name = "Zagrożone"
        symbology_layer_file = os.path.join(base_symbology_path, "Critical_location_style_OFF_in_3.lyrx")
    elif "DISCONNECTED_3857" in lyr.name:
        lyr.name = "Wyłączone"
        symbology_layer_file = os.path.join(base_symbology_path, "Critical_location_style_DISCONNECTED.lyrx")
    print(lyr.name)
    arcpy.management.ApplySymbologyFromLayer(lyr, symbology_layer_file, "VALUE_FIELD CROSS_TYPE CROSS_TYPE", "DEFAULT")

print('\n')
print('done')
