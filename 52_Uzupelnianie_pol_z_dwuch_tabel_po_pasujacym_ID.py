import arcpy

# Ścieżki do tabel
input_table = "Prawdopodobienstwo_UMTS2100.csv"
output_table = "PRG_POLY_19_04_2024"

# Użycie kursora do odczytu danych z tabeli wejściowej
with arcpy.da.SearchCursor(input_table, ['TERYT', 'prawd_średnie', 'prawd_min', 'prawd_maks']) as search_cursor:
    # Użycie kursora do aktualizacji danych w tabeli wyjściowej
    with arcpy.da.UpdateCursor(output_table, ['TERYT', 'AVG_3G_210', 'MIN_3G_210', 'MAX_3G_210']) as update_cursor:
        # Tworzenie słownika z danymi z tabeli wejściowej
        input_data = {row[0]: row[1:] for row in search_cursor}

        for update_row in update_cursor:
            id_value = update_row[0]
            if id_value in input_data:
                # Aktualizacja pól na podstawie wartości z tabeli wejściowej
#                 update_row[1:] = input_data[id_value]
#                 update_cursor.updateRow(update_row)
                # Aktualizacja pól na podstawie wartości z tabeli wejściowej
                values_to_update = input_data[id_value]
                # Ustawienie wartości na 0, jeśli są None
                update_row[1] = values_to_update[0] if values_to_update[0] is not None else 0
                update_row[2] = values_to_update[1] if values_to_update[1] is not None else 0
                update_row[3] = values_to_update[2] if values_to_update[2] is not None else 0
                update_cursor.updateRow(update_row)

print("Pola zostały zaktualizowane na podstawie ID 3.")