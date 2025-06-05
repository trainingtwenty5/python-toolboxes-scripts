# -*- coding: utf-8 -*-
import arcpy
import logging
# Ustawienie konfiguracji logowania
logging.basicConfig(filename='D:\\replikacja\\model_builder\\Python_3\\log_Azymuty.txt', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Przykładowe logowanie
logging.debug('Rozpoczęcie skryptu.')
arcpy.env.overwriteOutput = True
paths = {
    "sde": r'C:\Users\zz_gis_esri\AppData\Roaming\ESRI\Desktop10.8\ArcCatalog\126.185.136.190_azymut.sde',
    "_PUWG_92_": r'C:\Users\zz_gis_esri\AppData\Roaming\ESRI\Desktop10.8\projections\ETRS 1989 Poland CS92.prj',
    "_WGS_84_": r'C:\Users\zz_gis_esri\AppData\Roaming\ESRI\Desktop10.8\projections\WGS 1984 Web Mercator (auxiliary sphere).prj',
    "geobaza": r'D:\arcgisserver\mxd\2024_04_25_Azymuty\2024_05_02_Azymuty.gdb',

}

warstwy = [
    "mv_azimuth_fdd2100_t",
    "mv_azimuth_fdd3600_t",
    "mv_azimuth_gsm",
    "mv_azimuth_lte800",
    "mv_azimuth_lte900_t",
    "mv_azimuth_lte1800",
    "mv_azimuth_lte2100",
    "mv_azimuth_lte2600",
    "mv_azimuth_umts900",
    "mv_azimuth_umts2100"
]

print('\n')
print('Start')
print('\n')
for warstwa in warstwy:
    print(warstwa)
    try:
        if 'fdd2100' in warstwa or 'fdd3600' in warstwa:
            print('\n')
            print(f'Warstwa: {warstwa}')
            print('\n')

            arcpy.management.BearingDistanceToLine(fr'{paths["sde"]}\pgq_sde.azymuty.{warstwa}', fr'{paths["geobaza"]}\\{warstwa}_2180_t', 'xpos', 'ypos', 'radius', 'METERS', 'azimuth', 'DEGREES', 'GEODESIC', 'gcell_name', paths["_PUWG_92_"])
            print("BearingDistanceToLine wykonane pomyślnie.")

            #TRUNKEJD fr'{paths["geobaza"]}\\{warstwa}_2180_t' i append DO BAZY
            arcpy.management.TruncateTable(fr'{paths["sde"]}\\{warstwa}_2180_t')
            print(f'wykonanie TruncateTable {warstwa}_2180_t')
            arcpy.management.Append(fr'{paths["geobaza"]}\\{warstwa}_2180_t', fr'{paths["sde"]}\\{warstwa}_2180_t', "TEST", None, '', '')
            print(f'wykonanie Append {warstwa}_2180_t')


            arcpy.conversion.TableToTable(fr'{paths["sde"]}\pgq_sde.azymuty.{warstwa}', paths["geobaza"], fr'{warstwa}_tabela')
            print(f"TableToTable wykonane pomyślnie pgq_sde.azymuty.{warstwa}")


            arcpy.management.JoinField(fr'{paths["geobaza"]}\\{warstwa}_2180_t', "gcell_name", fr'{paths["geobaza"]}\\{warstwa}_tabela', "gcell_name", "loc_name;loc_obj;loc_code;gsite_name;gsite_obj;gsite_id;gcell_name;gcell_obj;gcell_id;band;data_aktualizacji")
            print("JoinField wykonane pomyślnie.")

            arcpy.Project_management(fr'{paths["geobaza"]}\\{warstwa}_2180_t', fr'{paths["geobaza"]}\\{warstwa}_3857_t', paths["_WGS_84_"])
            print(f"Project_management _PUWG_92_ wykonane pomyślnie {warstwa}_3857_t")
            arcpy.management.TruncateTable(fr'{paths["sde"]}\\{warstwa}_3857_t')
            print(f'wykonanie TruncateTable {warstwa}_3857_t')
            arcpy.management.Append(fr'{paths["geobaza"]}\\{warstwa}_3857_t', fr'{paths["sde"]}\\{warstwa}_3857_t', "TEST", None, '', '')
            print(f'wykonanie Append {warstwa}_3857_t')


        elif 'lte900' in warstwa:
            print('\n')
            print(f'Warstwa123: {warstwa}')
            print('\n')

            arcpy.management.BearingDistanceToLine(fr'{paths["sde"]}\pgq_sde.azymuty.{warstwa}', fr'{paths["geobaza"]}\\{warstwa}_2180_t', 'xpos', 'ypos', 'radius', 'METERS', 'azimuth', 'DEGREES', 'GEODESIC', 'c_obj', paths["_PUWG_92_"])
            print("BearingDistanceToLine wykonane pomyślnie.")


            arcpy.management.TruncateTable(fr'{paths["sde"]}\\{warstwa}_2180_t')
            print(f'wykonanie TruncateTable {warstwa}_2180_t')


            arcpy.management.Append(
                fr'{paths["geobaza"]}\\{warstwa}_2180_t',
                fr'{paths["sde"]}\\{warstwa}_2180_t',
                "NO_TEST",
                fr'xpos "xpos" true true false 8 Double 3 16,First,#,{paths["geobaza"]}\\{warstwa}_2180_t,xpos,-1,-1;'
                fr'ypos "ypos" true true false 8 Double 3 16,First,#,{paths["geobaza"]}\\{warstwa}_2180_t,ypos,-1,-1;'
                fr'radius "radius" true true false 8 Double 3 16,First,#,{paths["geobaza"]}\\{warstwa}_2180_t,radius,-1,-1;'
                fr'azimuth "azimuth" true true false 8 Double 3 16,First,#,{paths["geobaza"]}\\{warstwa}_2180_t,azimuth,-1,-1;'
                fr'cell_id "cell_id" true true false 4 Long 0 10,First,#,{paths["geobaza"]}\\{warstwa}_2180_t,c_obj,-1,-1',
                '', '')

            print(f'wykonanie Append {warstwa}_2180_t')

            arcpy.conversion.TableToTable(fr'{paths["sde"]}\pgq_sde.azymuty.{warstwa}', paths["geobaza"], fr'{warstwa}_tabela')
            print(f"TableToTable wykonane pomyślnie pgq_sde.azymuty.{warstwa}")

            arcpy.management.JoinField(fr'{paths["geobaza"]}\\{warstwa}_2180_t', "c_obj", fr'{paths["geobaza"]}\\{warstwa}_tabela', "c_obj", "loc_name;loc_obj;loc_code;site_name;site_obj;site_id;cell_name;cell_obj;cell_id;band;data_aktualizacji")
            print("JoinField wykonane pomyślnie.")

            arcpy.Project_management(fr'{paths["geobaza"]}\\{warstwa}_2180_t', fr'{paths["geobaza"]}\\{warstwa}_3857_t', paths["_WGS_84_"])
            print(f"Project_management _PUWG_92_ wykonane pomyślnie {warstwa}_3857_t")
            arcpy.management.TruncateTable(fr'{paths["sde"]}\\{warstwa}_3857_t')
            print(f'wykonanie TruncateTable222 {warstwa}_3857_t')
            arcpy.management.Append(fr'{paths["geobaza"]}\\{warstwa}_3857_t', fr'{paths["sde"]}\\{warstwa}_3857_t', "TEST", None, '', '')
            print(f'wykonanie Append {warstwa}_3857_t')

            print('\n')
            print(f'Done: {warstwa}')

            print('\n')
        else:
            print('\n')
            print(f'Warstwa: {warstwa}')
            print('\n')

            arcpy.management.BearingDistanceToLine(fr'{paths["sde"]}\pgq_sde.azymuty.{warstwa}', fr'{paths["geobaza"]}\\{warstwa}_2180_t', 'xpos', 'ypos', 'radius', 'METERS', 'azimuth', 'DEGREES', 'GEODESIC', 'c_obj', paths["_PUWG_92_"])
            print("BearingDistanceToLine wykonane pomyślnie.")


            arcpy.management.TruncateTable(fr'{paths["sde"]}\\{warstwa}_2180_t')
            print(f'wykonanie TruncateTable {warstwa}_2180_t')
            arcpy.management.Append(fr'{paths["geobaza"]}\\{warstwa}_2180_t', fr'{paths["sde"]}\\{warstwa}_2180_t', "TEST", None, '', '')
            print(f'wykonanie Append {warstwa}_2180_t')

            arcpy.conversion.TableToTable(fr'{paths["sde"]}\pgq_sde.azymuty.{warstwa}', paths["geobaza"], fr'{warstwa}_tabela')
            print(f"TableToTable wykonane pomyślnie pgq_sde.azymuty.{warstwa}")

            arcpy.management.JoinField(fr'{paths["geobaza"]}\\{warstwa}_2180_t', "c_obj", fr'{paths["geobaza"]}\\{warstwa}_tabela', "c_obj", "loc_name;loc_obj;loc_code;site_name;site_obj;site_id;cell_name;cell_obj;cell_id;band;data_aktualizacji")
            print("JoinField wykonane pomyślnie.")

            arcpy.Project_management(fr'{paths["geobaza"]}\\{warstwa}_2180_t', fr'{paths["geobaza"]}\\{warstwa}_3857_t', paths["_WGS_84_"])
            print(f"Project_management _PUWG_92_ wykonane pomyślnie {warstwa}_3857_t")
            arcpy.management.TruncateTable(fr'{paths["sde"]}\\{warstwa}_3857_t')
            print(f'wykonanie TruncateTable {warstwa}_3857_t')
            arcpy.management.Append(fr'{paths["geobaza"]}\\{warstwa}_3857_t', fr'{paths["sde"]}\\{warstwa}_3857_t', "TEST", None, '', '')
            print(f'wykonanie Append {warstwa}_3857_t')


    except Exception as e:
        logging.error(f'Błąd: {str(e)}')



arcpy.management.TruncateTable(fr"{paths['sde']}\\mv_azimuth_fdd3600_t_3857_table")
print(f'wykonanie TruncateTable mv_azimuth_fdd3600_t_3857_table')
arcpy.management.Append(fr'{paths["sde"]}\\mv_azimuth_fdd3600_t_3857_t', fr"{paths['sde']}\\pgq_sde.azymuty.mv_azimuth_fdd3600_t_3857_table", "TEST", None, '', '')
print(f'wykonanie Append pgq_sde.mv_azimuth_fdd3600_t_3857_table')
print(f'wykonanie aktualizacje daty')

print('Koniec')
logging.debug('Zakończenie skryptu.')

