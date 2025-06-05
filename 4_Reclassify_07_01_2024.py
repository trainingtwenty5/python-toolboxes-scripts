import rasterio
from rasterio.transform import from_origin
from rasterio.enums import Resampling
import time


# Ścieżka do wejściowego pliku rasterowego
input_raster_path = r'D:\ArcGIS\2023_12_28_5G_DSS_NEW\testowa_30_12_2023\Extract_raster_077_01_2024.tif'

# Ścieżka do wyjściowego pliku rasterowego po zreklasyfikowaniu
output_raster_path = r'D:\ArcGIS\2023_12_28_5G_DSS_NEW\testowa_30_12_2023\Reclassified_raster_077_01_2024_nodata_0072.tif'

# Wartość NoData
noData = 11
# Pomiar czasu rozpoczęcia operacji
start_time = time.time()


# Otwieranie istniejącego pliku rasterowego
with rasterio.open(input_raster_path) as src:
    # Odczyt danych z istniejącego pliku
    input_data = src.read(1)

    # Zmiana wartości zgodnie z zadanymi kryteriami
    output_data = input_data.copy()
    output_data[output_data == 15] = noData  # 15 to no data
    output_data[(output_data == 1) | (output_data == 2)] = 1  # 1 i 2 to wartość 1
    output_data[(output_data == 3) | (output_data == 4) | (output_data == 5)] = 2  # 3, 4, 5 to wartość 2
    
    try:
        # Tworzenie nowego pliku rasterowego z zreklasyfikowanymi danymi
        with rasterio.open(
                output_raster_path,
                'w',
                driver='GTiff',
                height=src.height,
                width=src.width,
                count=1,
                dtype='uint8',
                crs=src.crs,
                transform=src.transform,
        ) as dst:
            # Ustawienie wartości NoData
            dst.nodata = noData  # Możesz ustawić inną wartość NoData według potrzeb
            dst.write(output_data, 1)


        print("Zapisano pomyślnie.")
        print('reklasyfikacja - done')
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku rastrowego: {str(e)}")

end_time = time.time()

# Obliczenie czasu trwania operacji i wydrukowanie wyniku
duration = round((end_time - start_time) / 60, 2)
print(f"\nCzas trwania operacji: {duration} minut\n")

print('reklasyfikacja - done')