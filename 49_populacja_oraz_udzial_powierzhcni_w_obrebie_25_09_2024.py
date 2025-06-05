# Importowanie niezbędnych modułów
import arcpy

# Ustawienia przestrzeni roboczej
arcpy.env.overwriteOutput = True  # Umożliwia nadpisywanie istniejących plików

# Definicja zmiennych
workspace = r"D:\ArcGIS\Pokrycie_regionow_DSS_cband_20_09_2024\test_s.gdb"
Klastry_s = "Klastry_s"
DOM_DSS = "DOM_DSS_OPL_20240901_50m_MV_s"
DOM_CBAND = "DOM_CBAND3600_OPL_107dBm_20240901_MV_s"
XYexp_locit = "XYexp_locit_20231129_dane_2180"


# Funkcja do przeprowadzania operacji analitycznych
def process_data(input_feature, sum_feature, output_suffix):
    # Przecięcie (Intersect)
    intersect_output = f"{workspace}\\intersect_{output_suffix}"
    arcpy.analysis.Intersect(in_features=[[Klastry_s, ""], [input_feature, ""]],
                             out_feature_class=intersect_output, join_attributes="ALL")

    # Rozpuszczenie (Dissolve)
    dissolve_output = f"{workspace}\\dissolve_{output_suffix}"
    arcpy.management.Dissolve(in_features=intersect_output, out_feature_class=dissolve_output,
                              dissolve_field=["CLUSTER_ID"])

    # Podsumowanie w obrębie (Summarize Within)
    summarize_output = f"{workspace}\\summarize_{output_suffix}"
    arcpy.analysis.SummarizeWithin(in_polygons=dissolve_output, in_sum_features=sum_feature,
                                   out_feature_class=summarize_output, keep_all_polygons="KEEP_ALL",
                                   sum_fields=[["pop_tot", "Sum"]])

    return summarize_output

# Proces dla danych DSS
summarize_DSS = process_data(DOM_DSS, XYexp_locit, "DSS")

# Dodawanie pól do Klastrów
fields_to_add = ["pop_DSS", "pop_CBAND", "pop_TOT", "area_DSS", "area_CBAND", "area_TOT"]
for field in fields_to_add:
    arcpy.management.AddField(in_table=Klastry_s, field_name=field, field_type="DOUBLE")

# Łączenie danych z podsumowania z Klastrami
arcpy.management.JoinField(in_data=Klastry_s, in_field="CLUSTER_ID",
                           join_table=summarize_DSS, join_field="CLUSTER_ID",
                           fields=["Shape_area", "Sum_pop_tot"])

# Proces dla danych CBAND
summarize_CBAND = process_data(DOM_CBAND, XYexp_locit, "CBAND")

# Łączenie wyników z Klastrami dla CBAND
arcpy.management.JoinField(in_data=Klastry_s, in_field="CLUSTER_ID",
                           join_table=summarize_CBAND, join_field="CLUSTER_ID",
                           fields=["Shape_area", "Sum_pop_tot"])

# Podsumowanie dla trzeciego zestawu danych (przy użyciu XYexp_locit, który jest używany dwukrotnie)
Klastry_s_SummarizeWithin = f"{workspace}\\Klastry_s_SummarizeWithin"
arcpy.analysis.SummarizeWithin(in_polygons=Klastry_s, in_sum_features=XYexp_locit,
                               out_feature_class=Klastry_s_SummarizeWithin, keep_all_polygons="KEEP_ALL",
                               sum_fields=[["pop_tot", "Sum"]])

# Łączenie wyników podsumowania z Klastrami
arcpy.management.JoinField(in_data=Klastry_s, in_field="CLUSTER_ID",
                           join_table=Klastry_s_SummarizeWithin, join_field="CLUSTER_ID",
                           fields=["sum_pop_tot_12", "Shape_area"])

# Aktualizacja pól za pomocą UpdateCursor
with arcpy.da.UpdateCursor(Klastry_s, [
        "CLUSTER_ID", "pop_DSS", "area_DSS", "pop_CBAND", "area_CBAND",
        "pop_TOT", "area_TOT", "Shape_area", "Sum_pop_tot",
        "Shape_area_1", "Sum_pop_tot_1", "Shape_area_12", "Sum_pop_tot_12"
    ]) as cursor:
    for row in cursor:
        row[1] = row[8]  # pop_DSS = Sum_pop_tot
        row[2] = row[7] / 10000  # area_DSS = Shape_area / 10 000
        row[3] = row[10]  # pop_CBAND = Sum_pop_tot_1
        row[4] = row[9] #/ 10000  # area_CBAND = Shape_area_1 / 10 000
        row[5] = row[12]  # pop_TOT = Sum_pop_tot_12
        row[6] = row[11] / 10000  # area_TOT = Shape_area_12 / 10 000

        cursor.updateRow(row)  # Aktualizacja wiersza
