def znajdz_plik_w_projekcie(nazwa_pliku):
    # Pobierz aktualny projekt ArcGIS Pro
    projekt = arcpy.mp.ArcGISProject("CURRENT")

    # Przeszukaj wszystkie warstwy w projekcie
    for mapa in projekt.listMaps():
        for warstwa in mapa.listLayers():
            try:
                if warstwa.supports("DATASOURCE") and os.path.isfile(warstwa.dataSource):
                    if warstwa.name.lower() == nazwa_pliku.lower():
                        return warstwa.dataSource
            except AttributeError:
                pass

    # Pobierz ścieżkę do katalogu projektu
    katalog_projektu = os.path.dirname(projekt.filePath)

    # Przeszukaj projekt w poszukiwaniu pliku, w tym geobaz plikowych
    for root, dirs, files in os.walk(katalog_projektu):
        for plik in files:
            if plik.lower() == nazwa_pliku.lower():
                return os.path.join(root, plik)
        for dir in dirs:
            if dir.endswith(".gdb"):
                gdb_path = os.path.join(root, dir)
                arcpy.env.workspace = gdb_path
                for ds in arcpy.ListDatasets():
                    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                        if fc.lower() == nazwa_pliku.lower():
                            return os.path.join(gdb_path, ds, fc)
                for fc in arcpy.ListFeatureClasses():
                    if fc.lower() == nazwa_pliku.lower():
                        return os.path.join(gdb_path, fc)

    # Jeśli nie znaleziono pliku, zwróć None
    return None