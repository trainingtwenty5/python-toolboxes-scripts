import arcpy

project = arcpy.mp.ArcGISProject("CURRENT")
active_map = project.activeMap

if active_map:
    target_layer = "L800_20250124_XY_3857_t"
    tables = ["T2024_01_01_00_00_00",
        "T2024_02_01_00_00_00", "T2024_03_01_00_00_00",
        "T2024_04_01_00_00_00", "T2024_05_01_00_00_00", "T2024_06_01_00_00_00",
        "T2024_07_01_00_00_00", "T2024_08_01_00_00_00", "T2024_09_01_00_00_00",
        "T2024_10_01_00_00_00"
    ]

    for table in tables:
        try:
            #  Extract year and month for naming.  Handles variable table names.
            table_suffix = table.split('_')[0] + "_" + table.split('_')[1]
            print(table_suffix)

            arcpy.management.JoinField(target_layer, "OBJ_D", table, "obj_cell_d")
            fields = arcpy.ListFields(table)
            for field in fields:
                if field.name not in ["OBJECTID", "obj_cell_d"]:
                    new_field_name = f"{field.name}_{table_suffix}"  # Consistent naming with year_month
                    if not arcpy.ListFields(target_layer, new_field_name):
                        arcpy.management.AddField(target_layer, new_field_name, field.type)
                        arcpy.management.CalculateField(target_layer, new_field_name, f"!{field.name}!", "PYTHON3")

        except arcpy.ExecuteError:
            print(arcpy.GetMessages())
else:
    print("No active map.")