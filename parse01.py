import csv
from datetime import datetime
import re
import locale
from dateutil.relativedelta import relativedelta

# Henry Mangelsdorf 2022
# This parse will begin with only removing unique parcels. Parcels with only one row of sale history do not hold enough information to determine if it qualifies for tax refund. 
# Only if the the house price is above $300,000 and built after the year 2000 do I keep it 


# these are the arrays for the 3 different categories this parse sorts the parcels into
not_removed = []
removed = []
to_be_determined = []
not_removed_counter = 0
removed_counter = 0
to_be_determined_counter = 0

csv_headers = ['Parcel/Account','City/ZIP','Address','Date Of Sale','Sale Price','Instrument','Grantor','Grantee','Term Of Sale','Year Built', 'Year, Season, SEV/Assessed_Value, PRE/MBT','Year, Season, SEV/Assessed_Value, PRE/MBT','Previous Year, Season, SEV/Assessed_Value, PRE/MBT','Previous Year, Season, SEV/Assessed_Value, PRE/MBT','Extra SEV Info']

csv_original = []



with open('lexington-township-sanilac-county-11_03_2018-10_21_2022.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0: # skips over header so it is not added into the csv_orginal list
            line_count += 1
        else:
            line_count += 1
            csv_original.append(row)

last_index = len(csv_original)
print('Total') # total lines are displayed to make sure they are the same after the sorting method
print(last_index)



########################################################################################################################################################################################################################################################################################
for i in range(0,last_index):
    if i == 0: # the first row needs a different code since it has no row before it
        if csv_original[i][0] != csv_original[i+1][0] and csv_original[i][2] != csv_original[i+1][2]:
            
            ############################################################################################################################################
            
            decimal_point_char = locale.localeconv()['decimal_point']
            clean = re.sub(r'[^0-9'+decimal_point_char+r']+', '', csv_original[i][4])
            value = float(clean) # the house price
            ############################################################################################################################################

            if csv_original[i][9] != 'No Data to Display' and csv_original[i][9] != 'NA':
                if value > 300000 and float(csv_original[i][9]) > 2000: # keeps the parcel if the house price is above $300,000 and built past the year 2000
                    to_be_determined.append(csv_original[i])
                    to_be_determined.append('\n')
                    to_be_determined_counter += 1
                    continue
                else:
                    removed.append(csv_original[i])
                    removed.append('\n') 
                    removed_counter += 1
                    continue
            else:
                removed.append(csv_original[i])
                removed.append('\n') 
                removed_counter += 1
                continue

    ########################################################################################################################################################################################################################################################################################

    if i == last_index-1: # the final row needs different code since there is no row after it
        if csv_original[i][0] != csv_original[i-1][0] and csv_original[i][2] != csv_original[i-1][2]:
            
            ############################################################################################################################################
            
            decimal_point_char = locale.localeconv()['decimal_point']
            clean = re.sub(r'[^0-9'+decimal_point_char+r']+', '', csv_original[i][4])
            value = float(clean) # the house price
            ############################################################################################################################################

            if csv_original[i][9] != 'No Data to Display' and csv_original[i][9] != 'NA':
                if value > 300000 and float(csv_original[i][9]) > 2000: # keeps the parcel if the house price is above $300,000 and built past the year 2000
                    to_be_determined.append(csv_original[i])
                    to_be_determined.append('\n')
                    to_be_determined_counter += 1
                    continue
                else:
                    removed.append(csv_original[i])
                    removed.append('\n') 
                    removed_counter += 1
                    continue
            else:
                removed.append(csv_original[i]) 
                removed.append('\n')  
                removed_counter += 1
                continue
    
    ########################################################################################################################################################################################################################################################################################
    
    # checks if all other rows other than the first and last are single row parcels
    if (csv_original[i][0] != csv_original[i-1][0] and csv_original[i][2] != csv_original[i-1][2]) and (csv_original[i][0] != csv_original[i+1][0] and csv_original[i][2] != csv_original[i+1][2]):
        
        ############################################################################################################################################
        
        decimal_point_char = locale.localeconv()['decimal_point']
        clean = re.sub(r'[^0-9'+decimal_point_char+r']+', '', csv_original[i][4])
        value = float(clean) # the house price
        ############################################################################################################################################

        if csv_original[i][9] != 'No Data to Display' and csv_original[i][9] != 'NA':
            if value > 300000 and float(csv_original[i][9]) > 2000: # keeps the parcel if the house price is above $300,000 and built past the year 2000
                to_be_determined.append(csv_original[i])
                to_be_determined.append('\n')
                to_be_determined_counter += 1
            else:
                removed.append(csv_original[i])
                removed.append('\n')
                removed_counter += 1
        else:
            removed.append(csv_original[i]) 
            removed.append('\n')    
            removed_counter += 1
    else:
        not_removed.append(csv_original[i])
        not_removed_counter += 1

    ########################################################################################################################################################################################################################################################################################
print('Not Removed:')
print(not_removed_counter)
print('Removed:')
print(removed_counter)
print('To Be Determined:')
print(to_be_determined_counter)
print('New Total:')
print(not_removed_counter + removed_counter + to_be_determined_counter) # this second total is printed to compare with the previous total


    
with open('lexington-township-sanilac-county-11_03_2018-10_21_2022-parsed_01-01.csv', 'w') as f: #  to csv rows that were not removed by parse01 qualifiers
        write = csv.writer(f)
        write.writerow(csv_headers)
        write.writerows(not_removed)

with open('lexington-township-sanilac-county-11_03_2018-10_21_2022-parse01-removed.csv', 'w') as f: # writes to csv rows that were removed by parse01 qualifiers
        write = csv.writer(f)
        write.writerow(csv_headers)
        write.writerows(removed)

with open('lexington-township-sanilac-county-11_03_2018-10_21_2022-parse01-to-be-determined.csv', 'w') as f: # writes to csv rows that were removed by parse01 qualifiers
        write = csv.writer(f)
        write.writerow(csv_headers)
        write.writerows(to_be_determined)

##############################################################################################################################################################################

