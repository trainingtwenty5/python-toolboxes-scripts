import psycopg2
import arcpy
from math import radians, cos, sin
import os

# Dane do połączenia z bazą danych
conn_params = {
    'dbname': 'pgq_sde',
    'user': 'admin',
    'password': 'admin',
    'host': '126.185.136.190',
    'port': '5432'
}

# Lista warstw do przetworzenia
layers = [
    "huawei_l800",
    "huawei_l1800",
    "huawei_l2100",
    "huawei_l2600",
    "nokia_l800",
    "nokia_l1800",
    "nokia_l2100",
    "nokia_l2600"
]

# Definicje przedziałów promieni dla Nokii i Huaweia
nokia_radius_dict = {
    0: (0, 468),
    1: (468, 1248),
    2: (1248, 2028),
    3: (3432, 4524),
    4: (3432, 4524),
    5: (4524, 5070),
    6: (5070, 18000)
}

huawei_radius_dict = {
    0: (0, 312),
    1: (312, 624),
    2: (624, 1092),
    3: (1092, 2028),
    4: (2028, 3588),
    5: (3588, 6708),
    6: (6708, 15000)
}

# Funkcja do przypisywania przedziałów promieni na podstawie warstwy
def get_radius_dict(layer_name):
    if "nokia" in layer_name:
        return nokia_radius_dict
    elif "huawei" in layer_name:
        return huawei_radius_dict
    else:
        raise ValueError(f"Nieznana warstwa: {layer_name}")

# Funkcja do tworzenia punktów na podstawie azymutu i odległości
def create_point(x_center, y_center, azimuth, distance):
    angle = radians(azimuth)
    x = x_center + (distance * sin(angle))
    y = y_center + (distance * cos(angle))
    return arcpy.Point(x, y)

# Funkcja do generowania łuku z punktów
def generate_arc_points(x_center, y_center, start_angle, end_angle, radius, num_points=20):
    """Generuje punkty na łuku pomiędzy dwoma kątami dla danego promienia."""
    angle_step = (end_angle - start_angle) / num_points
    points = [
        create_point(x_center, y_center, start_angle + i * angle_step, radius)
        for i in range(num_points + 1)
    ]
    return points

# Funkcja do tworzenia pierścienia między dwoma promieniami
def create_ring(x_center, y_center, azimuth, inner_radius, outer_radius):
    start_angle = azimuth - 5  # Zakres azymutu, np. -5 stopni
    end_angle = azimuth + 5    # Zakres azymutu, np. +5 stopni

    # Punkty na łuku zewnętrznym
    outer_points = generate_arc_points(x_center, y_center, start_angle, end_angle, outer_radius)

    # Punkty na łuku wewnętrznym (odwrócony kierunek, aby zamknąć poligon)
    inner_points = generate_arc_points(x_center, y_center, end_angle, start_angle, inner_radius)

    # Łączymy punkty łuku zewnętrznego i wewnętrznego w odwróconej kolejności
    points = outer_points + inner_points
    return arcpy.Polygon(arcpy.Array(points))

# Ścieżka do pliku shapefile lub geobazy
output_gdb = r'D:\projekty_aprx\orange_projekty_aprx\time_advance\TEST_2.gdb'

# Definicja układu współrzędnych EPSG:3857 (Web Mercator)
spatial_ref = arcpy.SpatialReference(3857)

# Połącz się z bazą danych i pobierz dane z utworzonych widoków
for layer in layers:
    fetch_data_query = f"""
    SELECT 
        id, loc_obj, lsite_id, lcell_id, lcell_name, band, azimuth, ST_AsText(shape) as shape_wkt
    FROM tadvance.mv_t_{layer}_3857_s
    """
    data = []
    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(fetch_data_query)
                data = cur.fetchall()
    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania danych dla warstwy {layer}: {e}")
        continue

    # Pobranie odpowiedniego słownika promieni dla danej warstwy
    radius_dict = get_radius_dict(layer)

    for radius_index, (inner_radius, outer_radius) in radius_dict.items():
        # Sprawdź, czy klasa obiektów już istnieje, i usuń ją, jeśli tak
        output_fc = f"{layer}_ring_{inner_radius}_{outer_radius}"  # Nazwa klasy obiektów na podstawie warstwy i promieni
        fc_path = os.path.join(output_gdb, output_fc)
        if arcpy.Exists(fc_path):
            arcpy.Delete_management(fc_path)

        # Utworzenie nowej klasy obiektów z odpowiednim układem współrzędnych (EPSG:3857)
        arcpy.CreateFeatureclass_management(
            out_path=output_gdb,
            out_name=output_fc,
            geometry_type="POLYGON",
            spatial_reference=spatial_ref  # Tutaj dodajemy układ współrzędnych EPSG:3857
        )

        # Dodanie pól do klasy obiektów
        fields = [
            ('id', 'LONG'),
            ('loc_obj', 'LONG'),
            ('lsite_id', 'LONG'),
            ('lcell_id', 'LONG'),
            ('lcell_name', 'TEXT'),
            ('band', 'TEXT'),
            ('azimuth', 'DOUBLE')
        ]

        for field_name, field_type in fields:
            arcpy.AddField_management(fc_path, field_name, field_type)

        # Dodanie pierścieni do klasy obiektów na podstawie pobranych danych
        with arcpy.da.InsertCursor(fc_path, ["SHAPE@"] + [f[0] for f in fields]) as cursor:
            for row in data:
                id, loc_obj, lsite_id, lcell_id, lcell_name, band, azimuth, shape_wkt = row
                x_center, y_center = arcpy.FromWKT(shape_wkt).firstPoint.X, arcpy.FromWKT(shape_wkt).firstPoint.Y

                if azimuth is None:
                    print(f"Wiersz z id {id} ma brakującą wartość azimuth, pomijanie tego wiersza.")
                    continue

                # Tworzymy pierścień między wewnętrznym a zewnętrznym promieniem
                ring_polygon = create_ring(x_center, y_center, azimuth, inner_radius, outer_radius)
                cursor.insertRow([ring_polygon, id, loc_obj, lsite_id, lcell_id, lcell_name, band, azimuth])

print("Pierścienie zostały pomyślnie utworzone w układzie współrzędnych EPSG:3857.")
