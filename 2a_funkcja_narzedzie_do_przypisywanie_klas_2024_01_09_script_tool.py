import arcpy

def przypisz_klasy(obiekty_path, pole_wysokosci_obiektow, pole_klasy_shp, tabela_path, pole_klasy_tabeli):
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

    # Sprawdzenie, czy pole już istnieje
    if not arcpy.ListFields(obiekty_path, pole_klasy_shp):
        # Dodanie pola, jeśli jeszcze nie istnieje
        arcpy.AddField_management(obiekty_path, pole_klasy_shp, "DOUBLE", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')

    # Wczytanie klasy obiektów
    with arcpy.da.UpdateCursor(obiekty_path, [pole_wysokosci_obiektow, pole_klasy_shp]) as klasy_obiektow:
        for row in klasy_obiektow:
            Wysokość_obiektu = row[0]

            # Wczytanie drugiej tabeli
            with arcpy.da.SearchCursor(tabela_path, [pole_klasy_tabeli]) as druga_tabela:
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

                # Resetowanie drugiej tabeli
                druga_tabela.reset()

                # Aktualizacja pola klasy obiektów, jeśli znaleziono pasującą klasę
                if znaleziono_klase:
                    print(f"Przypisano do klasy: {row[1]}")

# Pobieranie parametrów z ArcGIS Pro
obiekty_path = arcpy.GetParameterAsText(0)
pole_wysokosci_obiektow = arcpy.GetParameterAsText(1)
pole_klasy_shp = arcpy.GetParameterAsText(2)
tabela_path = arcpy.GetParameterAsText(3)
pole_klasy_tabeli = arcpy.GetParameterAsText(4)


# Wywołanie funkcji
przypisz_klasy(obiekty_path, pole_wysokosci_obiektow, pole_klasy_shp, tabela_path, pole_klasy_tabeli)

arcpy.management.JoinField(obiekty_path, pole_klasy_shp, tabela_path, pole_klasy_tabeli, None, "NOT_USE_FM", None)