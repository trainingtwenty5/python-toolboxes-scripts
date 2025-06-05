import arcpy
import os

# Ustaw ścieżkę do źródłowej tabeli
input_table = r"D:\ArcGIS\2024_02_27_Critical_location\2024_02_27_Critical_location.gdb\loc_critical_ExportTable"  # Zmień na właściwą ścieżkę

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
    "BEST_SOLUTION_PLAN_DATE",
    "X_POS",
    "Y_POS",
    "LON_84",
    "LAT_84"
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
arcpy.conversion.TableToTable(input_table, output_gdb, output_table_name, field_mapping=field_mappings, where_clause=where_clause)


arcpy.management.XYTableToPoint(
    in_table=output_table_name,
    out_feature_class=r"D:\ArcGIS\2024_02_27_Critical_location\2024_02_27_Critical_location.gdb\Critical_location",
    x_field="X_POS",
    y_field="Y_POS",
    coordinate_system= r'D:\ArcGIS\projections\ETRS 1989 Poland CS92.prj',
)


#Wyrzuca nową warstwę
# a = r'D:\ArcGIS\2024_02_27_Critical_location\2024_02_27_Critical_location.gdb\Critical_location'
# b = r'D:\ArcGIS\2024_02_27_Critical_location\Krytyczne_lokalizacje_styl.stylx'
# arcpy.management.ApplySymbologyFromLayer(a, b, "VALUE_FIELD RISK_STATUS RISK_STATUS", "DEFAULT")
# Rozwiazanie ale w ARCGIS PRO
arcpy.management.ApplySymbologyFromLayer("Critical_location", r"D:\ArcGIS\2024_02_27_Critical_location\Critical_location_style.lyrx", "VALUE_FIELD RISK_STATUS RISK_STATUS", "DEFAULT")



# Set output file names
outdir = r"D:\ArcGIS\2024_02_27_Critical_location"
service_name = "Krytyczne_lokalizacje"
sddraft_filename = service_name + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)
sd_filename = service_name + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)

# Reference map to publish
aprx = arcpy.mp.ArcGISProject(r"D:\ArcGIS\2024_02_27_Critical_location\2024_02_27_Critical_location.aprx")
m = aprx.listMaps('Krytyczne_lokalizacje_mapa')[0]

# Create MapServiceDraft and set metadata and server folder properties
target_server_connection = r"D:\ArcGIS\2024_02_27_Critical_location\admin on psgis01.tp.gk.corp.tepenet_6443.ags"
sddraft = arcpy.sharing.CreateSharingDraft("STANDALONE_SERVER", "MAP_SERVICE", service_name, m)
sddraft.targetServer = target_server_connection
sddraft.credits = "Krytyczne_lokalizacje"
sddraft.description = "Krytyczne_lokalizacje"
sddraft.summary = "Krytyczne_lokalizacje"
sddraft.tags = "Krytyczne_lokalizacje"
sddraft.useLimitations = "Owned by Orange Polska"
sddraft.serverFolder = "Critical_locations"
sddraft.overwriteExistingService = True

# Create Service Definition Draft file
sddraft.exportToSDDraft(sddraft_output_filename)

# Stage Service
print("Start Staging")
arcpy.server.StageService(sddraft_output_filename, sd_output_filename)

# Publish to server
print("Start Uploading")
arcpy.server.UploadServiceDefinition(sd_output_filename, target_server_connection)

print("Finish Publishing")