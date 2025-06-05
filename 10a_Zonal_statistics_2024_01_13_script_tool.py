# -*- coding: utf-8 -*-
import arcpy
import rasterio
from rasterio.windows import from_bounds
import geopandas as gpd
import numpy as np
from shapely.geometry import box

class ZonalStatistics():

    def __init__(self, raster_path, kwadraty_shp_path, ZonalStatistics_output):
        self.raster_path = raster_path
        self.kwadraty_shp_path = kwadraty_shp_path
        self.ZonalStatistics_output = ZonalStatistics_output

    def calculate_zonal_statistics(self):
        # Wczytanie rastra za pomocą Rasterio
        with rasterio.open(self.raster_path) as src:
            raster = src.read(1)
            raster_transform = src.transform
            raster_bounds = src.bounds

        # Wczytanie warstwy siatki kwadratów jako GeoDataFrame za pomocą Geopandas
        kwadraty_gdf = gpd.read_file(self.kwadraty_shp_path)

        # Iteracja przez każdy obszar z warstwy siatki kwadratów
        for index, row in kwadraty_gdf.iterrows():
            # Ekstrakcja geometrii obszaru
            geometry = row['geometry']

            # Przekształcenie geometrii obszaru do współrzędnych rastra
            window = from_bounds(*geometry.bounds, transform=raster_transform)
            
            pixels = raster[int(window.row_off):int(window.row_off + window.height), int(window.col_off):int(window.col_off + window.width)].astype(float)
            # Obliczenie sumy wartości pikseli wewnątrz obszaru
            suma = np.sum(pixels)
            
            # Obliczenie sumy, maksymalnej, minimalnej i średniej wartości pikseli wewnątrz obszaru
            suma = np.sum(pixels)
            max_value = np.max(pixels)
            min_value = np.min(pixels)
            mean_value = np.mean(pixels)
            
            # Dodanie wartości sumy, maksymalnej, minimalnej i średniej jako nowe kolumny w warstwie siatki kwadratów
            kwadraty_gdf.at[index, 'suma'] = suma
            kwadraty_gdf.at[index, 'max_value'] = max_value
            kwadraty_gdf.at[index, 'min_value'] = min_value
            kwadraty_gdf.at[index, 'mean_value'] = mean_value
            
        # Zapisanie warstwy siatki kwadratów z dodaną kolumną sumy do pliku SHP
        kwadraty_gdf.to_file(self.ZonalStatistics_output)

if __name__ == "__main__":
    arcpy.env.overwriteOutput = True

    #parametr Data Typ: Raster Dataset, Direction: Input
    raster_path = arcpy.GetParameterAsText(0)
    #parametr Data Typ: Shapefile, Direction: Input
    kwadraty_shp_path = arcpy.GetParameterAsText(1)
    #parametr Data Typ: Shapefile, Direction: Output
    ZonalStatistics_output = arcpy.GetParameterAsText(2)

    zonal_stats = ZonalStatistics(raster_path, kwadraty_shp_path, ZonalStatistics_output)
    zonal_stats.calculate_zonal_statistics()