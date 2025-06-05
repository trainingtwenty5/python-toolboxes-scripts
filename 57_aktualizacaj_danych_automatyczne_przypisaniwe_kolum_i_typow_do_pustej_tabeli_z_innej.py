# -*- coding: utf-8 -*-
import arcpy
import logging
# Ustawienie konfiguracji logowania
logging.basicConfig(filename='D:\\replikacja\\model_builder\\Python_3\\log_stacje_act_all_NEW.txt', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Przykładowe logowanie
logging.debug('Rozpoczęcie skryptu.')


arcpy.env.overwriteOutput = True
paths = {
    "sde": r'D:\sde\126.185.136.190_stacje.sde',
    "_PUWG_92_": r'D:\projections\ETRS 1989 Poland CS92.prj',
    "_WGS_84_": r'D:\projections\WGS 1984 Web Mercator (auxiliary sphere).prj',
    "geobaza": r'D:\dane_gdb\skrypt_stacje_act_all\skrypt_stacje_act_all.gdb',
}


# arcpy.env.workspace = paths["sde"]
# a = arcpy.ListTables("pgq_sde.ogolne.mv_gn*", "ALL")
# print(a)

# mv_przeciazone_tables = [
#      'pgq_sde.ogolne.mv_gn',
#      'pgq_sde.ogolne.mv_gn_to_rollout_opl',
#      'pgq_sde.ogolne.mv_gn_to_rollout_tmpl'
# ]




# Lista nazw warstw
warstwy = [
    "mv_stacje_act",
    # "mv_stacje_act_gsm",
    # "mv_stacje_act_indoor",
    # "mv_stacje_act_l800",
    # "mv_stacje_act_l1800",
    # "mv_stacje_act_l2100",
    # "mv_stacje_act_l2600",
    # "mv_stacje_act_macro",
    # "mv_stacje_act_micro",
    # "mv_stacje_act_small",
    # "mv_stacje_act_w900",
    # "mv_stacje_act_w2100",
    # "mv_stacje_act_5g1800",
    # "mv_stacje_act_5g2100",
    # "mv_stacje_act_5g3600"
]

tabele = [
    "stacje_act",
    # "stacje_act_gsm",
    # "stacje_act_indoor",
    # "stacje_act_l800",
    # "stacje_act_l1800",
    # "stacje_act_l2100",
    # "stacje_act_l2600",
    # "stacje_act_macro",
    # "stacje_act_micro",
    # "stacje_act_small",
    # "stacje_act_w900",
    # "stacje_act_w2100",
    # "stacje_act_5g1800",
    # "stacje_act_5g2100",
    # "stacje_act_5g3600"
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






for warstwa, tabela in zip(warstwy, tabele):
    print(f'x')
    try:
        arcpy.management.XYTableToPoint(fr'{paths["sde"]}\pgq_sde.stacje.{warstwa}', fr'{paths["geobaza"]}\\{warstwa}_geom_2180_t', 'x', 'y', None, paths["_PUWG_92_"])
        print(f'wykonanie warstwy {paths["geobaza"]}\\{warstwa}_geom_2180_t')
        print('-------------------------------------------')

        arcpy.management.TruncateTable(fr"{paths['sde']}\\pgq_sde.stacje.{warstwa}_geom_2180_t")
        print(f'wykonanie TruncateTable {tabela}_geom_2180_t')

        print('Append')
        append_with_field_mapping(
            fr'{paths["geobaza"]}\\{warstwa}_geom_2180_t',
            fr"{paths['sde']}\\pgq_sde.stacje.{warstwa}_geom_2180_t"
        )
        print(fr"{paths['sde']}\\pgq_sde.stacje.{warstwa}_geom_2180_t")
        print(f'wykonanie Append {tabela}_geom_2180_t')

        arcpy.management.Project(fr'{paths["geobaza"]}\\{warstwa}_geom_2180_t', fr'{paths["geobaza"]}\\{tabela}_geom_3857_t', paths["_WGS_84_"])
        print(f'wykonanie warstwy {paths["geobaza"]}\\{tabela}_geom_3857_t')
        print('-------------------------------------------')
        print('-------------------------------------------')

        arcpy.management.TruncateTable(fr"{paths['sde']}\\pgq_sde.stacje.{tabela}_geom_3857_t")
        print(f'wykonanie TruncateTable {tabela}_geom_3857_t')
        print('-------------------------------------------')
        print('-------------------------------------------')
        append_with_field_mapping(
            fr'{paths["geobaza"]}\\{tabela}_geom_3857_t',
            fr"{paths['sde']}\\pgq_sde.stacje.{tabela}_geom_3857_t",
        )

        print(f'wykonanie Append do pgq_sde.stacje.{tabela}_geom_3857_t')
        logging.info(f'Zakończono przetwarzanie warstwy {warstwa} i tabeli {tabela}.')

    except Exception as e:
        logging.error(f'Błąd podczas przetwarzania warstwy {warstwa} i tabeli {tabela}: {str(e)}')


print('Koniec')
logging.debug('Zakończenie skryptu.')
