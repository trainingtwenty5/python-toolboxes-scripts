# -*- coding: utf-8 -*-
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import time
import arcpy

# Zapisanie wyniku do nowego pliku rastrowego z takim samym zasięgiem jak warstwa wektorowa
output_raster_path = r'D:\ArcGIS\2023_12_28_5G_DSS_NEW\testowa_30_12_2023\Extract_raster_5555_01_2024.tif'

# Wczytanie pliku rastrowego
with rasterio.open(r'D:\ArcGIS\5G_DSS\Dane\Daniel-20231212T131124Z-001\Daniel\cov_DSS_eo202311\COV_DSS_OPL_20231201_25m_cut_reclass.tif') as src:

    # Wczytanie danych maski w formacie wektorowym (np. Shapefile)
    mask_gdf = gpd.read_file(r'D:\ArcGIS\2023_12_28_5G_DSS_NEW\testowa_30_12_2023\e5_Maska_do_A03_Granice_gmin_Intersect.shp')

    # Pobranie zasięgu (extent) z warstwy wektorowej
    mask_extent = mask_gdf.total_bounds
    
    print('\n')
    print('wycienanie_do_maski')
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


    #with rasterio.open(output_raster_path, 'w', **src.profile) as dst:
    #    dst.write(out_image)
        
        
    # Konwertuj NumPy array na raster przy użyciu arcpy
    raster = arcpy.NumPyArrayToRaster(out_image, arcpy.Point(mask_extent[0], mask_extent[1]),
                                      src.res[0], src.res[1])
                                      
    # Ustawienie wartości NoData na podstawie wartości NoData z oryginalnego rastra
    #raster.noData = src.nodatavals[0] if src.nodatavals else None                                  

    # Zapisz rastrowy obiekt do nowego pliku
    try:
        raster.save(output_raster_path)
        print("Zapisano pomyślnie.")
        print('wycienanie_do_maski - done')
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku rastrowego: {str(e)}")

    


# Obliczenie czasu trwania operacji i wydrukowanie wyniku
duration = round((end_time - start_time) / 60, 2)
print(f"\nCzas trwania operacji: {duration} minut\n")


