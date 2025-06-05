import arcpy
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import psutil
import time



# Funkcja do wysyłania e-maila
def send_email(subject, body, recipient_emails):
    sender_email = "buchar123@gmail.com"
    email_password = "xxx"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)  # Łączy adresy e-mail przecinkami

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.sendmail(sender_email, recipient_emails, msg.as_string())
    except Exception as e:
        print(f"Błąd podczas wysyłania e-maila: {e}")


arcpy.env.workspace = r"D:\\ArcGIS\\ArcGIS_baza_SDE\\Admin.sde"

email_body_lista = []
total_tables = 0
okej = 0
stacje_reported = False  # Flag to check if stacje_act_geom_3857_t has been reported
processed_once = False  # Flag to ensure the loop runs only once
while True:
    vpn_connected = any('vpnui.exe' in process.info['name'] for process in psutil.process_iter(['pid', 'name']))
    if vpn_connected and not processed_once:
        print('---------Jesteś podłączony do VPN (Cisco AnyConnect)---------\n---------vpn open---------')

        today = datetime.now().date()
        lsita_1 = arcpy.ListTables("pgq_sde.smart.etl_smart", "ALL")
        lsita_2 = arcpy.ListTables("pgq_sde.stacje.stacje_act_geom_3857_table", "ALL")

        for table in lsita_1 + lsita_2:

            print(f"---------Tabela: {table} ---------")
            with arcpy.da.SearchCursor(table, ['tab', 'status', 'date'] if table in lsita_1 else ['data_aktualizacji']) as cursor:
                for row in cursor:

                    if table in lsita_1:
                        total_tables += 1
                        value_field0, value_field1, value_field2 = row
                        if value_field1 == 'OK' and value_field2 and value_field2.date() == today:
                            okej += 1
                        else:
                            email_body_lista.append(f'Status jest --{value_field1} -- dla tabeli  -- {value_field0} -- ale data nie jest aktualna w bazie -- {value_field2.date() if value_field2 else "brak daty"} --\n')
                    else:
                        value_field0 = row[0]
                        if value_field0 and value_field0.date() == today and not stacje_reported:
                            email_body_lista.append(f'NOWA INFORMACJA: tabela stacje_act_geom_3857_table jest zaktualizowana na dzień: -- {value_field0} -- \n')
                            stacje_reported = True


        processed_once = True  # Set the flag after processing


        if email_body_lista:
            recipient_emails = ["buchar123@gmail.com", "daniel.buchar@orange.com", "inez.beszterda@orange.com", "lukasz.brylak@orange.com"]
            subject = f"Raport zgodności tabel w pgq_sde.smart.etl_smart na dzień --{today}-- oraz tabeli stacje_act_geom_3857_table"
            body = f"Skrypt sprawdził zgodność wszystkich: --{total_tables}-- tabel, z czego tabel ze statusem 'OK' i aktualną datą jest: --{okej}--\n\n Tabele błędne to:\n{''.join(email_body_lista)}"
            print(body)

    time.sleep(5)  # 3600 sekund to 1 godzina

    if not vpn_connected:
        send_email(subject, body, recipient_emails)
        print("E-mail został wysłany.\nNie jesteś podłączony do VPN. Kończę działanie skryptu.")
        break
#recipient_emails = ["buchar123@gmail.com", "daniel.buchar@orange.com", "inez.beszterda@orange.com", "lukasz.brylak@orange.com"]


