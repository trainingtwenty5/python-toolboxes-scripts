# -*- coding: utf-8 -*-
import arcpy
import logging

arcpy.env.overwriteOutput = True


# Ustawienie konfiguracji logowania
logging.basicConfig(filename='D:\\replikacja\\model_builder\\Python_3\\log_fix_sprinter.txt', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
# Przykładowe logowanie
logging.debug('Rozpoczęcie skryptu.')
print("Start")

#arcpy.env.workspace = r"C:\\Users\\zz_gis_esri\\AppData\\Roaming\\ESRI\\Desktop10.8\\ArcCatalog\\126.185.136.190_ogolne.sde"
arcpy.env.workspace = r"C:\Users\buchadan\AppData\Roaming\ESRI\ArcGISPro\Favorites\ogolne.sde"

paths = {
    "sde": r'C:\Users\buchadan\AppData\Roaming\ESRI\ArcGISPro\Favorites\ogolne.sde',
    "_PUWG_92_": r'C:\Users\zz_gis_esri\AppData\Roaming\ESRI\Desktop10.8\projections\ETRS 1989 Poland CS92.prj',
    '_WGS_84_4326': r'C:\Users\zz_gis_esri\AppData\Roaming\ESRI\Desktop10.8\projections\WGS 1984.prj',
    "_WGS_84_3857": r'C:\Users\zz_gis_esri\AppData\Roaming\ESRI\Desktop10.8\projections\WGS 1984 Web Mercator (auxiliary sphere).prj',
    "geobaza": r'D:\arcgisserver\mxd\2024_05_16_Fix_sprinter_dane\2024_05_16_Fix_sprinter_dane.gdb',
}

warstwa = 'mv_fix_sprinter_dane'


try:

    #mv_fix_sprinter_dane
    print('Start - 4326')
    arcpy.management.XYTableToPoint(fr'{paths["sde"]}\pgq_sde.ogolne.mv_fix_sprinter_dane', fr'{paths["geobaza"]}\\{warstwa}_4326_t', 'wsp_geo_x', 'wsp_geo_y', None, paths["_WGS_84_4326"])
    print('Zakończono - 4326')



    print('Start - 3857')
    arcpy.management.TruncateTable(fr'{paths["sde"]}\\{warstwa}_3857_t')
    print(f'wykonanie TruncateTable {paths["sde"]}\\{warstwa}_3857_t')
    arcpy.management.Project(fr'{paths["geobaza"]}\\{warstwa}_4326_t', fr'{paths["geobaza"]}\\{warstwa}_3857_t', paths["_WGS_84_3857"])
    print(f'wykonanie Project')
    arcpy.management.Append(fr'{paths["geobaza"]}\\{warstwa}_3857_t', fr'{paths["sde"]}\\{warstwa}_3857_t', "TEST", None, '', '')
    print(f'wykonanie Append')
    print('Zakończono - 3857')



    print('Start - 2180')
    arcpy.management.TruncateTable(fr'{paths["sde"]}\\{warstwa}_2180_t')
    print(f'wykonanie TruncateTable {paths["sde"]}\\{warstwa}_2180_t')
    arcpy.management.Project(fr'{paths["geobaza"]}\\{warstwa}_3857_t', fr'{paths["geobaza"]}\\{warstwa}_2180_t', paths["_PUWG_92_"])
    print(f'wykonanie Project')
    arcpy.management.Append(fr'{paths["geobaza"]}\\{warstwa}_2180_t', fr'{paths["sde"]}\\{warstwa}_2180_t', "TEST", None, '', '')
    print(f'wykonanie Append')
    print('Zakończono - 2180')




except Exception as e:
    logging.error(f'Błąd: {str(e)}')

logging.debug('Zakończenie skryptu.')
print('Koniec')
