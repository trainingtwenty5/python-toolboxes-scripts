import arcpy
import os

# Otwórz projekt ArcGIS Pro
# aprx = arcpy.mp.ArcGISProject("current")

# Zdefiniuj listę warstw dostępnych w Geobazie
print('podaj path')
print('Wczytywanie warstw z geobazy profesjonalnej... to chwile zajmie...')
arcpy.env.workspace = r"D:\ArcGIS\Dane_zasiegowe_nr_1\Dane\paczka_opl_eo202312"

# Pobierz listę warstw, których nazwa zawiera frazy 'GES' lub 'OT'
# lista_warstw = arcpy.ListFeatureClasses('*GES_*') + arcpy.ListFeatureClasses('*OT_*')
lista_warstw_all = arcpy.ListRasters('*')
print('Raster all')
print(lista_warstw_all)

print('\n')

lista_warstw = arcpy.ListRasters("*")
print('Raster lista')
print(lista_warstw)
# print(f'Liczba warstw: {len(lista_warstw)}')
# print('Dane zostały wczytane')

print('podaj path')
folder_piramid = r'D:\Daniel\ArcGIS\Projects\Dane_zasiegowe_1\piramidy'
e2180 = r"D:\\ArcGIS\\projections\\PUWG_92.prj"
# e3857 = r"D:\ArcGIS\projections\WGS 1984 Web Mercator (auxiliary sphere).prj"

# output_feature_class_MV_raster = r'D:\ArcGIS\Dane_zasiegowe_nr_1\2024_01_16_MV_Dane_zasiegowe_3857.gdb'
# Ustawienia poziomu piramidy (przykładowa wartość - dostosuj do własnych potrzeb)


for warstwa_rastrowa in lista_warstw_all:
    # parametry

    # Wartość -1 oznacza pełne piramidy, czyli wszystkie dostępne poziomy
    # SKIP_EXISTING oznacza, że piramidy zostaną zbudowane tylko wtedy, gdy nie istnieją
    arcpy.management.BuildPyramids(warstwa_rastrowa, -1, "NONE", "NEAREST", "LZ77", 50, "SKIP_EXISTING")

    # print(wynik_raster)

    if warstwa_rastrowa in lista_warstw:
        arcpy.env.outputCoordinateSystem = e2180

        nazwa_bez_rozszerzenia, _ = os.path.splitext(warstwa_rastrowa)
        arcpy.management.BuildPyramids(warstwa_rastrowa, -1, "NONE", "NEAREST", "LZ77", 50, "SKIP_EXISTING")
        output_feature_class_MV_raster = fr'D:\ArcGIS\Dane_zasiegowe_nr_1\piramidy\\{nazwa_bez_rozszerzenia}_2180.tif'
        print('Path: ')
        print(output_feature_class_MV_raster)
        arcpy.management.ProjectRaster(warstwa_rastrowa, output_feature_class_MV_raster, e2180)





arcpy.env.workspace = r"D:\ArcGIS\Dane_zasiegowe_nr_1\2024_01_16_MV_Dane_zasiegowe_c.gdb"
e2180 = r"D:\\ArcGIS\\projections\\PUWG_92.prj"

# Pobierz listę warstw, których nazwa zawiera frazy 'GES' lub 'OT'
# lista_warstw = arcpy.ListFeatureClasses('*GES_*') + arcpy.ListFeatureClasses('*OT_*')
lista_warstw_all_mv = arcpy.ListFeatureClasses('*')
print(lista_warstw_all_mv)

for x in lista_warstw_all_mv:
    output_feature_class_MV = fr'D:\ArcGIS\Dane_zasiegowe_nr_1\DOM_202312_MV.gdb\\{x}_2180'
    print(output_feature_class_MV)

    arcpy.management.Project(x, output_feature_class_MV, e2180)