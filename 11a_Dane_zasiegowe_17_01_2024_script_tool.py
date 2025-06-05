# -*- coding: utf-8 -*-

import arcpy
import os


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Tool"
        self.alias = "Tool"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Dane zasiegowe by Daniel Buchar"
        self.description = "Dane zasiegowe"
        self.canRunInBackground = False


# getParameterInfo #############################################################################################################################################################################################################################################
    def getParameterInfo(self):
        """Define parameter definitions"""

        param0 = arcpy.Parameter(
            displayName="Ścieżka do folderu z danymi zasięgowymi - LTE, UMTS, GSM (Odszukaj - Folder - Input)",
            name="Folder_z_danymi",
            datatype="DEFolder",
            parameterType="Optional",
            direction="Input"
        )

        param1_4 = arcpy.Parameter(
            displayName="PUWG 92 (Odszukaj - File prj - Input)",
            name="PUWG_92",
            datatype="DEFile",
            parameterType="Optional",
            direction="Input",

        )

        param2_5 = arcpy.Parameter(
            displayName="Tabela - LTE (Odszukaj lcell - Feature class - Input)",
            name="join_table_lcelL",
            datatype="DETable",
            parameterType="Optional",
            direction="Input"
        )

        param3_6 = arcpy.Parameter(
            displayName="Tabela - UMTS (Odszukaj wcell - Feature class - Input)",
            name="join_table_wcell",
            datatype="DETable",
            parameterType="Optional",
            direction="Input"
        )

        param4_7 = arcpy.Parameter(
            displayName="Tabela - GSM (Odszukaj cell - Feature class - Input)",
            name="join_table_cell",
            datatype="DETable",
            parameterType="Optional",
            direction="Input"
        )


        param5_8 = arcpy.Parameter(
            displayName="Geobaza info (Utwórz nową - Geodatabase - Input - Backup)",
            name="output_info",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )

        param6_9 = arcpy.Parameter(
            displayName="Geobaza MV (Utwórz nową - Geodatabase - Input - Result)",
            name="output_MV",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )



        #param11.defaultEnvironmentName = "workspace"

#         param0.value = r'D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\Dane'
#         param0.value = r'D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\Dane'
#
#         param1_4.value = r'D:\ArcGIS\projections\PUWG_92.prj'
#
#         param2_5.value = r'D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\mv.gdb\lcell_20231231_Merge'
#         param3_6.value = r'D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\mv.gdb\wcell_20231231_Merge'
#         param4_7.value = r'D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\mv.gdb\cell_20231231_Merge'
#
#         param5_8.value = r'D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_2_styczen_2024\2024_02_09_info_Dane_zasiegowe_new_new.gdb'
#         param6_9.value = r'D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_2_styczen_2024\2024_02_09_MV_Dane_zasiegowe_new_new.gdb'



        param_lcell_7_1 = arcpy.Parameter(
            displayName="Dominance - LTE",
            name="Oblicz_LTE",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        param_wcell_8_2 = arcpy.Parameter(
            displayName="Dominance - UMTS",
            name="Oblicz_UMTS",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        param_cell_9_3 = arcpy.Parameter(
            displayName="Dominance - GSM",
            name="Oblicz_GSM",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        param_przeciazenia_10 = arcpy.Parameter(
            displayName="Przeciazenia (warunek: dominance w geobazie MV oraz połączenie do geobaza SDE)",
            name="Oblicz_przeciazenia",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        param11 = arcpy.Parameter(
            displayName="Geobaza SDE (Odszukaj - SDE Geodatabase - Input)",
            name="Geobaza_SDE",
            datatype="DEWorkspace",
            parameterType="Optional",
            direction="Input"
        )

        #param11.value = r'D:\ArcGIS\ArcGIS_baza_SDE\Admin_SDE.sde'

        param12 = arcpy.Parameter(
            displayName="Piramidy oraz geobaze w układzie 3857",
            name="Piramidy",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        param13 = arcpy.Parameter(
            displayName="Ścieżka do folderu z istniejącymi rastrami (Odszukaj - Folder - Input)",
            name="Folder_z_rastrami",
            datatype="DEFolder",
            parameterType="Optional",
            direction="Input"
        )

        #param13.value = r'D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\Dane\paczka_opl_eo202312'

        param14 = arcpy.Parameter(
            displayName="Geobaza 3857 (Utwórz nową - Geodatabase - Input)",
            name="geodatabase_3857",
            datatype="DEWorkspace",
            parameterType="Optional",
            direction="Input"
        )

        #param14.value = r'D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\2024_01_16_MV_Dane_zasiegowe_3857_new.gdb'

# do skasowania
#         param15 = arcpy.Parameter(
#             displayName="Folder dla rastrów wynikowych (Odszukaj - Folder - Input)",
#             name="rastry_wynik",
#             datatype="DEFolder",
#             parameterType="Optional",
#             direction="Input"
#         )
#
#         param15.value = r'D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\Folder_piramidy'

        param16 = arcpy.Parameter(
            displayName="WGS 1984 Web Mercator 3857 (Odszukaj - File prj)",
            name="uklad_3857",
            datatype="DEFile",
            parameterType="Optional",
            direction="Input"
        )

        #param16.value = r'D:\ArcGIS\projections\WGS 1984 Web Mercator (auxiliary sphere).prj'

        param17 = arcpy.Parameter(
            displayName="Dominance - DSS",
            name="dss",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )


#         param18 = arcpy.Parameter(
#             displayName="Dane wejsciowe dominance 5G DSS (Feature class - Input)",
#             name="path_warstwa_5G_DSS",
#             datatype="GPFeatureLayer",
#             parameterType="Required",
#             direction="Input")

        param18 = arcpy.Parameter(
            displayName="Ścieżka do folderu z danymi zasięgowymi - 5G DSS (Odszukaj - Folder - Input)",
            name="Folder_z_danymi_dss",
            datatype="DEFolder",
            parameterType="Optional",
            direction="Input"
        )

        #param18.value = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\Dane\dom_DSS_eo202312'

        param19 = arcpy.Parameter(
            displayName="Tabela - 5G DSS (Odszukaj gcell - Feature class - Input)",
            name="join_table_gell",
            datatype="DETable",
            parameterType="Optional",
            direction="Input"
        )
        #param19.value = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\braki\braki.gdb\gcell_20231231'


        param20 = arcpy.Parameter(
            displayName="Ścieżka do zapisu Maski - 5G DSS (Utwórz nową - Feature class - Output)",
            name="output_marge_DSS",
            datatype="DEWorkspace",
            parameterType="Optional",
            direction="Output"
        )

        #param20.value = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\ostateczne_5G_DSS_z_dnia_24_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024_new.gdb\Maska_5G_DSS_maska'

        param21 = arcpy.Parameter(
            displayName="Ścieżka country_border_and_sea_buffer_cala_polska (Odszukaj - Feature class - Input)",
            name="output_wynik_dss",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input"
        )

        #country_border_and_sea_buffer_cala_polska = r"D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\ostateczne_5G_DSS_z_dnia_24_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024_new.gdb\country_border_and_sea_buffer_cala_polska"
        #param21.value = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\ostateczne_5G_DSS_z_dnia_24_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024_new.gdb\country_border_and_sea_buffer_cala_polska'


        param22 = arcpy.Parameter(
            displayName="Dominance - 5G",
            name="Oblicz_5G",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        param23 = arcpy.Parameter(
            displayName="Ścieżka do folderu z danymi zasięgowymi - 5G (Odszukaj - Folder - Input)",
            name="Folder_z_danymi_5G",
            datatype="DEFolder",
            parameterType="Optional",
            direction="Input"
        )

        #param23.value = r'D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\Dane\dom_DSS_eo202312'

        param24 = arcpy.Parameter(
            displayName="Tabela - 5G (Odszukaj gcell - Feature class - Input)",
            name="join_table_gell_5G",
            datatype="DETable",
            parameterType="Optional",
            direction="Input"
        )


        param_lcell_7_1.value = True  # Domyślnie niezaznaczony
        param_wcell_8_2.value = True
        param_cell_9_3.value = True
        param_przeciazenia_10.value = True
        param12.value = True
        param17.value = True
        param22.value = True

#         param_lcell_7_1.value = False  # Domyślnie niezaznaczony
#         param_wcell_8_2.value = False
#         param_cell_9_3.value = False
#         param_przeciazenia_10.value = False
#         param12.value = False
#         param17.value = True
#         param22.value = True

        #pierwsza, a jesli sa dwie to druga cyfra mowi nam o kolejnoci parametru
        params = [param0, param_lcell_7_1, param_wcell_8_2, param_cell_9_3, param1_4, param2_5, param3_6, param4_7, param5_8, param6_9, param_przeciazenia_10, param11, param12, param13, param14, param16, param17, param18, param19, param20, param21, param22, param23, param24]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return



# updateMessages #############################################################################################################################################################################################################################################
    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""



        # Pobranie wartości z checkboxów
        param_lcell_77 = parameters[1].value
        param_wcell_88 = parameters[2].value
        param_cell_99 = parameters[3].value
        param_przeciazenia_1010 = parameters[10].value
        param_1212 = parameters[12].value
        param_gcell_2525 = parameters[16].value
        param_2222 = parameters[21].value

        # Sprawdzenie, czy wszystkie opcje zostały wybrane
        if param_lcell_77 and param_wcell_88 and param_cell_99 and param_przeciazenia_1010 and param_1212 and param_gcell_2525 and param_2222:
            # Jeśli wszystkie opcje są zaznaczone, nie ustawiaj żadnych komunikatów
            for param in [parameters[1], parameters[2], parameters[3], parameters[10], parameters[12], parameters[16], parameters[21]]:
                param.clearMessage()
        else:
            # Sprawdzanie pojedynczych opcji i ustawianie odpowiednich komunikatów
            for param in [parameters[1], parameters[2], parameters[3], parameters[10], parameters[12], parameters[16], parameters[21]]:
                if param.value:
                    param.setWarningMessage(f"Opcja {param.displayName} została wybrana.")
                else:
                    param.clearMessage()




        return




# execute #############################################################################################################################################################################################################################################
    def execute(self, parameters, messages):
        """The source code of the tool."""

# zmien_nazwy_pol_na_aliasy #############################################################################################################################################################################################################################################
#         def zmien_nazwy_pol_na_aliasy(lista_warstw):
# #             # Ustawia środowisko robocze na wskazaną geobazę
# #             arcpy.env.workspace = geobaza
# #             # Pobiera listę wszystkich warstw w geobazie
# #             lista_warstw = arcpy.ListFeatureClasses()
#
#             # Przechodzi przez każdą warstwę
#             for warstwa in lista_warstw:
#                 # Pobiera listę pól i ich aliasów
#                 pola = [pole.name for pole in arcpy.ListFields(warstwa)]
#
#                 aliasy = {pole.name: pole.aliasName for pole in arcpy.ListFields(warstwa)}
#                 #arcpy.AddMessage('aliasy')
#                 #arcpy.AddMessage(aliasy)
#                 # Zmienia nazwy pól na takie same jak aliasy
#                 for pole in pola:
#                     nazwa_aliasu = aliasy.get(pole)
#                     # Ensure the new field name is not "OBJECTID" or any other reserved name
#                     if nazwa_aliasu and pole != nazwa_aliasu and nazwa_aliasu.upper() != "OBJECTID" and nazwa_aliasu.upper() != "loc_name":
#                         arcpy.management.AlterField(warstwa, pole, new_field_name=nazwa_aliasu)

        def zmien_nazwy_pol_na_aliasy(lista_warstw):
            for warstwa in lista_warstw:
                pola = [pole.name for pole in arcpy.ListFields(warstwa)]
                aliasy = {pole.name: pole.aliasName for pole in arcpy.ListFields(warstwa)}
                istniejace_nazwy_pol = set(pola)  # Zbiór istniejących nazw pól

                for pole in pola:
                    nazwa_aliasu = aliasy.get(pole)
                    if nazwa_aliasu and pole != nazwa_aliasu and nazwa_aliasu.upper() != "OBJECTID":
                        # Sprawdź, czy nazwa aliasu już istnieje i zmień ją, jeśli to konieczne
                        nowa_nazwa = nazwa_aliasu
                        i = 1
                        while nowa_nazwa.upper() in istniejace_nazwy_pol:
                            nowa_nazwa = f"{nazwa_aliasu}_{i}"
                            i += 1
                        arcpy.management.AlterField(warstwa, pole, new_field_name=nowa_nazwa)
                        istniejace_nazwy_pol.add(nowa_nazwa.upper())  # Dodaj nową nazwę do zbioru

# DOMINANCE #############################################################################################################################################################################################################################################
       #arcpy.AddMessage('---------------------- Start - dane zasiegowe ----------------------')
        arcpy.env.overwriteOutput = True
        a = arcpy.env.workspace = parameters[0].valueAsText
        #arcpy.AddMessage(f'Folder_z_danymi: {a}')
        #e2180 = r"D:\ArcGIS\projections\PUWG_92.prj"
        e2180 = parameters[4].valueAsText
        #arcpy.AddMessage(f'PUWG_92: {e2180}')
        # Użyj Walk do rekurencyjnego przeglądania folderów i uzyskania plików SHP
        lista_1 = []
        lista_1UMTS = []
        lista_1GSM = []
        for folder, subfolders, files in arcpy.da.Walk(arcpy.env.workspace, datatype="FeatureClass"):
#             arcpy.AddMessage(f'folder: {folder}')
#             arcpy.AddMessage(f'subfolders: {subfolders}')
#             arcpy.AddMessage(f'files: {files}')
            for file in files:
                if 'LTE' in file:
                    lista_1.append(os.path.join(folder, file))
                # UMTS2100 co miesiac ale przelicza sie zawsze
                if 'UMTS' in file:
                    lista_1UMTS.append(os.path.join(folder, file))
                # co kwartal
                if 'GSM' in file:
                    lista_1GSM.append(os.path.join(folder, file))



#         arcpy.AddMessage('---------------------- CZESCI 0 - zmiennych ----------------------')
#
        join_table = parameters[5].valueAsText
#         arcpy.AddMessage(f'join_table_lcelL: {join_table}')
#
        join_table_wcell = parameters[6].valueAsText
#         arcpy.AddMessage(f'join_table_wcell: {join_table_wcell}')
#
        join_table_cell = parameters[7].valueAsText
#         arcpy.AddMessage(f'join_table_cell: {join_table_cell}')
#
        join_table_gcell = parameters[18].valueAsText
#         arcpy.AddMessage(f'join_table_gcell_5G_DSS: {join_table_gcell}')
#
#

        join_table_5G_gcell = parameters[23].valueAsText
#         arcpy.AddMessage(f'join_table_gcell_5G: {join_table_gcell}')
#
#

        output_info = parameters[8].valueAsText
#         arcpy.AddMessage(f'output_info: {output_info}')
#
        output_MV = parameters[9].valueAsText
#         arcpy.AddMessage(f'output_MV: {output_MV}')
#
#         arcpy.AddMessage('---------------------- KONIEC CZESCI 0 - zmiennych ----------------------')





        param_lcell_77 = parameters[1].value
        param_wcell_88 = parameters[2].value
        param_cell_99 = parameters[3].value
        param_przeciazenia_1010 = parameters[10].value
        param_1212 = parameters[12].value
        param_1717 = parameters[16].value
        param_2222 = parameters[21].value

# DOMINANCE LTE #############################################################################################################################################################################################################################################
        pola_do_usuniecia = []
        nazwy_plikow = []
        n = -1
        if param_lcell_77:
            arcpy.AddMessage('---------------------- CZESCI I - LTE ----------------------')

            for sciezka in lista_1:
                nazwa_pliku = os.path.basename(sciezka)
                nazwa_bez_rozszerzenia, rozszerzenie = os.path.splitext(nazwa_pliku)
                nazwy_plikow.append(nazwa_bez_rozszerzenia)
                n += 1

                arcpy.management.AddField(lista_1[n], "objj1", "Long")
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------474')
                arcpy.management.CalculateField(lista_1[n], "objj1", '!LEGEND!', "PYTHON3")
                arcpy.AddMessage(f'-------------{lista_1[n]}------------------')
                arcpy.AddMessage(f'-------------------------------')
                # join_table = 'lcell_20231130_Merge'

                #wynik_1 = arcpy.management.AddJoin(lista_1[n], "objj1", join_table, "LCELL_OBJ")
                wynik_1 = arcpy.management.AddJoin(lista_1[n], "objj1", join_table, "LCELL_OBJ")


                #NOWE PODEJSCIE ALE TO NA STALE DODAWALO KOLUMNY DO WARSTWY SHP - pomijam to teraz
                #r"D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\Dane\paczka_opl_eo202312\OPL_DOM_LTE1800_Eo202312"
                #r"D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\mv.gdb\lcell_20231231_Merge"
                #zeby nie bral pozniej do kopiowania stringa
                #arcpy.management.JoinField(lista_1[n], "objj1", join_table, "LCELL_OBJ")


                # chcemy ja nazwyać, warstwy maja się nazywac same

                # print(f'{output}\\{nazwy_plikow[n]})')

                #output_feature_class_info = fr'{output_info}\{nazwy_plikow[n]}_info'

                output_feature_class_info = fr'{output_info}'
                output_feature_class_info_name = fr'{nazwy_plikow[n]}_info'



#                 arcpy.AddMessage(f'wynik_1: {wynik_1}')
#                 arcpy.AddMessage(f'output_info: {output_info}')
#                 arcpy.AddMessage(f'output_feature_class_info_name: {output_feature_class_info_name}')


                #arcpy.management.CopyFeatures(wynik_1, output_feature_class_info)
                #arcpy.management.CopyFeatures(lista_1[n], output_feature_class_info)

                arcpy.conversion.FeatureClassToFeatureClass(wynik_1, output_info, output_feature_class_info_name)


                output_feature_class_MV = fr'{output_MV}'
                output_feature_class_MV_name = fr'{nazwy_plikow[n]}_MV'

                arcpy.env.outputCoordinateSystem = e2180
                #arcpy.management.CopyFeatures(wynik_1, output_feature_class_MV)
                #arcpy.management.CopyFeatures(lista_1[n], output_feature_class_MV)


                arcpy.AddMessage(f'Warstwa: {wynik_1}')
#                 arcpy.AddMessage(f'output_feature_class_MV: {output_feature_class_MV}')
#                 arcpy.AddMessage(f'output_feature_class_MV_name: {output_feature_class_MV_name}')

                arcpy.conversion.FeatureClassToFeatureClass(wynik_1, output_feature_class_MV, output_feature_class_MV_name)



                path_output_feature_class_MV = fr'{output_feature_class_MV}\{nazwy_plikow[n]}_MV'
                #arcpy.AddMessage(f'path_output_feature_class_MV LTE: {path_output_feature_class_MV}')
                # Usuń pola bezpośrednio z warstwy źródłowej
#                 lista_2 = arcpy.ListFields(path_output_feature_class_MV)
#
#                 for x in lista_2:
#
#                     pola_do_usuniecia.append(x.name)
#                 arcpy.AddMessage(f'Wszystkie pola: {pola_do_usuniecia}')
#
#                 arcpy.AddMessage(f'Wyswietla rekordy do usuniecia w MV: {pola_do_usuniecia[2:12]}')
#                 arcpy.management.DeleteField(path_output_feature_class_MV, pola_do_usuniecia[2:12])
#                 pola_do_usuniecia = []

                # Lista pól, które chcemy zachować
                pola_do_zachowania = ['OBJECTID_1', 'Shape', 'LOC_OBJ', 'LOC_CODE', 'LSITE_NAME', 'LSITE_OBJ', 'LSITE_ID', 'LCELL_NAME', 'LCELL_OBJ', 'LCELL_ID', 'NAME', 'PCI', 'Shape_Length', 'Shape_Area']

                # Pobierz listę wszystkich pól
                lista_pól = arcpy.ListFields(path_output_feature_class_MV)

                # Utwórz listę pól do usunięcia
                pola_do_usuniecia = []
                for pole in lista_pól:
                    if not any(fraza in pole.name for fraza in pola_do_zachowania):
                        pola_do_usuniecia.append(pole.name)

                # Wyświetl pola do usunięcia
                arcpy.AddMessage(f'Pola do usunięcia: {pola_do_usuniecia}')

                # Usuń wybrane pola
                if pola_do_usuniecia:
                    arcpy.management.DeleteField(path_output_feature_class_MV, pola_do_usuniecia)
                    #arcpy.AddMessage("Pola zostały usunięte.")
                else:
                    arcpy.AddMessage("Brak pól do usunięcia.")

                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------564')
                arcpy.AddMessage(f'Done: {nazwy_plikow[n]}_info')
                arcpy.AddMessage(f'Done: {nazwy_plikow[n]}_MV')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------')


            arcpy.AddMessage(f'---------------------- KONIEC - CZESCI I - LTE ----------------------')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')




# DOMINANCE UMTS #############################################################################################################################################################################################################################################
        d = -1
        nazwy_plikow_UMTS = []
        if param_wcell_88:
            arcpy.AddMessage('---------------------- CZESCI II - UMTS----------------------')

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


                output_feature_class_info = fr'{output_info}'
                output_feature_class_info_name = fr'{nazwy_plikow_UMTS[d]}_info'

                arcpy.AddMessage(f'Warstwa: {wynik_1}')
#                 arcpy.AddMessage(f'output_info: {output_info}')
#                 arcpy.AddMessage(f'output_feature_class_info_name: {output_feature_class_info_name}')
                #arcpy.management.CopyFeatures(wynik_1, output_feature_class_info)
                arcpy.conversion.FeatureClassToFeatureClass(wynik_1, output_info, output_feature_class_info_name)

                # print('UMTS - output_feature_class_info')
                #arcpy.AddMessage(output_feature_class_info)
                output_feature_class_MV = fr'{output_MV}'
                output_feature_class_MV_name = fr'{nazwy_plikow_UMTS[d]}_MV'
                # print('UMTS - output_feature_class_MV')
                #arcpy.AddMessage(output_feature_class_MV)


                arcpy.env.outputCoordinateSystem = e2180
                #arcpy.management.CopyFeatures(wynik_1, output_feature_class_MV)
                arcpy.conversion.FeatureClassToFeatureClass(wynik_1, output_feature_class_MV, output_feature_class_MV_name)

                # Usuń pola bezpośrednio z warstwy źródłowej
#                 lista_2 = arcpy.ListFields(output_feature_class_MV)
#                 for x in lista_2:
#                     pola_do_usuniecia.append(x.name)
#
#
#                 arcpy.AddMessage('Wyswietla rekordy do usuniecia w MV - UMTS')
#                 arcpy.AddMessage(pola_do_usuniecia[2:12])
#                 arcpy.management.DeleteField(output_feature_class_MV, pola_do_usuniecia[2:12])
#                 pola_do_usuniecia = []

                path_output_feature_class_MV = fr'{output_feature_class_MV}\{nazwy_plikow_UMTS[d]}_MV'
                #arcpy.AddMessage(f'path_output_feature_class_MV UMTS: {path_output_feature_class_MV}')

                # Lista pól, które chcemy zachować
                pola_do_zachowania1 = ['OBJECTID_1', 'Shape', 'LOC_NAME', 'LOC_OBJ', 'LOC_CODE', 'WSITE_NAME', 'WSITE_OBJ', 'WSITE_ID', 'WCELL_NAME', 'WCELL_OBJ', 'WCELL_CODE', 'LAC', 'BAND', 'BAND', 'PSC', 'Shape_Length', 'Shape_Area']


                # Pobierz listę wszystkich pól
                lista_pól1 = arcpy.ListFields(path_output_feature_class_MV)

                # Utwórz listę pól do usunięcia
                pola_do_usuniecia = []
                for pole in lista_pól1:
                    if not any(fraza in pole.name for fraza in pola_do_zachowania1):
                        pola_do_usuniecia.append(pole.name)

                # Wyświetl pola do usunięcia
                arcpy.AddMessage(f'Pola do usunięcia: {pola_do_usuniecia}')

                # Usuń wybrane pola
                if pola_do_usuniecia:
                    arcpy.management.DeleteField(path_output_feature_class_MV, pola_do_usuniecia)
                    arcpy.AddMessage("Pola zostały usunięte.")
                else:
                    arcpy.AddMessage("Brak pól do usunięcia.")

                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------663')
                arcpy.AddMessage(f'Done: {nazwy_plikow_UMTS[d]}_info')
                arcpy.AddMessage(f'Done: {nazwy_plikow_UMTS[d]}_MV')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------')


            arcpy.AddMessage('---------------------- KONIEC CZESCI II - UMTS----------------------')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')



# DOMINANCE GSM #############################################################################################################################################################################################################################################
        g = -1
        nazwy_plikow_GSM = []
        if param_cell_99:
            arcpy.AddMessage('---------------------- CZESCI III - GSM ----------------------')
            for sciezka in lista_1GSM:
                nazwa_pliku = os.path.basename(sciezka)
#                 print('GSM - nazwa_pliku')
#                 print(nazwa_pliku)
                nazwa_bez_rozszerzenia, rozszerzenie = os.path.splitext(nazwa_pliku)
                nazwy_plikow_GSM.append(nazwa_bez_rozszerzenia)
#                 print('nazwy_plikow_GSM.append(nazwa_bez_rozszerzenia) - gsm')
#                 print(nazwy_plikow_GSM)
                g += 1

                arcpy.management.AddField(lista_1GSM[g], "objj1", "Long")

                arcpy.management.CalculateField(lista_1GSM[g], "objj1", '!LEGEND!', "PYTHON3")

                wynik_1 = arcpy.management.AddJoin(lista_1GSM[g], "objj1", join_table_cell, "CELL_OBJ")

                # chcemy ja nazwyać, warstwy maja się nazywac same

                # print(f'{output}\\{nazwy_plikow[n]})')

                arcpy.AddMessage(f'Warstwa: {wynik_1}')

                output_feature_class_info = fr'{output_info}'
                output_feature_class_info_name = fr'{nazwy_plikow_GSM[g]}_info'
                # print('GSM - output_feature_class_info')
                #arcpy.AddMessage(output_feature_class_info)


                output_feature_class_MV = fr'{output_MV}'
                output_feature_class_MV_name = fr'{nazwy_plikow_GSM[g]}_MV'
                # print('GSM - output_feature_class_MV')
                #arcpy.AddMessage(output_feature_class_MV)

                #arcpy.management.CopyFeatures(wynik_1, output_feature_class_info)
                arcpy.conversion.FeatureClassToFeatureClass(wynik_1, output_info, output_feature_class_info_name)
                arcpy.env.outputCoordinateSystem = e2180
                #arcpy.management.CopyFeatures(wynik_1, output_feature_class_MV)
                arcpy.conversion.FeatureClassToFeatureClass(wynik_1, output_MV, output_feature_class_MV_name)

#                 # Usuń pola bezpośrednio z warstwy źródłowej
#                 lista_3 = arcpy.ListFields(output_feature_class_MV)
#                 # print('lista_2 - GSM')
#                 # print(lista_3)
#                 for x in lista_3:
#                     pola_do_usuniecia.append(x.name)
#
#
#                 arcpy.AddMessage('Wyswietla rekordy do usuniecia w MV - UMTS')
#                 arcpy.AddMessage(pola_do_usuniecia[2:12])
#                 arcpy.management.DeleteField(output_feature_class_MV, pola_do_usuniecia[2:12])
#                 pola_do_usuniecia = []

                path_output_feature_class_MV = fr'{output_feature_class_MV}\{nazwy_plikow_GSM[g]}_MV'
                arcpy.AddMessage(f'path_output_feature_class_MV GSM: {path_output_feature_class_MV}')
                # Lista pól, które chcemy zachować
                pola_do_zachowania2 = ['OBJECTID_1', 'Shape', 'LOC_NAME', 'LOC_OBJ', 'LOC_CODE', 'SITE_NAME', 'SITE_OBJ', 'SITE_CODE', 'CELL_NAME', 'CELL_OBJ', 'CELL_CODE', 'LAC', 'BAND', 'BCCH_CHAN', 'BCC', 'NCC', 'Shape_Length', 'Shape_Area']


                # Pobierz listę wszystkich pól
                lista_pól2 = arcpy.ListFields(path_output_feature_class_MV)

                # Utwórz listę pól do usunięcia
                pola_do_usuniecia = []
                for pole in lista_pól2:
                    if not any(fraza in pole.name for fraza in pola_do_zachowania2):
                        pola_do_usuniecia.append(pole.name)

                # Wyświetl pola do usunięcia
                arcpy.AddMessage(f'Pola do usunięcia: {pola_do_usuniecia}')

                # Usuń wybrane pola
                if pola_do_usuniecia:
                    arcpy.management.DeleteField(path_output_feature_class_MV, pola_do_usuniecia)

                    arcpy.AddMessage("Pola zostały usunięte.")
                else:
                    arcpy.AddMessage("Brak pól do usunięcia.")


                #################### poleeeeeeeeeeeeeeee do skasowania #################################################################
                arcpy.management.DeleteField(path_output_feature_class_MV, "C_CELL_OBJ")
                #################### poleeeeeeeeeeeeeeee do skasowania #################################################################
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------765')
                arcpy.AddMessage(f'Done: {nazwy_plikow_GSM[g]}_info')
                arcpy.AddMessage(f'Done: {nazwy_plikow_GSM[g]}_MV')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------')

            arcpy.AddMessage('---------------------- KONIEC CZESCI III - GSM  ----------------------')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')



# PRZECIAZENIA #############################################################################################################################################################################################################################################
        if param_przeciazenia_1010:
            arcpy.AddMessage('---------------------- CZESCI IV - Przeciązenia dla LTE ----------------------')
            output_MV = parameters[9].valueAsText
            arcpy.env.workspace = output_MV
            lista_MV = arcpy.ListFeatureClasses('*M_LTE*')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------785')
            arcpy.AddMessage('---------------------- TEST NA DZIAŁANIE ----------------------')
            arcpy.AddMessage('---------------------- Jeśli lista poniżej tego komunikatu jest pusta sprawdź, czy geobaza MV jest wprowadzona jako parametr do narzędzia geoprzetwarzania oraz czy dominance LTE są wykonane ----------------------')
            arcpy.AddMessage(f'Lista - dominance LTE: {lista_MV}')
            arcpy.AddMessage('---------------------- Jeśli lista powyżej tego komunikatu zawiera dominance LTE - może zlekcewarzyć ten TEST ----------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')


        if param_przeciazenia_1010 and len(lista_MV) == 0:
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------796')
            arcpy.AddMessage('---------------------- TEST NA DZIAŁANIE ----------------------')
            arcpy.AddMessage('UWAGA !!!!!!!!!!!!!!!!!!!!!!!!!!!!---------------------- Zrób dominance lte----------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage('---------------------- KONIEC CZESCI IV - Przeciązenia dla LTE ----------------------')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')


        if param_przeciazenia_1010 and len(lista_MV) >= 1:


            arcpy.env.overwriteOutput = True


            arcpy.env.workspace = output_MV
            lista_MV = arcpy.ListFeatureClasses('*M_LTE*')

            # Ustawienie środowiska pracy geobaze SDE
            #arcpy.env.workspace = r"C:\Users\buchadan\AppData\Roaming\Esri\ArcGISPro\Favorites\Admin_SDE.sde"
            sde = arcpy.env.workspace = parameters[11].valueAsText
            # Lista tabel do przefiltrowania z bazdy danych do tabel, od przeciazenia lte
            #lista_3 = arcpy.ListTables('*_przeciazone_lte_*')
            lista_3 = arcpy.ListTables('*_przeciazone_lte*')
            # Filtrowanie tabel, które nie kończą się na "_a" ani "_lte700"
            przeciazenia = [table for table in lista_3 if not (table.endswith("_a") or table.endswith("_lte700"))]
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------825')
            arcpy.AddMessage('---------------------- TEST NA DZIAŁANIE ----------------------')
            arcpy.AddMessage('---------------------- Jesli lista poniżej jest pusta - to sprawdż czy masz aktywne polaczenia z baza danych SDE ----------------------')
            arcpy.AddMessage(f'Lista - przeciazenia: {przeciazenia}')
            arcpy.AddMessage('---------------------- Jeśli lista powyżej tego komunikatu zawiera tabele przecinzone LTE - może zlekcewarzyć ten TEST ----------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')
            # Ustawienie środowiska pracy na drugą geobazę
            # arcpy.env.workspace = r"D:\\Daniel\\ArcGIS\\Projects\\Dane_zasiegowe\\Wynik_test_12_12_2023_MV.gdb"

            # output_MV = r'D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\Wynik_test_12_12_2023_MV.gdb'
            # przypisanie srodowiska do podanej sciezki output_MV zeby wybrac juz zrobione warstwy MV
            #output_MV = r'D:\ArcGIS\______________________________Dane_zasiegowe______________________________\Dane_zasiegowe_nr_1\2024_01_16_MV_Dane_zasiegowe_new.gdb'
            output_MV = parameters[9].valueAsText
            arcpy.env.workspace = output_MV

            # Lista warstw wektorowych MV
            # tutaj - _MV - tylko po to, zeby nie brac przeciazonych - jesli one juz z jakiegos powodu sa w geobazie
            # lista_MV = arcpy.ListFeatureClasses('* _MV') - WCZESNIEJ BYLO TAK

            # teraz to zmienilem
            lista_MV = arcpy.ListFeatureClasses('*M_LTE*')

            # Wyswietlenie warstw MV
            #arcpy.AddMessage('Lista warstwy MV')
            #arcpy.AddMessage(lista_MV)

            # wyciagniecie do listy - common_part_lista - wartosci: LTE800, LTE900, LTE1800, LTE2100, LTE2600 itp
            #
            common_part_lista = []
            for x in przeciazenia:
                # Wyciąganie części wspólnej nazwy - powiększenie liter - LTE
                common_part = x.split('_')[-1].upper()  # Używamy upper() aby powiekszyc litery, bo warstwy maja raz 'lte' a raz 'LTE'
                common_part_lista.append(common_part)

            #arcpy.AddMessage('Lista pomocnicza')
            #arcpy.AddMessage(common_part_lista)


            # Przeszukiwanie obu list w poszukiwaniu par
            # iterowanie sie przez liste z LTE lub UMTS (3g)
            for common in common_part_lista:

                # iteracja jest zawsze dla tego samego wspolnego elementu LTE800, LTE900, LTE1800, LTE2100, LTE2600
                # dodawanie do listy mv_match warstw, ktore sa akurat iterowane i zawieraja np. LTE900 (z geobazy)
                mv_match = [layer for layer in lista_MV if common.upper() in layer.upper()]
                # dodawanie do listy przeciazenie_match warstw, ktore sa akurat iterowane i zawieraja np. LTE900 (z SDE)
                przeciazenie_match = [table for table in przeciazenia if common.upper() in table.upper()]

                # sprawdzamy czy przeciazenie_match = True i mv_match = True - JESTLI TAK TO IDIZEMY dalej
                if przeciazenie_match and mv_match:
                    # mv_match[0] z geobazy - wczesniejsze warsrwy z bazy MV
                    # przeciazenie_match[0] z bazy danych SDE - zeby robic warstwe przeciazenia
                    arcpy.AddMessage(f'-------------------------------')
                    arcpy.AddMessage(f'-------------------------------879')
                    arcpy.AddMessage(f'Para: {mv_match[0]} - {przeciazenie_match[0]} ')


                    # szukanie kolumny LCELL_OBJ, ktora bedzie kluczem do narzedzia AddJoin
                    lista_4a = arcpy.ListFields(mv_match[0])
                    a = lista_4a[9].name
                    #arcpy.AddMessage(f'{a} dla {mv_match[0]}')

                    # szukanie kolumny cell_obj, ktora bedzie kluczem do narzedzia AddJoin (z bazy SDE)
                    # lista_4b = arcpy.ListFields(przeciazenie_match[0])
                    lista_4b = arcpy.ListFields(fr'{sde}\\{przeciazenie_match[0]}')
                    b = lista_4b[1].name
                    #arcpy.AddMessage(f'{b} dla {przeciazenie_match[0]}')


                    # odszukanie LCELL_OBJ"
                    arcpy.AddMessage(f'Join po kolumnie: -- {a} (zmienna dynamiczna) z warstwy {mv_match[0]} (zmienna dynamiczna)-- SPRAWDZENIE -- łączy sie z kolumną: -- {b} (zmienna dynamiczna)-- z warstwy {przeciazenie_match[0]} (zmienna dynamiczna)')


                    # indeks jesli chcemy to robic poza argciem pro
                    # arcpy.AddIndex_management(przeciazenie_match[0], b, "Idx_" + b)

                    # łaczenie warstwy z budynku SDE i warstwy

                    #TRY I EXPCECT POMAGA GDY JUŻ BYŁO ZŁĄCZENIE I PUSZCZAM SKRYTP KOLEJNY RAZ

                    abc = arcpy.management.AddJoin(mv_match[0], a, f'{sde}\{przeciazenie_match[0]}', b, join_type="KEEP_COMMON")
                    #arcpy.AddMessage("Join successful")
                    #arcpy.AddMessage('Tworzy: ')
                    output_feature_class_przeciazenia =   fr'{output_MV}\\przeciazenie_{common}'
                    arcpy.AddMessage(output_feature_class_przeciazenia)
                    arcpy.AddMessage(output_MV)
                    arcpy.AddMessage(f'-------------------------------')
                    arcpy.AddMessage(f'-------------------------------913')

#                 po tym jak zrobimy AddJoin - trzeba warstwe zapisac do geobazy - do wczesniej utworzonej sciezki
#                 ta sciezka jest skomponowana z dopisow LTE I UMTS
                    #arcpy.AddMessage('UWAGA !!!!!!!!!!!!!!!!!!!!!!!!!!!!---------------------- Sprawdz polaczenie z baza SDE ----------------------')

                    #arcpy.management.CopyFeatures(abc, output_feature_class_przeciazenia)
                    arcpy.conversion.FeatureClassToFeatureClass(abc, fr'{output_MV}', fr'przeciazenie_{common}')
                    arcpy.AddMessage(fr'{output_MV}')
                    arcpy.AddMessage(fr'przeciazenie_{common}')

            # Ustal nazwy kolumn, które chcesz zachować
            kolumny_do_zachowania = ["OBJECTID", "Shape", "LCELL_NAME", "Shape_Length", "Shape_Area"]

            # Tworzymy listę, która będzie zawierać wszystkie elementy, które będą do skasowania
            lista_do_skasowania = []

####################################################JESLI PUSZCZAM KOD BEZ PARAMETROW##############################################################################################
            arcpy.AddMessage(f'-------------TEST linia 933------------------')
            arcpy.AddMessage(f'-------------TEST------------------')
            lista_5 = arcpy.ListFields(output_feature_class_przeciazenia)
####################################################JESLI PUSZCZAM KOD BEZ PARAMETROW##############################################################################################


            # Znajdź pola do skasowania
            for pole in lista_5:
                # Sprawdź, czy nazwa pola nie znajduje się na liście kolumn do zachowania
                if pole.name not in kolumny_do_zachowania:
                    lista_do_skasowania.append(pole.name)

            # Teraz masz listę nazw pól do skasowania
            arcpy.AddMessage("Pola do skasowania:")
            arcpy.AddMessage(lista_do_skasowania)
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------947')
            # Pobierz listę nazw warstw wektorowych zaczynających się od 'przeciazenie*'
            lista_przeciazone = arcpy.ListFeatureClasses('przeciazenie*')

#             arcpy.AddMessage(f'###############################')
#             arcpy.AddMessage(f'###############################')
#             zmien_nazwy_pol_na_aliasy(lista_przeciazone)
#             arcpy.AddMessage(f'###############################')
#             arcpy.AddMessage(f'###############################')

            arcpy.AddMessage('Lista z przeciążeniami, od których teraz będziemy odejmować kolumny, żeby zostawić tylko OBJECTID, Shape -- LCELL_NAME -- Shape_Length, Shape_Area')
            arcpy.AddMessage(lista_przeciazone)
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')

            # Usuwanie kolumn, które są niepotrzebne, zostawienie tylko kolumny OBJECTID, Shape -- LCELL_NAME -- Shape_Length, Shape_Area
            for warstwa in lista_przeciazone:

                arcpy.AddMessage(f'Kasowanie kolumn dla: {warstwa}')
                # Usuwanie pól, które są na liście do skasowania
                arcpy.management.DeleteField(warstwa, lista_do_skasowania)
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------969')
                arcpy.AddMessage(f'Done: {warstwa}')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------')


#             # Lista pól, które chcemy zachować
#             pola_do_zachowania2 = ['OBJECTID_1', 'Shape', 'LOC_NAME', 'LOC_OBJ', 'LOC_CODE', 'SITE_NAME', 'SITE_OBJ', 'SITE_CODE', 'CELL_NAME', 'CELL_OBJ', 'CELL_CODE', 'LAC', 'BAND', 'BCCH_CHAN', 'BCC', 'NCC', 'Shape_Length', 'Shape_Area']
#
#
#             # Pobierz listę wszystkich pól
#             lista_pól2 = arcpy.ListFields(path_output_feature_class_MV)
#
#             # Utwórz listę pól do usunięcia
#             pola_do_usuniecia = []
#             for pole in lista_pól2:
#                 if not any(fraza in pole.name for fraza in pola_do_zachowania2):
#                     pola_do_usuniecia.append(pole.name)
#
#             # Wyświetl pola do usunięcia
#             arcpy.AddMessage(f'Pola do usunięcia: {pola_do_usuniecia}')
#
#             # Usuń wybrane pola
#             if pola_do_usuniecia:
#                 arcpy.management.DeleteField(path_output_feature_class_MV, pola_do_usuniecia)
#
#                 arcpy.AddMessage("Pola zostały usunięte.")
#             else:
#                 arcpy.AddMessage("Brak pól do usunięcia.")







            arcpy.AddMessage('---------------------- KONIEC CZESCI IV - Przeciązenia dla LTE ----------------------')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^ ZACZEKAJ TO MOŻE CHWILE TRWAĆ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')






# PIRAMIDY #############################################################################################################################################################################################################################################
        if param_1212:

            arcpy.AddMessage('---------------------- CZESCI V - Robienie Piramid i geobaza 3857----------------------')


            #arcpy.env.workspace = r"D:\ArcGIS\Dane_zasiegowe_nr_1\Dane\paczka_opl_eo202312"

            aa = arcpy.env.workspace = parameters[13].valueAsText

            # Pobierz listę warstw, których nazwa zawiera frazy 'GES' lub 'OT'
            # lista_warstw = arcpy.ListFeatureClasses('*GES_*') + arcpy.ListFeatureClasses('*OT_*')
            lista_warstw_all = arcpy.ListRasters('*', "TIF")
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------1029')
            arcpy.AddMessage('Rastery, na których zostaną wykonane piramidy - w wyniku nasze rastry wejsciowe będą już z piramidami i w układzie 3857: ')
            arcpy.AddMessage(lista_warstw_all)
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')

            lista_warstw = arcpy.ListRasters("*LTE*" + "*_5class_*" + "*.tif", "TIF") + arcpy.ListRasters("CA_OPL_*" + "*.tif", "TIF") + arcpy.ListRasters("*_UMTS*" + "_5class_*" + "*.tif", "TIF") + arcpy.ListRasters("*_GSM*" + "_5class_*" + "*.tif", "TIF")

            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------1038')
            arcpy.AddMessage('Rastery, którym zostanie zmieniony układ współrzędnych i zostaną przeniesione do geobazy z układem 3857: ')
            arcpy.AddMessage(lista_warstw)
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')
            # print(f'Liczba warstw: {len(lista_warstw)}')
            # print('Dane zostały wczytane')

            #arcpy.AddMessage('podaj path  -3')
            #folder_piramid = r'D:\Daniel\ArcGIS\Projects\Dane_zasiegowe_1\piramidy'
            #folder_piramid = parameters[15].valueAsText

            #e3857 = r"D:\ArcGIS\projections\WGS 1984 Web Mercator (auxiliary sphere).prj"
            e3857 = parameters[15].valueAsText
            #output_feature_class_MV_raster = r'D:\ArcGIS\Dane_zasiegowe_nr_1\2024_01_16_MV_Dane_zasiegowe_3857.gdb'
            output_feature_class_MV_raster = parameters[14].valueAsText
            # Ustawienia poziomu piramidy (przykładowa wartość - dostosuj do własnych potrzeb)


            for warstwa_rastrowa in lista_warstw_all:
                # parametry
                arcpy.env.overwriteOutput = True
                arcpy.env.outputCoordinateSystem = e3857


                # Wartość -1 oznacza pełne piramidy, czyli wszystkie dostępne poziomy
                # SKIP_EXISTING oznacza, że piramidy zostaną zbudowane tylko wtedy, gdy nie istnieją
                arcpy.management.BuildPyramids(warstwa_rastrowa, -1, "NONE", "NEAREST", "LZ77", 50, "SKIP_EXISTING")
                #arcpy.env.outputCoordinateSystem = e3857
                # czy to zadziała?
#                 arcpy.AddMessage(f'---------------TEST----------------')
#                 arcpy.AddMessage(fr'{aa}\{warstwa_rastrowa}')
#                 arcpy.AddMessage(f'------------- Linia 1069------------------')
                #arcpy.management.ProjectRaster(fr'{aa}\{warstwa_rastrowa}', fr'{aa}\{warstwa_rastrowa}_3857.tif', e3857)

                # print(wynik_raster)
                #output_feature_class_MV_raster = ''
                if warstwa_rastrowa in lista_warstw:
                    arcpy.env.outputCoordinateSystem = e3857
                    arcpy.env.overwriteOutput = True
                    nazwa_bez_rozszerzenia, _ = os.path.splitext(warstwa_rastrowa)
                    arcpy.management.BuildPyramids(warstwa_rastrowa, -1, "NONE", "NEAREST", "LZ77", 50, "SKIP_EXISTING")



                    #output_feature_class_MV_raster = fr'{output_feature_class_MV_raster}\{nazwa_bez_rozszerzenia}_3857'
                    output_feature_class_MV_raster_new = os.path.join(output_feature_class_MV_raster, f'{nazwa_bez_rozszerzenia}_3857')

                    #arcpy.AddMessage(output_feature_class_MV_raster_new)
                    arcpy.env.overwriteOutput = True
                    arcpy.management.ProjectRaster(warstwa_rastrowa, output_feature_class_MV_raster_new, e3857)

            #arcpy.env.workspace = r"D:\ArcGIS\Dane_zasiegowe_nr_1\2024_01_16_MV_Dane_zasiegowe_c.gdb"
            arcpy.env.workspace = parameters[9].valueAsText
            #e3857 = r"D:\ArcGIS\projections\WGS 1984 Web Mercator (auxiliary sphere).prj"
            e3857 = parameters[15].valueAsText

            # Pobierz listę warstw, których nazwa zawiera frazy 'GES' lub 'OT'
            # lista_warstw = arcpy.ListFeatureClasses('*GES_*') + arcpy.ListFeatureClasses('*OT_*')
            #lista_warstw_all_mv = arcpy.ListFeatureClasses('*')
            lista_warstw_all_mv = arcpy.ListFeatureClasses("*M_LTE*") + arcpy.ListFeatureClasses("CA_OPL_*") + arcpy.ListFeatureClasses("*M_UMTS*") + arcpy.ListFeatureClasses("*M_GSM*")
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------1100')
            arcpy.AddMessage('Klasy obiektów, którym zostanie zmieniony układ współrzędnych i zostaną przeniesione do geobazy z układem 3857:: ')
            arcpy.AddMessage(lista_warstw_all_mv)
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')

            arcpy.env.overwriteOutput = True
            for x in lista_warstw_all_mv:
                #arcpy.AddMessage("lista_warstw_all_mv")
                output_feature_class_MV = fr'{output_feature_class_MV_raster}\{x}_3857'
                #arcpy.AddMessage(output_feature_class_MV)

                arcpy.management.Project(x, output_feature_class_MV, e3857)

            arcpy.AddMessage('---------------------- KONIEC CZESCI V - Robienie Piramid i geobaza 3857----------------------')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')



# 5G DSS #############################################################################################################################################################################################################################################
        n = -1
        nazwy_plikow_dss = []
        if param_1717:
            #arcpy.AddMessage('---------------------- Start - DSS ----------------------')
            arcpy.AddMessage('---------------------- CZESCI VI - dane zasiegowe 5G DSS ---------------------')
            arcpy.env.overwriteOutput = True
            d = arcpy.env.workspace = parameters[17].valueAsText
#             arcpy.AddMessage(f'Folder_z_danymi: {d}')

            lista_1DSS = []
            for folder, subfolders, files in arcpy.da.Walk(arcpy.env.workspace, datatype="FeatureClass"):
#                 arcpy.AddMessage(f'folder_5G_DSS: {folder}')
#                 arcpy.AddMessage(f'subfolders_5G_DSS: {subfolders}')
#                 arcpy.AddMessage(f'files_5G_DSS: {files}')
                for file in files:
                    if 'DSS' in file:
                        lista_1DSS.append(os.path.join(folder, file))
                        arcpy.AddMessage(f'Dominance - 5G - DSS: {lista_1DSS}')


            for sciezka in lista_1DSS:
                nazwa_pliku = os.path.basename(sciezka)
                nazwa_bez_rozszerzenia, rozszerzenie = os.path.splitext(nazwa_pliku)
                nazwy_plikow_dss.append(nazwa_bez_rozszerzenia)
                #arcpy.AddMessage(f'111 nazwy_plikow: {nazwy_plikow_dss}')
                n += 1
#                 arcpy.AddMessage(f'lista_1DSS: {lista_1DSS}')
                arcpy.management.AddField(lista_1DSS[n], "objj1", "TEXT")

                #arcpy.management.CalculateField(lista_1[n], "objj1", '!TX_ID!', "PYTHON3")
                # Przykład funkcji, która przetwarza wartość pola TX_ID
                def remove_after_hash(value):
                    return value.split('#')[0] if '#' in value else value

                # Załóżmy, że lista_1[n] to ścieżka do warstwy, a 'objj1' to nazwa pola docelowego
                arcpy.management.CalculateField(
                    lista_1DSS[n],
                    "objj1",
                    "remove_after_hash(!TX_ID!)",
                    "PYTHON3",
                    code_block="""def remove_after_hash(value):
                    return value.split('#')[0] if '#' in value else value""")


                wynik_4 = arcpy.management.AddJoin(lista_1DSS[n], "objj1", join_table_gcell, "LCELL_NAME")




                output_feature_class_info = fr'{output_info}'
                output_feature_class_info_name = fr'{nazwy_plikow_dss[0]}_info'
                path_output_feature_class_info = fr'{output_feature_class_info}\{nazwy_plikow_dss[0]}_info'

                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------1176')
                arcpy.AddMessage(f'---------------Tworzenie warstwy info----------------')
                arcpy.AddMessage(f'1 Warstwa: {wynik_4}')
                arcpy.AddMessage(f'2 output_info: {output_info}')
                arcpy.AddMessage(f'3 output_feature_class_info_name: {output_feature_class_info_name}')
                arcpy.AddMessage(f'4 path_output_feature_class_info: {path_output_feature_class_info}')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------')

                arcpy.conversion.FeatureClassToFeatureClass(wynik_4, output_feature_class_info, output_feature_class_info_name)




            c = arcpy.env.workspace = parameters[9].valueAsText
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------1192')
            arcpy.AddMessage(f'Ścieżka do wybrania skad maja być brane dominance LTE w celu utworzenia maski - 5G DSS: {c}')
            lista_LTE = arcpy.ListFeatureClasses('*M_LTE800*') + arcpy.ListFeatureClasses('*M_LTE1800*') + arcpy.ListFeatureClasses('*M_LTE2600*')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')

            #arcpy.AddMessage(f'lista LTE do stworzenia maski - 5G DSS: {lista_LTE}')
            if len(lista_LTE[:]) != 0:
                arcpy.AddMessage(f'lista LTE do stworzenia maski - 5G DSS: {lista_LTE}')
            else:
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                arcpy.AddMessage(f'!!!!!!!!!!!!!UWAGA!!!!!!!!!!!!!1204')
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Musisz zrobić dominance LTE')
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


            # ściećka do zapisu joina
            arcpy.env.overwriteOutput = True
            output_join = parameters[8].valueAsText
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------1214')
            arcpy.AddMessage(f'Ścieżka do zapisu joina czyli geometrii LTE z domimanca - krok pośredni - 5G DSS: {output_join}')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')



            #tu nie wchodzimy kiedy nie ma nic w lista_LTE
            # Lista przechowująca wyniki AddJoin
            lista_wynikow_AddJoin = []
            lista_LTE_LOC_OBJ = []
            n = -1
            #pętla nr 1
            for x in lista_LTE:
                n += 1

                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------1231')
                arcpy.AddMessage('---------------Warstwa---------------')
                arcpy.AddMessage(x)


                # pole -- LOC_OBJ -- zeby mogl się po czym polaczyć
                fields = arcpy.ListFields(x,'*LOC_OBJ*')

                #pętla nr 2
                for field in fields:
                    #wyciagamy tylko loc_obj - z warstw - lte
                    lista_LTE_LOC_OBJ.append(field.name)



                arcpy.AddMessage('---------------Parametry wejsciowe do AddJoin---------------')

                arcpy.AddMessage(f'parametr 1: {lista_LTE[n]}')
                arcpy.AddMessage(f'parametr 2: {lista_LTE_LOC_OBJ[n]}')
                #arcpy.AddMessage(f'parametr 3: {path_output_feature_class_MV}')
                arcpy.AddMessage(f'{path_output_feature_class_info}')
                arcpy.AddMessage(f'parametr 4: To jest tekst - LOC_OBJ')

                wynik_0 = arcpy.management.AddJoin(lista_LTE[n], lista_LTE_LOC_OBJ[n], f'{path_output_feature_class_info}', "LOC_OBJ", join_type='KEEP_COMMON')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------1256')



                # output_join =  D:\ArcGIS\2_Dane_Zasiegowe_5G_DSS\5G_DSS_nr_1_grudzien_2023\ostateczne_5G_DSS_z_dnia_24_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024\Ostateczne_5G_DSS_z_dnia_25_01_2024_new.gdb
                output_feature_class_join = fr'{output_join}'
                output_feature_class_join_name = fr'{lista_LTE[n]}_join'

                arcpy.conversion.FeatureClassToFeatureClass(wynik_0, output_feature_class_join, output_feature_class_join_name)


            arcpy.env.workspace = output_join
            lista_LTE_marge = arcpy.ListFeatureClasses('*_join*')


            #arcpy.management.Merge("OPL_DOM_LTE800_Eo202312_MV_join;OPL_DOM_LTE900_Eo202312_MV_join;OPL_DOM_LTE1800_Eo202312_MV_join;OPL_DOM_LTE2600_Eo202312_MV_join;Po_polaczeniu_wszystkich_LTE_19_01_2024", output_Merge)
            if len(lista_LTE_marge) != 0:
                arcpy.management.Merge(lista_LTE_marge, "in_memory/output_Merge")
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------1275')
                arcpy.AddMessage(f'lista do zrobienia maski: {lista_LTE_marge}')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------')


                #Masaka
                country_border_and_sea_buffer_cala_polska = parameters[20].valueAsText


                output_maska = parameters[19].valueAsText

#                 arcpy.AddMessage(f'-------------------------------')
#                 arcpy.AddMessage(f'-------------------------------')
#                 arcpy.AddMessage(f'Parametr 1 do Clip: Merge z geometrii LTE')
#                 arcpy.AddMessage(f'Parametr 2 do Clip: ountry_border_and_sea_buffer_cala_polska')
#                 arcpy.AddMessage(f'Parametr 3 do Clip: {output_maska}')
#                 arcpy.AddMessage(f'-------------------------------')
#                 arcpy.AddMessage(f'-------------------------------')

                arcpy.analysis.Clip("in_memory/output_Merge", country_border_and_sea_buffer_cala_polska, output_maska)




                output_feature_class_MV = fr'{output_MV}'
                output_feature_class_MV_name = fr'{nazwy_plikow_dss[0]}_MV'

                arcpy.env.outputCoordinateSystem = e2180
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!Zapisa wartwy MV!!!!!!!!!!!!!!!!1305')
                arcpy.AddMessage(f'Warstwa: {wynik_4}')
                arcpy.AddMessage(f'output_MV: {output_MV}')
                arcpy.AddMessage(f'output_feature_class_MV_name: {output_feature_class_MV_name}')
                arcpy.conversion.FeatureClassToFeatureClass(wynik_4, output_feature_class_MV, f'{output_feature_class_MV_name}')
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


                # Lista pól, które chcemy zachować
                pola_do_zachowania = ['OBJECTID_1', 'Shape', 'LOC_OBJ', 'LOC_CODE', 'GSITE_NAME', 'GSITE_OBJ', 'GSITE_ID', 'GCELL_NAME', 'GCELL_OBJ', 'GCELL_ID', 'LTE2100_SHARED', 'LCELL_NAME', 'LOC_NAME', 'Shape_Length', 'Shape_Area']


                lista_pól = arcpy.ListFields(fr'{path_output_feature_class_info}')


                # Utwórz listę pól do usunięcia
                pola_do_usuniecia = []
                for pole in lista_pól:
                    if not any(fraza in pole.name for fraza in pola_do_zachowania):
                        pola_do_usuniecia.append(pole.name)

                # Wyświetl pola do usunięcia
                arcpy.AddMessage(f'Pola do usunięcia: {pola_do_usuniecia}')

                # Usuń wybrane pola
                if pola_do_usuniecia:
                    arcpy.management.DeleteField(f'{path_output_feature_class_info}', pola_do_usuniecia)
                    arcpy.AddMessage("Pola zostały usunięte.")
                else:
                    arcpy.AddMessage("Brak pól do usunięcia.")


                # Pobierz listę wszystkich pól
                path_output_feature_class_MV = fr'{output_feature_class_MV}\{nazwy_plikow_dss[0]}_MV'

                arcpy.analysis.Clip(f'{path_output_feature_class_info}', output_maska, path_output_feature_class_MV)

                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------13544')
                arcpy.AddMessage(f'Done: {nazwy_plikow_dss[0]}_info')
                arcpy.AddMessage(f'Done: {nazwy_plikow_dss[0]}_MV')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------')

                arcpy.AddMessage('---------------------- koniec CZESCI VI - dane zasiegowe 5G DSS ----------------------')
                arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')


            else:
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1358')
                arcpy.AddMessage(f'!!!!!!!!!!!!!UWAGA!!!!!!!!!!!!!')
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Musisz zrobić dominance LTE')
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

# zmien_nazwy_pol_na_aliasy #############################################################################################################################################################################################################################################
#         arcpy.AddMessage('---------------------- CZESCI VII - Zmien nazwy pÓl na aliasy ----------------------')
#         zmien_nazwy_pol_na_aliasy(parameters[17].valueAsText)
#         arcpy.AddMessage('---------------------- koniec CZESCI VII - Zmien nazwy pÓl na aliasy ----------------------')




# DOMINANCE 5G c-band #############################################################################################################################################################################################################################################


        pola_do_usuniecia = []
        nazwy_plikow = []
        n = -1
        if param_2222:

            arcpy.AddMessage('---------------------- CZESCI VII - dane zasiegowe 5G c-band ----------------------')
            arcpy.env.overwriteOutput = True
            d = arcpy.env.workspace = parameters[22].valueAsText
#             arcpy.AddMessage(f'Folder_z_danymi: {d}')

            lista_1_5G = []
            for folder, subfolders, files in arcpy.da.Walk(arcpy.env.workspace, datatype="FeatureClass"):
#                 arcpy.AddMessage(f'folder_5G_DSS: {folder}')
#                 arcpy.AddMessage(f'subfolders_5G_DSS: {subfolders}')
#                 arcpy.AddMessage(f'files_5G_DSS: {files}')
                for file in files:
                    if 'CBAND' in file:
                        lista_1_5G.append(os.path.join(folder, file))
                        arcpy.AddMessage(f'Dominance - 5G: {lista_1_5G}')


            for sciezka in lista_1_5G:
                nazwa_pliku = os.path.basename(sciezka)
                nazwa_bez_rozszerzenia, rozszerzenie = os.path.splitext(nazwa_pliku)
                nazwy_plikow.append(nazwa_bez_rozszerzenia)
                n += 1

                arcpy.management.AddField(lista_1_5G[n], "objj1", "Long")

                arcpy.management.CalculateField(lista_1_5G[n], "objj1", '!C_XCELL_OB!', "PYTHON3")

                # join_table = 'lcell_20231130_Merge'

                #wynik_1 = arcpy.management.AddJoin(lista_1[n], "objj1", join_table, "LCELL_OBJ")
                wynik_7 = arcpy.management.AddJoin(lista_1_5G[n], "objj1", join_table_5G_gcell, "GCELL_OBJ")


                #NOWE PODEJSCIE ALE TO NA STALE DODAWALO KOLUMNY DO WARSTWY SHP - pomijam to teraz
                #r"D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\Dane\paczka_opl_eo202312\OPL_DOM_LTE1800_Eo202312"
                #r"D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\mv.gdb\lcell_20231231_Merge"
                #zeby nie bral pozniej do kopiowania stringa
                #arcpy.management.JoinField(lista_1[n], "objj1", join_table, "LCELL_OBJ")


                # chcemy ja nazwyać, warstwy maja się nazywac same

                # print(f'{output}\\{nazwy_plikow[n]})')

                #output_feature_class_info = fr'{output_info}\{nazwy_plikow[n]}_info'

                output_feature_class_info = fr'{output_info}'
                output_feature_class_info_name = fr'{nazwy_plikow[n]}_info'


                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------1437')
                arcpy.AddMessage(f'Warstwa: {wynik_7}')
#                 arcpy.AddMessage(f'output_info: {output_info}')
#                 arcpy.AddMessage(f'output_feature_class_info_name: {output_feature_class_info_name}')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------1100')

                #arcpy.management.CopyFeatures(wynik_1, output_feature_class_info)
                #arcpy.management.CopyFeatures(lista_1[n], output_feature_class_info)

                arcpy.conversion.FeatureClassToFeatureClass(wynik_7, output_info, output_feature_class_info_name)


                output_feature_class_MV = fr'{output_MV}'
                output_feature_class_MV_name = fr'{nazwy_plikow[n]}_MV'

                arcpy.env.outputCoordinateSystem = e2180
                #arcpy.management.CopyFeatures(wynik_1, output_feature_class_MV)
                #arcpy.management.CopyFeatures(lista_1[n], output_feature_class_MV)


#                 arcpy.AddMessage(f'wynik_1: {wynik_7}')
#                 arcpy.AddMessage(f'output_feature_class_MV: {output_feature_class_MV}')
#                 arcpy.AddMessage(f'output_feature_class_MV_name: {output_feature_class_MV_name}')

                arcpy.conversion.FeatureClassToFeatureClass(wynik_7, output_feature_class_MV, output_feature_class_MV_name)



                path_output_feature_class_MV = fr'{output_feature_class_MV}\{nazwy_plikow[n]}_MV'
                arcpy.AddMessage(f'path_output_feature_class_MV LTE: {path_output_feature_class_MV}')
                # Usuń pola bezpośrednio z warstwy źródłowej
#                 lista_2 = arcpy.ListFields(path_output_feature_class_MV)
#
#                 for x in lista_2:
#
#                     pola_do_usuniecia.append(x.name)
#                 arcpy.AddMessage(f'Wszystkie pola: {pola_do_usuniecia}')
#
#                 arcpy.AddMessage(f'Wyswietla rekordy do usuniecia w MV: {pola_do_usuniecia[2:12]}')
#                 arcpy.management.DeleteField(path_output_feature_class_MV, pola_do_usuniecia[2:12])
#                 pola_do_usuniecia = []

                # Lista pól, które chcemy zachować
                pola_do_zachowania = ['OBJECTID_1', 'Shape', 'LOC_OBJ', 'LOC_CODE', 'GSITE_NAME', 'GSITE_OBJ', 'GSITE_ID', 'GCELL_NAME', 'GCELL_OBJ', 'GCELL_ID', 'NAME', 'PCI', 'Shape_Length', 'Shape_Area']

                # Pobierz listę wszystkich pól
                lista_pól = arcpy.ListFields(path_output_feature_class_MV)

                # Utwórz listę pól do usunięcia
                pola_do_usuniecia = []
                for pole in lista_pól:
                    if not any(fraza in pole.name for fraza in pola_do_zachowania):
                        pola_do_usuniecia.append(pole.name)

                # Wyświetl pola do usunięcia
                arcpy.AddMessage(f'Pola do usunięcia: {pola_do_usuniecia}')

                # Usuń wybrane pola
                if pola_do_usuniecia:
                    arcpy.management.DeleteField(path_output_feature_class_MV, pola_do_usuniecia)
                    arcpy.AddMessage("Pola zostały usunięte.")
                else:
                    arcpy.AddMessage("Brak pól do usunięcia.")


                arcpy.AddMessage(f'-------------------------------1504')
                arcpy.AddMessage(f'Done: {nazwy_plikow[n]}_info')
                arcpy.AddMessage(f'Done: {nazwy_plikow[n]}_MV')
                arcpy.AddMessage(f'-------------------------------')



            arcpy.AddMessage(f'---------------------- KONIEC - CZESCI V - dane zasiegowe 5G c-band ----------------------')



        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
