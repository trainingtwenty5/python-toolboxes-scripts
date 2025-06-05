import arcpy
import csv
arcpy.env.overwriteOutput = True

# WCZYTANIE warstwu punkowej
#warstwa_punktowa = r"C:\EsriTraining\Daniel\Daniel.gdb\Point"
warstwa_punktowa = input("Podaj ścieżkę do warstwy punktowej: ")


# wczytanie rastrow
#arcpy.env.workspace = r'C:\EsriTraining\Daniel\rastry'
arcpy.env.workspace = input("Podaj ścieżkę do przestrzeni roboczej rastrów: ")

lista_rastrow = arcpy.ListRasters('*')
print('#wczytanie rastrow')
print(lista_rastrow)
print('\n')

# wczytanie poligonów
#arcpy.env.workspace = r'C:\EsriTraining\Daniel\Poligony.gdb'
arcpy.env.workspace = input("Podaj ścieżkę do przestrzeni roboczej poligonów: ")
lista_poligonow = arcpy.ListFeatureClasses('*')
lista_poligonow = sorted(lista_poligonow)
print('#wczytanie poligonów')
print(lista_poligonow)
print('\n')

dane_do_przeciecia = []
n=0
for warstwa_rastrowa, warstwa_wektorowa in zip(lista_rastrow, lista_poligonow):
    print('\n')
    print('--------------------------#wczytanie pary: --------------------------')
    print('warstwa rastrowa: ' + warstwa_rastrowa)
    print('warstwa wektorowa: ' + warstwa_wektorowa)
    print('\n')


    # stworzenie ścieżki ponieważ bez tego nie chciał tworzyć warstwy wynikowej w odpowiedni sposób
    warstwa_rastrowa = r'C:\EsriTraining\Daniel\rastry\{}'.format(warstwa_rastrowa)
    dane_wynikowe_1 = r'C:\EsriTraining\Daniel\W.gdb\Dane_1_{}'.format(warstwa_wektorowa)
    print('dane_wynikowe_1')
    print(dane_wynikowe_1)

    # Przypisywanie punktow do rastra
    arcpy.sa.ExtractValuesToPoints(warstwa_punktowa, warstwa_rastrowa, dane_wynikowe_1, "NONE", "VALUE_ONLY")
    n+=1
    print(n)

    # print('To co jest brane do zczytania wartości')
    # print(warstwa_punktowa)
    # print(warstwa_rastrowa)
    # print('\n')


    dane_wynikowe_2 = r'C:\EsriTraining\Daniel\W.gdb\Razem_2_{}'.format(warstwa_wektorowa)
    print('dane_wynikowe_2')
    print(dane_wynikowe_2)

    # przecinanie się warstw ktora już ma wartość z rastra i dodanie do tebeli tego co w poligonie
    #arcpy.analysis.Intersect(dane_do_przeciecia, dane_wynikowe_2, "ALL", None, "INPUT")
    arcpy.SpatialJoin_analysis(dane_wynikowe_1, warstwa_wektorowa, dane_wynikowe_2)


    # klasaobiektów
    k = dane_wynikowe_2
    print('dane_wynikowe_2 - kolejny raz ')
    print(dane_wynikowe_2)
    # pola
    p = ['Join_Count', 'TARGET_FID', 'ID_PKT', 'RASTERVALU', 'Id', 'litologia']

    q = ' "Join_Count" = 1 or "Join_Count" = 0 '

    lista = ['Join_Count, TARGET_FID, ID_PKT, RASTERVALU, Id, litologia']


    with arcpy.da.SearchCursor(k, p, q) as Scursor:
        for row in Scursor:
            rowtext = "{}, {}, {}, {}, {}, {}".format(row[0], row[1], row[2], row[3], row[4], row[5])
            lista.append(rowtext)

    del Scursor
    textbody = '\n'.join(lista[:])
    # print(textbody)

    dane_wynikowe_5 = r'C:\EsriTraining\Daniel\{}.csv'.format(warstwa_wektorowa)
    print('dane_wynikowe_5')
    print(dane_wynikowe_5)

    csvf = open(dane_wynikowe_5, 'w')
    csvf.write(textbody)
    csvf.close()
    print('ok')