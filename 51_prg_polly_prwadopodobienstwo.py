# Importowanie wymaganych bibliotek
import arcpy


# Definicja funkcji prawdopodobieństwa
def prawdopodobieAstwo22222322(teryt_2017, umts_900, geobaza, dom_umts900_opl, folder_z_wynikami, umts900_table_path,
                               umts_suffix):
    # Zezwolenie na nadpisywanie wyników, jeśli to konieczne
    arcpy.env.overwriteOutput = True

    # Definicja układów współrzędnych
    wgs1984 = arcpy.SpatialReference(4326)  # WGS 1984
    pl_cs92 = arcpy.SpatialReference(2180)  # PL_CS92 (ETRF2000-PL_CS92)
    print(f'{umts900_table_path}')
    # Tworzenie warstwy XY z tabeli UMTS900
    arcpy.management.MakeXYEventLayer(
        table=umts_900,
        in_x_field="WGS_LON",
        in_y_field="WGS_LAT",
        out_layer=umts900_table_path,
        spatial_reference=wgs1984  # Użycie WGS 1984
    )
    print('\n')
    print('etap 1 - ok')
    print(f'{umts900_table_path}')
    print('\n')
    # Konwersja warstwy XY na feature class
    umts900_shapefile = arcpy.conversion.FeatureClassToFeatureClass(
        in_features=umts900_table_path,
        out_path=geobaza,
        out_name=f"shapefile_{umts_suffix}"  # Dodanie suffixu do nazwy pliku
    )[0]
    print('\n')
    print('etap 2 - ok - tak na prawę to klase obeitkow robimy')
    print('\n')

    # Projekcja na układ współrzędnych PL-CS92
    umts900_92 = geobaza + f"\\{umts_suffix}_92_"  # Dodanie suffixu do nazwy pliku
    print(f'{umts900_92}')
    arcpy.management.Project(
        in_dataset=umts900_shapefile,
        out_dataset=umts900_92,
        out_coor_system=pl_cs92  # Projekcja do PL-CS92
    )
    print('\n')
    print('etap 3 - ok')
    print('\n')
    # Tworzenie bufora wokół obiektów UMTS900
    umts900_92_Buffer = geobaza + f"\\{umts_suffix}_92_Buffer_"  # Dodanie suffixu do nazwy pliku
    arcpy.analysis.Buffer(
        in_features=umts900_92,
        out_feature_class=umts900_92_Buffer,
        buffer_distance_or_field="RADIUS"
    )
    print('\n')
    print('etap 4 - ok')
    print('\n')
    # Dodanie pola na obliczenie powierzchni okręgu
    umts900_92_Buffer_2_ = arcpy.management.AddField(
        in_table=umts900_92_Buffer,
        field_name="area_circle",
        field_type="DOUBLE"
    )[0]
    print('\n')
    print('etap 5- ok')
    print('\n')

    #     # Obliczanie powierzchni
    #     umts900_92_Buffer_Area = geobaza + f"\\{umts_suffix}_92_Buffer_Area"  # Dodanie suffixu do nazwy pliku
    #     arcpy.stats.CalculateAreas(
    #         Input_Feature_Class=umts900_92_Buffer_2_,
    #         Output_Feature_Class=umts900_92_Buffer_Area
    #     )

    # Obliczanie pola dla każdego obiektu
    umts900_92_Buffer_Area_2_ = arcpy.management.CalculateField(
        in_table=umts900_92_Buffer,
        field="area_circle",
        expression="!SHAPE.area!",
        expression_type="PYTHON3"
    )[0]

    print('\n')
    print('etap 6- ok')
    print('\n')
    # Projekcja warstwy DOM UMTS900 do CS92
    DOM_LTE1800 = geobaza + f"\\DOM_{umts_suffix}"  # Dodanie suffixu do nazwy pliku
    arcpy.management.Project(
        in_dataset=dom_umts900_opl,
        out_dataset=DOM_LTE1800,
        out_coor_system=pl_cs92  # Projekcja do PL-CS92
    )
    print('\n')
    print('etap 7- ok - projekcja ukladu - dlugo trwa')
    print('\n')
    # Przecięcie warstw buforów i DOM UMTS900
    umts900_92_Buffer_Area_Intersect = geobaza + f"\\{umts_suffix}_92_Buffer_Area_Intersect"  # Dodanie suffixu do nazwy pliku
    arcpy.analysis.Intersect(
        in_features=[[umts900_92_Buffer_Area_2_, ""], [DOM_LTE1800, ""]],
        out_feature_class=umts900_92_Buffer_Area_Intersect
    )

    print('\n')
    print('etap 8- ok')
    print('\n')

    # Wybór obiektów o zgodnych warunkach
    umts900_92_Buffer_Area_Intersect_Select = geobaza + f"\\{umts_suffix}_92_Buffer_Area_Intersect_Select"  # Dodanie suffixu do nazwy pliku
    print(f'{umts900_92_Buffer_Area_Intersect_Select}')
    arcpy.analysis.Select(
        in_features=umts900_92_Buffer_Area_Intersect,
        out_feature_class=umts900_92_Buffer_Area_Intersect_Select,
        ##################??????????????????????############################################
        where_clause=f"OBJ = {indekx}_OBJ"
        ##################??????????????????????############################################
    )
    print('\n')
    print('etap 9- ok')
    print('\n')
    # Rozpuszczanie obiektów na podstawie pól
    umts900_92_Buffer_Area_Intersect_Select_Dissolve = geobaza + f"\\{umts_suffix}_92_Buffer_Area_Intersect_Select_Diss"  # Dodanie suffixu do nazwy pliku
    print(f'{umts900_92_Buffer_Area_Intersect_Select_Dissolve}')
    arcpy.management.Dissolve(
        in_features=umts900_92_Buffer_Area_Intersect_Select,
        out_feature_class=umts900_92_Buffer_Area_Intersect_Select_Dissolve,
        dissolve_field=["OBJ", "area_circle", "LOC_NAME", "LOC_OBJ", "LOC_CODE", f"{indekx}_NAME", f"{indekx}_OBJ",
                        f"{indekx}_CODE"]
    )

    print('\n')
    print('etap 10 - ok')
    print('\n')

    #     # Obliczanie obszarów po rozpuszczeniu
    #     umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area = geobaza + f"\\{umts_suffix}_92_Buffer_Area_Intersect_Select_Diss_Area"  # Dodanie suffixu do nazwy pliku
    #     arcpy.stats.CalculateAreas(
    #         Input_Feature_Class=umts900_92_Buffer_Area_Intersect_Select_Dissolve,
    #         Output_Feature_Class=umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area
    #     )
    #     print('\n')
    #     print('etap 11 - ok')
    #     print('\n')

    # Dodanie pola do obliczenia procentów
    umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area_2_ = arcpy.management.AddField(
        in_table=umts900_92_Buffer_Area_Intersect_Select_Dissolve,
        field_name="procent",
        field_type="DOUBLE"
    )[0]
    print('\n')
    print('etap 12 - ok')
    print('\n')

    # Obliczanie procentowego pokrycia obszaru
    umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area_3_ = arcpy.management.CalculateField(
        in_table=umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area_2_,
        field="procent",
        expression="!SHAPE.area!*100/!area_circle!",
        expression_type="PYTHON3"
    )[0]

    print('\n')
    print('etap 13 - ok')
    print('\n')

    # Łączenie wyników procentowych z tabelą buforów
    umts900_92_Buffer_z_procentami_ = arcpy.management.JoinField(
        in_data=umts900_92_Buffer,
        in_field="OBJ",
        join_table=umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area_3_,
        join_field="OBJ",
        fields=["procent"]
    )[0]
    print('\n')
    print('etap 14 - ok')
    print('\n')

    # Przecięcie warstw UMTS900 z TERYT 2017
    umts900_TERYT_Intersect = geobaza + f"\\{umts_suffix}_TERYT_Intersect"  # Dodanie suffixu do nazwy pliku
    arcpy.analysis.Intersect(
        in_features=[[umts900_92_Buffer_z_procentami_, ""], [teryt_2017, ""]],
        out_feature_class=umts900_TERYT_Intersect
    )
    print('\n')
    print('etap 14 - ok')
    print('\n')
    # Statystyki z przeciętych wyników
    umts900_TERYT_Statistics = geobaza + f"\\{umts_suffix}_TERYT_Statistics"  # Dodanie suffixu do nazwy pliku
    arcpy.analysis.Statistics(
        in_table=umts900_TERYT_Intersect,
        out_table=umts900_TERYT_Statistics,
        statistics_fields=[["procent", "MEAN"], ["procent", "MIN"], ["procent", "MAX"]],
        case_field=["TERYT"]
    )

    print('\n')
    print('etap 15 - ok')
    print('\n')

    # Zmiana nazw pól
    arcpy.management.AlterField(
        in_table=umts900_TERYT_Statistics,
        field="MEAN_procent",
        new_field_name="prawd_średnie",
        new_field_alias="prawd_średnie"
    )

    print('\n')
    print('etap 16 - ok')
    print('\n')

    arcpy.management.AlterField(
        in_table=umts900_TERYT_Statistics,
        field="MIN_procent",
        new_field_name="prawd_min",
        new_field_alias="prawd_min"
    )

    print('\n')
    print('etap 17 - ok')
    print('\n')
    arcpy.management.AlterField(
        in_table=umts900_TERYT_Statistics,
        field="MAX_procent",
        new_field_name="prawd_maks",
        new_field_alias="prawd_maks"
    )
    print('\n')
    print('etap 18 - ok')
    print('\n')
    # Eksport wyników do CSV
    arcpy.conversion.TableToTable(
        in_rows=umts900_TERYT_Statistics,
        out_path=folder_z_wynikami,
        out_name=f"Prawdopodobienstwo_{umts_suffix}.csv"
    )
    print('\n')
    print('etap 19 - ok')
    print('\n')

    print('#####################koniec#####################')


###########TABELA###############
umts_900 = "EXT_JV_ESB_MV_PTK_DICT_SDE_GMLC_2G_ExportTable_test"
##########################


########### dominanca ###############
dom = "OPL_DOM_GSM_Eo202409_MV"
##########################


############ sufix ##############
umts_suffix = "GSM"
##########################


#################technologia############

# 2g  "CELL" ------------ MUSI BYĆ  _CODE //
indekx = "CELL"
# ["OBJ", "area_circle", "LOC_NAME", "LOC_OBJ", "LOC_CODE", "WCELL_NAME", "WCELL_OBJ", "WCELL_CODE"]

############## 3g "WCELL"--------------- MUSI BYĆ  _CODE //  ###################

# ["OBJ", "area_circle", "LOC_NAME", "LOC_OBJ", "LOC_CODE", "WCELL_NAME", "WCELL_OBJ", "WCELL_CODE"]
# indekx = "WCELL"
################################


##### 4g "LCELL" #########   DLA 4 G MUSI BYĆ NIE _CODE // ALE _ID ###################
# indekx = "LCELL"
# ["OBJ", "area_circle", "LOC_NAME", "LOC_OBJ", "LOC_CODE", f"{indekx}_NAME", f"{indekx}_OBJ", f"{indekx}_ID"]
##############


# 5g "GCELL"
# indekx = "GCELL"
# ["OBJ", "area_circle", "LOC_NAME", "LOC_OBJ", "LOC_CODE", f"{indekx}_NAME", f"{indekx}_OBJ", f"{indekx}_ID"]


# Deklaracja zmiennych
teryt_2017 = r"D:\projekty_aprx\orange_projekty_aprx\prawdopodobienstwo\Dane\TERYT2024.gdb\TERYT_2024_done"
geobaza = r"D:\projekty_aprx\orange_projekty_aprx\prawdopodobienstwo\prawdopodobienstwo_20241025\prawdopodobienstwo_20241025.gdb"
umts900_table_path = r"D:\projekty_aprx\orange_projekty_aprx\prawdopodobienstwo\prawdopodobienstwo_20241025\prawdopodobienstwo_20241025.gdb"
dom_umts900_opl = fr"D:\COVERAGE\dane_2024_09_poprawione\dane_2024_09_poprawione\2024_09_MV.gdb\\{dom}"
folder_z_wynikami = r"D:\projekty_aprx\orange_projekty_aprx\prawdopodobienstwo\dane_wynikowe_2024_10"
# Wywołanie funkcji z możliwością zmiany dopisku
prawdopodobieAstwo22222322(teryt_2017, umts_900, geobaza, dom_umts900_opl, folder_z_wynikami, umts900_table_path,
                           umts_suffix)
