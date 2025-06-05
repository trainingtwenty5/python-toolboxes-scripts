import arcpy
import os


# Function to update layer connection properties
def update_layer_connection(layer, gdb_path, raster):
    find_dict = {
        'connection_info': {'database': fr'{gdb_path}'},
        'dataset': fr'{layer.name}',
        'workspace_factory': 'File Geodatabase'
    }

    new_raster_path = arcpy.env.workspace
    replace_dict = {
        'connection_info': {'database': fr'{new_raster_path}'},
        'dataset': fr'{raster}',
        'workspace_factory': 'File Geodatabase'
    }

    layer.updateConnectionProperties(find_dict, replace_dict)


# Main code
project = arcpy.mp.ArcGISProject("CURRENT")
active_map = project.activeMap
arcpy.env.workspace = r"D:\COVERAGE\dane_2024_10\2024_10_DANE_3857.gdb"
new_data_sources = arcpy.ListRasters("*")
print(new_data_sources)

if active_map:
    layers = active_map.listLayers()
    raster_mapping = {
        "C-BAND": "OPL_COV_CBAND3600_5class",
        "DSS": "COV_DSS_OPL_20241101_50m_cut_reclass",
        "LTE 800": "OPL_COV_LTE800_5class",
        "LTE 900": "OPL_COV_LTE900_5class",
        "LTE 1800": "OPL_COV_LTE1800_5class",
        "LTE 2100": "OPL_COV_LTE2100_5class",
        "UMTS 900": "OPL_COV_UMTS900_5class",
        "UMTS 2100": "OPL_COV_UMTS2100_5class",
        "GSM": "OPL_COV_GSM_5class",
        "LTE 2600": "OPL_COV_LTE2600_5class",
        "LTE CA": "CA_OPL_",
        "LTE": "OPL_COV_LTE_5class_"
    }

    for layer in layers:
        if layer.isRasterLayer:
            gdb_path = os.path.dirname(layer.dataSource)
            print(f'Geobaza: {gdb_path}')
            print(f'Warstwa na mapie: {layer.name}\n')

            for key, raster in raster_mapping.items():
                if key in layer.name and raster in new_data_sources:
                    print('ok')
                    update_layer_connection(layer, gdb_path, raster)
                    print('\n')

project.save()
