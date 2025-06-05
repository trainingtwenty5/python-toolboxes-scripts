import arcpy

# Definiuj nazwy tabel i pola
table1_name = "TERYT_2024_Granice_wojewodztw_ko_SpatialJoin_v6"
field1_name = "TERYT1"

table2_name = "PLIK_WZORCOWY_prawdopodobieństwo_201701"
field2_name = "TERYT"

# Pobierz unikalne wartości z ob i GCELL_NAME
values_ob = set([row[0] for row in arcpy.da.SearchCursor(table1_name, field1_name)])
values_GCELL_NAME = set([row[0] for row in arcpy.da.SearchCursor(table2_name, field2_name)])

# Znajdź wspólne wartości
common_values = values_ob.intersection(values_GCELL_NAME)

# Wydrukuj wynik
#print("Wspólne wartości w kolumnach 'ob' i 'GCELL_NAME':")
#print(common_values)
print("Liczba wspólnych wartości: {}".format(len(common_values)))
