import arcpy
import os

# Ścieżki do warstw
POP = "XYexp_locit_20231129_dane_2180"
dss_layer = "DOM_DSS_OPL_20240901_50m_MV"
cband_layer = "DOM_CBAND3600_OPL_107dBm_20240901_MV"
test4_layer = "Klastry_s"
test5_layer = "Projekty_radio_s"

# Funkcja do docięcia warstwy i obliczenia powierzchni
def intersect_and_calculate_area(layer_to_intersect, intersecting_layer):
    intersect_output = os.path.join(arcpy.env.scratchGDB, "intersect_result")

    # Intersect warstwy
    arcpy.analysis.Intersect([layer_to_intersect, intersecting_layer], intersect_output)

    # Obliczenie powierzchni dociętej warstwy
    total_area = 0
    with arcpy.da.SearchCursor(intersect_output, ["SHAPE@"]) as cursor:
        for row in cursor:
            total_area += row[0].getArea("PLANAR", "SQUAREMETERS")

    # Usunięcie wyników tymczasowych
    arcpy.management.Delete(intersect_output)

    return total_area

# Funkcja do walidacji, czy warstwa jest poligonowa
def validate_polygon_layer(layer):
    desc = arcpy.Describe(layer)
    return desc.shapeType == 'Polygon'

# Sprawdzenie, czy warstwy są poligonowe
if validate_polygon_layer(dss_layer) and validate_polygon_layer(cband_layer) and \
   validate_polygon_layer(test4_layer) and validate_polygon_layer(test5_layer):

    # Dodanie kolumn do powierzchni i procentów w TEST4 i TEST5
    for layer in [test4_layer, test5_layer]:
        if "area_DSS" not in [field.name for field in arcpy.ListFields(layer)]:
            arcpy.management.AddField(layer, "area_DSS", "DOUBLE")
        if "area_CBand" not in [field.name for field in arcpy.ListFields(layer)]:
            arcpy.management.AddField(layer, "area_CBand", "DOUBLE")
        if "percent_DSS" not in [field.name for field in arcpy.ListFields(layer)]:
            arcpy.management.AddField(layer, "percent_DSS", "DOUBLE")
        if "percent_CBand" not in [field.name for field in arcpy.ListFields(layer)]:
            arcpy.management.AddField(layer, "percent_CBand", "DOUBLE")
        if "area_ha" not in [field.name for field in arcpy.ListFields(layer)]:  # Dodanie kolumny na powierzchnię w ha
            arcpy.management.AddField(layer, "area_ha", "DOUBLE")

    # Iteracja przez każdy poligon w TEST4 i TEST5
    for layer in [test4_layer, test5_layer]:
        with arcpy.da.UpdateCursor(layer, ["SHAPE@", "area_DSS", "area_CBand", "percent_DSS", "percent_CBand", "area_ha"]) as cursor:
            for row in cursor:
                # Docięcie warstw i obliczenie powierzchni
                dss_area = intersect_and_calculate_area(dss_layer, row[0])
                cband_area = intersect_and_calculate_area(cband_layer, row[0])

                # Uaktualnienie wartości powierzchni
                row[1] = dss_area
                row[2] = cband_area

                # Obliczanie procentów
                total_area = row[0].getArea("PLANAR", "SQUAREMETERS")  # Całkowita powierzchnia poligonu
                row[3] = (dss_area / total_area * 100) if total_area > 0 else 0
                row[4] = (cband_area / total_area * 100) if total_area > 0 else 0

                # Obliczanie powierzchni w hektarach (dzielenie przez 10 000)
                row[5] = total_area / 10000  # Powierzchnia w ha

                cursor.updateRow(row)

    # Wyświetlenie wyników
    for layer in [test4_layer, test5_layer]:
        with arcpy.da.SearchCursor(layer, ["area_DSS", "area_CBand", "area_ha"]) as cursor:
            total_dss_area = 0
            total_cband_area = 0
            total_ha_area = 0
            for row in cursor:
                total_dss_area += row[0]
                total_cband_area += row[1]
                total_ha_area += row[2]
            print(f"{layer} - Łączna powierzchnia DSS: {total_dss_area} m², Łączna powierzchnia C-Band: {total_cband_area} m², Łączna powierzchnia: {total_ha_area} ha")
else:
    print("Jedna lub więcej warstw nie jest poligonowa. Sprawdź dane wejściowe.")
