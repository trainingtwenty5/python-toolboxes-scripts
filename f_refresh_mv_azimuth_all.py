import psycopg2
from datetime import datetime
import logging

# Ustawienie konfiguracji logowania
logging.basicConfig(filename='D:\\replikacja\\model_builder\\Python_3\\log_f_refresh_mv_azimuth_all.txt', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Przykładowe logowanie
logging.debug('Rozpoczęcie skryptu.')

def f_refresh_mv_azimuth():
    tables_functions = {
        'azimuth_fdd2100': 'fc_mv_azimuth_fdd2100',
        'azimuth_fdd3600': 'fc_mv_azimuth_fdd3600',
        'azimuth_gsm': 'fc_mv_azimuth_gsm',
        'azimuth_lte700': 'fc_mv_azimuth_lte700',
        'azimuth_lte800': 'fc_mv_azimuth_lte800',
        'azimuth_lte900': 'fc_mv_azimuth_lte900',
        'azimuth_lte1800': 'fc_mv_azimuth_lte1800',
        'azimuth_lte2100': 'fc_mv_azimuth_lte2100',
        'azimuth_lte2600': 'fc_mv_azimuth_lte2600',
        'azimuth_umts900': 'fc_mv_azimuth_umts900',
        'azimuth_umts2100': 'fc_mv_azimuth_umts2100'
    }

    try:
        # Ustal połączenie z bazą danych
        conn = psycopg2.connect(
            dbname="pgq_sde",
            user="admin",
            password="admin",
            host="126.185.136.190",
            port="5432"
        )
        cursor = conn.cursor()

        current_date = datetime.now().date()

        for tab, function in tables_functions.items():
            # Pobierz status i datę z tabeli etl_smart w schemacie smart
            cursor.execute(f"""
                SELECT status, date_trunc('day', date)::date 
                FROM smart.etl_smart 
                WHERE tab = '{tab}'
            """)
            result = cursor.fetchone()

            if result is None:
                print(f"No data found for tab '{tab}' in smart.etl_smart")
                logging.debug(f"No data found for tab '{tab}' in smart.etl_smart")
                continue

            status, date = result

            # Debugowanie - wypisz wartości status i date oraz aktualną datę
            print(f"Fetched status: {status}, date: {date} for tab '{tab}'")
            logging.debug(f"Fetched status: {status}, date: {date} for tab '{tab}'")
            print(f"Current date: {current_date}")
            logging.debug(f"Current date: {current_date}")

            # Porównaj status i datę
            if status == 'OK' and date == current_date:
                # Wykonaj odpowiednią funkcję
                cursor.execute(f"SELECT azymuty.{function}()")
                conn.commit()
                print(f"Function azymuty.{function}() executed successfully for tab '{tab}'")
                logging.debug(f"Function azymuty.{function}() executed successfully for tab '{tab}'")
            else:
                print(f"Conditions not met for executing azymuty.{function}() for tab '{tab}'")
                logging.debug(f"Conditions not met for executing azymuty.{function}() for tab '{tab}'")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        logging.error(f"Database error: {e}")
        conn.rollback()

    except Exception as e:
        print(f"Error: {e}")
        logging.error(f'Błąd {str(e)}')

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Wywołanie funkcji
f_refresh_mv_azimuth()
logging.debug('Zakończenie skryptu.')
