# -*- coding: utf-8 -*-
import arcpy
import logging
import re

# Ustawienie konfiguracji logowania
logging.basicConfig(
    filename='D:\\replikacja\\model_builder\\Python_3\\log_Rollout.txt',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Przykładowe logowanie
logging.debug('Rozpoczęcie skryptu.')
print("Start")
arcpy.env.overwriteOutput = True

# Ustawienie przestrzeni roboczej
arcpy.env.workspace = r"D:\arcgisserver\mxd\2024_07_22_Rollout\Rollout.sde"

# Definicja ścieżek do SDE, projekcji i bazy geodanych
paths = {
    "sde": r'D:\sde\126.185.136.190_rollout.sde',
    "PUWG_92": r'D:\projections\ETRS 1989 Poland CS92.prj',
    "WGS_84": r'D:\projections\WGS 1984 Web Mercator (auxiliary sphere).prj',
    "geobaza": r'D:\projekty_aprx\orange_projekty_aprx\rollout\rollout.gdb',
}

# Lista warstw SDE
warstwy_SDE = [
    'pgq_sde.rollout.mv_opl_rollout_priorytety',
    'pgq_sde.rollout.mv_opl_rollout_priorytety_poz',
    'pgq_sde.rollout.mv_opl_tmpl_on_air_2021',
    'pgq_sde.rollout.mv_opl_b_l_2022',
    'pgq_sde.rollout.mv_opl_tmpl_on_air_2022',
    'pgq_sde.rollout.mv_opl_tmpl_on_air_2023',
    'pgq_sde.rollout.mv_opl_b_l_2022i',
    'pgq_sde.rollout.mv_opl_realizacja',
    'pgq_sde.rollout.mv_opl_plan_2020',
    'pgq_sde.rollout.mv_opl_b_l_2019',
    'pgq_sde.rollout.mv_opl_b_l_2021',
    'pgq_sde.rollout.mv_opl_tmpl_search',
    'pgq_sde.rollout.mv_opl_lccs_realizacja',
    'pgq_sde.rollout.mv_opl_roads_program',
    'pgq_sde.rollout.mv_opl_lccs_on_air',
    'pgq_sde.rollout.mv_opl_plan_2021',
    'pgq_sde.rollout.mv_opl_b_l_on_air_2022',
    'pgq_sde.rollout.mv_opl_b_l_on_air_2023',
    'pgq_sde.rollout.mv_opl_b_l_on_air_2024',
    'pgq_sde.rollout.mv_opl_b_l_on_air',
    'pgq_sde.rollout.mv_opl_b_l_on_air_spady',
    'pgq_sde.rollout.mv_opl_b_l_on_air_widok_ogolny',
    'pgq_sde.rollout.mv_opl_b_l_realizacja',
    'pgq_sde.rollout.mv_opl_b_l_realizacja_spady',
    'pgq_sde.rollout.mv_opl_b_l_realizacja_widok_ogolny',
    'pgq_sde.rollout.mv_opl_b_l_legalizacja',
    'pgq_sde.rollout.mv_opl_legalizacja',
    'pgq_sde.rollout.mv_opl_on_air',
    'pgq_sde.rollout.mv_opl_ongoing',
    'pgq_sde.rollout.mv_opl_b_l_2025i',
    'pgq_sde.rollout.mv_opl_rr_opl_infeasible',
    'pgq_sde.rollout.mv_opl_plan_2022',
    'pgq_sde.rollout.mv_opl_tmpl_realizacja',
    'pgq_sde.rollout.mv_opl_tmpl_admit_radio',
    'pgq_sde.rollout.mv_opl_tmpl_on_air',
    'pgq_sde.rollout.mv_opl_b_l_2024i'
]

def sanitize_name(name):
    """Zamień nieprawidłowe znaki na podkreślenia."""
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


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

for x in warstwy_SDE:
    try:
        print('\n')
        print('----------------------------------')
        print(f'Wczytana zmienna: {x}')
        print('----------------------------------')
        print('\n')
        sanitized_name = sanitize_name(x)
        print(f'input: {paths["sde"]}\\{x}')
        print('XYTableToPoint')
        arcpy.management.XYTableToPoint(
            fr'{paths["sde"]}\\{x}',
            fr'{paths["geobaza"]}\\{sanitized_name}_2180_t',
            "xpos", "ypos", None, paths["PUWG_92"]
        )
        print(f'output: {paths["geobaza"]}\\{sanitized_name}_2180_t')
        print('\n')

        print(f'input: {paths["geobaza"]}\\{sanitized_name}_2180_t')
        print('Project')
        arcpy.management.Project(
            fr'{paths["geobaza"]}\\{sanitized_name}_2180_t',
            fr'{paths["geobaza"]}\\{sanitized_name}_3857_t',
            paths["WGS_84"]
        )
        print(f'output: {paths["geobaza"]}\\{sanitized_name}_3857_t')
        print('\n')

        print('TruncateTable')
        arcpy.management.TruncateTable(fr'{paths["sde"]}\\{x}_3857_t')
        print(f'TruncateTable: {paths["sde"]}\\{x}_3857_t')
        print('\n')

        print(f'input: {paths["geobaza"]}\\{sanitized_name}_3857_t')
        print('Append')
        append_with_field_mapping(
            fr'{paths["geobaza"]}\\{sanitized_name}_3857_t',
            fr'{paths["sde"]}\\{x}_3857_t'
        )
        print(f'Append: {paths["sde"]}\\{x}_3857_t')
        print('\n')

        # print('TruncateTable')
        # arcpy.management.TruncateTable(fr'{paths["sde"]}\\{x}_2180_t')
        # print(f'TruncateTable: {paths["sde"]}\\{x}_2180_t')
        # print('\n')
        #
        # print('Append')
        # append_with_field_mapping(
        #     fr'{paths["geobaza"]}\\{sanitized_name}_2180_t',
        #     fr'{paths["sde"]}\\{x}_2180_t'
        # )
        # print(f'Append: {paths["sde"]}\\{x}_2180_t')
        # print('\n')

    except Exception as e:
        logging.error(f'Błąd: {str(e)}')

logging.debug('Zakończenie skryptu.')
print('Koniec')
