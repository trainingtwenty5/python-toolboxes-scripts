import psycopg2

# Dane do połączenia z bazą danych
conn_params = {
    'dbname': 'pgq_sde',
    'user': 'admin',
    'password': 'admin',
    'host': '126.185.136.190',
    'port': '5432'
}

# Definicje zapytań SQL
day_wh_id_query = """
SELECT DISTINCT day_wh_id
FROM smart.hl_lcell_algorithm1_d
LIMIT 10;
"""

previous_month_data_query = """
SELECT COUNT(*)
FROM smart.hl_lcell_algorithm1_d
WHERE "substring"(day_wh_id::text, 5, 2)::integer = 7
  AND "substring"(day_wh_id::text, 1, 4)::integer = 2024;
"""

raw_data_no_group_query = """
SELECT "substring"(day_wh_id::text, 5, 2) AS mm,
       "substring"(day_wh_id::text, 1, 4) AS yyyy,
       lsite_name,
       lcell_name,
       replace(l_ta_ue_index0::text, ','::text, '.'::text)::double precision AS l_ta_ue_index0,
       replace(l_ta_ue_index1::text, ','::text, '.'::text)::double precision AS l_ta_ue_index1,
       replace(l_ta_ue_index2::text, ','::text, '.'::text)::double precision AS l_ta_ue_index2,
       replace(l_ta_ue_index3::text, ','::text, '.'::text)::double precision AS l_ta_ue_index3,
       replace(l_ta_ue_index4::text, ','::text, '.'::text)::double precision AS l_ta_ue_index4,
       replace(l_ta_ue_index5::text, ','::text, '.'::text)::double precision AS l_ta_ue_index5,
       replace(l_ta_ue_index6::text, ','::text, '.'::text)::double precision AS l_ta_ue_index6
FROM smart.hl_lcell_algorithm1_d
WHERE "substring"(day_wh_id::text, 5, 2)::integer = 7
  AND "substring"(day_wh_id::text, 1, 4)::integer = 2024
LIMIT 10;
"""

raw_data_query = """
SELECT "substring"(a_1.day_wh_id::text, 5, 2) AS mm,
       "substring"(a_1.day_wh_id::text, 1, 4) AS yyyy,
       a_1.lsite_name,
       a_1.lcell_name,
       sum(replace(a_1.l_ta_ue_index0::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index0_s,
       sum(replace(a_1.l_ta_ue_index1::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index1_s,
       sum(replace(a_1.l_ta_ue_index2::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index2_s,
       sum(replace(a_1.l_ta_ue_index3::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index3_s,
       sum(replace(a_1.l_ta_ue_index4::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index4_s,
       sum(replace(a_1.l_ta_ue_index5::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index5_s,
       sum(replace(a_1.l_ta_ue_index6::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index6_s,
       sum(replace(a_1.l_ta_ue_index0::text, ','::text, '.'::text)::double precision + 
           replace(a_1.l_ta_ue_index1::text, ','::text, '.'::text)::double precision + 
           replace(a_1.l_ta_ue_index2::text, ','::text, '.'::text)::double precision + 
           replace(a_1.l_ta_ue_index3::text, ','::text, '.'::text)::double precision + 
           replace(a_1.l_ta_ue_index4::text, ','::text, '.'::text)::double precision + 
           replace(a_1.l_ta_ue_index5::text, ','::text, '.'::text)::double precision + 
           replace(a_1.l_ta_ue_index6::text, ','::text, '.'::text)::double precision) AS suma
FROM smart.hl_lcell_algorithm1_d a_1
WHERE "substring"(a_1.day_wh_id::text, 5, 2)::integer = 7
  AND "substring"(a_1.day_wh_id::text, 1, 4)::integer = 2024
GROUP BY a_1.lsite_name, a_1.lcell_name, "substring"(a_1.day_wh_id::text, 5, 2), "substring"(a_1.day_wh_id::text, 1, 4);
"""

test_query_template = """
SELECT a.loc_name,
       a.loc_obj,
       a.lsite_id,
       a.lsite_name,
       a.lcell_id,
       a.lcell_name,
       a.band,
       a.xpos::double precision AS xpos,
       a.ypos::double precision AS ypos,
       a.azimuth,
       bar.yyyy,
       bar.mm,
       bar.rh_0,
       bar.rh_1,
       bar.rh_2,
       bar.rh_3,
       bar.rh_4,
       bar.rh_5,
       bar.rh_6
FROM {azimuth_table} a
LEFT JOIN (
    SELECT raw_data.yyyy,
           raw_data.mm,
           raw_data.lsite_name,
           raw_data.lcell_name,
           round((raw_data.l_ta_ue_index0_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_0,
           round((raw_data.l_ta_ue_index1_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_1,
           round((raw_data.l_ta_ue_index2_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_2,
           round((raw_data.l_ta_ue_index3_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_3,
           round((raw_data.l_ta_ue_index4_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_4,
           round((raw_data.l_ta_ue_index5_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_5,
           round((raw_data.l_ta_ue_index6_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_6
    FROM (
        SELECT "substring"(a_1.day_wh_id::text, 5, 2) AS mm,
               "substring"(a_1.day_wh_id::text, 1, 4) AS yyyy,
               a_1.lsite_name,
               a_1.lcell_name,
               sum(replace(a_1.l_ta_ue_index0::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index0_s,
               sum(replace(a_1.l_ta_ue_index1::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index1_s,
               sum(replace(a_1.l_ta_ue_index2::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index2_s,
               sum(replace(a_1.l_ta_ue_index3::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index3_s,
               sum(replace(a_1.l_ta_ue_index4::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index4_s,
               sum(replace(a_1.l_ta_ue_index5::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index5_s,
               sum(replace(a_1.l_ta_ue_index6::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index6_s,
               sum(replace(a_1.l_ta_ue_index0::text, ','::text, '.'::text)::double precision + replace(a_1.l_ta_ue_index1::text, ','::text, '.'::text)::double precision + replace(a_1.l_ta_ue_index2::text, ','::text, '.'::text)::double precision + replace(a_1.l_ta_ue_index3::text, ','::text, '.'::text)::double precision + replace(a_1.l_ta_ue_index4::text, ','::text, '.'::text)::double precision + replace(a_1.l_ta_ue_index5::text, ','::text, '.'::text)::double precision + replace(a_1.l_ta_ue_index6::text, ','::text, '.'::text)::double precision) AS suma
        FROM smart.hl_lcell_algorithm1_d a_1
        WHERE "substring"(a_1.day_wh_id::text, 5, 2)::integer = 7
          AND "substring"(a_1.day_wh_id::text, 1, 4)::integer = 2024
        GROUP BY a_1.lsite_name, a_1.lcell_name, "substring"(a_1.day_wh_id::text, 5, 2), "substring"(a_1.day_wh_id::text, 1, 4)
    ) raw_data
) bar ON substring(a.lsite_name::text FROM 1 FOR position('_' IN a.lsite_name::text) - 1) = bar.lsite_name::text
    AND a.lcell_name::text = bar.lcell_name::text
WHERE bar.rh_0 IS NOT NULL OR bar.rh_1 IS NOT NULL OR bar.rh_2 IS NOT NULL OR bar.rh_3 IS NOT NULL OR bar.rh_4 IS NOT NULL OR bar.rh_5 IS NOT NULL OR bar.rh_6 IS NOT NULL;
"""

create_mv_query_template = """
DROP MATERIALIZED VIEW IF EXISTS {view_name}_t;

CREATE MATERIALIZED VIEW IF NOT EXISTS {view_name}_t
TABLESPACE tadvance
AS
SELECT test.loc_name,
       test.loc_obj,
       test.lsite_id,
       test.lsite_name,
       test.lcell_id,
       test.lcell_name,
       test.band,
       test.xpos,
       test.ypos,
       test.azimuth,
       test.yyyy,
       test.mm,
       test.rh_0,
       test.rh_1,
       test.rh_2,
       test.rh_3,
       test.rh_4,
       test.rh_5,
       test.rh_6
FROM (
    SELECT a.loc_name,
           a.loc_obj,
           a.lsite_id,
           a.lsite_name,
           a.lcell_id,
           a.lcell_name,
           a.band,
           a.xpos::double precision AS xpos,
           a.ypos::double precision AS ypos,
           a.azimuth,
           bar.yyyy,
           bar.mm,
           bar.rh_0,
           bar.rh_1,
           bar.rh_2,
           bar.rh_3,
           bar.rh_4,
           bar.rh_5,
           bar.rh_6
    FROM {azimuth_table} a
    LEFT JOIN (
        SELECT raw_data.yyyy,
               raw_data.mm,
               raw_data.lsite_name,
               raw_data.lcell_name,
               round((raw_data.l_ta_ue_index0_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_0,
               round((raw_data.l_ta_ue_index1_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_1,
               round((raw_data.l_ta_ue_index2_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_2,
               round((raw_data.l_ta_ue_index3_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_3,
               round((raw_data.l_ta_ue_index4_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_4,
               round((raw_data.l_ta_ue_index5_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_5,
               round((raw_data.l_ta_ue_index6_s / NULLIF(raw_data.suma, 0))::numeric, 2) AS rh_6
        FROM (
            SELECT "substring"(a_1.day_wh_id::text, 5, 2) AS mm,
                   "substring"(a_1.day_wh_id::text, 1, 4) AS yyyy,
                   a_1.lsite_name,
                   a_1.lcell_name,
                   sum(replace(a_1.l_ta_ue_index0::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index0_s,
                   sum(replace(a_1.l_ta_ue_index1::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index1_s,
                   sum(replace(a_1.l_ta_ue_index2::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index2_s,
                   sum(replace(a_1.l_ta_ue_index3::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index3_s,
                   sum(replace(a_1.l_ta_ue_index4::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index4_s,
                   sum(replace(a_1.l_ta_ue_index5::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index5_s,
                   sum(replace(a_1.l_ta_ue_index6::text, ','::text, '.'::text)::double precision) AS l_ta_ue_index6_s,
                   sum(replace(a_1.l_ta_ue_index0::text, ','::text, '.'::text)::double precision + replace(a_1.l_ta_ue_index1::text, ','::text, '.'::text)::double precision + replace(a_1.l_ta_ue_index2::text, ','::text, '.'::text)::double precision + replace(a_1.l_ta_ue_index3::text, ','::text, '.'::text)::double precision + replace(a_1.l_ta_ue_index4::text, ','::text, '.'::text)::double precision + replace(a_1.l_ta_ue_index5::text, ','::text, '.'::text)::double precision + replace(a_1.l_ta_ue_index6::text, ','::text, '.'::text)::double precision) AS suma
            FROM smart.hl_lcell_algorithm1_d a_1
            WHERE "substring"(a_1.day_wh_id::text, 5, 2)::integer = 7
              AND "substring"(a_1.day_wh_id::text, 1, 4)::integer = 2024
            GROUP BY a_1.lsite_name, a_1.lcell_name, "substring"(a_1.day_wh_id::text, 5, 2), "substring"(a_1.day_wh_id::text, 1, 4)
        ) raw_data
    ) bar ON substring(a.lsite_name::text FROM 1 FOR position('_' IN a.lsite_name::text) - 1) = bar.lsite_name::text
        AND a.lcell_name::text = bar.lcell_name::text
) test
WHERE test.rh_0 IS NOT NULL OR test.rh_1 IS NOT NULL OR test.rh_2 IS NOT NULL OR test.rh_3 IS NOT NULL OR test.rh_4 IS NOT NULL OR test.rh_5 IS NOT NULL OR test.rh_6 IS NOT NULL
WITH DATA;

ALTER TABLE IF EXISTS {view_name}_t
    OWNER TO tadvance;
"""

view_names = [
    "tadvance.mv_s_huawei_l800",
    "tadvance.mv_s_huawei_l1800",
    "tadvance.mv_s_huawei_l2100",
    "tadvance.mv_s_huawei_l2600",
    "tadvance.mv_s_nokia_l800",
    "tadvance.mv_s_nokia_l1800",
    "tadvance.mv_s_nokia_l2100",
    "tadvance.mv_s_nokia_l2600"
]

azimuth_tables = [
    "smart.azimuth_lte800",
    "smart.azimuth_lte1800",
    "smart.azimuth_lte2100",
    "smart.azimuth_lte2600",
    "smart.azimuth_lte800",
    "smart.azimuth_lte1800",
    "smart.azimuth_lte2100",
    "smart.azimuth_lte2600"
]

def debug_and_populate_mv(view_name, azimuth_table):
    try:
        # Ustal połączenie z bazą danych
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # Debugowanie: Wyświetl połączenie
        print(f"Połączono z bazą danych dla widoku {view_name}.")

        # Sprawdzenie wartości day_wh_id
        cursor.execute(day_wh_id_query)
        day_wh_id_results = cursor.fetchall()
        print("Przykładowe wartości day_wh_id:")
        for row in day_wh_id_results:
            print(row)

        # Sprawdzenie danych z lipca 2024
        cursor.execute(previous_month_data_query)
        previous_month_data_count = cursor.fetchone()[0]
        print(f"Liczba rekordów z lipca 2024: {previous_month_data_count}")

        # Uruchomienie podzapytania raw_data bez grupowania
        cursor.execute(raw_data_no_group_query)
        raw_data_no_group_results = cursor.fetchall()
        print(f"Liczba rekordów w podzapytaniu raw_data bez grupowania: {len(raw_data_no_group_results)}")

        # Uruchomienie podzapytania raw_data
        cursor.execute(raw_data_query)
        raw_data_results = cursor.fetchall()
        print(f"Liczba rekordów w podzapytaniu raw_data: {len(raw_data_results)}")

        # Uruchomienie pełnego zapytania test
        test_query = test_query_template.format(azimuth_table=azimuth_table)
        cursor.execute(test_query)
        test_results = cursor.fetchall()
        print(f"Liczba rekordów w pełnym zapytaniu test: {len(test_results)}")

        # Tworzenie widoku zmaterializowanego
        create_mv_query = create_mv_query_template.format(view_name=view_name, azimuth_table=azimuth_table)
        cursor.execute(create_mv_query)
        conn.commit()
        print(f"Widok zmaterializowany {view_name}_t został utworzony i uzupełniony pomyślnie.")

    except Exception as e:
        print(f"Wystąpił błąd dla widoku {view_name}: {e}")

    finally:
        # Zamknięcie połączenia
        cursor.close()
        conn.close()
        print("Połączenie z bazą danych zostało zamknięte.")


# Lista widoków i odpowiadających im tabel azimuth
view_names = [
    "tadvance.mv_s_huawei_l800",
    "tadvance.mv_s_huawei_l1800",
    "tadvance.mv_s_huawei_l2100",
    "tadvance.mv_s_huawei_l2600",
    "tadvance.mv_s_nokia_l800",
    "tadvance.mv_s_nokia_l1800",
    "tadvance.mv_s_nokia_l2100",
    "tadvance.mv_s_nokia_l2600"
]

azimuth_tables = [
    "smart.azimuth_lte800",
    "smart.azimuth_lte1800",
    "smart.azimuth_lte2100",
    "smart.azimuth_lte2600",
    "smart.azimuth_lte800",
    "smart.azimuth_lte1800",
    "smart.azimuth_lte2100",
    "smart.azimuth_lte2600"
]

# Iteracja przez widoki i tabele azimuth
for view_name, azimuth_table in zip(view_names, azimuth_tables):
    debug_and_populate_mv(view_name, azimuth_table)
