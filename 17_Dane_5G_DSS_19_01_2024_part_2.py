# brakuje
# OPL_DOM_LTE800_Eo202312_MV.lcell_20231231_Merge_LOC_OBJ IS NULL
# And OPL_DOM_LTE900_Eo202312_MV.lcell_20231231_Merge_LOC_OBJ IS NULL
# And OPL_DOM_LTE1800_Eo202312_MV.lcell_20231231_Merge_LOC_OBJ IS NULL
# And OPL_DOM_LTE2600_Eo202312_MV.lcell_20231231_Merge_LOC_OBJ IS NULL

#

# TO TRZEBA DOPISAĆ I TO BĘDZIEMY DODAWAĆ DO WYNIKU TEGO CO TUTAJ NA DOLE, SPRAWDZAMY TAM, CZY JAKIEŚ DOMINANCE NIE ZOSTAŁY BY PRZYPADKIEM WYRZUCONE
# Gdy dodamy wszyskie inne dominance lte BEZ 2100

import arcpy
import os



# nadpisywanie obiektow
arcpy.env.overwriteOutput = True

print('---------------------- Start - dane zasiegowe 5G DSS----------------------')
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

lista_LTE = arcpy.ListFeatureClasses('*M_LTE800*') + arcpy.ListFeatureClasses('*M_LTE1800*') + arcpy.ListFeatureClasses('*M_LTE2600*')
#lista_LTE = arcpy.ListFeatureClasses('*M_LTE800*') + arcpy.ListFeatureClasses('*M_LTE900*') + arcpy.ListFeatureClasses('*M_LTE1800*') + arcpy.ListFeatureClasses('*M_LTE2600*')
# lista_LTE =  arcpy.ListFeatureClasses('*M_LTE900*')
# print(lista_LTE)
n = -1

lista_LTE_LOC_OBJ = []
for x in lista_LTE:
    n += 1
    print('\n')
    print('---------------Warstwa---------------')
    print(x)

    # Czytanie listy zeby odszukać 2 rekord czyli pole -- LOC_OBJ -- zeby mogl się po czym polaczyć
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
    wynik_1 = arcpy.management.AddJoin(lista_LTE[n], pole_LOC_OBJ, path_warstwa_5G_DSS, "LOC_OBJ", join_type='KEEP_COMMON')


    #     print(f'wykonanie Joina dla: {lista_LTE[n]}_join')
    arcpy.env.outputCoordinateSystem = e2180
    arcpy.management.CopyFeatures(wynik_1, output_feature_class_join)
    print(f'Done dla: {lista_LTE[n]}_join')
    print('\n')
print(f'JOINY TRZEBA USUNĄĆ DLA WSZYSTKICH WARSTW LTE')

# TUTAJ TRZEBA POPRAWIĆ I DODAĆ WARSTWĘ  Po_polaczeniu_wszystkich_LTE_19_01_2024
# TUTAJ TRZEBA POPRAWIĆ I DODAĆ WARSTWĘ  Po_polaczeniu_wszystkich_LTE_19_01_2024
# TUTAJ TRZEBA POPRAWIĆ I DODAĆ WARSTWĘ  Po_polaczeniu_wszystkich_LTE_19_01_2024
# TUTAJ TRZEBA POPRAWIĆ I DODAĆ WARSTWĘ  Po_polaczeniu_wszystkich_LTE_19_01_2024
# TUTAJ TRZEBA POPRAWIĆ I DODAĆ WARSTWĘ  Po_polaczeniu_wszystkich_LTE_19_01_2024

arcpy.env.workspace = output_join
lista_LTE = arcpy.ListFeatureClasses('*_join*') + arcpy.ListFeatureClasses('*Po_polaczeniu_wszystkich*')
print(lista_LTE)


#ŁĄCZENIE POLIGONÓW -  ostateczny
output_Merge = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\ostateczne_5G_DSS_z_dnia_24_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024\Ostateczny_5G_DSS_25_01_2024.gdb\e1_Maska_25_01_2024'

#ŁĄCZENIE POLIGONÓW - normalne
#output_Merge = r"D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Normalne.gdb\e1_Maska_22_01_2024"

#ŁĄCZENIE POLIGONÓW - rozdmuchane
#output_Merge = r"D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Rozproszone.gdb\e1_Maska_22_01_2024_rozdmuchana"
#arcpy.management.Merge("OPL_DOM_LTE800_Eo202312_MV_join;OPL_DOM_LTE900_Eo202312_MV_join;OPL_DOM_LTE1800_Eo202312_MV_join;OPL_DOM_LTE2600_Eo202312_MV_join;Po_polaczeniu_wszystkich_LTE_19_01_2024", output_Merge)
wynik_Merge = arcpy.management.Merge(lista_LTE, output_Merge)
print('wynik_Merge')
print('\n')

#uniwarsalna masaka - przed zmianą path
#country_border_and_sea_buffer_cala_polska = r"D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Rozproszone.gdb\country_border_and_sea_buffer_cala_polska"
#uniwarsalna masaka - zmiana
country_border_and_sea_buffer_cala_polska = r"D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\porownanie_danych_5G_DSS_22012024\Rozproszone.gdb\country_border_and_sea_buffer_cala_polska"

# CLIP Maski do country_border_and_sea_buffer_cala_polska -  ostateczny
output_clip = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\ostateczne_5G_DSS_z_dnia_24_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024\Ostateczny_5G_DSS_25_01_2024.gdb\e2_Maska_Clip_25_01_2024'

# CLIP Maski do country_border_and_sea_buffer_cala_polska - normalne
#output_clip = r"D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Normalne.gdb\e2_Maska_Clip_22_01_2024"
# CLIP Maski do country_border_and_sea_buffer_cala_polska  - rozdmuchane
#output_clip = r"D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_20240122\porownanie_danych_5G_DSS_22012024\Rozproszone.gdb\e2_Maska_Clip_22_01_2024_rozdmuchana"
arcpy.analysis.Clip(wynik_Merge, country_border_and_sea_buffer_cala_polska, output_clip, None)
print('wynik_Clip')

print(f'koniec - done')