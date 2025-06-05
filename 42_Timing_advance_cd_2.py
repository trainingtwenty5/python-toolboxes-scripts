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

# Promienie do przetworzenia
radii = [0, 1, 2, 3, 4, 5, 6]

# Szablon skryptu SQL do sprawdzenia danych w tabeli źródłowej
check_data_script_template = """
SELECT * FROM tadvance.mv_s_{layer}_t LIMIT 10;
"""

# Szablon skryptu SQL do tworzenia widoku materializowanego
create_view_script_template = """
CREATE MATERIALIZED VIEW IF NOT EXISTS tadvance.mv_t_{layer}_3857_s
TABLESPACE tadvance
AS
SELECT 
    row_number() OVER (ORDER BY a.lcell_id)::integer AS id,
    a.loc_obj,
    a.lsite_id,
    a.lcell_id,
    a.lcell_name,
    a.band,
    a.azimuth,
    a.yyyy,
    a.mm,
    st_transform(
        st_setsrid(st_point(a.xpos, a.ypos), 2180),
        3857
    ) AS shape,
    a.rh_0::double precision AS rh_0,
    a.rh_1::double precision AS rh_1,
    a.rh_2::double precision AS rh_2,
    a.rh_3::double precision AS rh_3,
    a.rh_4::double precision AS rh_4,
    a.rh_5::double precision AS rh_5,
    a.rh_6::double precision AS rh_6,
    'time advance lte 800 hua'::text AS nazwa_warstwy,
    'now'::text::timestamp without time zone AS data_aktualizacji
FROM tadvance.mv_s_{layer}_t a;
"""

# Szablon skryptu do zmiany właściciela widoku materializowanego
alter_owner_script_template = """
ALTER TABLE IF EXISTS tadvance.mv_t_{layer}_3857_s
OWNER TO tadvance;
"""

# Połączenie się z bazą danych i wykonanie skryptów dla każdej warstwy
for layer in layers:
    check_data_script = check_data_script_template.format(layer=layer)
    create_view_script = create_view_script_template.format(layer=layer)
    alter_owner_script = alter_owner_script_template.format(layer=layer)

    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                # Sprawdzenie danych w tabeli źródłowej
                cur.execute(check_data_script)
                rows = cur.fetchall()

                if rows:
                    print(f"Przykładowe wiersze z tabeli źródłowej {layer}:")
                    for row in rows:
                        print(row)

                    # Utworzenie widoku materializowanego tylko wtedy, gdy tabela źródłowa zawiera dane
                    cur.execute(create_view_script)
                    cur.execute(alter_owner_script)
                    conn.commit()
                    print(f"Widok materializowany dla {layer} został utworzony i przypisano właściciela.")
                else:
                    print(f"Tabela źródłowa {layer} jest pusta.")
    except Exception as e:
        print(f"Wystąpił błąd dla warstwy {layer}: {e}")

# Ścieżka do pliku shapefile lub geobazy
output_gdb = r'D:\projekty_aprx\orange_projekty_aprx\time_advance\TEST5.gdb'

# Funkcja do tworzenia punktów na podstawie azymutu i odległości
def create_point(x_center, y_center, azimuth, distance):
    angle = radians(azimuth)
    x = x_center + (distance * sin(angle))  # Zmienione z cos na sin
    y = y_center + (distance * cos(angle))  # Zmienione z sin na cos
    return arcpy.Point(x, y)

# Połącz się z bazą danych i pobierz dane z utworzonych widoków
for layer in layers:
    fetch_data_query = f"""
    SELECT 
        id, loc_obj, lsite_id, lcell_id, lcell_name, band, azimuth, rh_0, rh_1, rh_2, rh_3, rh_4, rh_5, rh_6, ST_AsText(shape) as shape_wkt
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

    for radius in radii:
        # Sprawdź, czy klasa obiektów już istnieje, i usuń ją, jeśli tak
        output_fc = f"{layer}_rh_{radius}"  # Nazwa klasy obiektów na podstawie warstwy i promienia
        fc_path = os.path.join(output_gdb, output_fc)
        if arcpy.Exists(fc_path):
            arcpy.Delete_management(fc_path)

        # Utworzenie nowej klasy obiektów
        arcpy.CreateFeatureclass_management(out_path=output_gdb, out_name=output_fc, geometry_type="POLYGON")

        # Dodanie pól do klasy obiektów
        fields = [
            ('id', 'LONG'),
            ('loc_obj', 'LONG'),
            ('lsite_id', 'LONG'),
            ('lcell_id', 'LONG'),
            ('lcell_name', 'TEXT'),
            ('band', 'TEXT'),
            ('azimuth', 'DOUBLE'),
            (f'rh_{radius}', 'DOUBLE')
        ]

        for field_name, field_type in fields:
            arcpy.AddField_management(fc_path, field_name, field_type)

        # Dodanie poligonów do klasy obiektów na podstawie pobranych danych
        with arcpy.da.InsertCursor(fc_path, ["SHAPE@"] + [f[0] for f in fields]) as cursor:
            for row in data:
                id, loc_obj, lsite_id, lcell_id, lcell_name, band, azimuth, rh_0, rh_1, rh_2, rh_3, rh_4, rh_5, rh_6, shape_wkt = row
                x_center, y_center = arcpy.FromWKT(shape_wkt).firstPoint.X, arcpy.FromWKT(shape_wkt).firstPoint.Y

                if azimuth is None:
                    print(f"Wiersz z id {id} ma brakującą wartość azimuth, pomijanie tego wiersza.")
                    continue

                rh_value = [rh_0, rh_1, rh_2, rh_3, rh_4, rh_5, rh_6][radius]
                if rh_value is not None and rh_value > 0:
                    scaled_rh_value = rh_value * 500  # Współczynnik skalowania
                    start_angle = azimuth + radius * 10
                    end_angle = start_angle + 10

                    points = [
                        arcpy.Point(x_center, y_center),
                        create_point(x_center, y_center, start_angle, scaled_rh_value),
                        create_point(x_center, y_center, end_angle, scaled_rh_value),
                        arcpy.Point(x_center, y_center)
                    ]

                    polygon = arcpy.Polygon(arcpy.Array(points))
                    cursor.insertRow([polygon, id, loc_obj, lsite_id, lcell_id, lcell_name, band, azimuth, rh_value])

print("Poligony zostały pomyślnie utworzone.")
