def zmien_nazwy_pol_na_aliasy(geobaza):
    # Ustawia środowisko robocze na wskazaną geobazę
    arcpy.env.workspace = geobaza
    # Pobiera listę wszystkich warstw w geobazie
    lista_warstw = arcpy.ListFeatureClasses()

    # Przechodzi przez każdą warstwę
    for warstwa in lista_warstw:
        # Pobiera listę pól i ich aliasów
        pola = [pole.name for pole in arcpy.ListFields(warstwa)]

        aliasy = {pole.name: pole.aliasName for pole in arcpy.ListFields(warstwa)}
        arcpy.AddMessage('aliasy')
        arcpy.AddMessage(aliasy)
        # Zmienia nazwy pól na takie same jak aliasy
        for pole in pola:
            nazwa_aliasu = aliasy.get(pole)
            # Ensure the new field name is not "OBJECTID" or any other reserved name
            if nazwa_aliasu and pole != nazwa_aliasu and nazwa_aliasu.upper() != "OBJECTID":
                arcpy.management.AlterField(warstwa, pole, new_field_name=nazwa_aliasu)