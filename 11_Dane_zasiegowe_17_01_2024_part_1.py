import arcpy
import os

# nadpisywanie obiektow
arcpy.env.overwriteOutput = True

print('---------------------- Start - dane zasiegowe ----------------------')
print('\n')
# TRZEBA DODAĆ TABELE - BO NIE DZIEALA INDEKSOWANIE - UMTS jest osobno na dole i LTE osobno

# pgq_sde.przeciazone.mv_przeciazone_lte800
# pgq_sde.przeciazone.mv_przeciazone_lte900
# pgq_sde.przeciazone.mv_przeciazone_lte1800
# pgq_sde.przeciazone.mv_przeciazone_lte2100
# pgq_sde.przeciazone.mv_przeciazone_lte2600
# pgq_sde.przeciazone.mv_przeciazone_u900
# pgq_sde.przeciazone.mv_przeciazone_u2100


# Ustaw środowisko pracy ArcPy # Ścieżka do folderu z plikami SHP
arcpy.env.workspace = r'D:\ArcGIS\______________________________Dane_zasiegowe______________________________\Dane_zasiegowe_nr_1\Dane'
e2180 = r"D:\ArcGIS\projections\PUWG_92.prj"

# Użyj Walk do rekurencyjnego przeglądania folderów i uzyskania plików SHP
lista_1 = []
lista_1UMTS = []
lista_1GSM = []
for folder, subfolders, files in arcpy.da.Walk(arcpy.env.workspace, datatype="FeatureClass"):
    for file in files:
        if 'LTE' in file:
            lista_1.append(os.path.join(folder, file))
        # UMTS2100 co miesiac ale przelicza sie zawsze
        if 'UMTS' in file:
            lista_1UMTS.append(os.path.join(folder, file))
        # co kwartal
        if 'GSM' in file:
            lista_1GSM.append(os.path.join(folder, file))

print('Start - dane zasiegowe')

# join_table = input(r"Podaj path dla lcell typ: D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\mv.gdb\lcell_20231130_Merge")
join_table = r'D:\ArcGIS\______________________________Dane_zasiegowe______________________________\Dane_zasiegowe_nr_1\mv.gdb\lcell_20231231_Merge'
print('\n')

# join_table_wcell = input(r"Podaj path dla wcell typ: D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\mv.gdb\wcell_20231130_Merge'")
join_table_wcell = r'D:\ArcGIS\______________________________Dane_zasiegowe______________________________\Dane_zasiegowe_nr_1\mv.gdb\wcell_20231231_Merge'
print('\n')

# join_table_cell = input(r"Podaj path dla cell typ: D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\mv.gdb\cell_20231130_Merge'")
join_table_cell = r'D:\ArcGIS\______________________________Dane_zasiegowe______________________________\Dane_zasiegowe_nr_1\mv.gdb\cell_20231231_Merge'
print('\n')

# output_info = input(r"Podaj path dla -- info -- wynikow: D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\Wynik_test_12_12_2023.gdb")
print('\n')
output_info = r'D:\ArcGIS\______________________________Dane_zasiegowe______________________________\Dane_zasiegowe_nr_1\2024_01_16_info_Dane_zasiegowe_new.gdb'
# output_MV = input(r"Podaj path dla -- MV -- wynikow: D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\Wynik_test_12_12_2023_MV.gdb")
output_MV = r'D:\ArcGIS\______________________________Dane_zasiegowe______________________________\Dane_zasiegowe_nr_1\2024_01_16_MV_Dane_zasiegowe_new.gdb'
print('\n')

print('\n')
print('---------------------- Wczytanie zmiennych ----------------------')
print('\n')

print('\n')
print('---------------------- CZESCI I - LTE ----------------------')
print('\n')

pola_do_usuniecia = []
nazwy_plikow = []
n = -1
for sciezka in lista_1:
    nazwa_pliku = os.path.basename(sciezka)
    nazwa_bez_rozszerzenia, rozszerzenie = os.path.splitext(nazwa_pliku)
    nazwy_plikow.append(nazwa_bez_rozszerzenia)
    n += 1

    arcpy.management.AddField(lista_1[n], "objj1", "Long")

    arcpy.management.CalculateField(lista_1[n], "objj1", '!LEGEND!', "PYTHON3")

    # join_table = 'lcell_20231130_Merge'

    wynik_1 = arcpy.management.AddJoin(lista_1[n], "objj1", join_table, "LCELL_OBJ")

    # chcemy ja nazwyać, warstwy maja się nazywac same

    # print(f'{output}\\{nazwy_plikow[n]})')

    output_feature_class_info = fr'{output_info}\\{nazwy_plikow[n]}_info'
    # print(output_feature_class_info)
    output_feature_class_MV = fr'{output_MV}\\{nazwy_plikow[n]}_MV'
    # print(output_feature_class_MV)

    arcpy.management.CopyFeatures(wynik_1, output_feature_class_info)
    arcpy.env.outputCoordinateSystem = e2180
    arcpy.management.CopyFeatures(wynik_1, output_feature_class_MV)

    # Usuń pola bezpośrednio z warstwy źródłowej
    lista_2 = arcpy.ListFields(output_feature_class_MV)

    for x in lista_2:
        pola_do_usuniecia.append(x.name)

    print('\n')
    print('Wyswietla rekordy do usuniecia w MV')
    print(pola_do_usuniecia[2:12])
    arcpy.management.DeleteField(output_feature_class_MV, pola_do_usuniecia[2:12])
    pola_do_usuniecia = []

    print('\n')
    print(f'Done: {nazwy_plikow[n]}_info')
    print(f'Done: {nazwy_plikow[n]}_MV')
    print('\n')

print('\n')
print('---------------------- KONIEC - CZESCI I - LTE ----------------------')
print('\n')

print('\n')
print('---------------------- CZESCI II - UMTS----------------------')
print('\n')

d = -1
nazwy_plikow_UMTS = []
for sciezka in lista_1UMTS:
    nazwa_pliku = os.path.basename(sciezka)
    # print('umts - nazwa_pliku')
    # print(nazwa_pliku)
    nazwa_bez_rozszerzenia, rozszerzenie = os.path.splitext(nazwa_pliku)
    nazwy_plikow_UMTS.append(nazwa_bez_rozszerzenia)
    # print('nazwy_plikow_UMTS.append(nazwa_bez_rozszerzenia) - umst')
    # print(nazwy_plikow_UMTS)
    d += 1

    arcpy.management.AddField(lista_1UMTS[d], "objj1", "Long")

    arcpy.management.CalculateField(lista_1UMTS[d], "objj1", '!LEGEND!', "PYTHON3")

    wynik_1 = arcpy.management.AddJoin(lista_1UMTS[d], "objj1", join_table_wcell, "WCELL_OBJ")

    # chcemy ja nazwyać, warstwy maja się nazywac same

    # print(f'{output}\\{nazwy_plikow[n]})')

    output_feature_class_info = fr'{output_info}\\{nazwy_plikow_UMTS[d]}_info'
    # print('UMTS - output_feature_class_info')
    # print(output_feature_class_info)
    output_feature_class_MV = fr'{output_MV}\\{nazwy_plikow_UMTS[d]}_MV'
    # print('UMTS - output_feature_class_MV')
    # print(output_feature_class_MV)

    arcpy.management.CopyFeatures(wynik_1, output_feature_class_info)
    arcpy.env.outputCoordinateSystem = e2180
    arcpy.management.CopyFeatures(wynik_1, output_feature_class_MV)

    # Usuń pola bezpośrednio z warstwy źródłowej
    lista_2 = arcpy.ListFields(output_feature_class_MV)
    print('lista_2 - UMTS')
    print(lista_2)
    for x in lista_2:
        pola_do_usuniecia.append(x.name)

    print('\n')
    print('Wyswietla rekordy do usuniecia w MV - UMTS')
    print(pola_do_usuniecia[2:12])
    arcpy.management.DeleteField(output_feature_class_MV, pola_do_usuniecia[2:12])
    pola_do_usuniecia = []

    print('\n')
    print(f'Done: {nazwy_plikow_UMTS[d]}_info')
    print(f'Done: {nazwy_plikow_UMTS[d]}_MV')
    print('\n')

print('\n')
print('---------------------- KONIEC CZESCI II - UMTS----------------------')
print('\n')

print('\n')
print('---------------------- CZESCI III - GSM ----------------------')
print('\n')

g = -1

nazwy_plikow_GSM = []
for sciezka in lista_1GSM:
    nazwa_pliku = os.path.basename(sciezka)
    print('GSM - nazwa_pliku')
    print(nazwa_pliku)
    nazwa_bez_rozszerzenia, rozszerzenie = os.path.splitext(nazwa_pliku)
    nazwy_plikow_GSM.append(nazwa_bez_rozszerzenia)
    print('nazwy_plikow_GSM.append(nazwa_bez_rozszerzenia) - gsm')
    print(nazwy_plikow_GSM)
    g += 1

    arcpy.management.AddField(lista_1GSM[g], "objj1", "Long")

    arcpy.management.CalculateField(lista_1GSM[g], "objj1", '!LEGEND!', "PYTHON3")

    wynik_1 = arcpy.management.AddJoin(lista_1GSM[g], "objj1", join_table_cell, "CELL_OBJ")

    # chcemy ja nazwyać, warstwy maja się nazywac same

    # print(f'{output}\\{nazwy_plikow[n]})')

    output_feature_class_info = fr'{output_info}\\{nazwy_plikow_GSM[g]}_info'
    # print('GSM - output_feature_class_info')
    # print(output_feature_class_info)
    output_feature_class_MV = fr'{output_MV}\\{nazwy_plikow_GSM[g]}_MV'
    # print('GSM - output_feature_class_MV')
    # print(output_feature_class_MV)

    arcpy.management.CopyFeatures(wynik_1, output_feature_class_info)
    arcpy.env.outputCoordinateSystem = e2180
    arcpy.management.CopyFeatures(wynik_1, output_feature_class_MV)

    # Usuń pola bezpośrednio z warstwy źródłowej
    lista_3 = arcpy.ListFields(output_feature_class_MV)
    # print('lista_2 - GSM')
    # print(lista_3)
    for x in lista_3:
        pola_do_usuniecia.append(x.name)

    print('\n')
    print('Wyswietla rekordy do usuniecia w MV - UMTS')
    print(pola_do_usuniecia[2:12])
    arcpy.management.DeleteField(output_feature_class_MV, pola_do_usuniecia[2:12])
    pola_do_usuniecia = []

    print('\n')
    print(f'Done: {nazwy_plikow_GSM[g]}_info')
    print(f'Done: {nazwy_plikow_GSM[g]}_MV')
    print('\n')

print('\n')
print('---------------------- KONIEC CZESCI III - GSM  ----------------------')
print('\n')
