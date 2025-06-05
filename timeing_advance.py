# -*- coding: utf-8 -*-
import arcpy
import logging
import re

# Ustawienie konfiguracji logowania
logging.basicConfig(
    filename='D:\\replikacja\\model_builder\\Python_3\\log_time_advance.txt',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Przykładowe logowanie
logging.debug('Rozpoczęcie skryptu.')
print("Start")
arcpy.env.overwriteOutput = True

# Definicja ścieżek do SDE, projekcji i bazy geodanych
paths = {
    "sde": r'D:\sde\126.185.136.190_tadvance.sde',
    "_PUWG_92_": r'D:\projections\ETRS 1989 Poland CS92.prj',
    "_WGS_84_": r'D:\projections\WGS 1984 Web Mercator (auxiliary sphere).prj',
    "geobaza": r'D:\projekty_aprx\orange_projekty_aprx\time_advance\time_advance.gdb',
}

# Ustawienie przestrzeni roboczej na ścieżkę SDE
arcpy.env.workspace = fr'{paths["sde"]}'

# Lista klas obiektów pasujących do określonego wzoru
lista = arcpy.ListFeatureClasses('pgq_sde.tadvance.mv_t_*', 'ALL')

# Wydrukuj listę klas obiektów
print(lista)


def sanitize_name(name):
    """Zamień nieprawidłowe znaki na podkreślenia."""
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


def create_field_mapping(input_table, target_table):
    """Create field mapping string for Append tool."""
    input_fields = arcpy.ListFields(input_table)
    target_fields = arcpy.ListFields(target_table)

    field_mapping_str = ""
    for input_field in input_fields:
        if input_field.name in [field.name for field in target_fields]:
            field_mapping_str += f'{input_field.name} "{input_field.name}" true true false {input_field.length} {input_field.type} 0 0,First,#,{input_table},{input_field.name},-1,-1;'

    return field_mapping_str


# Iteracja przez listę klas obiektów
for x in lista:
    try:
        print('\n')
        print('----------------------------------')
        print(fr'Wczytana zmienna: {x}')
        print('----------------------------------')
        print('\n')

        # Zamiana 'mv' na 'tbl' w nazwie tabeli docelowej
        target_table = x.replace('mv', 'tbl')
        input_table_append = x.replace('pgq_sde.tadvance.', '')

        # Konwersja klasy obiektów do bazy geodanych
        arcpy.conversion.FeatureClassToGeodatabase(
            Input_Features=fr"{paths['sde']}\\{x}",
            Output_Geodatabase=fr"{paths['geobaza']}"
        )
        print('Konwersja zakończona dla:', x)
        print('\n')

        # Truncate target table
        arcpy.management.TruncateTable(fr'{paths["sde"]}\\{target_table}')
        print(f'Truncate zakończone dla: {target_table}')
        print('\n')

        # Create field mapping string
        field_mapping_str = create_field_mapping(fr"{paths['geobaza']}\\{input_table_append}",
                                                 fr'{paths["sde"]}\\{target_table}')
        print(f'Field Mapping: {field_mapping_str}')

        # Append data with field mapping
        arcpy.management.Append(
            inputs=fr"{paths['geobaza']}\\{input_table_append}",
            target=fr'{paths["sde"]}\\{target_table}',
            schema_type="NO_TEST",
            field_mapping=field_mapping_str,
            subtype="",
            expression="",
            match_fields=None,
            update_geometry="NOT_UPDATE_GEOMETRY"
        )
        print('Append zakończone dla:', input_table_append)
        print('\n')

    except Exception as e:
        # Logowanie wszelkich błędów, które wystąpią podczas przetwarzania
        logging.error('Błąd: {}'.format(str(e)))
        print(f'Błąd podczas przetwarzania dla {x}: {str(e)}')

# Wskazanie końca skryptu
print('Koniec')
logging.debug('Zakończenie skryptu.')
