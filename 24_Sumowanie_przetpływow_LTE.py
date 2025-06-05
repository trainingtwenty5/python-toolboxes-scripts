import arcpy

# Assuming 'your_feature_class' is the feature class you're working with
fc = 'SUMA_przeplywow_WYNIK_23_02_2024'

# Dictionary to map gridcode values to RSRP_dbm
gridcode_to_rsrp = {
    1: -116,
    2: -110,
    3: -103,
    4: -98,
    5: -92
}

# List of new fields to be added
new_fields = [
    'RSRP_dbm_LTE_1800',
    'RSRP_dbm_LTE_2100',
    'RSRP_dbm_LTE_800',
    'RSRP_dbm_LTE_2600'
]

# Corresponding gridcode fields
gridcode_fields = [
    'gridcode',
    'gridcode_1',
    'gridcode_12',
    'gridcode_12_13'
]

# Add new fields
for new_field in new_fields:
    arcpy.AddField_management(fc, new_field, 'SHORT')

# Update the new fields with the corresponding RSRP_dbm values
with arcpy.da.UpdateCursor(fc, gridcode_fields + new_fields) as cursor:
    for row in cursor:
        for i, gridcode_field in enumerate(gridcode_fields):
            # Assign the RSRP_dbm value based on the gridcode
            if row[i] in gridcode_to_rsrp:
                row[i + len(gridcode_fields)] = gridcode_to_rsrp[row[i]]
            else:
                row[i + len(gridcode_fields)] = None  # or some default value if needed
        cursor.updateRow(row)



# RSRP_dbm to MHz mapping
rsrp_to_mhz = {
    -116: [19, 39, 60, 77],
    -110: [26, 55, 84, 111],
    -103: [35, 74, 113, 150],
    -98: [41, 87, 133, 178],
    -92: [45, 95, 145, 195]
}

# LTE technology to index mapping (for the rsrp_to_mhz values)
lte_index = {
    'RSRP_dbm_LTE_1800': 1,  # 10MHz
    'RSRP_dbm_LTE_2100': 2,  # 15MHz
    'RSRP_dbm_LTE_800': 1,   # 10MHz
    'RSRP_dbm_LTE_2600': 2   # 15MHz
}

# Add a new field for "SUMA"
arcpy.AddField_management(fc, 'SUMA', 'LONG')

# List of RSRP_dbm fields for each LTE technology
rsrp_fields = [
    'RSRP_dbm_LTE_1800',
    'RSRP_dbm_LTE_2100',
    'RSRP_dbm_LTE_800',
    'RSRP_dbm_LTE_2600'
]

# Calculate "SUMA" values
with arcpy.da.UpdateCursor(fc, rsrp_fields + ['SUMA']) as cursor:
    for row in cursor:
        suma = 0
        for i, rsrp_field in enumerate(rsrp_fields):
            rsrp_value = row[i]
            if rsrp_value in rsrp_to_mhz:
                # Get the corresponding MHz value based on the RSRP value and LTE technology
                mhz_values = rsrp_to_mhz[rsrp_value]
                print(mhz_values)
                index = lte_index[rsrp_field]
                print(index)
                suma += mhz_values[index]
                print(suma)
        row[-1] = suma  # Set the SUMA value
        cursor.updateRow(row)
