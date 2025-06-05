print('----------------------------------- ORANGE ----------------------------------- ')
import arcpy
import os
import time

# Ustaw ścieżkę do źródłowej tabeli
input_table = r"D:\projekty_aprx\orange_projekty_aprx\2024_02_27_Critical_location\Dane\16_09_2024\16_09_2024.gdb\loc_critical_16_09_2024_CSV"  # Zmień na właściwą ścieżkę

# Ustaw ścieżkę do wynikowej tabeli (w tym przypadku folder wyjściowy i nazwa pliku wynikowego)
output_gdb = r"D:\projekty_aprx\orange_projekty_aprx\2024_02_27_Critical_location\Dane\16_09_2024\16_09_2024.gdb"

arcpy.management.AddField(input_table, "AKTUALIZACJA", "DATE")
arcpy.management.CalculateField(input_table, "AKTUALIZACJA", "time.strftime('%d/%m/%Y')")

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
    "BEST_SOLUTION_PLAN_DATE",
    "AKTUALIZACJA",
    "X_POS",
    "Y_POS",
    "LON_84",
    "LAT_84"
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
arcpy.conversion.TableToTable(input_table, output_gdb, output_table_name, field_mapping=field_mappings,
                              where_clause=where_clause)

# Utworzenie punktów w układzie WGS 1984
Critical_location_pkt = arcpy.management.XYTableToPoint(
    in_table=output_table_name,
    out_feature_class=output_gdb + r"\Critical_location",
    x_field="LON_84",
    y_field="LAT_84",
    coordinate_system=arcpy.SpatialReference(4326),  # WGS 1984
)

# Podział na warstwy
arcpy.analysis.SplitByAttributes(Critical_location_pkt, output_gdb, "RISK_STATUS")

# Dodatkowy podział warstw "RED" na "RED_OFF" i "RED_ON"
arcpy.env.workspace = output_gdb
warstwy = arcpy.ListFeatureClasses()

for warstwa in warstwy:
    if "RED" in warstwa:
        # Utwórz selekcję dla warstwy, gdzie DISCONNECT_DATE IS NOT NULL
        warstwa_1 = arcpy.management.SelectLayerByAttribute(warstwa, "NEW_SELECTION", "DISCONNECT_DATE IS NOT NULL",
                                                            None)
        # Utwórz warstwę dla selekcji i zapisz ją jako "RED_OFF"
        arcpy.management.CopyFeatures(warstwa_1, f"{warstwa}_OFF")

        # Utwórz selekcję dla warstwy, gdzie DISCONNECT_DATE IS NULL
        warstwa_2 = arcpy.management.SelectLayerByAttribute(warstwa, "NEW_SELECTION", "DISCONNECT_DATE IS NULL", None)
        # Utwórz warstwę dla selekcji i zapisz ją jako "RED_ON"
        arcpy.management.CopyFeatures(warstwa_2, f"{warstwa}_ON")

# Przekształcenie współrzędnych do układu WGS 1984 Web Mercator (auxiliary sphere)
coordinate_system_3857 = arcpy.SpatialReference(3857)  # WGS 1984 Web Mercator (auxiliary sphere)
suffixes = ["BLACK", "YELLOW", "RED_OFF", "RED_ON"]
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
map_obj = aprx.listMaps('ORANGE')[0]

# Usuń wszystkie warstwy z mapy
for lyr in map_obj.listLayers():
    map_obj.removeLayer(lyr)

# Dodaj nowe warstwy z 3857, zmień ich nazwy i zastosuj symbolizację
base_symbology_path = r"D:\projekty_aprx\orange_projekty_aprx\2024_02_27_Critical_location"
for lyr_path in layers_3857:
    lyr = map_obj.addDataFromPath(lyr_path)
    if "RED_ON" in lyr.name:
        lyr.name = "RED"
        symbology_layer_file = os.path.join(base_symbology_path, "Critical_location_style_RED_ON.lyrx")
    elif "YELLOW" in lyr.name:
        lyr.name = "YELLOW"
        symbology_layer_file = os.path.join(base_symbology_path, "Critical_location_style_YELLOW.lyrx")
    elif "BLACK" in lyr.name:
        lyr.name = "BLACK"
        symbology_layer_file = os.path.join(base_symbology_path, "Critical_location_style_BLACK.lyrx")
    elif "RED_OFF" in lyr.name:
        lyr.name = "RED_OFF"
        symbology_layer_file = os.path.join(base_symbology_path, "Critical_location_style_RED_OFF.lyrx")
    print(lyr.name)
    arcpy.management.ApplySymbologyFromLayer(lyr, symbology_layer_file, "VALUE_FIELD RISK_STATUS RISK_STATUS",
                                             "DEFAULT")

print('\n')
print('done')
