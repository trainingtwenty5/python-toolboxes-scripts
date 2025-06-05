# Importowanie wymaganych bibliotek
import arcpy


# Definicja funkcji prawdopodobieństwa
def prawdopodobieAstwo22222322(teryt_2017, umts_900, geobaza, dom_umts900_opl, folder_z_wynikami, umts900_table_path,
                               umts_suffix):
    # Zezwolenie na nadpisywanie wyników, jeśli to konieczne
    arcpy.env.overwriteOutput = False

    # Definicja układów współrzędnych
    wgs1984 = arcpy.SpatialReference(4326)  # WGS 1984
    pl_cs92 = arcpy.SpatialReference(2180)  # PL_CS92 (ETRF2000-PL_CS92)

    # Tworzenie warstwy XY z tabeli UMTS900
    arcpy.management.MakeXYEventLayer(
        table=umts_900,
        in_x_field="WGS_LON",
        in_y_field="WGS_LAT",
        out_layer=umts900_table_path,
        spatial_reference=wgs1984  # Użycie WGS 1984
    )

    # Konwersja warstwy XY na feature class
    umts900_shapefile = arcpy.conversion.FeatureClassToFeatureClass(
        in_features=umts900_table_path,
        out_path=geobaza,
        out_name=f"shapefile_{umts_suffix}"  # Dodanie suffixu do nazwy pliku
    )[0]

    # Projekcja na układ współrzędnych PL-CS92
    umts900_92 = geobaza + f"\\{umts_suffix}_92_"  # Dodanie suffixu do nazwy pliku
    arcpy.management.Project(
        in_dataset=umts900_shapefile,
        out_dataset=umts900_92,
        out_coor_system=pl_cs92  # Projekcja do PL-CS92
    )

    # Tworzenie bufora wokół obiektów UMTS900
    umts900_92_Buffer = geobaza + f"\\{umts_suffix}_92_Buffer_"  # Dodanie suffixu do nazwy pliku
    arcpy.analysis.Buffer(
        in_features=umts900_92,
        out_feature_class=umts900_92_Buffer,
        buffer_distance_or_field="RADIUS"
    )

    # Dodanie pola na obliczenie powierzchni okręgu
    umts900_92_Buffer_2_ = arcpy.management.AddField(
        in_table=umts900_92_Buffer,
        field_name="area_circle",
        field_type="DOUBLE"
    )[0]

    # Obliczanie powierzchni
    umts900_92_Buffer_Area = geobaza + f"\\{umts_suffix}_92_Buffer_Area"  # Dodanie suffixu do nazwy pliku
    arcpy.stats.CalculateAreas(
        Input_Feature_Class=umts900_92_Buffer_2_,
        Output_Feature_Class=umts900_92_Buffer_Area
    )

    # Obliczanie pola dla każdego obiektu
    umts900_92_Buffer_Area_2_ = arcpy.management.CalculateField(
        in_table=umts900_92_Buffer_Area,
        field="area_circle",
        expression="[F_AREA]",
        expression_type="VB"
    )[0]

    # Projekcja warstwy DOM UMTS900 do CS92
    DOM_LTE1800 = geobaza + f"\\DOM_{umts_suffix}"  # Dodanie suffixu do nazwy pliku
    arcpy.management.Project(
        in_dataset=dom_umts900_opl,
        out_dataset=DOM_LTE1800,
        out_coor_system=pl_cs92  # Projekcja do PL-CS92
    )

    # Przecięcie warstw buforów i DOM UMTS900
    umts900_92_Buffer_Area_Intersect = geobaza + f"\\{umts_suffix}_92_Buffer_Area_Intersect"  # Dodanie suffixu do nazwy pliku
    arcpy.analysis.Intersect(
        in_features=[[umts900_92_Buffer_Area_2_, ""], [DOM_LTE1800, ""]],
        out_feature_class=umts900_92_Buffer_Area_Intersect
    )

    # Wybór obiektów o zgodnych warunkach
    umts900_92_Buffer_Area_Intersect_Select = geobaza + f"\\{umts_suffix}_92_Buffer_Area_Intersect_Select"  # Dodanie suffixu do nazwy pliku
    arcpy.analysis.Select(
        in_features=umts900_92_Buffer_Area_Intersect,
        out_feature_class=umts900_92_Buffer_Area_Intersect_Select,
        where_clause="OBJ = WCELL_OBJ"
    )

    # Rozpuszczanie obiektów na podstawie pól
    umts900_92_Buffer_Area_Intersect_Select_Dissolve = geobaza + f"\\{umts_suffix}_92_Buffer_Area_Intersect_Select_Diss"  # Dodanie suffixu do nazwy pliku
    arcpy.management.Dissolve(
        in_features=umts900_92_Buffer_Area_Intersect_Select,
        out_feature_class=umts900_92_Buffer_Area_Intersect_Select_Dissolve,
        dissolve_field=["OBJ", "area_circle", "LOC_NAME", "LOC_OBJ", "LOC_CODE", "WCELL_NAME", "WCELL_OBJ",
                        "WCELL_CODE"]
    )

    # Obliczanie obszarów po rozpuszczeniu
    umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area = geobaza + f"\\{umts_suffix}_92_Buffer_Area_Intersect_Select_Diss_Area"  # Dodanie suffixu do nazwy pliku
    arcpy.stats.CalculateAreas(
        Input_Feature_Class=umts900_92_Buffer_Area_Intersect_Select_Dissolve,
        Output_Feature_Class=umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area
    )

    # Dodanie pola do obliczenia procentów
    umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area_2_ = arcpy.management.AddField(
        in_table=umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area,
        field_name="procent",
        field_type="DOUBLE"
    )[0]

    # Obliczanie procentowego pokrycia obszaru
    umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area_3_ = arcpy.management.CalculateField(
        in_table=umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area_2_,
        field="procent",
        expression="[F_AREA]*100/ [area_circle]",
        expression_type="VB"
    )[0]

    # Łączenie wyników procentowych z tabelą buforów
    umts900_92_Buffer_z_procentami_ = arcpy.management.JoinField(
        in_data=umts900_92_Buffer,
        in_field="OBJ",
        join_table=umts900_92_Buffer_Area_Intersect_Select_Dissolve_Area_3_,
        join_field="OBJ",
        fields=["procent"]
    )[0]

    # Przecięcie warstw UMTS900 z TERYT 2017
    umts900_TERYT_Intersect = geobaza + f"\\{umts_suffix}_TERYT_Intersect"  # Dodanie suffixu do nazwy pliku
    arcpy.analysis.Intersect(
        in_features=[[umts900_92_Buffer_z_procentami_, ""], [teryt_2017, ""]],
        out_feature_class=umts900_TERYT_Intersect
    )

    # Statystyki z przeciętych wyników
    umts900_TERYT_Statistics = geobaza + f"\\{umts_suffix}_TERYT_Statistics"  # Dodanie suffixu do nazwy pliku
    arcpy.analysis.Statistics(
        in_table=umts900_TERYT_Intersect,
        out_table=umts900_TERYT_Statistics,
        statistics_fields=[["procent", "MEAN"], ["procent", "MIN"], ["procent", "MAX"]],
        case_field=["TERYT"]
    )

    # Zmiana nazw pól
    arcpy.management.AlterField(
        in_table=umts900_TERYT_Statistics,
        field="MEAN_procent",
        new_field_name="prawd_średnie",
        new_field_alias="prawd_średnie"
    )
    arcpy.management.AlterField(
        in_table=umts900_TERYT_Statistics,
        field="MIN_procent",
        new_field_name="prawd_min",
        new_field_alias="prawd_min"
    )
    arcpy.management.AlterField(
        in_table=umts900_TERYT_Statistics,
        field="MAX_procent",
        new_field_name="prawd_maks",
        new_field_alias="prawd_maks"
    )

    # Eksport wyników do CSV
    arcpy.conversion.TableToTable(
        in_rows=umts900_TERYT_Statistics,
        out_path=folder_z_wynikami,
        out_name=f"Prawdopodobienstwo_{umts_suffix}.csv"
    )


# Deklaracja zmiennych
teryt_2017 = "Ścieżka_do_pliku_TERYT_2017"
umts_900 = "Ścieżka_do_pliku_UMTS_900"
geobaza = "Ścieżka_do_geobazy"
dom_umts900_opl = "Ścieżka_do_pliku_DOM_UMTS900"
folder_z_wynikami = "Ścieżka_do_folderu_z_wynikami"
umts900_table_path = "Ścieżka_do_tabeli_UMTS900"
umts_suffix = "UMTS900"

# Wywołanie funkcji z możliwością zmiany dopisku
prawdopodobieAstwo22222322(teryt_2017, umts_900, geobaza, dom_umts900_opl, folder_z_wynikami, umts900_table_path,
                           umts_suffix)
