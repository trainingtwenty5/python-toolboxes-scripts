# ORANGE
print('----------------------------------- clnx_sites ----------------------------------- ')
import arcpy
import os

# Ustaw ścieżkę do źródłowej tabeli
input_table = r"D:\arcgisserver\mxd\2024_03_01_Cellnex\Dane\clnx_sites_2024Q1\clnx_2024Q1.gdb\clnx_sites_2024Q1"  # Zmień na właściwą ścieżkę

# Ustaw ścieżkę do wynikowej tabeli (w tym przypadku folder wyjściowy i nazwa pliku wynikowego)
output_gdb = r"D:\arcgisserver\mxd\2024_03_01_Cellnex\Dane\clnx_sites_2024Q1\clnx_2024Q1.gdb"

arcpy.management.AddField(input_table, "AKTUALIZACJA", "DATE")
arcpy.management.CalculateField(input_table, "AKTUALIZACJA", "time.strftime('%d/%m/%Y')")

output_table_name = "e1_Clnx_Clear"
arcpy.env.overwriteOutput = True

# Lista kolumn do wyodrębnienia
fields = [
    "OWNER",
    "SITE",
    "LATITUDE",
    "LONGITUDE",
    "STRUCTURE_TYPE",
    "TOWER_HEIGHT",
    "MAX_ANTENNA_HEIGHT",
    "TENANT",
    "TENANT_SITE_CODE",
    "AKTUALIZACJA"
]

# Klauzula WHERE, która filtruje rekordy

# Utwórz mapowanie pól
field_mappings = arcpy.FieldMappings()
print(field_mappings)
for field in fields:
    print(field)
    field_map = arcpy.FieldMap()
    field_map.addInputField(input_table, field)
    field_mappings.addFieldMap(field_map)

where_clause = "OWNER IN ('Towerlink', 'OnTower')"
# Użyj funkcji TableToTable_conversion do skopiowania wybranych kolumn
arcpy.conversion.TableToTable(input_table, output_gdb, output_table_name, field_mapping=field_mappings,
                              where_clause=where_clause)

pkt = arcpy.management.XYTableToPoint(
    in_table=output_table_name,
    out_feature_class=output_gdb + r"\Clnx",
    x_field="LONGITUDE",
    y_field="LATITUDE",
    coordinate_system=r'C:\Users\zz_gis_esri\AppData\Roaming\ESRI\Desktop10.8\projections\WGS 1984.prj',
)

arcpy.analysis.SplitByAttributes(pkt, output_gdb, "OWNER")

# Ustaw środowisko arcpy
arcpy.env.workspace = output_gdb

# Lista warstw w bieżącym środowisku
warstwy = arcpy.ListFeatureClasses()

# # Przeglądaj wszystkie warstwy i wykonaj operacje na tych, które zawierają "RED" w nazwie
# for warstwa in warstwy:
#     if "RED" in warstwa:
#         # Utwórz selekcję dla warstwy, gdzie DISCONNECT_DATE IS NULL
#         warstwa_1 = arcpy.management.SelectLayerByAttribute(warstwa, "NEW_SELECTION", "DISCONNECT_DATE IS NOT NULL", None)
#         # Utwórz warstwę dla selekcji i zapisz ją jako "RED - OFF"
#         arcpy.management.CopyFeatures(warstwa_1, f"{warstwa}_OFF")

#         # Utwórz selekcję dla warstwy, gdzie DISCONNECT_DATE IS NOT NULL
#         warstwa_2 = arcpy.management.SelectLayerByAttribute(warstwa, "NEW_SELECTION", "DISCONNECT_DATE IS NULL", None)
#         # Utwórz warstwę dla selekcji i zapisz ją jako "RED"
#         arcpy.management.CopyFeatures(warstwa_2, f"{warstwa}_ON")


base_symbology_path = r"D:\arcgisserver\mxd\2024_03_01_Cellnex"

# Define the suffixes
suffixes = ["OnTower", "Towerlink"]

coordinate_system_a = r'C:\Users\zz_gis_esri\AppData\Roaming\ESRI\Desktop10.8\projections\WGS 1984 Web Mercator (auxiliary sphere).prj'
# Loop through each suffix to apply the corresponding symbology
for suffix in suffixes:
    # Construct the full path to the feature class and symbology layer file
    feature_class_path = os.path.join(output_gdb, suffix)

    symbology_layer_file = os.path.join(base_symbology_path, suffix + ".lyr")

    # Apply the symbology from the layer file to the feature class
    arcpy.management.ApplySymbologyFromLayer(feature_class_path, symbology_layer_file, None, "DEFAULT")

print('----------------------------------- Zamiana nazw ----------------------------------- ')
# Otwórz projekt ArcGIS Pro
aprx = arcpy.mp.ArcGISProject("current")

############## EDYCJA ######################

# Przejdź przez wszystkie warstwy w danej mapie
map_obj = aprx.listMaps('Cellnex_map1')[0]

# Lista warstw do zmiany
warstwy_do_zmiany = map_obj.listLayers()

# Przejdź przez wszystkie warstwy w danej mapie
for lyr in warstwy_do_zmiany:
    # Pobierz alias warstwy i wyświetl go
    lyr_name = lyr.name
    # print(lyr_name)
    for warstwa in warstwy_do_zmiany:

        if "Towerlink" in lyr_name:
            lyr.name = "TPL"

        elif "OnTower" in lyr_name:
            lyr.name = "OTP"

print('\n')
print('done1')

print('----------------------------------- Warstwy bez stylu - NIE PUBLIKOWAĆ ----------------------------------- ')