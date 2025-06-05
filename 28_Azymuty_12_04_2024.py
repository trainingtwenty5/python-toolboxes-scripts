# -*- coding: utf-8 -*-
import arcpy
import logging

# Ustawienie konfiguracji logowania
logging.basicConfig(filename='D:\\replikacja\\model_builder\\Python_3\\log_Azymuty.txt', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Przykładowe logowanie
logging.debug('Rozpoczęcie skryptu.')

arcpy.env.overwriteOutput = True

paths = {
    "sde": r'C:\Users\buchadan\AppData\Roaming\Esri\ArcGISPro\Favorites\126.185.136.190_azymut.sde',
    "_PUWG_92_": r'D:\projections\ETRS 1989 Poland CS92.prj',
    "_WGS_84_": r'D:\projections\WGS 1984 Web Mercator (auxiliary sphere).prj',
    "geobaza": r'D:\projekty_aprx\orange_projekty_aprx\azymuty\azymuty_t.gdb',
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


def create_field_mapping(input_table, target_table):
    field_mappings = arcpy.FieldMappings()

    input_fields = arcpy.ListFields(input_table)
    target_fields = arcpy.ListFields(target_table)

    input_field_names = [f.name for f in input_fields]
    target_field_names = [f.name for f in target_fields]

    for field_name in input_field_names:
        if field_name in target_field_names:
            field_map = arcpy.FieldMap()
            field_map.addInputField(input_table, field_name)
            field_mappings.addFieldMap(field_map)

    return field_mappings


def append_with_field_mapping(input_table, target_table):
    field_mappings = create_field_mapping(input_table, target_table)
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


print('\n')
print('Start')
print('\n')
for warstwa in warstwy:
    try:
        print('\n')
        print('###########################')
        print(f'Warstwa: {warstwa}')
        print('###########################')
        print('\n')

        if 'fdd2100' in warstwa or 'fdd3600' in warstwa:
            arcpy.management.BearingDistanceToLine(
                in_table=fr'{paths["sde"]}\pgq_sde.azymuty.{warstwa}',
                out_featureclass=fr'{paths["geobaza"]}\\{warstwa}_2180_t',
                x_field='xpos', y_field='ypos', distance_field='radius',
                distance_units='METERS', bearing_field='azimuth', bearing_units='DEGREES',
                line_type='GEODESIC', id_field='gcell_name', spatial_reference=paths["_PUWG_92_"]
            )
            print("BearingDistanceToLine wykonane pomyślnie.")

            arcpy.management.TruncateTable(fr'{paths["sde"]}\\{warstwa}_2180_t')
            print(f'wykonanie TruncateTable {warstwa}_2180_t')

            append_with_field_mapping(
                input_table=fr'{paths["geobaza"]}\{warstwa}_2180_t',
                target_table=fr'{paths["sde"]}\{warstwa}_2180_t'
            )
            print(f'wykonanie Append {warstwa}_2180_t')

            arcpy.conversion.TableToTable(fr'{paths["sde"]}\pgq_sde.azymuty.{warstwa}', paths["geobaza"],
                                          fr'{warstwa}_tabela')
            print(f"TableToTable wykonane pomyślnie pgq_sde.azymuty.{warstwa}")

            arcpy.management.JoinField(
                in_data=fr'{paths["geobaza"]}\\{warstwa}_2180_t',
                in_field="gcell_name",
                join_table=fr'{paths["geobaza"]}\\{warstwa}_tabela',
                join_field="gcell_name",
                fields="loc_name;loc_obj;loc_code;gsite_name;gsite_obj;gsite_id;gcell_name;gcell_obj;gcell_id;band;data_aktualizacji"
            )
            print("JoinField wykonane pomyślnie.")

            arcpy.management.Project(
                in_dataset=fr'{paths["geobaza"]}\\{warstwa}_2180_t',
                out_dataset=fr'{paths["geobaza"]}\\{warstwa}_3857_t',
                out_coor_system=paths["_WGS_84_"]
            )
            print(f"Project_management _PUWG_92_ wykonane pomyślnie {warstwa}_3857_t")

            arcpy.management.TruncateTable(fr'{paths["sde"]}\\{warstwa}_3857_t')
            print(f'wykonanie TruncateTable {warstwa}_3857_t')

            append_with_field_mapping(
                input_table=fr'{paths["geobaza"]}\{warstwa}_3857_t',
                target_table=fr'{paths["sde"]}\{warstwa}_3857_t'
            )
            print(f'wykonanie Append {warstwa}_3857_t')

        else:
            if warstwa == "mv_azimuth_lte900_t":
                # daltego, ze pole c_obj tutaj nie dziala, jest typy longinteager i jego wartosci zaniakaja
                id_field = "cell_name"
                join_field = "cell_name"

            else:
                id_field = "c_obj"
                join_field = "c_obj"

            arcpy.management.BearingDistanceToLine(
                in_table=fr'{paths["sde"]}\pgq_sde.azymuty.{warstwa}',
                out_featureclass=fr'{paths["geobaza"]}\{warstwa}_2180_t',
                x_field="xpos", y_field="ypos", distance_field="radius",
                distance_units="METERS", bearing_field="azimuth", bearing_units="DEGREES",
                line_type="GEODESIC", id_field=id_field, spatial_reference=paths["_PUWG_92_"],
                attributes="NO_ATTRIBUTES"
            )
            print("BearingDistanceToLine wykonane pomyślnie.")

            arcpy.management.TruncateTable(fr'{paths["sde"]}\\{warstwa}_2180_t')
            print(f'wykonanie TruncateTable {warstwa}_2180_t')

            append_with_field_mapping(
                input_table=fr'{paths["geobaza"]}\\{warstwa}_2180_t',
                target_table=fr'{paths["sde"]}\\{warstwa}_2180_t'
            )
            print(f'wykonanie Append {warstwa}_2180_t')

            arcpy.conversion.TableToTable(fr'{paths["sde"]}\pgq_sde.azymuty.{warstwa}', paths["geobaza"],
                                          fr'{warstwa}_tabela')
            print(f"TableToTable wykonane pomyślnie pgq_sde.azymuty.{warstwa}")

            arcpy.management.JoinField(
                in_data=fr'{paths["geobaza"]}\\{warstwa}_2180_t',
                in_field=id_field,
                join_table=fr'{paths["geobaza"]}\\{warstwa}_tabela',
                join_field=join_field,
                fields="loc_name;loc_obj;loc_code;site_name;site_obj;site_id;cell_name;cell_obj;cell_id;band;data_aktualizacji"
            )
            print("JoinField wykonane pomyślnie.")

            arcpy.management.Project(
                in_dataset=fr'{paths["geobaza"]}\\{warstwa}_2180_t',
                out_dataset=fr'{paths["geobaza"]}\\{warstwa}_3857_t',
                out_coor_system=paths["_WGS_84_"]
            )
            print(f"Project_management _PUWG_92_ wykonane pomyślnie {warstwa}_3857_t")

            arcpy.management.TruncateTable(fr'{paths["sde"]}\\{warstwa}_3857_t')
            print(f'wykonanie TruncateTable {warstwa}_3857_t')

            append_with_field_mapping(
                input_table=fr'{paths["geobaza"]}\\{warstwa}_3857_t',
                target_table=fr'{paths["sde"]}\\{warstwa}_3857_t'
            )
            print(f'wykonanie Append {warstwa}_3857_t')

    except Exception as e:
        logging.error(f'Błąd: {str(e)}')

logging.debug('Zakończenie skryptu.')
print('###########################')
arcpy.management.TruncateTable(fr"{paths['sde']}\\mv_azimuth_fdd3600_t_3857_table")
print(f'wykonanie TruncateTable mv_azimuth_fdd3600_t_3857_table')
arcpy.management.Append(fr'{paths["sde"]}\\mv_azimuth_fdd3600_t_3857_t',
                        fr"{paths['sde']}\\pgq_sde.azymuty.mv_azimuth_fdd3600_t_3857_table", "TEST", None, '', '')
print(f'wykonanie Append pgq_sde.azymuty.mv_azimuth_fdd3600_t_3857_table')
print('Koniec')
