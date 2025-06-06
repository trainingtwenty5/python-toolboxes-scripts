import arcpy

# Pobierz bieżący projekt ArcGIS Pro
project = arcpy.mp.ArcGISProject("CURRENT")

# Wybierz aktywną mapę
active_map = project.activeMap

# Sprawdzenie, czy mapa jest aktywna
if active_map:
    # Lista warstw na mapie
    layers = active_map.listLayers()

    # Iteracja przez każdą warstwę
    for layer in layers:
        if layer.isFeatureLayer:  # Sprawdza, czy warstwa jest warstwą wektorową
            print(f'Warstwa: {layer.name}')

            # Odczytaj wszystkie pola z tabeli atrybutów warstwy
            fields = arcpy.ListFields(layer)

            # Wyświetl nazwy pól
            print("Nazwy kolumn (pól):")
            for field in fields:
                print(f"- {field.name}")

            print()  # Dodatkowa linia odstępu po każdej warstwie

    # Lista tabel na mapie
    tables = active_map.listTables()

    # Iteracja przez każdą tabelę
    for table in tables:
        print(f'Tabela: {table.name}')

        # Odczytaj wszystkie pola z tabeli
        fields = arcpy.ListFields(table)

        # Wyświetl nazwy pól
        print("Nazwy kolumn (pól):")
        for field in fields:
            print(f"- {field.name}")

        print()  # Dodatkowa linia odstępu po każdej tabeli

else:
    print("Brak aktywnej mapy w projekcie.")
