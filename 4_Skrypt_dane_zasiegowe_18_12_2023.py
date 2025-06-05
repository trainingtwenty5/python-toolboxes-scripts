import arcpy
import os
# nadpisywanie obiektow 
arcpy.env.overwriteOutput = True
# Ustaw œrodowisko pracy ArcPy # Œcie¿ka do folderu z plikami SHP
arcpy.env.workspace = r'D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\Dane'
e2180 = r"C:\\Users\\zz_gis_esri\\AppData\\Roaming\\ESRI\\Desktop10.8\\projections\\PUWG_92.prj"

# U¿yj Walk do rekurencyjnego przegl¹dania folderów i uzyskania plików SHP
lista_1 = []
lista_1UMTS = []
for folder, subfolders, files in arcpy.da.Walk(arcpy.env.workspace, datatype="FeatureClass"):
    for file in files:
        if 'LTE' in file:
            lista_1.append(os.path.join(folder, file))
        if 'UMTS900' in file:
            lista_1UMTS.append(os.path.join(folder, file))

print('Start - dane zasiegowe')

#join_table = input(r"Podaj path dla lcell typ: D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\mv.gdb\lcell_20231130_Merge")
join_table = r'D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\mv.gdb\lcell_20231130_Merge'
print('\n')


#join_table_wcell = input(r"Podaj path dla wcell typ: D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\mv.gdb\wcell_20231130_Merge'")
join_table_wcell = r'D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\mv.gdb\wcell_20231130_Merge'
print('\n')

#output_info = input(r"Podaj path dla -- info -- wynikow: D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\Wynik_test_18_12_2023.gdb")
print('\n')
output_info = r'D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\Wynik_test_18_12_2023.gdb'
#output_MV = input(r"Podaj path dla -- MV -- wynikow: D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\Wynik_test_18_12_2023_MV.gdb")
output_MV = r'D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\Wynik_test_18_12_2023_MV.gdb'
print('\n')

print('wczytanie path')

pola_do_usuniecia = []
nazwy_plikow = []
n = -1



for sciezka in lista_1:
    nazwa_pliku = os.path.basename(sciezka)
    nazwa_bez_rozszerzenia, rozszerzenie = os.path.splitext(nazwa_pliku)
    nazwy_plikow.append(nazwa_bez_rozszerzenia)
    n += 1
 
             
    arcpy.management.AddField(lista_1[n], "objj1", "Long")

    arcpy.management.CalculateField(lista_1[n], "objj1", '!LEGEND!', "PYTHON3")

    #join_table = 'lcell_20231130_Merge'
    
    wynik_1 = arcpy.management.AddJoin(lista_1[n], "objj1", join_table, "LCELL_OBJ")

    # chcemy ja nazwyaæ, warstwy maja siê nazywac same 

   
    #print(f'{output}\\{nazwy_plikow[n]})')

    output_feature_class_info = fr'{output_info}\\{nazwy_plikow[n]}_info'
    #print(output_feature_class_info)
    output_feature_class_MV =   fr'{output_MV}\\{nazwy_plikow[n]}_MV'
    #print(output_feature_class_MV)
    
    arcpy.management.CopyFeatures(wynik_1, output_feature_class_info)
    arcpy.env.outputCoordinateSystem = e2180
    arcpy.management.CopyFeatures(wynik_1, output_feature_class_MV)
      
    # Usuñ pola bezpoœrednio z warstwy Ÿród³owej
    lista_2 = arcpy.ListFields(output_feature_class_MV)

    for x in lista_2:
        pola_do_usuniecia.append(x.name)
        
    print('\n')
    print('Wyswietla rekordy do usuniecia w MV')
    print(pola_do_usuniecia[2:12])
    arcpy.management.DeleteField(output_feature_class_MV, pola_do_usuniecia[2:12])
    pola_do_usuniecia = []
    
    print('\n')
    print(f'Done: {nazwy_plikow[n]}_info')
    print(f'Done: {nazwy_plikow[n]}_MV')
    print('\n')
    
    
print('\n')          
print('---------------------- Koniec - CZESCI I - stworzenie MV ----------------------')
print('\n')

    
print('\n')          
print('---------------------- CZESCI I CD - UMTS ----------------------')
print('\n')    
    
d = -1  
nazwy_plikow_UMTS = []
for sciezka in lista_1UMTS:
    nazwa_pliku = os.path.basename(sciezka)
    print('umts - nazwa_pliku')
    print(nazwa_pliku)
    nazwa_bez_rozszerzenia, rozszerzenie = os.path.splitext(nazwa_pliku)
    nazwy_plikow_UMTS.append(nazwa_bez_rozszerzenia)
    print('nazwy_plikow_UMTS.append(nazwa_bez_rozszerzenia) - umst')
    print(nazwy_plikow_UMTS)
    d += 1
 
             
    arcpy.management.AddField(lista_1UMTS[d], "objj1", "Long")

    arcpy.management.CalculateField(lista_1UMTS[d], "objj1", '!LEGEND!', "PYTHON3")


    
    wynik_1 = arcpy.management.AddJoin(lista_1UMTS[d], "objj1", join_table_wcell, "WCELL_OBJ")

    # chcemy ja nazwyaæ, warstwy maja siê nazywac same 

   
    #print(f'{output}\\{nazwy_plikow[n]})')

    output_feature_class_info = fr'{output_info}\\{nazwy_plikow_UMTS[d]}_info'
    print('umst - output_feature_class_info')
    print(output_feature_class_info)
    output_feature_class_MV =   fr'{output_MV}\\{nazwy_plikow_UMTS[d]}_MV'
    print('umst - output_feature_class_MV')
    print(output_feature_class_MV)
    
    arcpy.management.CopyFeatures(wynik_1, output_feature_class_info)
    arcpy.env.outputCoordinateSystem = e2180
    arcpy.management.CopyFeatures(wynik_1, output_feature_class_MV)
      
    # Usuñ pola bezpoœrednio z warstwy Ÿród³owej
    lista_2 = arcpy.ListFields(output_feature_class_MV)
    print('lista_2 - umst')
    print(lista_2)
    for x in lista_2:
        pola_do_usuniecia.append(x.name)
        
    print('\n')
    print('Wyswietla rekordy do usuniecia w MV - UMTS')
    print(pola_do_usuniecia[2:12])
    arcpy.management.DeleteField(output_feature_class_MV, pola_do_usuniecia[2:12])
    pola_do_usuniecia = [] 
    
    print('\n')
    print(f'Done: {nazwy_plikow_UMTS[d]}_info')
    print(f'Done: {nazwy_plikow_UMTS[d]}_MV')
    print('\n')
        
print('\n')          
print('---------------------- kONIEC CZESCI I CD - UMTS ----------------------')
print('\n')    



# Ustawienie œrodowiska pracy geobaze SDE
arcpy.env.workspace = r"C:\\Users\\zz_gis_esri\\AppData\\Roaming\\ESRI\\Desktop10.8\\ArcCatalog\\126.185.136.190_sde_.sde"

# Lista tabel do przefiltrowania z bazdy danych do tabel, od przeciazenia lte
lista_3 = arcpy.ListTables('*_przeciazone_lte*')
print('\n') 
print(lista_3)
print('\n')

# Filtrowanie tabel, które nie koñcz¹ siê na "_a" ani "_lte700"
przeciazenia = [table for table in lista_3 if not (table.endswith("_a") or table.endswith("_lte700"))]
print('\n')
print('Lista przeciazenia')
print(przeciazenia )

# Ustawienie œrodowiska pracy na drug¹ geobazê
#arcpy.env.workspace = r"D:\\Daniel\\ArcGIS\\Projects\\Dane_zasiegowe\\Wynik_test_18_12_2023_MV.gdb"

#output_MV = r'D:\Daniel\ArcGIS\Projects\Dane_zasiegowe\Wynik_test_18_12_2023_MV.gdb'
# przypisanie srodowiska do podanej sciezki output_MV zeby wybrac juz zrobione warstwy MV
arcpy.env.workspace = output_MV
# Lista warstw wektorowych MV
# tutaj - _MV - tylko po to, zeby nie brac przeciazonych - jesli one juz z jakiegos powodu sa w geobazie 
lista_MV = arcpy.ListFeatureClasses('*_MV')
print('\n')
# Wyswietlenie warstw MV
print('Lista warstwy MV')
print(lista_MV)


# wyciagniecie do listy - common_part_lista - wartosci: LTE800, LTE900, LTE1800, LTE2100, LTE2600 itp
#
common_part_lista = []
for x in przeciazenia:
    # Wyci¹ganie czêœci wspólnej nazwy - powiêkszenie liter - LTE
    common_part = x.split('_')[-1].upper()  # U¿ywamy upper() aby powiekszyc litery, bo warstwy maja raz 'lte' a raz 'LTE'
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
        #print(a)
        
        # szukanie kolumny cell_obj, ktora bedzie kluczem do narzedzia AddJoin (z bazy SDE)
        #lista_4b = arcpy.ListFields(przeciazenie_match[0])
        lista_4b = arcpy.ListFields(fr'C:\\Users\\zz_gis_esri\\AppData\\Roaming\\ESRI\\Desktop10.8\\ArcCatalog\\126.185.136.190_sde_.sde\\{przeciazenie_match[0]}')
        b = lista_4b[1].name
        #print(b)

        #odszukanie LCELL_OBJ"
        print(f'po LCELL_OBJ (tekst) kolumnie: -- {a} (zmienna) -- SPRAWDZENIE -- laczy sie kolumna: -- {b} -- z warstwy {przeciazenie_match[0]}')
        print('\n')

        # ³aczenie warstwy z budynku SDE i warstwy 
        wynik_2 = arcpy.management.AddJoin(mv_match[0], a, przeciazenie_match[0], b, join_type="KEEP_COMMON")
        
        print('Tworzy: ')
        output_feature_class_przeciazenia =   fr'{output_MV}\\przeciazenie_{common}' 
        print(output_feature_class_przeciazenia)
        
        #po tym jak zrobimy AddJoin - trzeba warstwe zapisac do geobazy - do wczesniej utworzonej sciezki
        # ta sciezka jest skomponowana z dopisow LTE I UMTS
        arcpy.management.CopyFeatures(wynik_2, output_feature_class_przeciazenia)

            
            
# Usuñ pola bezpoœrednio z warstwy Ÿród³owej
# tworzy jedna liste po to, zeby od wszystkich warstw przeciazen usunac pola, ktre nam sa zbedne
# na dobry poczatek patrzymy sprawdzamy wszyskie listy
lista_5 = arcpy.ListFields(output_feature_class_przeciazenia)

# tworzymy liste, ktora bedzie zawierama wszyskie elementy, ktre beda do skawoania
lista_do_w = []
for index, x in enumerate(lista_5):
    #wskazanie pol, ktore wg. indeksow 0,1,8,31,32, ktore odpowiadaja kolejno OBJECTID, Shape -- LCELL_NAME --  Shape_Length, Shape_Area
    if index != 0 and index != 1 and index != 8 and index != 31 and index != 32:
        lista_do_w.append(x.name)


# print('\n')
# print('Wyswietla rekordy do usuniecia w MV - ZOSTAWIAMY OBJECTID, Shape -- LCELL_NAME --  Shape_Length, Shape_Area')
# print(lista_do_w)

# wyszykanie juz utworzonych warstw przeciazenia 
lista_przeciazone = arcpy.ListFeatureClasses('przeciazenie*')
# usuwanie kolumn, ktore sa niepotrzene, zostawienie tylko kolumny OBJECTID, Shape -- LCELL_NAME --  Shape_Length, Shape_Area
for x in lista_przeciazone:
    print('\n') 
    print(f'kasowanie rekordow dla: {x}')
    #kasowanie kolumn, ktore nie sa nam potrzebne
    arcpy.management.DeleteField(x, lista_do_w)
    
    
print('\n')          
print('---------------------- Koniec - CZESCI II - stworzenie przeciazen ----------------------')
print('\n')

print('Meta - dane zasiegowe')
