import csv
import re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def dms_to_decimal(dms_str):
    """Konwertuje współrzędne w formacie DMS (stopnie, minuty, sekundy) na format dziesiętny."""
    parts = re.split('[°\'"]+', dms_str)
    degrees = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    return degrees + (minutes / 60) + (seconds / 3600)

def przelicz_wspolrzedne_csv(input_file, output_file):
    # Wczytaj dane z pliku CSV
    with open(input_file, mode='r', newline='', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile, delimiter=';')  # Użyj średnika jako separatora
        data = list(reader)

    # Zidentyfikuj indeksy kolumn
    header = data[0]
    print("Nagłówki pliku CSV:", header)  # Dodano do debugowania
    try:
        latitude_index = header.index('Latitude')
        longitude_index = header.index('Longitude')
    except ValueError as e:
        messagebox.showerror("Błąd", f"Nie znaleziono kolumny: {e}")
        return

    # Przelicz wartości w kolumnach Latitude i Longitude
    for row in data[1:]:
        row[latitude_index] = dms_to_decimal(row[latitude_index])
        row[longitude_index] = dms_to_decimal(row[longitude_index])

    # Zapisz zmienione dane do nowego pliku CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=';')  # Użyj średnika jako separatora
        writer.writerows(data)

    messagebox.showinfo("Sukces", f"Dane zostały zapisane do {output_file}")

def wybierz_plik():
    input_file = filedialog.askopenfilename(title="Wybierz plik CSV", filetypes=[("CSV files", "*.csv")])
    if input_file:
        output_file = filedialog.asksaveasfilename(title="Zapisz plik jako", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if output_file:
            przelicz_wspolrzedne_csv(input_file, output_file)

# Tworzenie okna głównego
root = tk.Tk()
root.title("Przeliczanie współrzędnych")

# Tworzenie przycisku do wyboru pliku
button = tk.Button(root, text="Wybierz plik CSV", command=wybierz_plik)
button.pack(pady=20)

# Uruchomienie pętli głównej
root.mainloop()
