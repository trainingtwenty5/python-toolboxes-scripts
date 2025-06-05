
import arcpy
lista =[700, 800, 900, 1800, 2100,2600]
w = r"D:\ArcGIS\2024_01_08_AVR_DIST\2024_01_08_AVR_DIST.gdb\lcell_dist_summary_20240108"
r = r"D:\ArcGIS\2024_01_08_AVR_DIST\2024_01_08_AVR_DIST_skrypt.gdb\test_lcell_dist_summa_"
for x in lista:
    print(x)
    rr = r+'{}'.format(x)
    
    arcpy.analysis.TableSelect(w, rr, f"BAND_NUMBER = {x}")
    print(rr)
print('done')


