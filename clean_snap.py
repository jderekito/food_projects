import arcpy
from arcpy import env
env.overwriteOutput = True

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
with arcpy.da.SearchCursor(fc, ['SHAPE@', name_field,match_filter_field],
                           where_clause=snap_select) as cursor:
    for row in cursor:
        # Print the name of the residential road
        print("Checking for : "+row[1]+" in the SNAP list")
        # Select stores with matching Match_Code
        non_snap_select = u'{0} LIKE \'{1}\''.format(arcpy.AddFieldDelimiters(fc, match_filter_field), row[2])
        print(non_snap_select)

        # Loop through each non-SNAP store
        with arcpy.da.SearchCursor(fc, ['SHAPE@', name_field,match_filter_field],
                                    where_clause=non_snap_select) as inner_cursor:
            for inner_row in inner_cursor:
                print row[0].distanceTo(inner_row[0])

                #Update the SNAP_DUB by OBJECTID
                update_fields = ['WELL_YIELD', 'WELL_CLASS']
                # Create update cursor for feature class
                with arcpy.da.UpdateCursor(fc, fields) as update_cursor:
                    for update_row in cursor:
                        #set vals

                        # Update the cursor with the updated list
                        update_cursor.updateRow(update_row)
