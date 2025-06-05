import arcpy
import time
# Ścieżki do baz danych
gdb = r'D:\arcgisserver\mxd\2024_04_24_Low_band\Dane\2805\2805.gdb'
sde_stackje = r'C:\Users\buchadan\AppData\Roaming\ESRI\ArcGISPro\Favorites\Stacje.sde'

raster_lte_800 = r'D:\dane\coverage\coverage_20240430\2024_04_DANE_3857.gdb\OPL_COV_LTE800_5class_Eo202404'

# Ścieżka do kolejnej warstwy
stacje = fr'{sde_stackje}\pgq_sde.stacje.stacje_act_geom_3857_t'

tabela = fr'{gdb}\NC_PTK_DUAL_LOWBAND_INFORMATIONCSV'
wgs84 = r'C:\Users\zz_gis_esri\AppData\Roaming\ESRI\Desktop10.8\projections\WGS 1984.prj'
# Dodawanie drugiego joinu

a = arcpy.management.JoinField(tabela, "LOC_OBJ", stacje, "loc_obj",)
arcpy.management.XYTableToPoint(a, fr'{gdb}\wszystkie_stacje', "lon84", "lat84", z_field=None, coordinate_system=wgs84)



# Dodanie nowego pola typu DATE
arcpy.management.AddField(fr'{gdb}\wszystkie_stacje', "AKTUALIZACJA", "DATE")

# Obliczenie wartości pola "AKTUALIZACJA" na podstawie aktualnej daty
current_date = time.strftime('%d/%m/%Y')
arcpy.management.CalculateField(fr'{gdb}\wszystkie_stacje', "AKTUALIZACJA", f"'{current_date}'", "PYTHON3")

# Lista kolumn, które chcesz zachować
desired_fields = [
    "Shape", "OBJECTID", "AKTUALIZACJA", "REGION", "ZONA", "PROJECT", "LOC_OBJ",
    "NETWORKS_CODE", "NETWORKS_NAME", "KLASTER_KPI",
    "VENDOR", "G5R_STATUS", "LOC_OBJ", "Shape_Length", "Shape_Area"
]



# Zachowanie tylko wybranych kolumn
#all_fields = [f.name for f in arcpy.ListFields(fr'{gdb}\wszystkie_stacje')]
#fields_to_delete = [f for f in all_fields if f not in desired_fields]

print(all_fields)
print('\n')
print('\n')
print('\n')
#print(fields_to_delete)

arcpy.management.DeleteField(fr'{gdb}\wszystkie_stacje', fields_to_delete)

dominance = r"D:\arcgisserver\mxd\2024_04_24_Low_band\dominance.sde\pgq_sde.dominance.lte800"

arcpy.conversion.ExportFeatures(dominance, fr'{gdb}\LTE800')



arcpy.management.JoinField(fr'{gdb}\LTE800', "LOC_OBJ", fr'{gdb}\wszystkie_stacje', "LOC_OBJ")

arcpy.analysis.Select(fr'{gdb}\LTE800', fr'{gdb}\Dominance_LTE800', "LOC_OBJ_1 IS NOT NULL")
arcpy.management.ApplySymbologyFromLayer(fr'{gdb}\Dominance_LTE800', r"D:\arcgisserver\mxd\2024_04_24_Low_band\Dominance_LTE800.lyrx")


arcpy.analysis.Select(fr'{gdb}\wszystkie_stacje', fr'{gdb}\Stacje_zrobione', "G5R_STATUS = 'ACCEPTED'")
arcpy.management.ApplySymbologyFromLayer(fr'{gdb}\Stacje_zrobione', r"D:\arcgisserver\mxd\2024_04_24_Low_band\Stacje_zrobione.lyrx")
arcpy.analysis.Select(fr'{gdb}\wszystkie_stacje', fr'{gdb}\Stacje_planowane', "G5R_STATUS <> 'ACCEPTED'")
arcpy.management.ApplySymbologyFromLayer(fr'{gdb}\Stacje_planowane', r"D:\arcgisserver\mxd\2024_04_24_Low_band\Stacje_planowane.lyrx")

out_raster = arcpy.sa.ExtractByMask(raster_lte_800, fr'{gdb}\Dominance_LTE800', "INSIDE");
out_raster.save(fr'{gdb}\Zasiegi_LTE800')
arcpy.management.ApplySymbologyFromLayer(fr'{gdb}\Zasiegi_LTE800', r"D:\arcgisserver\mxd\2024_04_24_Low_band\Zasiegi_LTE800.lyrx")


print('----------------------------------- Zamiana nazw ----------------------------------- ')
# Otwórz projekt ArcGIS Pro
aprx = arcpy.mp.ArcGISProject("current")

############## EDYCJA ######################

# Przejdź przez wszystkie warstwy w danej mapie
map_obj = aprx.listMaps('Low_band_mapa')[0]

# Lista warstw do zmiany
warstwy_do_zmiany = map_obj.listLayers()

# Przejdź przez wszystkie warstwy w danej mapie
for lyr in warstwy_do_zmiany:
    # Pobierz alias warstwy i wyświetl go
    lyr_name = lyr.name
    print(lyr_name)
    for warstwa in warstwy_do_zmiany:

        if "Stacje_planowane_Layer" in lyr_name:
            lyr.name = "Stacje_planowane"
        elif "Stacje_zrobione_Layer" in lyr_name:
            lyr.name = "Stacje_zrobione"
        elif "Dominance_LTE800_Layer" in lyr_name:
            lyr.name = "Dominance_LTE800"
        elif "Zasiegi_LTE800_Layer" in lyr_name:
            lyr.name = "Zasiegi_LTE800"

print('\n')
print('done')