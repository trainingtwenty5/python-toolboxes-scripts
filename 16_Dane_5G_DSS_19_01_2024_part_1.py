import arcpy
import os

# nadpisywanie obiektow
arcpy.env.overwriteOutput = True

print('---------------------- Start - dane zasiegowe 5G DSS Part 1----------------------')
arcpy.env.workspace = r'D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1\2024_01_16_MV_Dane_zasiegowe_new.gdb'
# arcpy.env.workspace =
e2180 = r"D:\ArcGIS\projections\PUWG_92.prj"


# podaj ścieżkę do warstwy 5G DSS - ostateczny
path_warstwa_5G_DSS = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\ostateczne_5G_DSS_z_dnia_24_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024.gdb\DOM_DSS_OPL_20240101_50m_rozdmuchana_v2_ostateczna_25_01_2024_edycja'

# podaj ścieżkę do warstwy 5G DSS - normalne
#path_warstwa_5G_DSS = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Normalne.gdb\DOM_DSS_OPL_20240101_50m_LOC_OBJ'
# podaj ścieżkę do warstwy 5G DSS - rozrposzone
#path_warstwa_5G_DSS = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Rozproszone.gdb\DOM_DSS_OPL_20240101_50m_rozdmuchana_LOC_OBJ'


# ściećka gdzie zapisać joina - ostateczny
output_join = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\ostateczne_5G_DSS_z_dnia_24_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024\Ostateczny_5G_DSS_25_01_2024.gdb'

# ściećka gdzie zapisać joina - normalne
#output_join = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Normalne.gdb'
# ściećka gdzie zapisać joina - rozrposzone
#output_join = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Rozproszone.gdb'

# czytamy wszystkie listy lte ale bez 2100

#lista_LTE = arcpy.ListFeatureClasses('*M_LTE800*') + arcpy.ListFeatureClasses('*M_LTE900*') + arcpy.ListFeatureClasses('*M_LTE1800*') + arcpy.ListFeatureClasses('*M_LTE2600*')
lista_LTE = arcpy.ListFeatureClasses('*M_LTE800*') + arcpy.ListFeatureClasses('*M_LTE1800*') + arcpy.ListFeatureClasses('*M_LTE2600*')
# lista_LTE =  arcpy.ListFeatureClasses('*M_LTE900*')
# print(lista_LTE)
n = -1

# Lista przechowująca wyniki AddJoin
lista_wynikow_AddJoin = []

lista_LTE_LOC_OBJ = []
for x in lista_LTE:
    n += 1
    print('\n')
    print('---------------Warstwa---------------')
    print(x)

    # pole -- LOC_OBJ -- zeby mogl się po czym polaczyć
    fields = arcpy.ListFields(x,'*LOC_OBJ*')


    for field in fields:
        lista_LTE_LOC_OBJ.append(field.name)
        # print(f"{field.name} has a type of {field.type} with a length of {field.length}")
        # print(n)

    #     print('Lista dla pola do łączenia się - potrzebne do Joina')
    #     print(lista_LTE_LOC_OBJ)
    #     #Łączymy po kolei kaązdą LTE do
    #     print('Path do wyniku:')
    output_feature_class_join = fr'{output_join}\\{lista_LTE[n]}_join'
    #     print(output_feature_class_join)

    print('---------------Pole------------------pole_LOC_OBJ---------------')
    pole_LOC_OBJ = lista_LTE_LOC_OBJ[n]
    print(pole_LOC_OBJ)
    print('\n')

    # print("{}".format(pole_LOC_OBJ))
    print('---------------WEJSCIE DO AddJoin---------------')
    print(lista_LTE[n])
    print(pole_LOC_OBJ)
    print(path_warstwa_5G_DSS)
    print("LOC_OBJ")

    # dobry przyklad dla lte 900
    # arcpy.management.AddJoin("OPL_DOM_LTE900_Eo202312_MV", "lcell_20231231_Merge_LOC_OBJ", "DOM_DSS_OPL_20240101_25m", "LOC_OBJ", "KEEP_COMMON", "NO_INDEX_JOIN_FIELDS")
    wynik_0 = arcpy.management.AddJoin(path_warstwa_5G_DSS, "LOC_OBJ", lista_LTE[n], pole_LOC_OBJ)

    # Dodajemy obiekt Layer do listy wyników AddJoin
    lista_wynikow_AddJoin.append(wynik_0)

# Uzyskujemy listę ścieżek do danych wynikowych z obiektów Layer
# lista_sciezek_wynikow_AddJoin = [layer.dataSource for layer in lista_wynikow_AddJoin]


# Uzyskujemy listę ścieżek do danych wynikowych z obiektów Result
lista_sciezek_wynikow_AddJoin = [wynik.getOutput(0) for wynik in lista_wynikow_AddJoin]
#ostateczny
output_union = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\ostateczne_5G_DSS_z_dnia_24_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024\Ostateczny_5G_DSS_25_01_2024.gdb\DOM_DSS_OPL_20240101_50m_rozdmuchana_v2_ostateczna_25_01_2024_edycja_Union'
#normalna
# = r"D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Normalne.gdb\DOM_DSS_OPL_20240101_50m_LOC_OBJ_Union"
#rozdmychana
#output_union = r"D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Rozproszone.gdb\DOM_DSS_OPL_20240101_50m_rozdmuchana_LOC_OBJ_Union"


print('\n')
print('lista - lista_sciezek_wynikow_AddJoin: - można sprawdzić ilościowo czy jest tyle ile ma być')
print(lista_sciezek_wynikow_AddJoin)
# Przekazujemy listę ścieżek do danych wynikowych jako wejście do Union
wynik_union = arcpy.analysis.Union(lista_sciezek_wynikow_AddJoin, output_union, "NO_FID", None, "GAPS")
print('wynik_union')

#sql = "OPL_DOM_LTE800_Eo202312_MV_lcell_20231231_Merge_LOC_OBJ IS NULL And OPL_DOM_LTE900_Eo202312_MV_lcell_20231231_Merge_LOC_OBJ IS NULL And OPL_DOM_LTE1800_Eo202312_MV_lcell_20231231_Merge_LOC_OBJ IS NULL And OPL_DOM_LTE2600_Eo202312_MV_lcell_20231231_Merge_LOC_OBJ IS NULL"
sql = "OPL_DOM_LTE800_Eo202312_MV_lcell_20231231_Merge_LOC_OBJ IS NULL And OPL_DOM_LTE1800_Eo202312_MV_lcell_20231231_Merge_LOC_OBJ IS NULL And OPL_DOM_LTE2600_Eo202312_MV_lcell_20231231_Merge_LOC_OBJ IS NULL"
wynik_selection = arcpy.management.SelectLayerByAttribute(wynik_union, "NEW_SELECTION", sql, None)
print('wynik_selection')

#ostateczny
output_wynik = r"D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\ostateczne_5G_DSS_z_dnia_24_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024\Ostateczny_5G_DSS_25_01_2024.gdb\Po_polaczeniu_wszystkich_LTE_25_01_2024"

#normalna
#output_wynik = r"D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Normalne.gdb\Po_polaczeniu_wszystkich_LTE_22_01_2024"
#rozdmychana

#output_wynik = r"D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Rozproszone.gdb\Po_polaczeniu_wszystkich_LTE_22_01_2024_rozdmuchana"
arcpy.env.outputCoordinateSystem = e2180
arcpy.management.CopyFeatures(wynik_selection, output_wynik)

print(f'koniec - done')


# 5G DSS - TO SAMO CO WYŻEJ ALE ZROBIONE DLA NARZĘDZIA SKRYPTU#############################################################################################################################################################################################################################################
#             arcpy.env.overwriteOutput = True
#             c = arcpy.env.workspace = parameters[9].valueAsText
#             arcpy.AddMessage(f'Ścieżka do wybrania dominance LTE w celu utworzenia - 5G DSS: {c}')
#             e2180 = parameters[4].valueAsText
#             arcpy.AddMessage(f'e2180: {e2180}')
#
#
#             # Ścieżka do warstwy 5G DSS
#             path_warstwa_5G_DSS = parameters[18].valueAsText
#             arcpy.AddMessage(f'Dane wejsciowe 5G DSS: {path_warstwa_5G_DSS}')
#             # ściećka do zapisu joina
#             arcpy.env.overwriteOutput = True
#             output_join = parameters[19].valueAsText
#             arcpy.AddMessage(f'Ścieżka do zapisu joina 5G DSS: {output_join}')
#
#
#
#
#             lista_LTE = arcpy.ListFeatureClasses('*M_LTE800*') + arcpy.ListFeatureClasses('*M_LTE1800*') + arcpy.ListFeatureClasses('*M_LTE2600*')
#             arcpy.AddMessage(f'lista LTE do stworzenia 5G DSS: {lista_LTE}')
#
#             # Lista przechowująca wyniki AddJoin
#             lista_wynikow_AddJoin = []
#             lista_LTE_LOC_OBJ = []
#             n = -1
#             #pętla nr 1
#             for x in lista_LTE:
#                 n += 1
#
#                 arcpy.AddMessage('---------------Warstwa---------------')
#                 arcpy.AddMessage(x)
#
#                 # pole -- LOC_OBJ -- zeby mogl się po czym polaczyć
#                 fields = arcpy.ListFields(x,'*LOC_OBJ*')
#
#                 #pętla nr 2
#                 for field in fields:
#                     #wyciagamy tylko loc_obj - z warstw - lte
#                     lista_LTE_LOC_OBJ.append(field.name)
#
#
#
#
#                 #Jesteś w pętli nr 1
#                 arcpy.AddMessage('---------------Parametry wejsciowe do AddJoin---------------')
#                 arcpy.AddMessage(f'parametr 1: {path_warstwa_5G_DSS}')
#                 arcpy.AddMessage(f'parametr 2: To jest tekst - LOC_OBJ')
#                 arcpy.AddMessage(f'parametr 3: {lista_LTE[n]}')
#                 arcpy.AddMessage(f'parametr 4: {lista_LTE_LOC_OBJ[n]}')
#                 wynik_0 = arcpy.management.AddJoin(path_warstwa_5G_DSS, "LOC_OBJ", lista_LTE[n], lista_LTE_LOC_OBJ[n])
#                 arcpy.AddMessage('---------------done - AddJoin---------------')
#
#                 # output_join =  D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\ostateczne_5G_DSS_z_dnia_24_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024_new.gdb
#                 output_feature_class_join = fr'{output_join}'
#                 output_feature_class_join_name = fr'{lista_LTE[n]}_join'
#                 arcpy.AddMessage(f'output_feature_class_join: {output_feature_class_join}\{lista_LTE[n]}_join')
#                 arcpy.conversion.FeatureClassToFeatureClass(wynik_0, output_feature_class_join, output_feature_class_join_name)
#
#
#                 # Dodajemy obiekt Layer do listy wyników AddJoin
#                 lista_wynikow_AddJoin.append(wynik_0)
#
#
#             # Uzyskujemy listę ścieżek do danych wynikowych z obiektów Result
#             lista_sciezek_wynikow_AddJoin = [wynik.getOutput(0) for wynik in lista_wynikow_AddJoin]
#
#
#             arcpy.env.overwriteOutput = True
#             output_union = parameters[20].valueAsText
#             arcpy.AddMessage(f'Ścieżka do zapisu union 5G DSS: {output_union}')
#
#             #arcpy.AddMessage('lista - lista_sciezek_wynikow_AddJoin: - można sprawdzić ilościowo czy jest tyle ile ma być')
#
#             # Przekazujemy listę ścieżek do danych wynikowych jako wejście do Union
#             arcpy.analysis.Union(lista_sciezek_wynikow_AddJoin, output_union, "NO_FID", None, "GAPS")
#             arcpy.AddMessage('wynik_union')
#
#             #sql = "OPL_DOM_LTE800_Eo202312_MV_lcell_20231231_Merge_LOC_OBJ IS NULL And OPL_DOM_LTE900_Eo202312_MV_lcell_20231231_Merge_LOC_OBJ IS NULL And OPL_DOM_LTE1800_Eo202312_MV_lcell_20231231_Merge_LOC_OBJ IS NULL And OPL_DOM_LTE2600_Eo202312_MV_lcell_20231231_Merge_LOC_OBJ IS NULL"
#             #sql = "OPL_DOM_LTE800_Eo202312_MV_LOC_OBJ IS NULL And OPL_DOM_LTE1800_Eo202312_MV_LOC_OBJ IS NULL"
#             sql = ""
#             if len(lista_LTE[:]) == 1:
#                 sql = f"{lista_LTE[0]}_LOC_OBJ IS NULL"
#                 arcpy.AddMessage('1 warstwa lte')
#             elif len(lista_LTE[:]) == 2:
#                 sql = f"{lista_LTE[0]}_LOC_OBJ IS NULL And {lista_LTE[1]}_LOC_OBJ IS NULL"
#                 arcpy.AddMessage('2 warstwa lte')
#             elif len(lista_LTE[:]) == 3:
#                 sql = f"{lista_LTE[0]}_LOC_OBJ IS NULL And {lista_LTE[1]}_LOC_OBJ And {lista_LTE[2]}_LOC_OBJ"
#                 arcpy.AddMessage('3 warstwa lte')
#
#             arcpy.AddMessage(f'sql: {sql}')
#             wynik_selection = arcpy.management.SelectLayerByAttribute(output_union, "NEW_SELECTION", sql)
#             #KEEP_COMMON oznacza, że połączenie zachowa tylko rekordy, które są wspólne dla obu warstw danych
#             #join_type='KEEP_COMMON'
#             #wynik_selection = arcpy.management.SelectLayerByAttribute(output_union, "NEW_SELECTION", sql, invert_where_clause=True)
#
#             arcpy.AddMessage('wynik_selection')
#
#             #Wynik 5G DSS
#             arcpy.env.overwriteOutput = True
#             output_wynik = parameters[21].valueAsText
#             arcpy.AddMessage(f'Ścieżka do zapisu wyniku 5G DSS: {output_wynik}')
#
#             arcpy.env.outputCoordinateSystem = e2180
#             arcpy.management.CopyFeatures(wynik_selection, output_wynik)
#
#
#             arcpy.env.workspace = output_join
#
#             #######################Kradnie ostatni element z ciagu output_wynik############################
#             # Pobierz nazwę pliku z output_wynik
#             nazwa_pliku = os.path.basename(output_wynik)
#
#             # Utwórz filtr dla ostatniego elementu
#             filtr = f'{nazwa_pliku}'
#             arcpy.AddMessage(f'Skrada ostatni element: {filtr}')
#             #######################Kradnie ostatni element z ciagu output_wynik############################
#
#             lista_LTE_marge = arcpy.ListFeatureClasses('*_join*') + arcpy.ListFeatureClasses(filtr)
#
#             arcpy.AddMessage(f'Lista do stworzenia maski: {lista_LTE_marge}')
#
#
#             #ŁĄCZENIE POLIGONÓW -  ostateczny
#             #output_Merge = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\ostateczne_5G_DSS_z_dnia_24_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024_new.gdb\e1_Maska_25_01_2024'
#             output_Merge = parameters[22].valueAsText
#
#             #arcpy.management.Merge("OPL_DOM_LTE800_Eo202312_MV_join;OPL_DOM_LTE900_Eo202312_MV_join;OPL_DOM_LTE1800_Eo202312_MV_join;OPL_DOM_LTE2600_Eo202312_MV_join;Po_polaczeniu_wszystkich_LTE_19_01_2024", output_Merge)
#             arcpy.management.Merge(lista_LTE_marge, output_Merge)
#
#             #uniwarsalna masaka - zmiana
#             country_border_and_sea_buffer_cala_polska = parameters[23].valueAsText
#             # CLIP Maski do country_border_and_sea_buffer_cala_polska -  ostateczny
#             output_clip = parameters[24].valueAsText
#
#             arcpy.AddMessage(f'Parametr 1 do Clip: {output_Merge}')
#             arcpy.AddMessage(f'Parametr 2 do Clip: {country_border_and_sea_buffer_cala_polska}')
#             arcpy.AddMessage(f'Parametr 3 do Clip: {output_clip}')
#
#             arcpy.analysis.Clip(output_Merge, country_border_and_sea_buffer_cala_polska, output_clip, None)
#
#             arcpy.AddMessage('---------------------- koniec CZESCI VI - dane zasiegowe 5G DSS ----------------------')


# # zmien_nazwy_pol_na_aliasy #############################################################################################################################################################################################################################################
#         zmien_nazwy_pol_na_aliasy(parameters[18].valueAsText)