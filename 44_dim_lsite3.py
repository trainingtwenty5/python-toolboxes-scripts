# -*- coding: utf-8 -*-
import arcpy
import logging
import psycopg2


# Ustawienie konfiguracji logowania
logging.basicConfig(filename='D:\\replikacja\\model_builder\\Python_3\\log_dim_liste.txt', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Przykładowe logowanie
logging.debug('Rozpoczęcie skryptu.')

arcpy.env.overwriteOutput = True
paths = {
    "sde": r'C:\Users\buchadan\AppData\Roaming\Esri\ArcGISPro\Favorites\126.185.136.190_ogolne.sde',
    "_PUWG_92_": r'D:\projections\ETRS 1989 Poland CS92.prj',
	'_WGS_84_4326': r'D:\projections\WGS 1984.prj',
	"_WGS_84_3857": r'D:\projections\WGS 1984 Web Mercator (auxiliary sphere).prj',
    "geobaza": r'D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb',
}


# Ustal połączenie z bazą danych
try:

    conn = psycopg2.connect(
        dbname="pgq_sde",
        user="admin",
        password="admin",
        host="126.185.136.190",
        port="5432"
    )
    print("Połączono z bazą danych")

    # Utwórz kursor
    cur = conn.cursor()

    # Utwórz tabelę na podstawie danych z materializowanego widoku
    create_table_query = """
    CREATE TABLE IF NOT EXISTS ogolne.mv_dim_lsite_vendor_table AS
    SELECT * FROM ogolne.mv_dim_lsite_vendor_t;
    """
    cur.execute(create_table_query)
    conn.commit()
    print("Tabela została utworzona na podstawie materializowanego widoku")

    # Zamknij kursor i połączenie
    cur.close()
    conn.close()
    print("Połączenie z bazą danych zostało zamknięte")

except Exception as error:
    print("Wystąpił błąd podczas połączenia z bazą danych: ", error)


print('-------------------------------------------')
print('-------------------------------------------')
print('-------------------------------------------')
print('-------------------------------------------')

t = 'mv_dim_liste_vendor_geom'
try:
    # print(fr'{paths["sde"]}\pgq_sde.ogolne.mv_dim_lsite_vendor')
    # print(fr'{paths["sde"]}\\{t}_2180_t')
    print('______________________')
    #arcpy.SpatialReference(3857)
    arcpy.management.XYTableToPoint(fr'{paths["sde"]}\pgq_sde.ogolne.mv_dim_lsite_vendor_t', fr'{paths["geobaza"]}\\{t}_2180_t_new2', "xpos", "ypos", None, paths["_PUWG_92_"])

    arcpy.management.Project(fr'{paths["geobaza"]}\{t}_2180_t_new2', fr'{paths["geobaza"]}\{t}_3857_t_new2', paths["_WGS_84_3857"])

    arcpy.management.TruncateTable(
        in_table=fr'{paths["sde"]}\pgq_sde.ogolne.mv_dim_liste_vendor_geom_2180_t'
    )

    arcpy.management.TruncateTable(
        in_table=fr'{paths["sde"]}\pgq_sde.ogolne.mv_dim_liste_vendor_geom_3857_t'
    )

    arcpy.management.Append(
        inputs=fr'{paths["geobaza"]}\\{t}_2180_t_new2',
        target=fr'{paths["sde"]}\pgq_sde.ogolne.mv_dim_liste_vendor_geom_2180_t',
        schema_type="NO_TEST",
        field_mapping=r'id "id" true true false 4 Long 0 10,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,id,-1,-1;lsite_wh_id "lsite_wh_id" true true false 8 Double 3 16,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,lsite_wh_id,-1,-1;loc_wh_id "loc_wh_id" true true false 8 Double 3 16,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,loc_wh_id,-1,-1;lsite_id "lsite_id" true true false 8 Double 3 16,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,lsite_id,-1,-1;lsite_name "lsite_name" true true false 60 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,lsite_name,0,59;lsite_vendor "lsite_vendor" true true false 30 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,lsite_vendor,0,29;lsite_version "lsite_version" true true false 30 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,lsite_version,0,29;lsite_owner "lsite_owner" true true false 10 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,lsite_owner,0,9;reg_code "reg_code" true true false 3 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,reg_code,0,2;proj_code "proj_code" true true false 10 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,proj_code,0,9;proj_name "proj_name" true true false 20 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,proj_name,0,19;netis_obj "netis_obj" true true false 8 Double 3 16,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,netis_obj,-1,-1;netis_loc_obj "netis_loc_obj" true true false 8 Double 3 16,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,netis_loc_obj,-1,-1;netis_ver "netis_ver" true true false 10 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,netis_ver,0,9;status "status" true true false 30 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,status,0,29;status_opr "status_opr" true true false 30 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,status_opr,0,29;consolidation "consolidation" true true false 2 Short 0 5,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,consolidation,-1,-1;eff_date "eff_date" true true false 8 Date 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,eff_date,-1,-1;upd_date "upd_date" true true false 8 Date 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,upd_date,-1,-1;exp_date "exp_date" true true false 8 Date 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,exp_date,-1,-1;mri "mri" true true false 1 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,mri,0,254;lsite_nems_name "lsite_nems_name" true true false 20 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,lsite_nems_name,0,19;scg_nems_name "scg_nems_name" true true false 30 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,scg_nems_name,0,29;msite_wh_id "msite_wh_id" true true false 8 Double 3 16,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,msite_wh_id,-1,-1;msite_nems_name "msite_nems_name" true true false 20 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,msite_nems_name,0,19;msite_name "msite_name" true true false 60 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,msite_name,0,59;xpos "xpos" true true false 8 Double 1 12,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,xpos,-1,-1;ypos "ypos" true true false 8 Double 1 12,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,ypos,-1,-1;nazwa_warstwy "nazwa_warstwy" true true false 25 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,nazwa_warstwy,0,24;data_aktualizacji "data_aktualizacji" true true false 8 Date 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_2180_t_new1,data_aktualizacji,-1,-1',
        subtype="",
        expression="",
        match_fields=None,
        update_geometry="NOT_UPDATE_GEOMETRY"
    )

    arcpy.management.Append(
        inputs=fr'{paths["geobaza"]}\{t}_3857_t_new2',
        target=fr'{paths["sde"]}\pgq_sde.ogolne.mv_dim_liste_vendor_geom_3857_t',
        schema_type="NO_TEST",
        field_mapping=r'id "id" true true false 4 Long 0 10,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,id,-1,-1;lsite_wh_id "lsite_wh_id" true true false 8 Double 3 16,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,lsite_wh_id,-1,-1;loc_wh_id "loc_wh_id" true true false 8 Double 3 16,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,loc_wh_id,-1,-1;lsite_id "lsite_id" true true false 8 Double 3 16,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,lsite_id,-1,-1;lsite_name "lsite_name" true true false 60 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,lsite_name,0,59;lsite_vendor "lsite_vendor" true true false 30 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,lsite_vendor,0,29;lsite_version "lsite_version" true true false 30 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,lsite_version,0,29;lsite_owner "lsite_owner" true true false 10 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,lsite_owner,0,9;reg_code "reg_code" true true false 3 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,reg_code,0,2;proj_code "proj_code" true true false 10 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,proj_code,0,9;proj_name "proj_name" true true false 20 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,proj_name,0,19;netis_obj "netis_obj" true true false 8 Double 3 16,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,netis_obj,-1,-1;netis_loc_obj "netis_loc_obj" true true false 8 Double 3 16,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,netis_loc_obj,-1,-1;netis_ver "netis_ver" true true false 10 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,netis_ver,0,9;status "status" true true false 30 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,status,0,29;status_opr "status_opr" true true false 30 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,status_opr,0,29;consolidation "consolidation" true true false 2 Short 0 5,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,consolidation,-1,-1;eff_date "eff_date" true true false 8 Date 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,eff_date,-1,-1;upd_date "upd_date" true true false 8 Date 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,upd_date,-1,-1;exp_date "exp_date" true true false 8 Date 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,exp_date,-1,-1;mri "mri" true true false 1 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,mri,0,254;lsite_nems_name "lsite_nems_name" true true false 20 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,lsite_nems_name,0,19;scg_nems_name "scg_nems_name" true true false 30 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,scg_nems_name,0,29;msite_wh_id "msite_wh_id" true true false 8 Double 3 16,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,msite_wh_id,-1,-1;msite_nems_name "msite_nems_name" true true false 20 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,msite_nems_name,0,19;msite_name "msite_name" true true false 60 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,msite_name,0,59;xpos "xpos" true true false 8 Double 1 12,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,xpos,-1,-1;ypos "ypos" true true false 8 Double 1 12,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,ypos,-1,-1;nazwa_warstwy "nazwa_warstwy" true true false 25 Text 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,nazwa_warstwy,0,24;data_aktualizacji "data_aktualizacji" true true false 8 Date 0 0,First,#,D:\dane_gdb\Skrypt_dim_liste\Skrypt_dim_liste.gdb\mv_dim_liste_vendor_geom_3857_t_new1,data_aktualizacji,-1,-1',
        subtype="",
        expression="",
        match_fields=None,
        update_geometry="NOT_UPDATE_GEOMETRY"
    )

    print(fr'finish')



except Exception as e:
    logging.error('Błąd: {}'.format(str(e)))

print('Koniec')
logging.debug('Zakończenie skryptu.')
