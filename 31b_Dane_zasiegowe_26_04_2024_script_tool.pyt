# -*- coding: utf-8 -*-

import arcpy
import os
from arcpy import sa

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Tool"
        self.alias = "Tool"

        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Dane zasiegowe by Daniel Buchar new"
        self.description = "Dane zasiegowe new"
        self.canRunInBackground = False


# getParameterInfo #############################################################################################################################################################################################################################################
    def getParameterInfo(self):
        """Define parameter definitions"""




        wczytanie_danych = arcpy.Parameter(
            displayName="Ścieżka do folderu z danymi zasięgowymi - GSM, UMTS, LTE, 5G, rastry  (Odszukaj - Folder - Input)",
            name="wczytanie_danych",
            datatype="DEFolder",
            parameterType="Optional",
            direction="Input"
        )

        checkbox_gsm = arcpy.Parameter(
            displayName="Dominance - GSM",
            name="checkbox_gsm",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        checkbox_umts = arcpy.Parameter(
            displayName="Dominance - UMTS",
            name="checkbox_umts",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        checkbox_lte = arcpy.Parameter(
            displayName="Dominance - LTE",
            name="checkbox_lte",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        checkbox_dss = arcpy.Parameter(
            displayName="Dominance - 5G DSS",
            name="checkbox_dss",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        checkbox_cband = arcpy.Parameter(
            displayName="Dominance - 5G CBAND",
            name="checkbox_cband",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        path_92 = arcpy.Parameter(
            displayName="PUWG 92 (Odszukaj - File prj - Input)",
            name="path_92",
            datatype="DEFile",
            parameterType="Optional",
            direction="Input",
        )

        path_tabela_gsm = arcpy.Parameter(
            displayName="Tabela - GSM (Odszukaj cell - Feature class - Input)",
            name="path_tabela_gsm",
            datatype="DETable",
            parameterType="Optional",
            direction="Input"
        )

        path_tabela_umts = arcpy.Parameter(
            displayName="Tabela - UMTS (Odszukaj wcell - Feature class - Input)",
            name="path_tabela_umts",
            datatype="DETable",
            parameterType="Optional",
            direction="Input"
        )

        path_tabela_lte = arcpy.Parameter(
            displayName="Tabela - LTE (Odszukaj lcell - Feature class - Input)",
            name="path_tabela_lte",
            datatype="DETable",
            parameterType="Optional",
            direction="Input"
        )

        path_tabela_dss_cband = arcpy.Parameter(
            displayName="Tabela - 5G DSS / 5G CBAND (Odszukaj gcell - Feature class - Input)",
            name="join_table_gcell",
            datatype="DETable",
            parameterType="Optional",
            direction="Input"
        )

        _output_info_ = arcpy.Parameter(
            displayName="Geobaza info (Utwórz nową - Geodatabase - Input - Backup)",
            name="_output_info_",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )

        _output_MV_ = arcpy.Parameter(
            displayName="Geobaza MV (Utwórz nową - Geodatabase - Input - Result)",
            name="_output_MV_",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )

        checkbox_przeciazenia = arcpy.Parameter(
            displayName="Przeciazenia (warunek: dominance w geobazie MV oraz połączenie do geobaza SDE)",
            name="checkbox_przeciazenia",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )

        path_sde = arcpy.Parameter(
            displayName="Geobaza SDE (Odszukaj - SDE Geodatabase - Input)",
            name="path_sde",
            datatype="DEWorkspace",
            parameterType="Optional",
            direction="Input"
        )



        checkbox_piramidy = arcpy.Parameter(
            displayName="Piramidy oraz geobaze w układzie 3857 (rastry wejsciowe muszą mieć nadany układ)",
            name="checkbox_piramidy",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )


        output_3857 = arcpy.Parameter(
            displayName="Geobaza 3857 (Utwórz nową - Geodatabase - Input)",
            name="_output_3857_",
            datatype="DEWorkspace",
            parameterType="Optional",
            direction="Input"
        )

        path_wgs84 = arcpy.Parameter(
            displayName="WGS 1984 Web Mercator 3857 (Odszukaj - File prj)",
            name="path_wgs84",
            datatype="DEFile",
            parameterType="Optional",
            direction="Input"
        )



#         wczytanie_danych.value = r'D:\ArcGIS\0_Dane_Zasiegowe_DONE\2024_03\Paczka'
#         checkbox_gsm.value = True
#         checkbox_umts.value = True
#         checkbox_lte.value = True
#         checkbox_dss.value = True
#         checkbox_cband.value = True
        path_92.value = r'D:\ArcGIS\projections\PUWG_92.prj'
#         path_tabela_gsm.value = r'D:\ArcGIS\0_Dane_Zasiegowe_DONE\2024_03\31B_SKRYPT\MV.gdb\cell_202403'
#
#         path_tabela_umts.value = r'D:\ArcGIS\0_Dane_Zasiegowe_DONE\2024_03\31B_SKRYPT\MV.gdb\wcell_202403'
#         path_tabela_lte.value = r'D:\ArcGIS\0_Dane_Zasiegowe_DONE\2024_03\31B_SKRYPT\MV.gdb\lcell_202403'
#         path_tabela_dss_cband.value = r'D:\ArcGIS\0_Dane_Zasiegowe_DONE\2024_03\31B_SKRYPT\MV.gdb\dss_cband_202403'
#         _output_info_.value = r'D:\ArcGIS\0_Dane_Zasiegowe_DONE\2024_03\31B_SKRYPT\INFO.gdb'
#         _output_MV_.value = r'D:\ArcGIS\0_Dane_Zasiegowe_DONE\2024_03\31B_SKRYPT\MV.gdb'
        path_wgs84.value = r'D:\ArcGIS\projections\WGS 1984 Web Mercator (auxiliary sphere).prj'
#         output_3857.value = r'D:\ArcGIS\0_Dane_Zasiegowe_DONE\2024_03\31B_SKRYPT\DANE_3857.gdb'


        params = [wczytanie_danych, checkbox_gsm, checkbox_umts, checkbox_lte, checkbox_dss, checkbox_cband, path_92, path_tabela_gsm, path_tabela_umts, path_tabela_lte, path_tabela_dss_cband, _output_info_, _output_MV_, checkbox_przeciazenia, path_sde, checkbox_piramidy, path_wgs84, output_3857]


        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

#     def assign_parameters(self, parameters):
#         for i in range(len(parameters)):
#             setattr(self, f'param_{i}_value', parameters[i].value)
#             setattr(self, f'param_{i}', parameters[i])
#
# updateMessages #############################################################################################################################################################################################################################################
#     def updateMessages(self, parameters):
#         """Modify the messages created by internal validation for each tool
#         parameter.  This method is called after internal validation."""
#
#         self.assign_parameters(parameters)
#
#         # Sprawdzenie, czy wszystkie opcje zostały wybrane
#         if all(getattr(self, f'param_{i}_value') for i in [1, 2, 3, 10, 12, 17, 22]):
#             # Jeśli wszystkie opcje są zaznaczone, nie ustawiaj żadnych komunikatów
#             for i in [1, 2, 3, 10, 12, 17, 22]:
#                 getattr(self, f'param_{i}').clearMessage()
#         else:
#             # Sprawdzanie pojedynczych opcji i ustawianie odpowiednich komunikatów
#             for i in [1, 2, 3, 10, 12, 17, 22]:
#                 param = getattr(self, f'param_{i}')
#                 if param.value:
#                     param.setWarningMessage(f"Opcja {param.displayName} została wybrana.")
#                 else:
#                     param.clearMessage()
#         return


# updateMessages #############################################################################################################################################################################################################################################

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

#         param_1_value = parameters[1].value
#         param_2_value = parameters[2].value
#         param_3_value = parameters[3].value
#         param_10_value = parameters[10].value
#         param_12_value = parameters[12].value
#         param_17_value = parameters[17].value
#         param_22_value = parameters[22].value
#
#
#         param_1 = parameters[1]
#         param_2 = parameters[2]
#         param_3 = parameters[3]
#         param_10 = parameters[10]
#         param_12 = parameters[12]
#         param_17 = parameters[17]
#         param_22 = parameters[22]



#         # Sprawdzenie, czy wszystkie opcje zostały wybrane
#         if param_1_value and param_2_value and param_3_value and param_10_value and param_12_value and param_17_value and param_22_value:
#             # Jeśli wszystkie opcje są zaznaczone, nie ustawiaj żadnych komunikatów
#             for param in [param_1, param_3, param_12, param_22]:
#                 param.clearMessage()
#         else:
#             # Sprawdzanie pojedynczych opcji i ustawianie odpowiednich komunikatów
#             for param in [param_1, param_2, param_3, param_10, param_12, param_17, param_22]:
#                 if param.value:
#                     param.setWarningMessage(f"Opcja {param.displayName} została wybrana.")
#                 else:
#                     param.clearMessage()
        return



####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################################################

    def process_dominance(self, output_info, output_MV, _path_92_,
                            _checkbox_gsm_, lista_GSM, _path_tabela_gsm_,
                            _checkbox_umts_, lista_UMTS, _path_tabela_umts_,
                            _checkbox_lte_, lista_LTE, _path_tabela_lte_,
                            _checkbox_dss_, lista_DSS, _checkbox_cband_, lista_CBAND, _path_tabela_dss_cband_):

        if _checkbox_gsm_:
            arcpy.AddMessage('---------------------- CZESCI III - GSM ----------------------')
            self.process_technology(lista_GSM, _path_tabela_gsm_, output_info, output_MV, _path_92_, 'GSM', 'C')

        if _checkbox_umts_:
            arcpy.AddMessage('---------------------- CZESCI II - UMTS----------------------')
            self.process_technology(lista_UMTS, _path_tabela_umts_, output_info, output_MV, _path_92_, 'UMTS','WC')

        if _checkbox_lte_:
            arcpy.AddMessage('---------------------- CZESCI I - LTE ----------------------')
            self.process_technology(lista_LTE, _path_tabela_lte_, output_info, output_MV, _path_92_, 'LTE','LC')

        if _checkbox_dss_:
            arcpy.AddMessage('---------------------- CZESCI IV - DSS ----------------------')
            self.process_technology(lista_DSS, _path_tabela_dss_cband_, output_info, output_MV, _path_92_, 'DSS', 'LC')

        if _checkbox_cband_:
            arcpy.AddMessage('---------------------- CZESCI V - CBAND ----------------------')
            self.process_technology(lista_CBAND, _path_tabela_dss_cband_, output_info, output_MV, _path_92_, 'CBAND', 'GC')




    def process_technology(self, lista_sciezek, join_table, output_info, output_MV, _path_92_, technology, letter):
        nazwy_plikow = []

        for index, sciezka in enumerate(lista_sciezek):


            nazwa_pliku = os.path.basename(sciezka)
            nazwa_bez_rozszerzenia, _ = os.path.splitext(nazwa_pliku)
            nazwy_plikow.append(nazwa_bez_rozszerzenia)


            if technology in ['GSM', 'UMTS', 'LTE']:

                arcpy.management.AddField(lista_sciezek[index], "objj", "Long")
                arcpy.management.CalculateField(lista_sciezek[index], "objj", '!C_CELL_OBJ!', "PYTHON3")
                arcpy.AddMessage(f'f{lista_sciezek[index]}')

                wynik_1 = arcpy.management.AddJoin(lista_sciezek[index], "objj", join_table, f"{letter[:]}ELL_OBJ")

                output_feature_class_info_name = f'{nazwy_plikow[index]}_info'
                arcpy.conversion.FeatureClassToFeatureClass(wynik_1, output_info, output_feature_class_info_name)

                output_feature_class_MV_name = f'{nazwy_plikow[index]}_MV'
                arcpy.env.outputCoordinateSystem = _path_92_
                arcpy.conversion.FeatureClassToFeatureClass(wynik_1, output_MV, output_feature_class_MV_name)

                path_output_feature_class_MV = os.path.join(output_MV, f'{nazwy_plikow[index]}_MV')
                pola_do_zachowania = self.get_fields_to_keep(technology)
                pola_do_usuniecia = self.get_fields_to_remove(path_output_feature_class_MV, pola_do_zachowania)

                arcpy.management.AddField(path_output_feature_class_MV, "styl", "SHORT")
                self.update_field_styl(path_output_feature_class_MV, f"{letter[:]}ELL_NAME", "styl")

            def remove_after_hash(value):
                return value.split('#')[0] if '#' in value else value

            #przez to, ze dostajemy rozne dane to kolumny sie czasami roznia przewqaznie jest to TX_ID ale zdarzają się wyjątki
            def get_column_name(table, possible_names):
                for name in possible_names:
                    if name in [field.name for field in arcpy.ListFields(table)]:
                        arcpy.AddMessage(f'pola - sprawdzanie czy jest TX_ID CZY Transmitte')
                        arcpy.AddMessage(f'Tym razem masz dla warstwy shp C-BANDA lub DSS kolumne o nazwie: {name}')
                        return name
                return None

            possible_column_names = ["TX_ID", "Transmitte"]

            if technology in ['DSS', 'CBAND']:
                field_type = "TEXT" if technology == 'DSS' else "Long"
                arcpy.management.AddField(lista_sciezek[index], "objj", field_type)


                column_name = get_column_name(lista_sciezek[index], possible_column_names)
                if technology == 'DSS':
                    arcpy.management.CalculateField(
                        lista_sciezek[index],
                        "objj",
                        f"remove_after_hash(!{column_name}!)",
                        "PYTHON3",
                        code_block="""def remove_after_hash(value):
                            return value.split('#')[0] if '#' in value else value"""
                    )
                    join_field = f"{letter[:]}ELL_NAME"
                else:  # CBAND
                    arcpy.management.CalculateField(lista_sciezek[index], "objj", '!C_XCELL_OB!', "PYTHON3")
                    join_field = f"{letter[:]}ELL_OBJ"

                wynik_2 = arcpy.management.AddJoin(lista_sciezek[index], "objj", join_table, join_field)

                arcpy.conversion.FeatureClassToFeatureClass(wynik_2, output_info, f'{nazwy_plikow[index]}_info')
                arcpy.env.outputCoordinateSystem = _path_92_
                arcpy.conversion.FeatureClassToFeatureClass(wynik_2, output_MV, f'{nazwy_plikow[index]}_MV')

            if technology == 'DSS':
                arcpy.AddMessage('---------------------- Cześć robiona tylko dla DSS - tworzenie maski DSS ----------------------')
                self.DSS_create_mask(output_info, output_MV, f'{nazwy_plikow[index]}_info')

                arcpy.env.workspace = output_info
                maska_DSS = arcpy.ListFeatureClasses('*_maska*')
                arcpy.AddMessage(f'Tworzenie maski')
                arcpy.AddMessage(f'{output_info}\\{nazwy_plikow[index]}_info')
                arcpy.AddMessage(f'{output_info}\\{maska_DSS[0]}')
                arcpy.AddMessage(f'{output_MV}\\{nazwy_plikow[index]}_MV')
                arcpy.AddMessage('---------------------- Clip DSS - To może troche zająć ... zaczekaj  ----------------------')
                arcpy.analysis.Clip(f'{output_info}\\{nazwy_plikow[index]}_info', f'{output_info}\\{maska_DSS[0]}', f'{output_MV}\\{nazwy_plikow[index]}_MV')

            path_output_feature_class_MV = os.path.join(output_MV, f'{nazwy_plikow[index]}_MV')
            pola_do_zachowania = self.get_fields_to_keep(technology)
            pola_do_usuniecia = self.get_fields_to_remove(path_output_feature_class_MV, pola_do_zachowania)

            arcpy.management.AddField(path_output_feature_class_MV, "styl", "SHORT")
            self.update_field_styl(path_output_feature_class_MV, f"{letter[:]}ELL_NAME", "styl")




            # 3857
            if pola_do_usuniecia:
                arcpy.management.DeleteField(path_output_feature_class_MV, pola_do_usuniecia)
                arcpy.AddMessage(f'Kasowanie pol - done')
            arcpy.AddMessage(f'Done: {nazwy_plikow[index]}_info')
            arcpy.AddMessage(f'Done: {nazwy_plikow[index]}_MV')



    def get_fields_to_keep(self, technology):
        if technology == 'GSM':
            return ['OBJECTID_1', 'Shape', 'LOC_NAME', 'LOC_OBJ', 'LOC_CODE', 'SITE_NAME', 'SITE_OBJ', 'SITE_CODE', 'CELL_NAME', 'CELL_OBJ', 'CELL_CODE', 'LAC', 'BAND', 'BCCH_CHAN', 'BCC', 'NCC', 'Shape_Length', 'Shape_Area', 'styl']
        elif technology == 'UMTS':
            return ['OBJECTID_1', 'Shape', 'LOC_NAME', 'LOC_OBJ', 'LOC_CODE', 'WSITE_NAME', 'WSITE_OBJ', 'WSITE_ID', 'WCELL_NAME', 'WCELL_OBJ', 'WCELL_CODE', 'LAC', 'BAND', 'PSC', 'Shape_Length', 'Shape_Area', 'styl']
        elif technology == 'LTE':
            return ['OBJECTID_1', 'Shape', 'LOC_OBJ', 'LOC_CODE', 'LSITE_NAME', 'LSITE_OBJ', 'LSITE_ID', 'LCELL_NAME', 'LCELL_OBJ', 'LCELL_ID', 'NAME', 'PCI', 'Shape_Length', 'Shape_Area', 'styl']
        elif technology == "DSS":
            return ['OBJECTID_1', 'Shape', 'LOC_OBJ', 'LOC_CODE', 'GSITE_NAME', 'GSITE_OBJ', 'GSITE_ID', 'GCELL_NAME', 'GCELL_OBJ', 'GCELL_ID', 'LTE2100_SHARED', 'LCELL_NAME', 'LOC_NAME', 'Shape_Length', 'Shape_Area', 'styl']
        elif technology == "CBAND":
            return ['OBJECTID_1', 'Shape', 'LOC_OBJ', 'LOC_CODE', 'GSITE_NAME', 'GSITE_OBJ', 'GSITE_ID', 'GCELL_NAME', 'GCELL_OBJ', 'GCELL_ID', 'NAME', 'PCI', 'Shape_Length', 'Shape_Area', 'styl']
        else:
            return []

########################### nie kasować ############################################
    #STARA - DZIALA ALE DLA CBAND zostawia pole LCELL_NAME
    def get_fields_to_remove(self, path_feature_class, pola_do_zachowania):
        pola_do_usuniecia = []
        lista_pól = arcpy.ListFields(path_feature_class)
        for pole in lista_pól:
            if not any(fraza in pole.name for fraza in pola_do_zachowania):
                pola_do_usuniecia.append(pole.name)
        return pola_do_usuniecia
########################### nie kasować ############################################

#     # NOWA - DO PRZETESTOWANIA - dokładnie takie same nazwy kolumn
#     def get_fields_to_remove(self, path_feature_class, pola_do_zachowania):
#         pola_do_usuniecia = []
#         lista_pól = arcpy.ListFields(path_feature_class)
#         for pole in lista_pól:
#             if pole.name not in pola_do_zachowania:
#                 pola_do_usuniecia.append(pole.name)
#         return pola_do_usuniecia


    def update_field_styl(self, feature_class, field_name, new_field_name):
        with arcpy.da.UpdateCursor(feature_class, [field_name, new_field_name]) as cursor:
            for row in cursor:
                field_value, new_field_value = row[0], row[1]
                if field_value is None:
                    new_field_value = 0
                else:
                    parts = field_value.split('_')
                    #arcpy.AddMessage(f'parts: {parts}')
                    if len(parts) > 1:
                        last_part = parts[0]
                        if len(last_part) >= 2:
                            extracted_chars = last_part[-2]
                            new_field_value = extracted_chars
                            #arcpy.AddMessage(f'new_field_value: {new_field_value}')
                row[1] = new_field_value
                cursor.updateRow(row)


    def DSS_create_mask(self, output_info, output_MV,output_feature_class_info_name):
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = output_MV
        arcpy.AddMessage(f'-------------------------------')
        arcpy.AddMessage(f'-------------------------------')
        arcpy.AddMessage(f'Ścieżka do wybrania skad maja być brane dominance LTE w celu utworzenia maski - 5G DSS: {output_MV}')
        lista_LTE = arcpy.ListFeatureClasses('*M_LTE800*') + arcpy.ListFeatureClasses('*M_LTE1800*') + arcpy.ListFeatureClasses('*M_LTE2600*')
        arcpy.AddMessage(f'-------------------------------')
        arcpy.AddMessage(f'-------------------------------')


        #arcpy.AddMessage(f'lista LTE do stworzenia maski - 5G DSS: {lista_LTE}')
        if len(lista_LTE[:]) != 0:
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'lista LTE do stworzenia maski - 5G DSS: {lista_LTE}')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')
        else:
            arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            arcpy.AddMessage(f'lista LTE do stworzenia maski - 5G DSS jest pusata: {lista_LTE}')
            arcpy.AddMessage(f'!!!!!!!!!!!!!UWAGA!!!!!!!!!!!!!1204')
            arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Wykonaj dominance dla LTE800, LTE1800 oraz LTE2600')
            arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            arcpy.AddMessage(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


        for x in lista_LTE:

            arcpy.AddMessage(f'Parametry do AddJoin zeby wyrać takie dominance LTE, których LOC_OBJ jest równy LOC_OBJ warstwy DSS')
            arcpy.AddMessage(f'parametr 1: {x}')
            arcpy.AddMessage(f'parametr 2: LOC_OBJ')
            arcpy.AddMessage(f'{output_feature_class_info_name}')
            arcpy.AddMessage(f'parametr 4: LOC_OBJ')

            #arcpy.env.workspace = output_info
            wynik_0 = arcpy.management.AddJoin(x, "LOC_OBJ", f'{output_info}//{output_feature_class_info_name}', "LOC_OBJ", join_type='KEEP_COMMON')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------1256')


            arcpy.conversion.FeatureClassToFeatureClass(wynik_0, output_info, f'{x}_join')


        arcpy.env.workspace = output_info
        lista_LTE_marge = arcpy.ListFeatureClasses('*_join*')


        if len(lista_LTE_marge) != 0:
            arcpy.management.Merge(lista_LTE_marge, "in_memory/output_Merge")
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------1275')
            arcpy.AddMessage(f'lista klas obiektow do zrobienia maski: {lista_LTE_marge}')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')



            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.conversion.FeatureClassToFeatureClass("in_memory/output_Merge", output_info, f'{output_feature_class_info_name}_maska')
            arcpy.AddMessage(f'Maska zapisana w --------- {output_info} --------- o nazwie: --------- {output_feature_class_info_name}_maska ---------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')

    def has_coordinate_system(self, raster_path):
        desc = arcpy.Describe(raster_path)
        return desc.spatialReference is not None

# execute #############################################################################################################################################################################################################################################
    def execute(self, parameters, messages):
        """The source code of the tool."""


        _wczytanie_danych_ = parameters[0].valueAsText
        _checkbox_gsm_ =  parameters[1].value
        _checkbox_umts_ = parameters[2].value
        _checkbox_lte_ = parameters[3].value
        _checkbox_dss_ = parameters[4].value
        _checkbox_cband_ = parameters[5].value
        _path_92_ = parameters[6].valueAsText
        _path_tabela_gsm_ = parameters[7].valueAsText
        _path_tabela_umts_ = parameters[8].valueAsText
        _path_tabela_lte_ = parameters[9].valueAsText
        _path_tabela_dss_cband_= parameters[10].valueAsText
        output_info = parameters[11].valueAsText
        output_MV = parameters[12].valueAsText
        _checkbox_przeciazenia_ = parameters[13].value
        _path_sde_ = parameters[14].valueAsText
        _checkbox_piramidy_ = parameters[15].value
        _path_wgs84_ = parameters[16].valueAsText
        _output_3857_ = parameters[17].valueAsText



# DOMINANCE #############################################################################################################################################################################################################################################

        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = _wczytanie_danych_


        lista_GSM = []
        lista_UMTS = []
        lista_LTE = []
        lista_DSS = []
        lista_CBAND = []
        for folder, subfolders, files in arcpy.da.Walk(arcpy.env.workspace, datatype="FeatureClass"):
            for file in files:

                if _checkbox_gsm_ and 'GSM' in file:
                    lista_GSM.append(os.path.join(folder, file))
                if _checkbox_umts_ and 'UMTS' in file:
                    lista_UMTS.append(os.path.join(folder, file))
                if _checkbox_lte_ and 'LTE' in file:
                    lista_LTE.append(os.path.join(folder, file))
                if _checkbox_dss_ and 'DSS' in file:
                    lista_DSS.append(os.path.join(folder, file))
                if _checkbox_cband_ and 'CBAND' in file:
                    lista_CBAND.append(os.path.join(folder, file))


        arcpy.AddMessage(f'---------------------- START - CZESCI I - Wczytanie danych ----------------------')
        arcpy.AddMessage(f'---------------------------------------------------------------------------------')
        arcpy.AddMessage(f'---------------------------------------------------------------------------------')
        arcpy.AddMessage(f'Dane wejsciowe GSM:---------------------- {lista_GSM} ----------------------')
        arcpy.AddMessage(f'Dane wejsciowe UMTS:---------------------- {lista_UMTS} ----------------------')
        arcpy.AddMessage(f'Dane wejsciowe LTE:---------------------- {lista_LTE} ----------------------')
        arcpy.AddMessage(f'Dane wejsciowe DSS:---------------------- {lista_DSS} ----------------------')
        arcpy.AddMessage(f'Dane wejsciowe CBAND:---------------------- {lista_CBAND} ----------------------')
        arcpy.AddMessage(f'---------------------------------------------------------------------------------')
        arcpy.AddMessage(f'---------------------------------------------------------------------------------')
        arcpy.AddMessage(f'---------------------- koniec - CZESCI I - Wczytania danych ----------------------')


        self.process_dominance(output_info, output_MV, _path_92_,
                                _checkbox_gsm_, lista_GSM, _path_tabela_gsm_,
                                _checkbox_umts_, lista_UMTS, _path_tabela_umts_,
                                _checkbox_lte_, lista_LTE, _path_tabela_lte_,
                                _checkbox_dss_, lista_DSS, _checkbox_cband_, lista_CBAND, _path_tabela_dss_cband_)


# PRZECIAZENIA #############################################################################################################################################################################################################################################

        if _checkbox_przeciazenia_:
            arcpy.AddMessage('---------------------- CZESCI IV - Przeciązenia dla LTE ----------------------')

            arcpy.env.workspace = output_MV
            lista_MV = arcpy.ListFeatureClasses('*M_LTE*')

            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage('---------------------- TEST NA DZIAŁANIE ----------------------')
            arcpy.AddMessage('---------------------- Jeśli lista poniżej ⬇⬇⬇ tego komunikatu jest pusta wtedy: ---------------------- TEST NEGATYWNY ---------------------- sprawdź, czy dominance LTE są wykonane')
            arcpy.AddMessage(f'Lista - dominance LTE: {lista_MV}')
            arcpy.AddMessage('---------------------- Jeśli lista powyżej ⬆⬆⬆ tego komunikatu zawiera dominance LTE ---------------------- TEST POZYTYWNY ----------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')



        if _checkbox_przeciazenia_ and len(lista_MV) >= 1:


            arcpy.env.overwriteOutput = True


            arcpy.env.workspace = output_MV
            lista_MV = arcpy.ListFeatureClasses('*M_LTE*')

            # Ustawienie środowiska pracy geobaze SDE
            #arcpy.env.workspace = r"C:\Users\buchadan\AppData\Roaming\Esri\ArcGISPro\Favorites\Admin_SDE.sde"
            sde = arcpy.env.workspace = _path_sde_
            # Lista tabel do przefiltrowania z bazdy danych do tabel, od przeciazenia lte
            #lista_3 = arcpy.ListTables('*_przeciazone_lte_*')
            lista_3 = arcpy.ListTables('*_przeciazone_lte*')

            # Filtrowanie tabel, które nie kończą się na "_a" ani "_lte700"
            przeciazenia = [table for table in lista_3 if not (table.endswith("_a") or table.endswith("_lte700") or table.endswith("lte900_3857_table"))]
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------825')
            arcpy.AddMessage('---------------------- TEST NA DZIAŁANIE ----------------------')
            arcpy.AddMessage('---------------------- Jesli lista poniżej ⬇⬇⬇ jest pusta wtedy: ---------------------- TEST NEGATYWNY ---------------------- sprawdż, czy masz aktywne polaczenia z baza danych SDE ----------------------')
            arcpy.AddMessage(f'Lista - przeciazenia: {przeciazenia}')
            arcpy.AddMessage('---------------------- Jeśli lista powyżej ⬆⬆⬆ tego komunikatu zawiera tabele z przeciążeniami technologi LTE ---------------------- TEST POZYTYWNY ----------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')

            arcpy.env.workspace = output_MV

            lista_MV = arcpy.ListFeatureClasses('*M_LTE*')
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

                    abc = arcpy.management.AddJoin(mv_match[0], a, f'{sde}\{przeciazenie_match[0]}', b, join_type="KEEP_COMMON")
                    output_feature_class_przeciazenia =   fr'{output_MV}\\przeciazenie_{common}'
                    arcpy.AddMessage(output_feature_class_przeciazenia)
                    arcpy.AddMessage(output_MV)
                    arcpy.AddMessage(f'-------------------------------')
                    arcpy.AddMessage(f'-------------------------------913')


                    arcpy.conversion.FeatureClassToFeatureClass(abc, fr'{output_MV}', fr'przeciazenie_{common}')
                    arcpy.AddMessage(fr'{output_MV}')
                    arcpy.AddMessage(fr'przeciazenie_{common}')

            # Ustal nazwy kolumn, które chcesz zachować

            kolumny_do_zachowania = ["OBJECTID", "OBJECTID_1", "Shape", "LCELL_NAME", "Shape_Length", "Shape_Area"]

            # Tworzymy listę, która będzie zawierać wszystkie elementy, które będą do skasowania
            lista_do_skasowania = []

####################################################JESLI PUSZCZAM KOD BEZ PARAMETROW##############################################################################################
#             arcpy.AddMessage(f'-------------TEST linia 802------------------')
            lista_5 = arcpy.ListFields(output_feature_class_przeciazenia)
#             xx = r'D:\ArcGIS\0_Dane_Zasiegowe_DONE\2024_06\2024_06_MV.gdb\przeciazenie_LTE900'
#
#             lista_5 = arcpy.ListFields(xx)
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

            arcpy.AddMessage('Lista z przeciążeniami, od których teraz będziemy odejmować kolumny, żeby zostawić tylko OBJECTID, Shape -- LCELL_NAME -- Shape_Length, Shape_Area')
            arcpy.AddMessage(lista_przeciazone)
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')

            # Usuwanie kolumn, które są niepotrzebne, zostawienie tylko kolumny OBJECTID, Shape -- LCELL_NAME -- Shape_Length, Shape_Area
            for warstwa in lista_przeciazone:

                arcpy.AddMessage(f'Kasowanie kolumn dla: {warstwa}')
                arcpy.management.DeleteField(fr'{output_MV}\{warstwa}', lista_do_skasowania)
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------839')
                arcpy.AddMessage(f'Done: {warstwa}')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------')

            arcpy.AddMessage('---------------------- KONIEC CZESCI IV - Przeciązenia dla LTE ----------------------')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^ ZACZEKAJ TO MOŻE CHWILE TRWAĆ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')





# PIRAMIDY #############################################################################################################################################################################################################################################

        if _checkbox_piramidy_:
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage('---------------------- CZESCI VI - Robienie Piramid i geobaza 3857----------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.env.workspace = _wczytanie_danych_



            # Sprawdzenie czy folder nie istnieje już
            if not arcpy.Exists(os.path.join(_wczytanie_danych_, "Rastry_PUWG_92")):
                # Utworzenie folderu
                os.makedirs(os.path.join(_wczytanie_danych_, "Rastry_PUWG_92"))
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'---------------------- Folder o {_wczytanie_danych_}\\nazwie Rastry_PUWG_92 ---------------------- został utworzony pomyślnie ----------------------')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------')
            else:
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------')
                print("Folder już istnieje.")
                arcpy.AddMessage(f'---------------------- Folder o {_wczytanie_danych_}\\nazwie Rastry_PUWG_92 ---------------------- już istnieje ----------------------')
                arcpy.AddMessage(f'-------------------------------')
                arcpy.AddMessage(f'-------------------------------')


            raster_DSS = arcpy.ListRasters("*_DSS*.tif", "TIF")
            if len(raster_DSS) != 0:

                arcpy.AddMessage(f'Wczytanie rastra DSS: {_wczytanie_danych_}\\{raster_DSS[0]}')
                arcpy.env.workspace = output_MV
                arcpy.env.overwriteOutput = True
                dominance_MV_DSS = arcpy.ListFeatureClasses("*M_DSS*")
                arcpy.AddMessage(f'Wczytanie dominance dla technologii 5G DSS: {output_MV}\\{dominance_MV_DSS[0]}')

                # Docinanie rastra DSS wejsciowego do domimance MV DSS
                arcpy.AddMessage(f'---------------------- ExtractByMask  - Start  ----------------------')
                nazwa_bez_tif, _ = os.path.splitext(raster_DSS[0])


                out_raster = arcpy.sa.ExtractByMask(fr"{_wczytanie_danych_}\\{raster_DSS[0]}", fr'{output_MV}\\{dominance_MV_DSS[0]}')
                #musi tak byc bo inaczej dawal 2 razy .tif.tif
                out_raster.save(fr'{_wczytanie_danych_}\\{nazwa_bez_tif}_extract.tif')

                #Projektowanie ukladu do 92
                arcpy.management.ProjectRaster(fr'{_wczytanie_danych_}\\{nazwa_bez_tif}_extract.tif', fr'{_wczytanie_danych_}\\Rastry_PUWG_92\\{nazwa_bez_tif}.tif', _path_92_)

                #Tworzenie piramidy juz w folderze PUWG_92
                arcpy.management.BuildPyramids(fr'{_wczytanie_danych_}\\Rastry_PUWG_92\\{nazwa_bez_tif}.tif', -1, "NONE", "NEAREST", "LZ77", 50, "SKIP_EXISTING")


                #arcpy.env.overwriteOutput = True
                arcpy.AddMessage(f'---------------------- ProjectRaster --------------------------')
                arcpy.AddMessage(f'---------------------- Parametr 1 ---- {_wczytanie_danych_}\\Rastry_PUWG_92\\{nazwa_bez_tif}.tif --------------------------')
                arcpy.AddMessage(f'---------------------- Parametr 2 ---- {_output_3857_}\\{nazwa_bez_tif}  --------------------------')
                arcpy.AddMessage(f'---------------------- Parametr 3 ---- {_path_wgs84_} --------------------------')

                arcpy.management.ProjectRaster(fr'{_wczytanie_danych_}\\Rastry_PUWG_92\\{nazwa_bez_tif}.tif', fr'{_output_3857_}\\{nazwa_bez_tif}', _path_wgs84_)

                arcpy.AddMessage(f'---------------------- ExtractByMask - End ----------------------')

                arcpy.AddMessage(f'---------------------- KONIEC - CZESCI VI - Rastr DSS docięty do maski ----------------------')
            else:
                arcpy.AddMessage(f'---------------------- W danych brakuje rastra z nazwą DSS ----------------------')




            arcpy.env.workspace = _wczytanie_danych_

            # Pobierz listę warstw, których nazwa zawiera frazy 'GES' lub 'OT'
            # lista_warstw = arcpy.ListFeatureClasses('*GES_*') + arcpy.ListFeatureClasses('*OT_*')
            lista_rastrow_all = arcpy.ListRasters('*', "TIF")
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------1544aa')
            arcpy.AddMessage(f'Rasterą wejściowym zostaną zbudowane piramidamy oraz zostaną przeprojektowane do układu 3857')
            arcpy.AddMessage(lista_rastrow_all)

            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')

            lista_rastrow_filtered = [raster for raster in lista_rastrow_all if "DSS" not in raster]
            arcpy.AddMessage(f'Rastery bez DSS bo ten jest juz w folderze {_wczytanie_danych_}\\Rastry_PUWG_92')


            arcpy.AddMessage(lista_rastrow_filtered)
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')
            lista_rastrow_do_geobazy_3857 = arcpy.ListRasters("*LTE*" + "*_5class_*" + "*.tif", "TIF") + arcpy.ListRasters("CA_OPL_*" + "*.tif", "TIF") + arcpy.ListRasters("*_UMTS*" + "_5class_*" + "*.tif", "TIF") + arcpy.ListRasters("*_GSM*" + "_5class_*" + "*.tif", "TIF") + arcpy.ListRasters("*_UMTS*" + "*.tif", "TIF") + arcpy.ListRasters("*DSS*" + "*.tif", "TIF") + arcpy.ListRasters("*_CBAND*" + "*.tif", "TIF")

            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------1553')
            arcpy.AddMessage('Rastery, które zostaną dodane do geobazy 3857')
            arcpy.AddMessage(lista_rastrow_filtered)
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')




            for r in lista_rastrow_filtered:
                arcpy.env.overwriteOutput = True
                arcpy.env.outputCoordinateSystem = _path_wgs84_
                arcpy.management.BuildPyramids(r, -1, "NONE", "NEAREST", "LZ77", 50, "SKIP_EXISTING")

                arcpy.env.outputCoordinateSystem = _path_92_

#                 arcpy.AddMessage(fr'{_wczytanie_danych_}\{r}')
#                 arcpy.AddMessage(fr'{_wczytanie_danych_}\\Rastry_PUWG_92\\{r}')
#                 arcpy.AddMessage(_path_92_)
# tu coś jest do poprawy
#                 # Sprawdzenie, czy rastry mają zdefiniowany układ współrzędnych
#                 if self.has_coordinate_system(fr'{_wczytanie_danych_}\\{r}'):
#                     arcpy.AddMessage(f"Rastr {r} ma zdefiniowany układ współrzędnych.")
#                 else:
#                     arcpy.AddMessage(f"Raster {r} nie ma zdefiniowanego układu współrzędnych.")
#                   if self.has_coordinate_system(fr'{_wczytanie_danych_}\\{r}'):
#                                 arcpy.AddMessage(f"Rastr {r} ma zdefiniowany układ współrzędnych.")
#                             else:
#                                 arcpy.AddError(f"Raster {r} nie ma zdefiniowanego układu współrzędnych.")
#                                 sys.exit("Przerwano wykonanie skryptu z powodu braku zdefiniowanego układu współrzędnych.")
#
#                             try:
#                                 arcpy.management.ProjectRaster(fr'{_wczytanie_danych_}\\{r}', fr'{_wczytanie_danych_}\\Rastry_PUWG_92\\{r}', _path_92_)
#                                 arcpy.AddMessage(f'---------------------- Rastr ---- {r} ---- zamieniony na PUWG92 ----------------------')
#                             except arcpy.ExecuteError:
#                                 arcpy.AddError("Wystąpił błąd podczas przetwarzania rastra.")
#                                 sys.exit("Przerwano wykonanie skryptu z powodu błędu podczas przetwarzania rastra.")



                arcpy.management.ProjectRaster(fr'{_wczytanie_danych_}\\{r}', fr'{_wczytanie_danych_}\\Rastry_PUWG_92\\{r}', _path_92_)

                arcpy.AddMessage(f'---------------------- Rastr ---- {r} ---- zamieniony na PUWG92 ----------------------')



                # TUTAJ JEST IF co znaczy, ze jesli ta warstwa z lista_rastrow_filtered (- a w nij nigdy nie bedzie DSS) zawiera sie w lista_rastrow_do_geobazy_3857
                # warstwa DSS jest juz wczesniej zrobiona
                if r in lista_rastrow_do_geobazy_3857:
                    arcpy.env.overwriteOutput = True
                    #arcpy.env.outputCoordinateSystem = _path_wgs84_
                    #nazwa_bez_rozszerzenia, _ = os.path.splitext(warstwa_rastrowa)
                    #arcpy.management.BuildPyramids(warstwa_rastrowa, -1, "NONE", "NEAREST", "LZ77", 50, "SKIP_EXISTING")


                    #arcpy.env.overwriteOutput = True
                    arcpy.AddMessage(f'---------------------- ProjectRaster --------------------------')
                    arcpy.AddMessage(f'---------------------- Parametr 1 ---- {_wczytanie_danych_}\\Rastry_PUWG_92\\{r} --------------------------')
                    nazwa_rastra, _ = os.path.splitext(r)
                    arcpy.AddMessage(f'---------------------- Parametr 2 ---- {_output_3857_}\\{nazwa_rastra} --------------------------')
                    arcpy.AddMessage(f'---------------------- Parametr 3 ---- {_path_wgs84_} --------------------------')

                    arcpy.management.ProjectRaster(fr'{_wczytanie_danych_}\\Rastry_PUWG_92\\{r}', fr'{_output_3857_}\\{nazwa_rastra}', _path_wgs84_)
                    arcpy.AddMessage(f'---------------------- Rastr ---- {r} ---- dodany do geobazy_3857 ----------------------')
                    arcpy.AddMessage(f'-------------------------------')
                    arcpy.AddMessage(f'-------------------------------')


            arcpy.env.workspace = output_MV
            lista_warstw_do_geobazy_3857 = arcpy.ListFeatureClasses("*M_LTE*") + arcpy.ListFeatureClasses("CA_OPL_*") + arcpy.ListFeatureClasses("*M_UMTS*") + arcpy.ListFeatureClasses("*M_GSM*") + arcpy.ListFeatureClasses("*M_CBAND*")+ arcpy.ListFeatureClasses("*M_DSS*")
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------1621')
            arcpy.AddMessage('Klasy obiektów, które zostaną dodane do geobazy_3857')
            arcpy.AddMessage(lista_warstw_do_geobazy_3857)
            arcpy.AddMessage(f'-------------------------------')
            arcpy.AddMessage(f'-------------------------------')


            for x in lista_warstw_do_geobazy_3857:
                #arcpy.AddMessage("lista_warstw_all_mv")
                arcpy.env.overwriteOutput = True
                #output_feature_class_MV = fr'{_output_3857_}\{x}_3857'
                #arcpy.AddMessage(output_feature_class_MV)

                arcpy.AddMessage(f'---------------------- Project --------------------------')
                arcpy.AddMessage(f'---------------------- Parametr 1 ---- {output_MV}\\{x} --------------------------')
                arcpy.AddMessage(f'---------------------- Parametr 2 ---- {_output_3857_}\\{x} --------------------------')
                arcpy.AddMessage(f'---------------------- Parametr 3 ---- {_path_wgs84_} --------------------------')

####################### SA JUŻ PRZEKOPIOWANE ###############################################################################################################################################################################################################
                arcpy.management.Project(fr'{output_MV}\\{x}', fr'{_output_3857_}\\{x}', _path_wgs84_)
####################### SA JUŻ PRZEKOPIOWANE ###############################################################################################################################################################################################################

            arcpy.AddMessage('---------------------- KONIEC CZESCI VII - Robienie Piramid i geobaza 3857----------------------')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            arcpy.AddMessage(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')


            arcpy.env.workspace = output_MV
            feature_classes = arcpy.ListFeatureClasses('*_MV')
            arcpy.AddMessage(f'Warstwy do kasowania pola Styl w geobazie MV - Kolumny styl zostają w geobazie_3857: {feature_classes}')
            # Loop through each feature class and delete the "style" field
            for fc in feature_classes:
                fields = arcpy.ListFields(fc)
                for field in fields:
                    if field.name == "styl":
                        arcpy.DeleteField_management(fc, "styl")
                        arcpy.AddMessage(f"Deleted 'styl' field from {fc}")

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
