import arcpy

# Ścieżki do danych
warstwa = "L800_20250124_XY_3857_t4"
tabele = ["T2024_01_01_00_00_00", "T2024_02_01_00_00_00", "T2024_03_01_00_00_00",
    "T2024_04_01_00_00_00", "T2024_05_01_00_00_00", "T2024_06_01_00_00_00",
    "T2024_07_01_00_00_00", "T2024_08_01_00_00_00", "T2024_09_01_00_00_00",
    "T2024_10_01_00_00_00"
]
# Pętla wykonująca złączenia
for tabela in tabele:
    try:
        # Utwórz prefix na podstawie nazwy tabeli (T2024_01 lub T2024_02)
        prefix = tabela[:8]

        # Lista pól do złączenia (wszystkie pola z tabeli oprócz OBJECTID)
        fields = [f.name for f in arcpy.ListFields(tabela) if f.name != 'OBJECTID']

        # Przygotuj nowe nazwy pól
        new_field_names = [f"{prefix}_{field}" for field in fields]

        # Wykonaj złączenie
        arcpy.JoinField_management(
            in_data=warstwa,
            in_field="OBJ_D",
            join_table=tabela,
            join_field="obj_cell_d",
            fields=fields
        )

        # Zmień nazwy pól
        for old_name, new_name in zip(fields, new_field_names):
            try:
                arcpy.AlterField_management(
                    in_table=warstwa,
                    field=old_name,
                    new_field_name=new_name,
                    new_field_alias=new_name
                )
            except:
                print(f"Nie można zmienić nazwy pola {old_name} na {new_name}")

        print(f"Złączono tabelę: {tabela}")
    except Exception as e:
        print(f"Błąd podczas łączenia tabeli {tabela}: {str(e)}")
