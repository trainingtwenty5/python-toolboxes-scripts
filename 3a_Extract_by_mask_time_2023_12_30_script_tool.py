# -*- coding: utf-8 -*-
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import time
import arcpy

# Wczytanie pliku rastrowego
input_rasterio = arcpy.GetParameterAsText(0)
with rasterio.open(input_rasterio) as src:

    # Wczytanie danych maski w formacie wektorowym (np. Shapefile)
    input_mask_gdf = arcpy.GetParameterAsText(1)
    mask_gdf = gpd.read_file(input_mask_gdf)

    # Zapisanie wyniku do nowego pliku rastrowego z takim samym zasięgiem jak warstwa wektorowa
    output_raster_path = arcpy.GetParameterAsText(2)

    # Pobranie zasięgu (extent) z warstwy wektorowej
    mask_extent = mask_gdf.total_bounds
    
    print('\n')
    print('Wycinanie do maski')
    print('\n')
    
    print("Zasięg (Extent) z warstwy wektorowej ArcGIS Pro:")
    print("Top: ", mask_extent[3])
    print("Bottom: ", mask_extent[1])
    print("Left:", mask_extent[0])
    print("Right:", mask_extent[2])
  
    # Pomiar czasu rozpoczęcia operacji
    start_time = time.time()

    # Wykonanie operacji maskowania
    out_image, out_transform = mask(src, shapes=mask_gdf.geometry, crop=True)

    # Pomiar czasu zakończenia operacji
    end_time = time.time()

    # Konwertuj NumPy array na raster przy użyciu arcpy
    raster = arcpy.NumPyArrayToRaster(out_image, arcpy.Point(mask_extent[0], mask_extent[1]),
                                      src.res[0], src.res[1])

    # Zapisz rastrowy obiekt do nowego pliku
    try:
        raster.save(output_raster_path)
        print("Zapisano pomyślnie.")
        print('Wycinanie do maski - zakończono')
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku rastrowego: {str(e)}")

# Obliczenie czasu trwania operacji i wydrukowanie wyniku
duration = round((end_time - start_time) / 60, 2)
print(f"\nCzas trwania operacji: {duration} minut\n")