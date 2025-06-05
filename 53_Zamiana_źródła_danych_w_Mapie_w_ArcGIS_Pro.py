import arcpy
import os

# Pobierz bieżący projekt ArcGIS Pro
project = arcpy.mp.ArcGISProject("CURRENT")

# Wybierz aktywną mapę
active_map = project.activeMap

arcpy.env.workspace = r"D:\COVERAGE\dane_2024_10\2024_10_DANE_3857.gdb"
new_data_sources = arcpy.ListRasters("*")

if active_map:
    # Lista warstw na mapie
    layers = active_map.listLayers()

    for layer in layers:
        if layer.isRasterLayer:  # Sprawdź, czy warstwa jest typu Raster
            # Wyciągnij ścieżkę do geobazy i nazwę warstwy
            full_data_source = layer.dataSource
            gdb_path = os.path.dirname(full_data_source)  # Ścieżka do geobazy
            layer_name = os.path.basename(full_data_source)  # Nazwa warstwy

            print(f'Geobaza: {gdb_path}')
            print(f'Nazwa warstwy: {layer_name}')
            layer_name = layer.name
            print(f'Warstwa na mapie: {layer_name}')
            print('\n')

            if "C-BAND" in layer.name:
                for raster in new_data_sources:
                    if "OPL_COV_CBAND3600_5class" in raster:
                        print('ok')
                        find_dict = {
                            'connection_info': {'database': fr'{gdb_path}'},
                            'dataset': fr'{layer_name}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(find_dict)
                        print('\n')
                        # new_raster_path = arcpy.env.workspace + "\\" + raster
                        new_raster_path = arcpy.env.workspace
                        replace_dict = {
                            'connection_info': {'database': fr'{new_raster_path}'},
                            'dataset': fr'{raster}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(replace_dict)
                        print('\n')
                        layer.updateConnectionProperties(find_dict, replace_dict)

            elif "DSS" in layer.name:
                for raster in new_data_sources:
                    if "COV_DSS_OPL_20241101_50m_cut_reclass" in raster:
                        print('ok')
                        find_dict = {
                            'connection_info': {'database': fr'{gdb_path}'},
                            'dataset': fr'{layer_name}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(find_dict)
                        print('\n')
                        # new_raster_path = arcpy.env.workspace + "\\" + raster
                        new_raster_path = arcpy.env.workspace
                        replace_dict = {
                            'connection_info': {'database': fr'{new_raster_path}'},
                            'dataset': fr'{raster}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(replace_dict)
                        print('\n')
                        layer.updateConnectionProperties(find_dict, replace_dict)

            elif "LTE 800" in layer.name:
                for raster in new_data_sources:
                    if "OPL_COV_LTE800_5class" in raster:
                        print('ok')
                        find_dict = {
                            'connection_info': {'database': fr'{gdb_path}'},
                            'dataset': fr'{layer_name}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(find_dict)
                        print('\n')
                        # new_raster_path = arcpy.env.workspace + "\\" + raster
                        new_raster_path = arcpy.env.workspace
                        replace_dict = {
                            'connection_info': {'database': fr'{new_raster_path}'},
                            'dataset': fr'{raster}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(replace_dict)
                        print('\n')
                        layer.updateConnectionProperties(find_dict, replace_dict)
            elif "LTE 900" in layer.name:
                for raster in new_data_sources:
                    if "OPL_COV_LTE900_5class" in raster:
                        print('ok')
                        find_dict = {
                            'connection_info': {'database': fr'{gdb_path}'},
                            'dataset': fr'{layer_name}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(find_dict)
                        print('\n')
                        # new_raster_path = arcpy.env.workspace + "\\" + raster
                        new_raster_path = arcpy.env.workspace
                        replace_dict = {
                            'connection_info': {'database': fr'{new_raster_path}'},
                            'dataset': fr'{raster}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(replace_dict)
                        print('\n')
                        layer.updateConnectionProperties(find_dict, replace_dict)

            elif "LTE 1800" in layer.name:
                for raster in new_data_sources:
                    if "OPL_COV_LTE1800_5class" in raster:
                        find_dict = {
                            'connection_info': {'database': fr'{gdb_path}'},
                            'dataset': fr'{layer_name}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(find_dict)
                        print('\n')
                        # new_raster_path = arcpy.env.workspace + "\\" + raster
                        new_raster_path = arcpy.env.workspace
                        replace_dict = {
                            'connection_info': {'database': fr'{new_raster_path}'},
                            'dataset': fr'{raster}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(replace_dict)
                        print('\n')
                        layer.updateConnectionProperties(find_dict, replace_dict)

            elif "LTE 2100" in layer.name:
                for raster in new_data_sources:
                    if "OPL_COV_LTE2100_5class" in raster:
                        find_dict = {
                            'connection_info': {'database': fr'{gdb_path}'},
                            'dataset': fr'{layer_name}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(find_dict)
                        print('\n')
                        # new_raster_path = arcpy.env.workspace + "\\" + raster
                        new_raster_path = arcpy.env.workspace
                        replace_dict = {
                            'connection_info': {'database': fr'{new_raster_path}'},
                            'dataset': fr'{raster}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(replace_dict)
                        print('\n')
                        layer.updateConnectionProperties(find_dict, replace_dict)
            elif "UMTS 900" in layer.name:
                for raster in new_data_sources:
                    if "OPL_COV_UMTS900_5class" in raster:
                        find_dict = {
                            'connection_info': {'database': fr'{gdb_path}'},
                            'dataset': fr'{layer_name}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(find_dict)
                        print('\n')
                        # new_raster_path = arcpy.env.workspace + "\\" + raster
                        new_raster_path = arcpy.env.workspace
                        replace_dict = {
                            'connection_info': {'database': fr'{new_raster_path}'},
                            'dataset': fr'{raster}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(replace_dict)
                        print('\n')
                        layer.updateConnectionProperties(find_dict, replace_dict)
            elif "UMTS 2100" in layer.name:
                for raster in new_data_sources:
                    if "OPL_COV_UMTS2100_5class" in raster:
                        find_dict = {
                            'connection_info': {'database': fr'{gdb_path}'},
                            'dataset': fr'{layer_name}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(find_dict)
                        print('\n')
                        # new_raster_path = arcpy.env.workspace + "\\" + raster
                        new_raster_path = arcpy.env.workspace
                        replace_dict = {
                            'connection_info': {'database': fr'{new_raster_path}'},
                            'dataset': fr'{raster}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(replace_dict)
                        print('\n')
                        layer.updateConnectionProperties(find_dict, replace_dict)
            elif "GSM" in layer.name:
                for raster in new_data_sources:
                    if "OPL_COV_GSM_5class" in raster:
                        find_dict = {
                            'connection_info': {'database': fr'{gdb_path}'},
                            'dataset': fr'{layer_name}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(find_dict)
                        print('\n')
                        # new_raster_path = arcpy.env.workspace + "\\" + raster
                        new_raster_path = arcpy.env.workspace
                        replace_dict = {
                            'connection_info': {'database': fr'{new_raster_path}'},
                            'dataset': fr'{raster}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(replace_dict)
                        print('\n')
                        layer.updateConnectionProperties(find_dict, replace_dict)

            elif "LTE 2600" in layer.name:
                for raster in new_data_sources:
                    if "OPL_COV_LTE2600_5class" in raster:
                        find_dict = {
                            'connection_info': {'database': fr'{gdb_path}'},
                            'dataset': fr'{layer_name}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(find_dict)
                        print('\n')
                        # new_raster_path = arcpy.env.workspace + "\\" + raster
                        new_raster_path = arcpy.env.workspace
                        replace_dict = {
                            'connection_info': {'database': fr'{new_raster_path}'},
                            'dataset': fr'{raster}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(replace_dict)
                        print('\n')
                        layer.updateConnectionProperties(find_dict, replace_dict)

            elif "LTE" in layer.name:
                for raster in new_data_sources:
                    if "OPL_COV_LTE_5class_" in raster:
                        find_dict = {
                            'connection_info': {'database': fr'{gdb_path}'},
                            'dataset': fr'{layer_name}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(find_dict)
                        print('\n')
                        # new_raster_path = arcpy.env.workspace + "\\" + raster
                        new_raster_path = arcpy.env.workspace
                        replace_dict = {
                            'connection_info': {'database': fr'{new_raster_path}'},
                            'dataset': fr'{raster}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(replace_dict)
                        print('\n')
                        layer.updateConnectionProperties(find_dict, replace_dict)

            elif "LTE CA" in layer.name:
                for raster in new_data_sources:
                    if "CA_OPL_" in raster:
                        find_dict = {
                            'connection_info': {'database': fr'{gdb_path}'},
                            'dataset': fr'{layer_name}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(find_dict)
                        print('\n')
                        # new_raster_path = arcpy.env.workspace + "\\" + raster
                        new_raster_path = arcpy.env.workspace
                        replace_dict = {
                            'connection_info': {'database': fr'{new_raster_path}'},
                            'dataset': fr'{raster}',
                            'workspace_factory': 'File Geodatabase'
                        }

                        print(replace_dict)
                        print('\n')
                        layer.updateConnectionProperties(find_dict, replace_dict)

project.save()
