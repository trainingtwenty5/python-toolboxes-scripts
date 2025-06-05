print('---------------------- START CZESCI IV - Przeciązenia dla LTE ----------------------')
print('\n')

# TYLKO LTE2600
# TYLKO LTE1800
# TYLKO LTE900
# TYLKO LTE2100


arcpy.env.overwriteOutput = True
# Ustawienie środowiska pracy geobaze SDE
arcpy.env.workspace = r"C:\Users\buchadan\AppData\Roaming\Esri\ArcGISPro\Favorites\Admin_SDE.sde"

# Lista tabel do przefiltrowania z bazdy danych do tabel, od przeciazenia lte
lista_3 = arcpy.ListTables('*_przeciazone_lte*')

# Filtrowanie tabel, które nie kończą się na "_a" ani "_lte700"
przeciazenia = [table for table in lista_3 if not (table.endswith("_a") or table.endswith("_lte700"))]
print('\n')
print('Lista przeciazenia')
print(przeciazenia)

# Ustawienie środowiska pracy na drugą geobazę
# arcpy.env.workspace = r"D:\\Daniel\\ArcGIS\\Projects\\Dane_zasiegowe\\Wynik_test_12_12_2023_MV.gdb"

# output_MV = r'D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\Wynik_test_12_12_2023_MV.gdb'
# przypisanie srodowiska do podanej sciezki output_MV zeby wybrac juz zrobione warstwy MV
output_MV = r'D:\ArcGIS\______________________________Dane_zasiegowe______________________________\Dane_zasiegowe_nr_1\2024_01_16_MV_Dane_zasiegowe_new.gdb'
arcpy.env.workspace = output_MV

# Lista warstw wektorowych MV
# tutaj - _MV - tylko po to, zeby nie brac przeciazonych - jesli one juz z jakiegos powodu sa w geobazie
# lista_MV = arcpy.ListFeatureClasses('* _MV') - WCZESNIEJ BYLO TAK

# teraz to zmienilem
lista_MV = arcpy.ListFeatureClasses('*M_LTE*')
print('\n')
# Wyswietlenie warstw MV
print('Lista warstwy MV')
print(lista_MV)

# wyciagniecie do listy - common_part_lista - wartosci: LTE800, LTE900, LTE1800, LTE2100, LTE2600 itp
#
common_part_lista = []
for x in przeciazenia:
    # Wyciąganie części wspólnej nazwy - powiększenie liter - LTE
    common_part = x.split('_')[
        -1].upper()  # Używamy upper() aby powiekszyc litery, bo warstwy maja raz 'lte' a raz 'LTE'
    common_part_lista.append(common_part)
print('\n')
print('Lista pomocnicza')
print(common_part_lista)
print('\n')

# Przeszukiwanie obu list w poszukiwaniu par
# iterowanie sie przez liste z LTE lub UMTS (3g)
for common in common_part_lista:
    # iteracja jest zawsze dla tego samego wspolnego elementu LTE800, LTE900, LTE1800, LTE2100, LTE2600
    # dodawanie do listy mv_match warstw, ktore sa akurat iterowane i zawieraja np. LTE900 (z geobazy)
    mv_match = [layer for layer in lista_MV if common.upper() in layer.upper()]
    # dodawanie do listy przeciazenie_match warstw, ktore sa akurat iterowane i zawieraja np. LTE900 (z SDE)
    przeciazenie_match = [table for table in przeciazenia if common.upper() in table.upper()]

    # sprawdzamy czy przeciazenie_match = True i mv_match = True - JESTLI TAK TO IDIZEMY dalej
    if przeciazenie_match and mv_match:
        # mv_match[0] z geobazy - wczesniejsze warsrwy z bazy MV
        # przeciazenie_match[0] z bazy danych SDE - zeby robic warstwe przeciazenia
        print('----------------------------------------')
        print(f'Para: {mv_match[0]} - {przeciazenie_match[0]} ')
        print('----------------------------------------')

        # szukanie kolumny LCELL_OBJ, ktora bedzie kluczem do narzedzia AddJoin
        lista_4a = arcpy.ListFields(mv_match[0])
        a = lista_4a[9].name
        # print(a)

        # szukanie kolumny cell_obj, ktora bedzie kluczem do narzedzia AddJoin (z bazy SDE)
        # lista_4b = arcpy.ListFields(przeciazenie_match[0])
        lista_4b = arcpy.ListFields(fr'C:\Users\buchadan\AppData\Roaming\Esri\ArcGISPro\Favorites\Admin_SDE.sde\\{przeciazenie_match[0]}')
        b = lista_4b[1].name
        # print(b)

        # odszukanie LCELL_OBJ"
        print(f'po LCELL_OBJ (tekst) kolumnie: -- {a} (zmienna) -- SPRAWDZENIE -- łączy sie kolumna: -- {b} -- z warstwy {przeciazenie_match[0]}')
        print('\n')

        # indeks jesli chcemy to robic poza argciem pro
        # arcpy.AddIndex_management(przeciazenie_match[0], b, "Idx_" + b)

        # łaczenie warstwy z budynku SDE i warstwy

        # TRY I EXPCECT POMAGA GDY JUŻ BYŁO ZŁĄCZENIE I PUSZCZAM SKRYTP KOLEJNY RAZ
#         try:
#             wynik_2 = arcpy.management.AddJoin(mv_match[0], a, przeciazenie_match[0], b, join_type="KEEP_COMMON")
#             print("Join successful")
#             print('Tworzy: ')
#             output_feature_class_przeciazenia =   fr'{output_MV}\\przeciazenie_{common}'
#             print(output_feature_class_przeciazenia)
#         except arcpy.ExecuteError:
#             print(arcpy.GetMessages(2))  # Print the error messages

# po tym jak zrobimy AddJoin - trzeba warstwe zapisac do geobazy - do wczesniej utworzonej sciezki
# ta sciezka jest skomponowana z dopisow LTE I UMTS
#         arcpy.management.CopyFeatures(wynik_2, output_feature_class_przeciazenia)


print('\n')
print(
    '---------------------- Koniec - CZESCI II - ZMIENIONEEEEEEEEEE NA DOLE od tego miejsca do końca kodu ----------------------')
print('\n')

# Usuń pola bezpośrednio z warstwy źródłowej
# tworzy jedna liste po to, zeby od wszystkich warstw przeciazen usunac pola, ktre nam sa zbedne
# na dobry poczatek patrzymy sprawdzamy wszyskie listy
lista_5 = arcpy.ListFields(output_feature_class_przeciazenia)

# tworzymy liste, ktora bedzie zawierama wszyskie elementy, ktre beda do skawoania
lista_do_w = []
for index, x in enumerate(lista_5):
    # wskazanie pol, ktore wg. indeksow 0,1,8,31,32, ktore odpowiadaja kolejno OBJECTID, Shape -- LCELL_NAME --  Shape_Length, Shape_Area

    # PRZESUNIĘTE INDEKSY BO przy robieniu BKRAÓW dodałem kolumnę ZATEM index != 32 and index != 33:

    if index != 0 and index != 1 and index != 8 and index != 32 and index != 33:
        lista_do_w.append(x.name)
print('Pytanie czy jest pusat czy mie?')
print(lista_do_w)

# print('\n')
# print('Wyswietla rekordy do usuniecia w MV - ZOSTAWIAMY OBJECTID, Shape -- LCELL_NAME --  Shape_Length, Shape_Area')
# print(lista_do_w)

# wyszykanie juz utworzonych warstw przeciazenia
lista_przeciazone = arcpy.ListFeatureClasses('przeciazenie*')
print('Pytanie czy jest pusat czy mie?')
print(lista_przeciazone)
# usuwanie kolumn, ktore sa niepotrzene, zostawienie tylko kolumny OBJECTID, Shape -- LCELL_NAME --  Shape_Length, Shape_Area
for x in lista_przeciazone:
    print('\n')
    print(f'kasowanie rekordow dla: {x}')
    # kasowanie kolumn, ktore nie sa nam potrzebne
#     arcpy.management.DeleteField(x, lista_do_w)


print('\n')
print('---------------------- Koniec - CZESCI IV - stworzenie PRZECIĄŻEŃ DLA LTE ----------------------')
print('\n')

print('Meta LTE - dane zasiegowe')