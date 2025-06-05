import arcpy

# Definiuj nazwy tabel i pola
table1_name = r"D:\ArcGIS\2023_12_30_Prawdopodobienstwo\TERYT2024.gdb\TERYT_2024_done_Project_Mikroregiony_DONE"
table2_name = r"D:\ArcGIS\2023_12_30_Prawdopodobienstwo\Prawdopodobienstwo.gdb\PLIK_WZORCOWY_prawdopodobieństwo_201701"

fields_to_compare = ["TERYT", "NAME_PRG", "COMMUNE_NA", "COMMUNE", "TYPE", "TYPE_NAME",
                     "DISTRICT", "DISTRICT_N", "PROVINCE", "PROVINCE_N", "POP",
                     "ROLLOUT_TY", "ROLLOUT__1", "PROJ_CODE"]

# Inicjalizuj zbiory na wartości
common_values_count = {}
different_values = {}

# Porównaj każde pole z tabeli1 z odpowiadającym mu polem w tabeli2
for field in fields_to_compare:
    values_ob = set([str(row[0]).lower() for row in arcpy.da.SearchCursor(table1_name, field)])
    values_GCELL_NAME = set([str(row[0]).lower() for row in arcpy.da.SearchCursor(table2_name, field)])

    different_values[field] = values_ob.symmetric_difference(values_GCELL_NAME)
    common_values_count[field] = len(values_ob.intersection(values_GCELL_NAME))

    # Wydrukuj różne wartości dla każdego pola
    # print("\nRóżne wartości w kolumnie '{}':".format(field))
    # print(different_values[field])

    # Wygeneruj zapytanie SQL dla różnych wartości w polu 'TERYT'
    if field == 'TERYT':
        if len(different_values[field]) > 1:
            sql_query = " OR ".join(["TERYT = '{}'".format(value) for value in different_values[field]])
            print("\nZapytanie SQL dla różnych wartości w kolumnie 'TERYT':")
            print("({})".format(sql_query))

# Wydrukuj wspólne wartości dla każdego pola
for field, count in common_values_count.items():
    print("\nLiczba wspólnych wartości w kolumnie '{}': {}".format(field, count))
