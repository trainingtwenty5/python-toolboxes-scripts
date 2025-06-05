## Ostrzeżenie Prawne

Kopiowanie i pobieranie repozytorium oraz korzystanie z niego bez odpowiednich formalności prawnych jest surowo zabronione.

## Narzędzia i Skrypty

### Skrypt typu (np. 10a) to Script tool [What is a script tool?]([https://desktop.arcgis.com/en/arcmap/latest/analyze/creating-tools/what-is-a-script-tool-.htm](https://desktop.arcgis.com/en/arcmap/latest/analyze/creating-tools/a-quick-tour-of-creating-script-tools.htm)).

Skrypt z literą 'a' to narzędzie do ArcGISa, które umożliwia wykonywanie określonych funkcji. Poniżej znajdziesz informacje dotyczące PARAMETRÓW, KTÓRE TRZEBA UZUPEŁNIĆ SAMODZIENIE.

### Skrypt 3a 

Poniżej znajdziesz informacje dotyczące skryptu:

- **Nazwa:** Skrypt 3a
- **Opis:** Extract_by_mask - Raster, a *Shp.
- **Parametry:**
  - Parametr 1: Plik rastrowy, który będzie wycinany
    - Data Typ: (Raster Dataset),
    - Direction: (Input).
    
  - Parametr 2:  Wczytanie danych maski w formacie wektorowym (np. Shapefile)
    - Data Typ: (Shapefile),
    - Direction: (Input).
    
  - Parametr 3:  Zapisanie wyniku do nowego pliku rastrowego z takim samym zasięgiem jak warstwa wektorowa
    - Data Typ: (Raster Dataset),
    - Direction: (Output).

### Skrypt 4a 

Poniżej znajdziesz informacje dotyczące skryptu:

- **Nazwa:** Skrypt 4a
- **Opis:** Reclassify - Rastra 5 klasowego i NoData.
- **Parametry:**
  - Parametr 0: Ścieżka do wejściowego pliku rasterowego
    - Data Typ: (Raster Dataset),
    - Direction: (Input).
    
  - Parametr 1: Ścieżka do wyjściowego pliku rasterowego po zreklasyfikowaniu
    - Data Typ: (Raster Dataset),
    - Direction: (Output).
    
  - Parametr 2: Wartości NoData - użytkownik wpisuje te wartości, oddzielone przecinkami 
    - Data Typ: (String),
    - Direction: (Output).
  
  - Parametr 3:  reklasyfikacja wartości 1
    - Data Typ: (String),
    - Direction: (Output).
  
  - Parametr 4:  reklasyfikacja wartości 2
    - Data Typ: (String),
    - Direction: (Output).
  
  - Parametr 5:  reklasyfikacja wartości 3
    - Data Typ: (String),
    - Direction: (Output).
  
  - Parametr 6:  reklasyfikacja wartości 4
    - Data Typ: (String),
    - Direction: (Output).
  
  - Parametr 7:  reklasyfikacja wartości 5
    - Data Typ: (String),
    - Direction: (Output).

### Skrypt 10a

Poniżej znajdziesz informacje dotyczące skryptu:

- **Nazwa:** Skrypt 10a
- **Opis:** ZonalStatistics - suma, max_value, min_value, mean_value.
- **Parametry:**
  - Parametr 0: Plik rastrowy, z którego będzie odczytywać wartości
    - Data Typ: (Raster Dataset),
    - Direction: (Input).
    
  - Parametr 1: Plik *SHP, któty jest naszym zoonem do zliczania statystyk
    - Data Typ: (Shapefile),
    - Direction: (Input).
    
  - Parametr 2: Wynikowy plik *shp
    - Data Typ: (Shapefile),
    - Direction: (Output).
