# -*- coding: utf-8 -*-
import arcpy
import logging
import re

# Ustawienie konfiguracji logowania
logging.basicConfig(
    filename='D:\\replikacja\\model_builder\\Python_3\\log_Rollout_create_2180.txt',
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
}

# Lista warstw SDE
warstwy_SDE = [
    # 'pgq_sde.rollout.mv_ncep2',
    'pgq_sde.rollout.mv_opl_b_l_2024i',
    'pgq_sde.rollout.mv_opl_b_l_2025i',
    'pgq_sde.rollout.mv_opl_b_l_legalizacja',
    'pgq_sde.rollout.mv_opl_b_l_on_air',
    'pgq_sde.rollout.mv_opl_b_l_on_air_2024',
    'pgq_sde.rollout.mv_opl_b_l_on_air_spady',
    'pgq_sde.rollout.mv_opl_b_l_on_air_widok_ogolny',
    'pgq_sde.rollout.mv_opl_b_l_realizacja',
    'pgq_sde.rollout.mv_opl_b_l_realizacja_spady',
    'pgq_sde.rollout.mv_opl_b_l_realizacja_widok_ogolny',
    'pgq_sde.rollout.mv_opl_legalizacja',
    'pgq_sde.rollout.mv_opl_on_air',
    'pgq_sde.rollout.mv_opl_ongoing',
    'pgq_sde.rollout.mv_opl_realizacja',
    'pgq_sde.rollout.mv_opl_tmpl_on_air',
    'pgq_sde.rollout.mv_opl_tmpl_realizacja',
    'pgq_sde.rollout.mv_opl_tmpl_admit_radio',
    'pgq_sde.rollout.mv_opl_tmpl_search'
]

def sanitize_name(name):
    """Zamień nieprawidłowe znaki na podkreślenia."""
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)

def add_fields_from_template(input_table, target_table):
    """Dodaj pola z input_table do target_table."""
    fields = arcpy.ListFields(input_table)
    for field in fields:
        if field.type not in ('OID', 'Geometry'):
            arcpy.management.AddField(
                in_table=target_table,
                field_name=field.name,
                field_type=field.type,
                field_precision=field.precision,
                field_scale=field.scale,
                field_length=field.length,
                field_alias=field.aliasName,
                field_is_nullable="NULLABLE" if field.isNullable else "NON_NULLABLE",
                field_is_required="REQUIRED" if field.required else "NON_REQUIRED",
                field_domain=field.domain
            )

pl_cs92 = arcpy.SpatialReference(2180)  # PL_CS92 (ETRF2000-PL_CS92)
for x in warstwy_SDE:
    print('\n')
    print('----------------------------------')
    print(f'Wczytana zmienna: {x}')
    print('----------------------------------\n')

    sanitized_name = sanitize_name(x)
    new_table_path = fr"D:\projekty_aprx\orange_projekty_aprx\rollout_gisserver\126.185.136.190_rollout.sde\{sanitized_name}_2180_t"
    print(sanitized_name)

    arcpy.management.CreateFeatureclass(
        out_path=r"D:\projekty_aprx\orange_projekty_aprx\rollout_gisserver\126.185.136.190_rollout.sde",
        out_name=f'{sanitized_name}_2180_t',
        geometry_type="POINT",
        template="",
        has_m="DISABLED",
        has_z="DISABLED",
        spatial_reference=pl_cs92,
        config_keyword="",
        spatial_grid_1=0,
        spatial_grid_2=0,
        spatial_grid_3=0,
        out_alias="",
        oid_type="SAME_AS_TEMPLATE"
    )
    print(f'Utworzono tabelę {new_table_path}')

    add_fields_from_template(input_table=fr'{paths["sde"]}\{x}_3857_t', target_table=new_table_path)
    print(f'Dodano pola do tabeli {new_table_path}')

print("Koniec")
