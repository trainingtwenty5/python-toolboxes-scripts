import rasterio
from rasterio.transform import from_origin
from rasterio.enums import Resampling
import arcpy
import time
arcpy.env.overwriteOutput = True
# Ścieżka do wejściowego pliku rasterowego
input_raster_path = arcpy.GetParameterAsText(0)
# Ścieżka do wyjściowego pliku rasterowego po zreklasyfikowaniu
output_raster_path = arcpy.GetParameterAsText(1)
# Wartości NoData - użytkownik wpisuje te wartości, oddzielone przecinkami
noData_values = [int(val.strip()) for val in arcpy.GetParameterAsText(2).split(",")]

# Parametry opcjonalne z domyślnymi wartościami
default_value_3 = int(arcpy.GetParameterAsText(3)) if arcpy.GetParameter(3) and arcpy.GetParameterAsText(3) != '' else 0
default_value_4 = int(arcpy.GetParameterAsText(4)) if arcpy.GetParameter(4) and arcpy.GetParameterAsText(4) != '' else 1
default_value_5 = int(arcpy.GetParameterAsText(5)) if arcpy.GetParameter(5) and arcpy.GetParameterAsText(5) != '' else 2
default_value_6 = int(arcpy.GetParameterAsText(6)) if arcpy.GetParameter(6) and arcpy.GetParameterAsText(6) != '' else 3
default_value_7 = int(arcpy.GetParameterAsText(7)) if arcpy.GetParameter(7) and arcpy.GetParameterAsText(7) != '' else 4
default_value_8 = int(arcpy.GetParameterAsText(8)) if arcpy.GetParameter(8) and arcpy.GetParameterAsText(8) != '' else 5

# Pomiar czasu rozpoczęcia operacji
start_time = time.time()
# Otwieranie istniejącego pliku rasterowego
with rasterio.open(input_raster_path) as src:
    # Odczyt danych z istniejącego pliku
    input_data = src.read(1)
    # Zmiana wartości zgodnie z zadanymi kryteriami
    output_data = input_data.copy()
    for noData_value in noData_values:
        output_data[output_data == noData_value] = src.nodata  # Ustaw wartość NoData zgodnie z wartością wprowadzoną przez użytkownika
    #output_data[output_data == noData_value] = src.nodata
    output_data[output_data == 0] = default_value_3
    output_data[output_data == 1] = default_value_4
    output_data[output_data == 2] = default_value_5
    output_data[output_data == 3] = default_value_6
    output_data[output_data == 4] = default_value_7
    output_data[output_data == 5] = default_value_8

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
            # dst.nodata = noData  # Możesz ustawić inną wartość NoData według potrzeb
            dst.nodata = src.nodata
            # Możesz ustawić inną wartość NoData według potrzeb
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