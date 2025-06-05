#MUSI BYĆ TYLKO 1 MAPA

import arcpy

# Ustawia środowisko robocze
arcpy.env.workspace = r'D:\ArcGIS\3_Dane_Zasiegowe_LTE_4G_UMTS_3G_GSM_2G\Dane_zasiegowe_nr_1_grudzien_2023\2024_01_16_MV_Dane_zasiegowe_3857_copy.gdb'

# Otwiera projekt ArcGIS Pro
projekt_aprx = arcpy.mp.ArcGISProject('CURRENT')

# Pobiera listę warstw danych w projekcie
lista_warstw = projekt_aprx.listMaps()[0].listLayers()
print(lista_warstw)
# Przechodzi przez każdą warstwę
for warstwa in lista_warstw:
    # Pobiera listę pól i ich aliasów
    pola = [pole.name for pole in arcpy.ListFields(warstwa)]
    aliasy = {pole.name: pole.aliasName for pole in arcpy.ListFields(warstwa)}

    # Zmienia nazwy pól na takie same jak aliasy
    for pole in pola:
        nazwa_aliasu = aliasy.get(pole)
        if nazwa_aliasu:
            arcpy.management.AlterField(warstwa, pole, new_field_name=nazwa_aliasu)

print("Zmieniono nazwy pól na takie same jak aliasy.")
