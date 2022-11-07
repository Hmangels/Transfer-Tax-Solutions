import csv
import locale
import re
from datetime import datetime
from re import sub
from dateutil.relativedelta import relativedelta
from decimal import Decimal

# Henry Mangelsdorf 2022




# PARSE 1
# This parse will begin with removing single rows parcels which will go to their own array and csv.
# The commented out code within parse 1 is an alternate parse that is not to be used as of 11/7/2022. It only keeps single row parcels if the the house price is above $300,000 and built after the year 2000.




########################################################################################################################################################################################################################################################################################
########################################################################################################################################################################################################################################################################################
disqualifying_words = []
csv_headers = ['Parcel/Account','City/ZIP','Address','Date Of Sale','Sale Price','Instrument','Grantor','Grantee','Term Of Sale','Year Built', 'Year, Season, SEV/Assessed_Value, PRE/MBT','Year, Season, SEV/Assessed_Value, PRE/MBT','Previous Year, Season, SEV/Assessed_Value, PRE/MBT','Previous Year, Season, SEV/Assessed_Value, PRE/MBT','Extra SEV Info']
csv_original = []

not_removed = []
disqualified = []
qualified = []
to_be_determined = []
single_row = []

not_removed_counter = 0
disqualified_counter = 0
qualified_counter = 0
to_be_determined_counter = 0





with open('city-of-livonia-wayne-county-8_20_2019-8_20_2022.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0: # skips over header so it is not added into the csv_orginal list
            line_count += 1
        else:
            line_count += 1
            csv_original.append(row)

with open('disqualifying_words.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        disqualifying_words.append(row)

last_index = len(csv_original)
print('\n')
print('Beginning - Total') # total lines are displayed to make sure they are the same after the sorting method
print(last_index)
print('\n')

########################################################################################################################################################################################################################################################################################
for i in range(0,last_index):
    if i == 0: # The first row needs a different code since it has no row before it.
        if csv_original[i][0] != csv_original[i+1][0] and csv_original[i][2] != csv_original[i+1][2]:
            single_row.append(csv_original[i])
            continue
            
                

    ########################################################################################################################################################################################################################################################################################

    if i == last_index-1: # The final row needs different code since there is no row after it.
        if csv_original[i][0] != csv_original[i-1][0] and csv_original[i][2] != csv_original[i-1][2]:
            single_row.append(csv_original[i])
            continue
               
    
    ########################################################################################################################################################################################################################################################################################
    
    # Checks if all other rows other than the first and last are single row parcels.
    if (csv_original[i][0] != csv_original[i-1][0] and csv_original[i][2] != csv_original[i-1][2]) and (csv_original[i][0] != csv_original[i+1][0] and csv_original[i][2] != csv_original[i+1][2]):
                single_row.append(csv_original[i])
                
        
    else:
        not_removed.append(csv_original[i])
########################################################################################################################################################################################################################################################################################


########################################################################################################################################################################################################################################################################################
#for i in range(0,last_index):
#    if i == 0: # the first row needs a different code since it has no row before it
#        if csv_original[i][0] != csv_original[i+1][0] and csv_original[i][2] != csv_original[i+1][2]:
#            
#            ############################################################################################################################################
#            decimal_point_char = locale.localeconv()['decimal_point']
#            clean = re.sub(r'[^0-9'+decimal_point_char+r']+', '', csv_original[i][4])
#            value = float(clean) # the house price
#            ############################################################################################################################################
#
#            if csv_original[i][9] != 'No Data to Display' and csv_original[i][9] != 'NA':
#                if value > 300000 and float(csv_original[i][9]) > 2000: # keeps the parcel if the house price is above $300,000 and built past the year 2000
#                    to_be_determined.append(csv_original[i])
#                    #to_be_determined_counter += 1
#                    continue
#                else:
#                    disqualified.append(csv_original[i])
#                    #disqualified_counter += 1
#                    continue
#            else:
#                disqualified.append(csv_original[i])
#                #disqualified_counter += 1
#                continue
#
########################################################################################################################################################################################################################################################################################
#
#    if i == last_index-1: # the final row needs different code since there is no row after it
#        if csv_original[i][0] != csv_original[i-1][0] and csv_original[i][2] != csv_original[i-1][2]:
#            
#            ############################################################################################################################################
#            decimal_point_char = locale.localeconv()['decimal_point']
#            clean = re.sub(r'[^0-9'+decimal_point_char+r']+', '', csv_original[i][4])
#            value = float(clean) # the house price
#            ############################################################################################################################################
#
#            if csv_original[i][9] != 'No Data to Display' and csv_original[i][9] != 'NA':
#                if value > 300000 and float(csv_original[i][9]) > 2000: # keeps the parcel if the house price is above $300,000 and built past the year 2000
#                    to_be_determined.append(csv_original[i])
#                    #to_be_determined_counter += 1
#                    continue
#                else:
#                    disqualified.append(csv_original[i])
#                    #disqualified_counter += 1
#                    continue
#            else:
#                disqualified.append(csv_original[i]) 
#                #disqualified_counter += 1
#                continue
#    
########################################################################################################################################################################################################################################################################################
    
    # checks if all other rows other than the first and last are single row parcels
#    if (csv_original[i][0] != csv_original[i-1][0] and csv_original[i][2] != csv_original[i-1][2]) and (csv_original[i][0] != csv_original[i+1][0] and csv_original[i][2] != csv_original[i+1][2]):
#        
#        ############################################################################################################################################
#        decimal_point_char = locale.localeconv()['decimal_point']
#        clean = re.sub(r'[^0-9'+decimal_point_char+r']+', '', csv_original[i][4])
#        value = float(clean) # the house price
#        ############################################################################################################################################
#
#        if csv_original[i][9] != 'No Data to Display' and csv_original[i][9] != 'NA':
#            if value > 300000 and float(csv_original[i][9]) > 2000: # keeps the parcel if the house price is above $300,000 and built past the year 2000
#                to_be_determined.append(csv_original[i])
#                #to_be_determined_counter += 1
#            else:
#                disqualified.append(csv_original[i])
#                #disqualified_counter += 1
#        else:
#            disqualified.append(csv_original[i])   
#            #disqualified_counter += 1
#    else:
#        not_removed.append(csv_original[i])
#        #not_removed_counter += 1

print('Parse One - Not Removed:')
print('Len(): ' + str(len(not_removed)))
print('Parse One - Disqualified:')
print('Len(): ' + str(int(len(disqualified))))
print('Parse One - To Be Determined:')
print('Len(): ' + str(int(len(to_be_determined))))
print('Parse One - Qualified:')
print('Len(): ' + str(len(qualified)))
print('Parse One - Single Row:')
print('Len(): ' + str(len(single_row)))
print('Parse One - Total:')
print('Len(): ' + str(len(not_removed) + (int(len(disqualified))) + (int(len(qualified))) + (int(len(to_be_determined))) + (int(len(single_row)))))
print('\n')

    
########################################################################################################################################################################################################################################################################################
########################################################################################################################################################################################################################################################################################


# PARSE 2
# parcels with only two rows and and the latter row has all 100.0000% PRE/MBT and the SEV for the latter row is less than or equal to the SEV for the earlier row.
########################################################################################################################################################################################################################################################################################


def convert(lst): # Converts the string into list. (I think this was for parsing the strings of columns 10 - 13)
   return eval(lst)

last_index = len(not_removed)

list_of_parcel_groups=[]
parcel_group = []
for i in range(0,last_index): # This groups together records that are in the same parcel/address.
    if i == last_index-1:
        parcel_group.append(not_removed[i])
        list_of_parcel_groups.append(parcel_group)  
    else:
        if not_removed[i][2] != not_removed[i-1][2]:
            list_of_parcel_groups.append(parcel_group)
            parcel_group = []
            parcel_group.append(not_removed[i])
            continue
        parcel_group.append(not_removed[i])



del list_of_parcel_groups[0]

not_removed = []

for i in range(len(list_of_parcel_groups)):
    SEV_list_0 = [] 
    SEV_list_1 = []
    PRE_MBT_list_0 = []
    PRE_MBT_check = False

    if (len(list_of_parcel_groups[i])) != 2:
        for item in list_of_parcel_groups[i]:
            not_removed.append(item)
        


    if len(list_of_parcel_groups[i]) == 2: # if the parcel group consists of only 2 records.
        for j in range(10,14):
            if(list_of_parcel_groups[i][0][j] != 'NA'):
                PRE_MBT_list_0.append(convert(list_of_parcel_groups[i][0][j])[3]) # This gathers all the PRE/MBT percentages.
                if(j == 10): # SEV for winter season of the sale date
                    SEV_list_0.append(convert(list_of_parcel_groups[i][0][j])[2])
                if(j == 11): # SEV for summer season of the sale date
                    SEV_list_0.append(convert(list_of_parcel_groups[i][0][j])[2])

        if len(SEV_list_0) == 2: # If the SEV list has two values check to see if they match and if so, remove the 2nd element so that we can just refer to the first element.
            if SEV_list_0[0] == SEV_list_0[1]:
                del SEV_list_0[1]

        for j in range(10,14):
            if(list_of_parcel_groups[i][1][j] != 'NA'):

                if(j == 10): # SEV for winter season of the sale date.
                    SEV_list_1.append(convert(list_of_parcel_groups[i][1][j])[2])
                if(j == 11): # SEV for summer season of the sale date.
                    SEV_list_1.append(convert(list_of_parcel_groups[i][1][j])[2])

        if len(SEV_list_1) == 2: # If the SEV list has two values check to see if they match and if so remove the 2nd element so that we can just refer to the first element.
            if SEV_list_1[0] == SEV_list_1[1]:
                del SEV_list_1[1]

        if len(PRE_MBT_list_0) > 0 :
            PRE_MBT_check = all(element == '100.0000%' for element in PRE_MBT_list_0) #If every value in the PRE_MBT_list_0 is == to 100.0000% then make the PRE_MBT check == true.
        if (len(SEV_list_0) > 0) and (len(SEV_list_1) > 0):
            assessed_value_0 = Decimal(sub(r'[^\d.]', '', SEV_list_0[0]))
            assessed_value_1 = Decimal(sub(r'[^\d.]', '', SEV_list_1[0]))
        if (len(SEV_list_0) > 0) and (len(SEV_list_1) > 0):
            if (assessed_value_0 <= assessed_value_1) and PRE_MBT_check: 
                for item in list_of_parcel_groups[i]:
                    qualified.append(item)
            else:
                for item in list_of_parcel_groups[i]:
                    not_removed.append(item)
               
                    
        else:
            for item in list_of_parcel_groups[i]:
                not_removed.append(item) 
                
            
                                             


print('Parse Two - Not Removed:')
print('Len(): ' + str(len(not_removed)))
print('Parse Two - Disqualified:')
print('Len(): ' + str(int(len(disqualified))))
print('Parse Two - To Be Determined:')
print('Len(): ' + str(int(len(to_be_determined))))
print('Parse Two - Qualified:')
print('Len(): ' + str(len(qualified)))
print('Parse Two - Single Row:')
print('Len(): ' + str(len(single_row)))
print('Parse Two - Total:')
print('Len(): ' + str(len(not_removed) + (int(len(disqualified))) + (int(len(qualified))) + (int(len(to_be_determined))) + (int(len(single_row)))))
print('\n')

########################################################################################################################################################################################################################################################################################
########################################################################################################################################################################################################################################################################################


    
# PARSE 3
# 11/7/2022
# Two sales in sucession. Or two sales in the same year. The grantee in the former sale equals the grantor in the in the latter sale. The latter sale is past the cutoff date. 
# The SEV in the latter year is greater than the former year's SEV. The homestead is 100% for latter sale including all seasons and previous year for two sales in sucession.
# When two sales are in the same year there is no homestead check. There is a check to make sure same year sale parcels are at least 2 months apart.
# The grantor or grantee name does not contain disqualifying words.

########################################################################################################################################################################################################################################################################################

cutoff_date = datetime.now() - relativedelta(years=4) # Cutoff date is 4 years ago from today.
cutoff_date_str = cutoff_date.strftime("%m/%d/%Y")


def convert(lst): # Converts the string into list. (I think this was for parsing the strings of columns 10 - 13)
   return eval(lst)

last_index_0 = len(not_removed)

list_of_parcel_groups=[]
parcel_group = []
for i in range(0,last_index_0): # This groups together records that are in the same parcel/address.
    if i == last_index_0-1:
        parcel_group.append(not_removed[i])
        list_of_parcel_groups.append(parcel_group)  
    else:
        if not_removed[i][2] != not_removed[i-1][2]:
            list_of_parcel_groups.append(parcel_group)
            parcel_group = []
            parcel_group.append(not_removed[i])
            continue
        parcel_group.append(not_removed[i])



not_removed = []
del list_of_parcel_groups[0]
for i in range(len(list_of_parcel_groups)):
   

    disqualified_word_check = False
    parcel_row_num = len(list_of_parcel_groups[i])
    last_index = parcel_row_num - 1
    
    if (parcel_row_num) == 1 or (parcel_row_num) == 2:
        for item in list_of_parcel_groups[i]:
            not_removed.append(item)
        continue

    

    for j in range(0,last_index):
        if list_of_parcel_groups[i][j+1][7] == list_of_parcel_groups[i][j][6]:
            for word in disqualifying_words: # Checks for  the presence of disqualifying words in the Grantor and Grantee.
                if (' ' + str(word[0]) + ' ') in str(list_of_parcel_groups[i][j][6]).upper():   
                    disqualified_word_check = True
            if(disqualified_word_check): 
                if(j==last_index-1):
                        for item in list_of_parcel_groups[i]:
                             not_removed.append(item)
                continue
            string_input_with_date = list_of_parcel_groups[i][j][3]
            date = datetime.strptime(string_input_with_date, "%m/%d/%Y") # This is the date of the latter sale.
            if(date.date() > cutoff_date.date()):
                SEV_list_0 = [] 
                SEV_list_1 = []
                PRE_MBT_list_0 = []
                PRE_MBT_check = False
                for k in range(10,14):
                    if(list_of_parcel_groups[i][j][k] != 'NA'):
                        PRE_MBT_list_0.append(convert(list_of_parcel_groups[i][j][k])[3]) # This Gathers all the PRE/MBT percentages
                        if(k == 10): # SEV for winter season of the sale date
                            SEV_list_0.append(convert(list_of_parcel_groups[i][j][k])[2])
                        if(k == 11): # SEV for summer season of the sale date
                            SEV_list_0.append(convert(list_of_parcel_groups[i][j][k])[2])

                if len(SEV_list_0) == 2: # If the SEV list has two values check to see if they match and if so remove the 2nd element so that we can just refer to the first element.
                    if SEV_list_0[0] == SEV_list_0[1]:
                        del SEV_list_0[1]

                for k in range(10,14):
                    if(list_of_parcel_groups[i][j+1][k] != 'NA'):
                        if(k == 10): # SEV for winter season of the sale date.
                            SEV_list_1.append(convert(list_of_parcel_groups[i][j+1][k])[2])
                        if(k == 11): # SEV for summer season of the sale date.
                            SEV_list_1.append(convert(list_of_parcel_groups[i][j+1][k])[2])

                if len(SEV_list_1) == 2: # If the SEV list has two values check to see if they match and if so, remove the 2nd element so that we can just refer to the first element.
                    if SEV_list_1[0] == SEV_list_1[1]:
                        del SEV_list_1[1]
                if len(PRE_MBT_list_0) > 0 :
                    PRE_MBT_check = all(element == '100.0000%' for element in PRE_MBT_list_0) # if every value in the PRE_MBT_list_0 is == to 100.0000% then make the PRE_MBT check == true.
                else:
                    if(j==last_index-1):
                        for item in list_of_parcel_groups[i]:
                             not_removed.append(item)
                    continue

                if (len(SEV_list_0) > 0) and (len(SEV_list_1) > 0):
                    assessed_value_0 = Decimal(sub(r'[^\d.]', '', SEV_list_0[0]))
                    assessed_value_1 = Decimal(sub(r'[^\d.]', '', SEV_list_1[0]))
                else:
                    if(j==last_index-1):
                        for item in list_of_parcel_groups[i]:
                             not_removed.append(item)
                    continue
                if (assessed_value_0 < assessed_value_1) and PRE_MBT_check: # If both sales are not in the same year then their SEV will not be equal. So if value 0 is < value 1 it might qualify.
                    for item in list_of_parcel_groups[i]:
                        qualified.append(item)
                    break
                string_input_with_date1 = list_of_parcel_groups[i][j][3] # These are the dates used for the 3 month gap check.
                string_input_with_date2 = list_of_parcel_groups[i][j+1][3]
                date1 = datetime.strptime(string_input_with_date1, "%m/%d/%Y")
                date2 = datetime.strptime(string_input_with_date2, "%m/%d/%Y")
                if (assessed_value_0 == assessed_value_1) and ((date1.year - date2.year) * 12 + (date1.month - date2.month) >= 2): # This is the 3 month gap check. I use 2 here instead of 3 as a sort of buffer. I do not include a PRE/MBT check because in this case the previous year homestead does not matter. Also the homestead in the current year for same year sales is tricky.
                    for item in list_of_parcel_groups[i]:
                        qualified.append(item)
                    break
                else:
                    if(j==last_index-1):
                        for item in list_of_parcel_groups[i]:
                                not_removed.append(item)
                    continue
            else:
                if(j==last_index-1):
                    for item in list_of_parcel_groups[i]:
                            not_removed.append(item)
                continue
        else:
            if(j==last_index-1):
                for item in list_of_parcel_groups[i]:
                    not_removed.append(item)
            continue

with open('sorting-test-001.csv', 'w') as f: # For test purposes.
        write = csv.writer(f)
        write.writerow(csv_headers)
        write.writerows(qualified)       
            

print('Parse Three - Not Removed:')
print('Len(): ' + str(len(not_removed)))
print('Parse Three - Disqualified:')
print('Len(): ' + str(int(len(disqualified))))
print('Parse Three - To Be Determined:')
print('Len(): ' + str(int(len(to_be_determined))))
print('Parse Three - Qualified:')
print('Len(): ' + str(len(qualified)))
print('Parse Three - Single Row:')
print('Len(): ' + str(len(single_row)))
print('Parse Three - Total:')
print('Len(): ' + str(len(not_removed) + (int(len(disqualified))) + (int(len(qualified))) + (int(len(to_be_determined))) + (int(len(single_row)))))
print('\n')
