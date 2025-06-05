import arcpy

# Utworzenie słownika dla zakresów klas
zakresy_klas = {
    10: (0, 10),
    20: (10, 20),
    30: (20, 30),
    40: (20, 30),
    50: (30, 40),
    60: (50, 60),
    70: (60, 70),
    80: (70, 80),
    90: (80, 90),
    100: (90, 100),
    110: (100, 110),
    111: (110, float('inf'))
}

# Ścieżki do plików shapefile
obiekty_path = r'D:\ArcGIS\2024_01_08_AVR_DIST\Dane\Maszty.shp'
# Nazwy pól w tabeli klas obiektów
pole_wysokosci_obiektow = 'h'
pole_klasy_shp = 'klase_shp'

# Ścieżki do tabeli
tabela_path = r'D:\ArcGIS\2024_01_08_AVR_DIST\2024_01_08_AVR_DIST.gdb\rollout_L1800_in_ExportTable'

# Nazwy pól w tabeli klas obiektów i drugiej tabeli
pole_klasy_tabeli = 'Klasa'


# Sprawdzenie, czy pole już istnieje
if not arcpy.ListFields(obiekty_path, pole_klasy_shp):
    # Dodanie pola, jeśli jeszcze nie istnieje
    arcpy.AddField_management(obiekty_path, pole_klasy_shp, "DOUBLE", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

# Wczytanie klasy obiektów
klasy_obiektow = arcpy.da.UpdateCursor(obiekty_path, [pole_wysokosci_obiektow, pole_klasy_shp])

# Przetwarzanie klas obiektów
for row in klasy_obiektow:
    Wysokość_obiektu = row[0]

    # Wczytanie drugiej tabeli
    druga_tabela = arcpy.da.SearchCursor(tabela_path, [pole_klasy_tabeli])

    # Flaga do sprawdzenia, czy znaleziono pasującą klasę
    znaleziono_klase = False

    # Przetwarzanie drugiej tabeli
    for record in druga_tabela:
        klasa_tabeli = record[0]
 

        # Sprawdzenie, do której klasy należy wysokość obiektu
        for klasa, zakres in zakresy_klas.items():
            if zakres[0] <= Wysokość_obiektu < zakres[1]:
                # Przypisanie rekordu do odpowiedniej klasy
                print(f'{zakres[0]}' + '<=' + f'{Wysokość_obiektu}' + '<' + f'{zakres[1]}')
                if klasa_tabeli == klasa:
                    znaleziono_klase = True
                    row[1] = klasa
                    klasy_obiektow.updateRow(row)
                    break  # Zakończ pętlę, gdy znajdziesz pasującą klasę
    druga_tabela.reset()

    # Aktualizacja pola klasy obiektów, jeśli znaleziono pasującą klasę
    if znaleziono_klase:
        print(f"Przypisano do klasy: {row[1]}")
