import arcpy
from arcpy import env
env.overwriteOutput = True

# Post-man step #1: select/delete snaps that are dups
# Post-man step #2: select/update snap to 1 for all non-snaps that are snap_dups

from arcpy import env
env.workspace = r"C:\Data\PhD\Projects\FoodProjects\Data\Food_Deserts\Scratch.gdb"
fc = "GROC_W_SNAP2"
snap_filter_field = 'SNAP'
name_field = 'Store_Name'
match_filter_field = "Match_Code"

# Select SNAP stores
snap_select = u'{0} = 1'.format(arcpy.AddFieldDelimiters(fc, snap_filter_field))
print(snap_select)

# Loop through each SNAP store
with arcpy.da.SearchCursor(fc, ['SHAPE@', name_field,match_filter_field, 'OID@'], where_clause=snap_select) as cursor:
    for row in cursor:
        snap_dup_checker = False
        # Print the name of the residential road
        print("Checking for : "+row[1]+" in the SNAP list")

        # Select stores with matching Match_Code, that aren't SNAPs (this is key)
        non_snap_select = u'{0} LIKE \'{1}\' AND {2} = {3}'.format(arcpy.AddFieldDelimiters(fc, match_filter_field), row[2], snap_filter_field, 0)
        # Loop through each non-SNAP store
        # Distance beween bases on Baseball field is about 90 feet, which is about 27.5 meters
        # Update SNAP_DUP w/ all non-snap duplicates
        with arcpy.da.SearchCursor(fc, ['SHAPE@', 'OID@', snap_filter_field], where_clause=non_snap_select) as inner_cursor:
            for inner_row in inner_cursor:
                print(str(row[0].distanceTo(inner_row[0])) + " distance on OID: " + str(inner_row[1]))
                if row[0].distanceTo(inner_row[0])<30.0:
                    snap_dup_select = u'{0} = {1}'.format(arcpy.AddFieldDelimiters(fc, "OBJECTID"), inner_row[1])
                    update_fields = ['SNAP_DUP']
                    with arcpy.da.UpdateCursor(fc, update_fields,where_clause=snap_dup_select) as update_cursor:
                        for update_row in update_cursor:
                            update_row[0] = 1
                            update_cursor.updateRow(update_row)
                    snap_dup_checker = True
        if snap_dup_checker:
            # Update SNAP_DUP for this particular SNAP as it will be deleted
            snap_dup_select = u'{0} = {1}'.format(arcpy.AddFieldDelimiters(fc, "OBJECTID"), row[3])
            update_fields = ['SNAP_DUP']
            with arcpy.da.UpdateCursor(fc, update_fields,where_clause=snap_dup_select) as update_cursor:
                for update_row in update_cursor:
                    update_row[0] = 1
                    update_cursor.updateRow(update_row)
