# -*- coding: utf-8 -*-
import arcpy
import logging
# Ustawienie konfiguracji logowania
logging.basicConfig(filename='D:\\replikacja\\model_builder\\Python_3\\log_gn_NEW.txt', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Przykładowe logowanie
logging.debug('Rozpoczęcie skryptu.')


arcpy.env.overwriteOutput = True
paths = {
    "sde": r'C:\Users\buchadan\AppData\Roaming\Esri\ArcGISPro\Favorites\126.185.136.190_ogolne.sde',
    "_PUWG_92_": r'D:\projections\ETRS 1989 Poland CS92.prj',
	'_WGS_84_4326': r'D:\projections\WGS 1984.prj',
	"_WGS_84_3857": r'D:\projections\WGS 1984 Web Mercator (auxiliary sphere).prj',
    "geobaza": r'D:\dane_gdb\GN_Skrypt\GN_Skrypt.gdb'
}


# arcpy.env.workspace = paths["sde"]
# a = arcpy.ListTables("pgq_sde.ogolne.mv_gn*", "ALL")
# print(a)

# mv_przeciazone_tables = [
#      'pgq_sde.ogolne.mv_gn',
#      'pgq_sde.ogolne.mv_gn_to_rollout_opl',
#      'pgq_sde.ogolne.mv_gn_to_rollout_tmpl'
# ]
warstwy = [
     'mv_gn',
     'mv_gn_to_rollout_opl',
     'mv_gn_to_rollout_tmpl'
]

def append_with_field_mapping(input_table, target_table):
    """Append data from input_table to target_table with field mapping."""
    field_mappings = arcpy.FieldMappings()
    input_fields = arcpy.ListFields(input_table)
    target_fields = arcpy.ListFields(target_table)

    # Stwórz mapowanie dla każdego pola źródłowego, jeśli istnieje w tabeli docelowej
    for input_field in input_fields:
        if input_field.name in [field.name for field in target_fields]:
            field_map = arcpy.FieldMap()
            field_map.addInputField(input_table, input_field.name)
            field_mappings.addFieldMap(field_map)

    arcpy.management.Append(
        inputs=input_table,
        target=target_table,
        schema_type="NO_TEST",
        field_mapping=field_mappings,
        subtype="",
        expression="",
        match_fields=None,
        update_geometry="NOT_UPDATE_GEOMETRY"
    )


for x in warstwy:
    print(x)
    print(fr'{paths["sde"]}\{x}')
    print(fr'{paths["geobaza"]}\\{x}_2180_t')
    print('\n')
    #arcpy.management.XYTableToPoint(fr'{paths["sde"]}\\{x}', fr'{paths["geobaza"]}\\{x}_2180_t', "wspx", "wspy", None, paths["_PUWG_92_"])
    arcpy.management.XYTableToPoint(
        in_table=fr'{paths["sde"]}\pgq_sde.ogolne.{x}',
        out_feature_class=fr'{paths["geobaza"]}\\{x}_2180_t',
        x_field="wspx",
        y_field="wspy",
        z_field=None,
        coordinate_system=paths["_PUWG_92_"]
    )

    arcpy.management.Project(fr'{paths["geobaza"]}\\{x}_2180_t', fr'{paths["geobaza"]}\\{x}_3857_t', paths["_WGS_84_3857"])

    print('TruncateTable')
    arcpy.management.TruncateTable(fr'{paths["sde"]}\\{x}_3857')
    print(f'TruncateTable: {paths["sde"]}\\{x}')
    print('\n')

    print(f'input: {paths["geobaza"]}\\{x}_3857_t')
    print('Append')
    append_with_field_mapping(
        fr'{paths["geobaza"]}\\{x}_3857_t',
        fr'{paths["sde"]}\\{x}_3857'
    )
    print(f'Append: {paths["sde"]}\\{x}_3857_t')
    print('\n')

print('Koniec')
# logging.debug('Zakończenie skryptu.')
