import psycopg2

# Ustawienia połączenia z bazą danych
DB_NAME = "pgq_sde"
USER = "admin"
PASSWORD = "admin"
HOST = "126.185.136.190"
PORT = "5432"

try:
    # Nawiązywanie połączenia z bazą danych
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

    cursor = connection.cursor()

    # SQL do utworzenia materializowanego widoku z dopiskiem '_t'
    create_mv_query = """
    CREATE MATERIALIZED VIEW IF NOT EXISTS ogolne.mv_dim_lsite_vendor_t
    TABLESPACE ogolne
    AS
    SELECT row_number() OVER (ORDER BY dim_lsite.netis_loc_obj)::integer AS id,
        dim_lsite.lsite_wh_id,
        dim_lsite.loc_wh_id,
        dim_lsite.lsite_id,
        dim_lsite.lsite_name,
        dim_lsite.lsite_vendor,
        dim_lsite.lsite_version,
        dim_lsite.lsite_owner,
        dim_lsite.reg_code,
        dim_lsite.proj_code,
        dim_lsite.proj_name,
        dim_lsite.netis_obj,
        dim_lsite.netis_loc_obj,
        dim_lsite.netis_ver,
        dim_lsite.status,
        dim_lsite.status_opr,
        dim_lsite.consolidation,
        dim_lsite.eff_date,
        dim_lsite.upd_date,
        dim_lsite.exp_date,
        dim_lsite.mri,
        dim_lsite.lsite_nems_name,
        dim_lsite.scg_nems_name,
        dim_lsite.msite_wh_id,
        dim_lsite.msite_nems_name,
        dim_lsite.msite_name,
        loc.xpos,
        loc.ypos,
        'Dim lsite vendor'::character varying(25) AS nazwa_warstwy,
        CURRENT_TIMESTAMP AS data_aktualizacji
    FROM smart.dim_lsite
    LEFT JOIN smart.loc ON dim_lsite.netis_loc_obj = loc.obj
    WHERE dim_lsite.mri::text = 'Y' AND dim_lsite.exp_date >= CURRENT_DATE AND dim_lsite.status::text = 'ACTIVE'
    WITH DATA;
    """

    # Wykonanie zapytania
    cursor.execute(create_mv_query)

    # Zmiana właściciela i nadanie uprawnień
    alter_owner_query = """
    ALTER TABLE IF EXISTS ogolne.mv_dim_lsite_vendor_t
        OWNER TO ogolne;
    """
    cursor.execute(alter_owner_query)

    grant_select_query = """
    GRANT SELECT ON TABLE ogolne.mv_dim_lsite_vendor_t TO admin;
    GRANT ALL ON TABLE ogolne.mv_dim_lsite_vendor_t TO ogolne;
    """
    cursor.execute(grant_select_query)

    # Zatwierdzenie transakcji
    connection.commit()
    print("Materializowany widok 'mv_dim_lsite_vendor_t' został utworzony i uprawnienia nadane.")

except Exception as e:
    print(f"Wystąpił błąd: {e}")

finally:
    # Zamknięcie połączenia
    if cursor:
        cursor.close()
    if connection:
        connection.close()
