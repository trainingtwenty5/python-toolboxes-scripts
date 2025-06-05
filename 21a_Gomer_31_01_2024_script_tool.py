# -*- coding: utf-8 -*-

import arcpy
from arcpy.sa import *
import os


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox Gomer"
        self.alias = "DanielBuchar"


        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Gomer by Daniel Buchar"
        self.description = "Gomer"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""


        param0 = arcpy.Parameter(
            displayName="Plik wejściowy (point)",
            name="plik_wejsciowy",
            #datatype="DEFeatureClass",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="Zasieg_GSM",
            name="Zasieg_GSM",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Input")

        param2 = arcpy.Parameter(
            displayName="Zasieg_UMTS_900",
            name="Zasieg_UMTS_900",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Input")

        param3 = arcpy.Parameter(
            displayName="Zasieg_UMTS_2100",
            name="Zasieg_UMTS_2100",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Input")

        param4 = arcpy.Parameter(
            displayName="Zasieg_LTE_800",
            name="Zasieg_LTE_800",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Input")

        param5 = arcpy.Parameter(
            displayName="Zasieg_LTE_900",
            name="Zasieg_LTE_900",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Input")

        param6 = arcpy.Parameter(
            displayName="Zasieg_LTE_1800",
            name="Zasieg_LTE_1800",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Input")

        param7 = arcpy.Parameter(
            displayName="Zasieg_LTE_2100",
            name="Zasieg_LTE_2100",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Input")

        param8 = arcpy.Parameter(
            displayName="Zasieg_LTE_2600",
            name="Zasieg_LTE_2600",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Input")

        param9 = arcpy.Parameter(
            displayName="Zasieg_5G_2100_DSS",
            name="Zasieg_5G_2100_DSS",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Input")

        param10 = arcpy.Parameter(
            displayName="Zasieg_5G_3600",
            name="Zasieg_5G_3600",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Input")


        param11 = arcpy.Parameter(
            displayName="Geobaza domyślna ustawiona samodzielnie (do zapisu Spatial Join tylko dla dodatkowej warstwy)",
            name="Geobaza domyślna ustawiona samodzielnie (do zapisu Spatial Join tylko dla dodatkowej warstwy)",
            datatype="DEWorkspace",
            #datatype="GPString",
            parameterType="Optional",
            direction="Input")

        param12 = arcpy.Parameter(
            displayName="Komorki_GSM",
            name="Komorki_GSM",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        param13 = arcpy.Parameter(
            displayName="Komorki_UMTS_900",
            name="Komorki_UMTS_900",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        param14 = arcpy.Parameter(
            displayName="Komorki_UMTS_2100",
            name="Komorki_UMTS_2100",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        param15 = arcpy.Parameter(
            displayName="Komorki_LTE_800",
            name="Komorki_LTE_800",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        param16 = arcpy.Parameter(
            displayName="Komorki_LTE_900",
            name="Komorki_LTE_900",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        param17 = arcpy.Parameter(
            displayName="Komorki_LTE_1800",
            name="Komorki_LTE_1800",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        param18 = arcpy.Parameter(
            displayName="Komorki_LTE_2100",
            name="Komorki_LTE_2100",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        param19 = arcpy.Parameter(
            displayName="Komorki_LTE_2600",
            name="Komorki_LTE_2600",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        param20 = arcpy.Parameter(
            displayName="Komorki_5G_2100_DSS",
            name="Komorki_5G_2100_DSS",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        param21 = arcpy.Parameter(
            displayName="Komorki_5G_3600",
            name="Komorki_5G_3600",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

#         #Trzeba dodać do listy params
        param22 = arcpy.Parameter(
            displayName="Dodatkowa_warstwa",
            name="Dodatkowa_warstwa",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")


        # Parametr dla rastrów 5-klasowych
        param_5class = arcpy.Parameter(
            displayName="Dopisanie dla rasterów 5-klasowe",
            name="is_5class",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )
        param_5class.value = True  # Domyślnie zaznaczony

        # Parametr dla rastrów 2-klasowych
        param_2class = arcpy.Parameter(
            displayName="Dopisanie dla rasterów inout",
            name="is_2class",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        param_2class.value = False  # Domyślnie niezaznaczony

        #param0.filter.list = ["Point"]






        #param0.filter.type = "Featureclass"
        param0.filter.list = ["Point"]



        param11.defaultEnvironmentName = "workspace"



        param12.filter.list = ["Polygon"]

        param13.filter.list = ["Polygon"]
        param14.filter.list = ["Polygon"]
        param15.filter.list = ["Polygon"]
        param16.filter.list = ["Polygon"]
        param17.filter.list = ["Polygon"]
        param18.filter.list = ["Polygon"]
        param19.filter.list = ["Polygon"]
        param20.filter.list = ["Polygon"]
        param21.filter.list = ["Polygon"]
        #param22.filter.list = ["Polygon"]



        params = [param0, param_5class, param_2class, param1, param2, param3, param4, param5, param6, param7, param8, param9, param10, param11, param12, param13, param14, param15, param16, param17,param18, param19, param20, param21, param22]




        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # Jeśli pierwszy parametr został zmieniony, znajdź plik w projekcie
        if parameters[0].altered:
            plik_wejsciowy = parameters[0].valueAsText
            sciezka_do_pliku = self.znajdz_plik_w_projekcie(plik_wejsciowy)

            # Jeśli ścieżka do pliku została znaleziona, przypisz ją do parametru
            if sciezka_do_pliku:
                parameters[0].value = sciezka_do_pliku  # Ustaw ścieżkę do pliku jako wartość parametru

        # Tutaj możesz dodać dodatkową logikę dla innych parametrów

        return

    def znajdz_plik_w_projekcie(self, nazwa_pliku):
                # Pobierz aktualny projekt ArcGIS Pro
                projekt = arcpy.mp.ArcGISProject("CURRENT")

                # Przeszukaj wszystkie warstwy w projekcie
                for mapa in projekt.listMaps():
                    for warstwa in mapa.listLayers():
                        try:
                            if warstwa.supports("DATASOURCE") and os.path.isfile(warstwa.dataSource):
                                if warstwa.name.lower() == nazwa_pliku.lower():
                                    return warstwa.dataSource
                        except AttributeError:
                            pass

                # Pobierz ścieżkę do katalogu projektu
                katalog_projektu = os.path.dirname(projekt.filePath)

                # Przeszukaj projekt w poszukiwaniu pliku, w tym geobaz plikowych
                for root, dirs, files in os.walk(katalog_projektu):
                    for plik in files:
                        if plik.lower() == nazwa_pliku.lower():
                            return os.path.join(root, plik)
                    for dir in dirs:
                        if dir.endswith(".gdb"):
                            gdb_path = os.path.join(root, dir)
                            arcpy.env.workspace = gdb_path
                            for ds in arcpy.ListDatasets():
                                for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                                    if fc.lower() == nazwa_pliku.lower():
                                        return os.path.join(gdb_path, ds, fc)
                            for fc in arcpy.ListFeatureClasses():
                                if fc.lower() == nazwa_pliku.lower():
                                    return os.path.join(gdb_path, fc)

                # Jeśli nie znaleziono pliku, zwróć None
                return None





    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool parameter."""



        # Pobranie wartości z checkboxów
        is_5class_validacja = parameters[1].value  # Wartość Boolean
        inout_validacja = parameters[2].value      # Wartość Boolean

        # Sprawdzenie, czy oba checkboxy są zaznaczone
        if is_5class_validacja and inout_validacja:
            parameters[1].setErrorMessage("Wybierz tylko jedną opcję: 5-klasową lub inout.")
            parameters[2].setErrorMessage("Wybierz tylko jedną opcję: 5-klasową lub inout.")
        elif not is_5class_validacja and not inout_validacja:
            parameters[1].setErrorMessage("Musisz wybrać jedną z opcji: 5-klasową lub inout.")
            parameters[2].setErrorMessage("Musisz wybrać jedną z opcji: 5-klasową lub inout.")
        else:
            # Jeśli nie ma błędów, wyczyść komunikaty
            parameters[1].clearMessage()
            parameters[2].clearMessage()
            # Ustawienie komunikatów ostrzegawczych dla parametrów rastrowych
            rastrowe_parametry = {
                3: "GSM",
                4: "UMTS900",
                5: "UMTS2100",
                6: "LTE800",
                7: "LTE900",
                8: "LTE1800",
                9: "LTE2100",
                10: "LTE2600",
                11: "DSS",
                12: "cband",
            }
            additional_string = "5class" if is_5class_validacja else "inout"
            for param_index, expected_string in rastrowe_parametry.items():
                raster_param = parameters[param_index].valueAsText
                if raster_param and (expected_string not in raster_param or additional_string not in raster_param):
                    parameters[param_index].setWarningMessage(f"Raster nie zawiera '{expected_string}' lub '{additional_string}' w nazwie.")


            dominance_parametry = {
                14: "GSM",
                15: "UMTS900",
                16: "UMTS2100",
                17: "LTE800",
                18: "LTE900",
                19: "LTE1800",
                20: "LTE2100",
                21: "LTE2600",
                22: "DSS",
                23: "cband",
            }

            for param_index, expected_string in dominance_parametry.items():
                dom_param = parameters[param_index].valueAsText
                if dom_param and expected_string not in dom_param:
                    parameters[param_index].setWarningMessage(f"Dominance nie zawiera '{expected_string}' w nazwie.")

            # Lista przechowująca ścieżki do warstw, które nie są None ani puste
            warstwy = [
                param.valueAsText for param in parameters[14:24]
                if param.valueAsText is not None and param.valueAsText != ""
            ]

            # Sprawdzenie, czy żadna ścieżka nie jest duplikatem
            if len(warstwy) > len(set(warstwy)):
                # Ustawienie komunikatu o błędzie dla każdego parametru, który jest duplikatem
                unikalne_warstwy = set()
                for i, param in enumerate(parameters[14:24]):
                    warstwa = param.valueAsText
                    if warstwa and warstwa in unikalne_warstwy:
                        param.setErrorMessage("Ta sama warstwa została dodana więcej niż raz.")
                    unikalne_warstwy.add(warstwa)



        return



    def execute(self, parameters, messages):
        """The source code of the tool."""

        arcpy.env.overwriteOutput = True



        plik_wejsciowy = parameters[0].valueAsText





        is_5class = parameters[1].valueAsText  # Zakładając, że to przedostatni parametr
        is_2class = parameters[2].valueAsText  # Zakładając, że to ostatni parametr

        zasieg_gsm = parameters[3].valueAsText
        arcpy.AddMessage(f'wczytanie rastra zasieg_gsm: {zasieg_gsm}')
        zasieg_umts900 = parameters[4].valueAsText
        arcpy.AddMessage(f'wczytanie rastra zasieg_umts900: {zasieg_umts900}')
        zasieg_umts2100 = parameters[5].valueAsText
        arcpy.AddMessage(f'wczytanie rastra zasieg_umts2100: {zasieg_umts2100}')

        zasieg_lte800 = parameters[6].valueAsText
        arcpy.AddMessage(f'wczytanie rastra zasieg_lte800: {zasieg_lte800}')
        zasieg_lte900 = parameters[7].valueAsText
        arcpy.AddMessage(f'wczytanie rastra zasieg_lte900: {zasieg_lte900}')


        zasieg_lte1800 = parameters[8].valueAsText
        arcpy.AddMessage(f'wczytanie rastra zasieg_lte1800: {zasieg_lte1800}')


        zasieg_lte2100 = parameters[9].valueAsText
        arcpy.AddMessage(f'wczytanie rastra zasieg_lte2100: {zasieg_lte2100}')
        zasieg_lte2600 = parameters[10].valueAsText
        arcpy.AddMessage(f'wczytanie rastra zasieg_lte2600: {zasieg_lte2600}')
        zasieg_g5_2100 = parameters[11].valueAsText
        arcpy.AddMessage(f'wczytanie rastra zasieg_g5_2100: {zasieg_g5_2100}')
        zasieg_g5_3600 = parameters[12].valueAsText
        arcpy.AddMessage(f'wczytanie rastra zasieg_g5_3600: {zasieg_g5_3600}')





        lista_rastrow = []

        def dodaj_raster_do_listy(zasieg, nazwa_raster, nazwa_legenda):
            #if zasieg and arcpy.Exists(zasieg):
            if zasieg:
                # Sprawdzenie, czy nazwa rastra zawiera określony ciąg znaków
                if nazwa_legenda in zasieg:  # Używamy nazwa_legenda jako ciągu do wyszukania
                    lista_rastrow.append([zasieg, nazwa_raster])
                    arcpy.AddMessage(f'zasięg: --------------{zasieg}--------------')
                    arcpy.AddField_management(plik_wejsciowy, nazwa_legenda, "TEXT")
                    arcpy.AddMessage(f'Sprawdzenie Rastrow dodanych {lista_rastrow}')
                else:
                    arcpy.AddWarning(f'Raster {zasieg} nie zawiera "{nazwa_legenda}" w nazwie.')

        # Lista nazw i legend dla rastrow
        rastrowe_parametry = [
            (zasieg_gsm, "GSM_raster", "GSM"),
            (zasieg_umts900, "UMTS900_raster", "UMTS900"),
            (zasieg_umts2100, "UMTS2100_raster", "UMTS2100"),
            (zasieg_lte800, "LTE800_raster", "LTE800"),
            (zasieg_lte900, "LTE900_raster", "LTE900"),
            (zasieg_lte1800, "LTE1800_raster", "LTE1800"),

            (zasieg_lte2100, "LTE2100_raster", "LTE2100"),
            (zasieg_lte2600, "LTE2600_raster", "LTE2600"),
            (zasieg_g5_2100, "DSS_raster", "DSS"),
            (zasieg_g5_3600, "cband_raster", "cband"),
            # Dodaj tutaj kolejne parametry, jeśli są dostępne
        ]



        # Iteracja przez listę rastrowych parametrów i dodawanie ich do listy, jeśli istnieją
        for i, (zasieg, nazwa_raster, nazwa_legenda) in enumerate(rastrowe_parametry, start=1):
            arcpy.AddMessage(f'Checking if raster exists: {zasieg}')
            dodaj_raster_do_listy(zasieg, nazwa_raster, nazwa_legenda)


        # Wykonanie ExtractMultiValuesToPoints tylko jeśli lista_rastrow nie jest pusta
        if lista_rastrow:
            arcpy.sa.ExtractMultiValuesToPoints(plik_wejsciowy, lista_rastrow, "NONE")
#         else:
#             arcpy.AddWarning("Nie dodano żadnych rastrow do analizy.")


        # Ustaw workspace
        # Ekstrahuj wartości do punktów
        # ExtractMultiValuesToPoints(plik_wejsciowy, lista_rastrow, "NONE")









        lista_kolumn = arcpy.ListFields(plik_wejsciowy)

        # Inicjalizuj pustą listę par
        pary_pol = []
        # Iteruj przez kolumny i szukaj par



        for kolumna in lista_kolumn:

            for prefix in ["GSM", "UMTS2100", "UMTS900", "LTE800", "LTE900", "LTE1800", "LTE2100", "LTE2600",
                           "DSS", "cband"]:
                #arcpy.AddMessage(f'tu sprawdzam')
                #if kolumna.name.startswith(prefix):
                if kolumna.name.startswith(f"{prefix}_raster"):
                    arcpy.AddMessage(kolumna.name.startswith(f"{prefix}_raster"))
                    pola_do_uzupelnienia_przez_kursor = [f"{prefix}_raster", f"{prefix}"]
                    para = {"raster_prefix": prefix, "Para": pola_do_uzupelnienia_przez_kursor}
                    #arcpy.AddMessage(f'{para}')
                    pary_pol.append(para)
                    #arcpy.AddMessage(f'{pary_pol}')
                    break

        # print(pary_pol)
        # Przypisz odpowiednie wartości do nowych pól w zależności od wartości w kolumnie


        if is_5class == 'true':
            arcpy.AddMessage(f'is_5class == true')
            for para in pary_pol:
                with arcpy.da.UpdateCursor(plik_wejsciowy, para["Para"]) as cursor:
                    arcpy.AddMessage(f'Przypisanie -- outdoor, in-car, indoor, deep indoor, very deep indoor-- dla pary: {para["Para"]}')
                    for row in cursor:
                        if row[0] == 1:
                            row[1] = "outdoor"
                        elif row[0] == 2:
                            row[1] = "in-car"
                        elif row[0] == 3:
                            row[1] = "indoor"
                        elif row[0] == 4:
                            row[1] = "deep indoor"
                        elif row[0] == 5:
                            row[1] = "very deep indoor"
                        else:

                            row[1] = "Brak"
                        cursor.updateRow(row)

        if is_2class == 'true':
            arcpy.AddMessage(f'is_2class == true')
            for para in pary_pol:
                with arcpy.da.UpdateCursor(plik_wejsciowy, para["Para"]) as cursor:
                    for row in cursor:
                        if row[0] == 1:
                            row[1] = "outdoor"
                        elif row[0] == 2:
                            row[1] = "indoor"

                        else:
                            row[1] = "Brak"
                        cursor.updateRow(row)



        workspace_z_parametru = parameters[13].valueAsText
        arcpy.env.workspace = workspace_z_parametru


        #Define parameters
        komorki_gsm = parameters[14].valueAsText
        komorki_umts900 = parameters[15].valueAsText
        komorki_umts2100 = parameters[16].valueAsText
        komorki_lte800 = parameters[17].valueAsText
        komorki_lte900 = parameters[18].valueAsText
        komorki_lte1800 = parameters[19].valueAsText
        komorki_lte2100 = parameters[20].valueAsText
        komorki_lte2600 = parameters[21].valueAsText

        komorki_5g2100 = parameters[22].valueAsText
        komorki_5g3600 = parameters[23].valueAsText

        Dodatkowa_warstwa = parameters[24].valueAsText

        def dodaj_pola(plik_wejsciowy, komorki, nazwa_LOC_NAME, nazwa_LOC_OBJ, nazwa_CELL_NAME,nazwa_CELL_OBJ):

            if komorki:
                arcpy.AddField_management(plik_wejsciowy, nazwa_LOC_NAME, "TEXT")
                arcpy.AddField_management(plik_wejsciowy, nazwa_LOC_OBJ, "Long")
                arcpy.AddField_management(plik_wejsciowy, nazwa_CELL_NAME, "TEXT")
                arcpy.AddField_management(plik_wejsciowy, nazwa_CELL_OBJ, "Long")


        # Use the function for each set of parameters
        dodaj_pola(plik_wejsciowy, komorki_gsm, "LOC_NAME_GSM", "LOC_OBJ_GSM", "CELL_NAME_GSM","CELL_OBJ_GSM")
        dodaj_pola(plik_wejsciowy, komorki_umts900, "LOC_NAME_UMTS_2100", "LOC_OBJ_UMTS_2100", "WCELL_NAME_UMTS_2100", "WCELL_OBJ_UMTS_2100")
        dodaj_pola(plik_wejsciowy, komorki_umts2100, "LOC_NAME_UMTS_900", "LOC_OBJ_UMTS_900", "WCELL_NAME_UMTS_900", "WCELL_OBJ_UMTS_900")
        dodaj_pola(plik_wejsciowy, komorki_lte800, "LOC_NAME_LTE_800", "LOC_OBJ_LTE_800", "LCELL_NAME_LTE_800", "LCELL_OBJ_LTE_800")
        dodaj_pola(plik_wejsciowy, komorki_lte900, "LOC_NAME_LTE_900", "LOC_OBJ_LTE_900","LCELL_NAME_LTE_900", "LCELL_OBJ_LTE_900")
        dodaj_pola(plik_wejsciowy, komorki_lte1800, "LOC_NAME_lTE_1800", "LOC_OBJ_lTE_1800","LCELL_NAME_lTE_1800", "LCELL_OBJ_lTE_1800")
        dodaj_pola(plik_wejsciowy, komorki_lte2600, "LOC_NAME_LTE_2600", "LOC_OBJ_LTE_2600","LCELL_NAME_LTE_2600", "LCELL_OBJ_LTE_2600")
        dodaj_pola(plik_wejsciowy, komorki_lte2100, "LOC_NAME_LTE_2100", "LOC_OBJ_LTE_2100","LCELL_NAME_LTE_2100", "LCELL_OBJ_LTE_2100")
        dodaj_pola(plik_wejsciowy, komorki_5g2100, "LOC_NAME_5G_2100_DSS", "LOC_OBJ_5G_2100", "GCELL_NAME_5G_2100", "GCELL_OBJ_5G_2100")
        dodaj_pola(plik_wejsciowy, komorki_5g3600, "LOC_NAME_5G_3600", "LOC_OBJ_5G_3600","GCELL_NAME_5G_3600", "GCELL_OBJ_5G_3600")

#
#         # TO SĄ TAKIE JAKIE MUSZA BYĆ -  fields_to_extract_zrodlo
#         def przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, warstwa_zrodlowa, warstwa_docelowa, fields_to_extract_zrodlo,
#                                          fields_to_extract):
#             if warstwa_zrodlowa:
#                 arcpy.env.overwriteOutput = True
#                 arcpy.SpatialJoin_analysis(plik_wejsciowy, warstwa_zrodlowa, warstwa_docelowa)



        def przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, warstwa_zrodlowa, fields_to_extract_zrodlo, fields_to_extract_docelowe):
            arcpy.env.overwriteOutput = True
            if warstwa_zrodlowa:
                # Wykonaj Spatial Join i zapisz wynik w pamięci
                joined_layer = arcpy.SpatialJoin_analysis(plik_wejsciowy, warstwa_zrodlowa, "in_memory/joined_layer", "JOIN_ONE_TO_ONE", "KEEP_ALL")[0]

    #             # Dodaj brakujące pola do warstwy wejściowej, jeśli nie istnieją
    #             for dest_field in fields_to_extract_docelowe:
    #                 if len(arcpy.ListFields(plik_wejsciowy, dest_field)) == 0:SummarizeWithin_layer_1
    #                     arcpy.AddField_management(plik_wejsciowy, dest_field, "TEXT")

                # Przepisz wartości z pól wynikowych Spatial Join do pól wejściowych
                with arcpy.da.UpdateCursor(plik_wejsciowy, fields_to_extract_docelowe + ["OBJECTID"]) as cursor_wejsciowy:
                    for row in cursor_wejsciowy:
                        objectid = row[-1]  # OBJECTID z warstwy wejściowej
                        with arcpy.da.SearchCursor(joined_layer, fields_to_extract_zrodlo + ["TARGET_FID"]) as cursor_zrodlowy:
                            for row_zrodlowy in cursor_zrodlowy:
                                if row_zrodlowy[-1] == objectid:  # Porównaj TARGET_FID z OBJECTID
                                    for i, src_field in enumerate(fields_to_extract_zrodlo):
                                        dest_field = fields_to_extract_docelowe[i]
                                        dest_index = cursor_wejsciowy.fields.index(dest_field)
                                        row[dest_index] = row_zrodlowy[i]  # Przepisz wartość
                                    cursor_wejsciowy.updateRow(row)  # Aktualizuj wiersz w warstwie wejściowej
                                    break

#         # Przykład użycia funkcji
#         przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, komorki_lte900,
#                                               ["LOC_NAME", "LOC_OBJ", "LCELL_NAME", "LCELL_OBJ"],
#                                               ["LOC_NAME_LTE_900", "LOC_OBJ_LTE_900", "LCELL_NAME_LTE_900", "LCELL_OBJ_LTE_900"])

        przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, komorki_gsm,
                                     ["LOC_NAME", "LOC_OBJ", "CELL_NAME", "CELL_OBJ"],
                                     ["LOC_NAME_GSM", "LOC_OBJ_GSM", "CELL_NAME_GSM", "CELL_OBJ_GSM"])

        przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, komorki_umts900,
                                     ["LOC_NAME", "LOC_OBJ", "WCELL_NAME", "WCELL_OBJ"],
                                     ["LOC_NAME_UMTS_2100", "LOC_OBJ_UMTS_2100", "WCELL_NAME_UMTS_2100",
                                      "WCELL_OBJ_UMTS_2100"])

        przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, komorki_umts2100,
                                     ["LOC_NAME", "LOC_OBJ", "WCELL_NAME", "WCELL_OBJ"],
                                     ["LOC_NAME_UMTS_900", "LOC_OBJ_UMTS_900", "WCELL_NAME_UMTS_900",
                                      "WCELL_OBJ_UMTS_900"])

        przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, komorki_lte800,
                                     ["LOC_NAME", "LOC_OBJ", "LCELL_NAME", "LCELL_OBJ"],
                                     ["LOC_NAME_LTE_800", "LOC_OBJ_LTE_800", "LCELL_NAME_LTE_800", "LCELL_OBJ_LTE_800"])

        przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, komorki_lte900,
                                     ["LOC_NAME", "LOC_OBJ", "LCELL_NAME", "LCELL_OBJ"],
                                     ["LOC_NAME_LTE_900", "LOC_OBJ_LTE_900", "LCELL_NAME_LTE_900", "LCELL_OBJ_LTE_900"])

        przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, komorki_lte1800,
                                     ["LOC_NAME", "LOC_OBJ", "LCELL_NAME", "LCELL_OBJ"],
                                     ["LOC_NAME_lTE_1800", "LOC_OBJ_lTE_1800", "LCELL_NAME_lTE_1800",
                                      "LCELL_OBJ_lTE_1800"])

        przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, komorki_lte2600,
                                     ["LOC_NAME", "LOC_OBJ", "LCELL_NAME", "LCELL_OBJ"],
                                     ["LOC_NAME_LTE_2600", "LOC_OBJ_LTE_2600", "LCELL_NAME_LTE_2600",
                                      "LCELL_OBJ_LTE_2600"])

        przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, komorki_lte2100,
                                     ["LOC_NAME", "LOC_OBJ", "LCELL_NAME", "LCELL_OBJ"],
                                     ["LOC_NAME_LTE_2100", "LOC_OBJ_LTE_2100", "LCELL_NAME_LTE_2100",
                                      "LCELL_OBJ_LTE_2100"])


        przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, komorki_5g2100,
                                     ["LOC_NAME", "LOC_OBJ", "GCELL_NAME", "GCELL_OBJ"],
                                     ["LOC_NAME_5G_2100_DSS", "LOC_OBJ_5G_2100", "GCELL_NAME_5G_2100",
                                      "GCELL_OBJ_5G_2100"])

        przepisz_wartosci_joina_do_nowych_pol(plik_wejsciowy, komorki_5g3600,
                                     ["LOC_NAME", "LOC_OBJ", "GCELL_NAME", "GCELL_OBJ"],
                                     ["LOC_NAME_5G_3600", "LOC_OBJ_5G_3600", "GCELL_NAME_5G_3600", "GCELL_OBJ_5G_3600"])


        def przepisz_wartosci_joina_do_nowych_pol_extra(plik_wejsciowy, warstwa_zrodlowa, wynik_SpatialJoin):
            arcpy.env.overwriteOutput = True
            if Dodatkowa_warstwa:
                arcpy.AddMessage(f'przepisz_wartosci_joina_do_nowych_pol_extra')


                arcpy.SpatialJoin_analysis(plik_wejsciowy, warstwa_zrodlowa, wynik_SpatialJoin, "JOIN_ONE_TO_ONE")
        opis_warstwy = arcpy.Describe(plik_wejsciowy)
       #arcpy.AddMessage(f'{opis_warstwy.name}_warstwa_dodatkowa')
        przepisz_wartosci_joina_do_nowych_pol_extra(plik_wejsciowy, Dodatkowa_warstwa, f'{opis_warstwy.name}_warstwa_dodatkowa')



        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return