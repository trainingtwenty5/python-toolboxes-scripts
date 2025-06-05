import arcpy
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import psutil
import time
from dateutil import parser


# Funkcja do wysyłania e-maila
def send_email(subject, body, recipient_emails):
    sender_email = "buchar123@gmail.com"
    email_password = "XX"
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


# Lokalizacja plików
# arcpy.env.workspace = r"D:\ArcGIS\12_01_2024_Piotr_trocyk_True_5G\admin.sde"
arcpy.env.workspace = r"D:\\ArcGIS\\ArcGIS_baza_SDE\\Admin.sde"

email_body_lista = []
email_body_lista1 = []
a = True
# Pętla nieskończona do monitorowania stanu VPN
n = 0
okej = 0
while True:

    # Sprawdź, czy jesteś podłączony do VPN
    vpn_connected = False  # Przyjmujemy, że nie jesteś podłączony do VPN
    # Sprawdź dostępność procesu związanego z Cisco AnyConnect (vpnui.exe)
    for process in psutil.process_iter(['pid', 'name']):
        if 'vpnui.exe' in process.info['name']:
            vpn_connected = True
            print('---------Jesteś podłączony do VPN (Cisco AnyConnect)---------')

    # do query na tabeli - tu nic
    q = ''

    # Jeśli jesteś podłączony do VPN, pobierz tabelę z bazy danych i zapamiętaj dane

    if vpn_connected:
        print('\n')
        print('---------vpn open---------')

        today = datetime.now().date()
        table_data = []

        lsita_1 = arcpy.ListTables("pgq_sde.smart.etl_smart", "ALL")
        email_body = ""  # Zmienna do przechowywania treści wiadomości e-mail

        if n == 0:
            for table in lsita_1:
                print("---------Tabela: ", table, " ---------")

                with arcpy.da.SearchCursor(table, ['tab', 'status', 'date'], q) as cursor:
                    for row in cursor:
                        value_field0 = row[0]
                        n += 1
                        value_field1 = row[1]
                        value_field2 = row[2]

                        if value_field1 == 'OK':
                            if value_field2 is not None and value_field2.date() == today:
                                # email_body += f'ok  -- {value_field0}-- na dzien z widnowska --{today}-- ostatnia aktualizacja informacja z bazy to --{value_field2.date()}---------------ok\n'
                                # print(email_body)
                                okej += 1

                            # if value_field2.date() != today:
                            else:
                                email_body_lista.append(
                                    f'Status jest --{value_field1} -- dla tabeli  -- {value_field0} -- ale data nie jest aktualna w bazie -- {value_field2.date()} --\n')
                                # print(email_body)
                        else:
                            if value_field2 is not None:
                                email_body_lista.append(
                                    f'Błąd w tabeli : -- {value_field0} --  ostatnia aktualizacja to -- {value_field2.date()} -- jednak status jest zly -- {value_field1} --\n')
                                # print(email_body)
                            else:
                                email_body_lista.append(
                                    f'Błąd w tabeli : -- {value_field0} --  brakuje ostatnij aktualizacji\n')
                                # print(email_body)

            print('\n')
            print('---------Tylko raz---------')
            print(n)
            print('\n')

        # Wysyłanie e-maila tylko raz dziennie
        if len(email_body_lista) >= 1:
            recipient_emails = ["buchar123@gmail.com", "daniel.buchar@orange.com", "inez.beszterda@orange.com",
                                "lukasz.brylak@orange.com"]
            subject = f"Raport zgodności tabel w pgq_sde.smart.etl_smart na dzień --{today}--"
            body = f"Skrypt sprawdził zgodność wszystkich: --{n}-- tabel, z czego tabel ze statusem 'OK' i aktualną datą jest: --{okej}--\n\n Tabele błędne to:\n{''.join(email_body_lista)}"
            print(body)

    # Poczekaj 1 godzinę przed ponownym sprawdzeniem
    time.sleep(5)  # 3600 sekund to 1 godzina

    # Przerwij pętlę nieskończoną, jeśli nie jesteś podłączony do VPN
    if not vpn_connected:
        # Wywołaj funkcję send_email
        send_email(subject, body, recipient_emails)
        print("E-mail został wysłany.")
        print("Nie jesteś podłączony do VPN. Kończę działanie skryptu.")

        break


