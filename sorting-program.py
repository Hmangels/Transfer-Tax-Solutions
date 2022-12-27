import csv
import locale
import re
import itertools
from datetime import datetime
from re import sub
from dateutil.relativedelta import relativedelta
from decimal import Decimal

# Henry Mangelsdorf 2022


# 11/21/2022 I added this piece of code throughout the script:

# new_list_of_parcel_groups = []
# for elem in list_of_parcel_groups:
#     if elem not in new_list_of_parcel_groups:
#         new_list_of_parcel_groups.append(elem)
# list_of_parcel_groups = new_list_of_parcel_groups

# It removes duplicates unless the duplicates were right next to eachother. The program still sees them as just one parcel. 

# 12/12/2022 I added code in parse one to keep duplicate single row parcels from being appended to single_row or disqualified

########################################################################################################################################################################################################################################################################################
# PARSE 1
# This parse will begin with removing single rows parcels which will go to their own array and csv. 11/9/2022- I added a disqualifying rule if the grantor contains a disqualifying word.
# The commented out code within parse 1 is an alternate parse that is not to be used as of 11/7/2022 and it does not have a disqualifying word check for future reference. It only keeps single row parcels if the the house price is above $300,000 and built after the year 2000.
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





with open('city-of-lansing-ingham-county-01_14_2019-12_21_2022.csv') as csv_file:
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
    disqualified_word_check = False
    if i == 0: # The first row needs a different code since it has no row before it.
        if csv_original[i][0] != csv_original[i+1][0] and csv_original[i][2] != csv_original[i+1][2]:
            for word in disqualifying_words: # Checks for  the presence of disqualifying words in the Grantor and Grantee.
                if (' ' + str(word[0]) + ' ') in (' '+str(csv_original[i][6]).upper()+' '): 
                    disqualified_word_check = True
            if(disqualified_word_check):
                if csv_original[i] not in disqualified:
                    disqualified.append(csv_original[i])
                continue
            else:
                if csv_original[i] not in single_row:
                    single_row.append(csv_original[i])
                continue
            
                

    ########################################################################################################################################################################################################################################################################################

    if i == last_index-1: # The final row needs different code since there is no row after it.
        if csv_original[i][0] != csv_original[i-1][0] and csv_original[i][2] != csv_original[i-1][2]:
            for word in disqualifying_words: # Checks for  the presence of disqualifying words in the Grantor and Grantee.
                if (' ' + str(word[0]) + ' ') in (' '+str(csv_original[i][6]).upper()+' '): 
                    disqualified_word_check = True
            if(disqualified_word_check):
                if csv_original[i] not in disqualified:
                    disqualified.append(csv_original[i])
                continue
            else:
                if csv_original[i] not in single_row:
                    single_row.append(csv_original[i])
                continue
               
    
    ########################################################################################################################################################################################################################################################################################
    
    # Checks if all other rows other than the first and last are single row parcels.
    if (csv_original[i][0] != csv_original[i-1][0] and csv_original[i][2] != csv_original[i-1][2]) and (csv_original[i][0] != csv_original[i+1][0] and csv_original[i][2] != csv_original[i+1][2]):
        for word in disqualifying_words: # Checks for  the presence of disqualifying words in the Grantor and Grantee.
                if (' ' + str(word[0]) + ' ') in (' '+str(csv_original[i][6]).upper()+' '): 
                    disqualified_word_check = True
        if(disqualified_word_check):
            if csv_original[i] not in disqualified:
                disqualified.append(csv_original[i])
            continue
        else:
            if csv_original[i] not in single_row:
                single_row.append(csv_original[i])
            continue
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




total_for_percentages = ( (len(not_removed) + len(disqualified) + (len(qualified))) + (len(to_be_determined)) + (len(single_row))  )
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
print('Parse One - Pre-Duplicate Removal Total:')
print('Len(): ' + str(len(not_removed) + (int(len(disqualified))) + (int(len(qualified))) + (int(len(to_be_determined))) + (int(len(single_row)))))
print('\n')
not_removed_percentage_str = str(round(float(len(not_removed)/total_for_percentages),3))  + '  '
disqualified_percentage_str = str(round(float(len(disqualified)/total_for_percentages),3))  + '  '
to_be_determined_percentage_str = str(round(float(len(to_be_determined)/total_for_percentages),3))  + '  '
qualfied_percentage_str = str(round(float(len(qualified)/total_for_percentages),3))  + '  '
single_row_percentage_str = str(round(float(len(single_row)/total_for_percentages),3))  + '  '

print("Not Removed = " + not_removed_percentage_str + "  Disqualified = " + disqualified_percentage_str + "  TBD = " + to_be_determined_percentage_str + "  Qualified = " + qualfied_percentage_str + "  Single Rows = " + single_row_percentage_str)
print('\n')
print('\n')

    
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

new_list_of_parcel_groups = []
for elem in list_of_parcel_groups:
    if elem not in new_list_of_parcel_groups:
        new_list_of_parcel_groups.append(elem)
list_of_parcel_groups = new_list_of_parcel_groups


for i in range(len(list_of_parcel_groups)):
    SEV_list_0 = [] 
    SEV_list_1 = []
    PRE_MBT_list_0 = []
    PRE_MBT_check = False
    disqualified_word_check_00 = False

    if (len(list_of_parcel_groups[i])) != 2:
        for item in list_of_parcel_groups[i]:
            not_removed.append(item)
        


    if len(list_of_parcel_groups[i]) == 2: # if the parcel group consists of only 2 records.

        if list_of_parcel_groups[i][1][7] == list_of_parcel_groups[i][0][6]:
                for word in disqualifying_words: # Checks for  the presence of disqualifying words in the Grantor and Grantee.
                    if (' ' + str(word[0]) + ' ') in (' '+str(list_of_parcel_groups[i][0][6]).upper()+' '):   
                        disqualified_word_check_00 = True
                if(disqualified_word_check_00): 
                    for item in list_of_parcel_groups[i]:
                        not_removed.append(item)
                    continue

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
            if (assessed_value_0 < assessed_value_1) and PRE_MBT_check: 
                for item in list_of_parcel_groups[i]:
                    qualified.append(item)
                continue
            if (assessed_value_0 < assessed_value_1) and not PRE_MBT_check:
                for item in list_of_parcel_groups[i]:
                    disqualified.append(item)
                continue
            if (assessed_value_0 > assessed_value_1):
                for item in list_of_parcel_groups[i]:
                    disqualified.append(item)
                continue
            string_input_with_date1 = list_of_parcel_groups[i][0][3] # These are the dates used for the 3 month gap check.
            string_input_with_date2 = list_of_parcel_groups[i][1][3]
            date1 = datetime.strptime(string_input_with_date1, "%m/%d/%Y")
            date2 = datetime.strptime(string_input_with_date2, "%m/%d/%Y")
            if (assessed_value_0 == assessed_value_1) and ((date1.year - date2.year) * 12 + (date1.month - date2.month) >= 2): # This is the 3 month gap check. I use 2 here instead of 3 as a sort of buffer. I do not include a PRE/MBT check because in this case the previous year homestead does not matter. Also the homestead in the current year for same year sales is tricky.
                for item in list_of_parcel_groups[i]:
                    qualified.append(item)
            else:
                for item in list_of_parcel_groups[i]:
                    disqualified.append(item)
                
               
                    
        else:
            for item in list_of_parcel_groups[i]:
                not_removed.append(item) 
                
            
                                             

total_for_percentages = ( (len(not_removed) + len(disqualified) + (len(qualified))) + (len(to_be_determined)) + (len(single_row))  )
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
print('Parse Two - True Total:')
print('Len(): ' + str(len(not_removed) + (int(len(disqualified))) + (int(len(qualified))) + (int(len(to_be_determined))) + (int(len(single_row)))))
print('\n')
not_removed_percentage_str = str(round(float(len(not_removed)/total_for_percentages),3))  + '  '
disqualified_percentage_str = str(round(float(len(disqualified)/total_for_percentages),3))  + '  '
to_be_determined_percentage_str = str(round(float(len(to_be_determined)/total_for_percentages),3))  + '  '
qualfied_percentage_str = str(round(float(len(qualified)/total_for_percentages),3))  + '  '
single_row_percentage_str = str(round(float(len(single_row)/total_for_percentages),3))  + '  '

print("Not Removed = " + not_removed_percentage_str + "  Disqualified = " + disqualified_percentage_str + "  TBD = " + to_be_determined_percentage_str + "  Qualified = " + qualfied_percentage_str + "  Single Rows = " + single_row_percentage_str)
print('\n')
print('\n')

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

new_list_of_parcel_groups = []
for elem in list_of_parcel_groups:
    if elem not in new_list_of_parcel_groups:
        new_list_of_parcel_groups.append(elem)
list_of_parcel_groups = new_list_of_parcel_groups

for i in range(len(list_of_parcel_groups)):
    

    disqualified_word_check_01 = False
    parcel_row_num = len(list_of_parcel_groups[i])
    last_index = parcel_row_num - 1 # The last index here is one less than the parcel row number because otherwise it would run into an index out of bounds error because of j + 1.
    
    if (parcel_row_num) == 1 or (parcel_row_num) == 2:
        for item in list_of_parcel_groups[i]:
            not_removed.append(item)
        continue

    

    for j in range(0,last_index):
        if list_of_parcel_groups[i][j+1][7] == list_of_parcel_groups[i][j][6]:
            for word in disqualifying_words: # Checks for  the presence of disqualifying words in the Grantor and Grantee.
                if (' ' + str(word[0]) + ' ') in (' '+str(list_of_parcel_groups[i][j][6]).upper()+' '):   
                    disqualified_word_check_01 = True
            if(disqualified_word_check_01): 
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
                PRE_MBT_list_1 = []
                PRE_MBT_check = False
                PRE_MBT_same_year_check = False
                for k in range(10,14):
                    if(list_of_parcel_groups[i][j][k] != 'NA'):
                        PRE_MBT_list_0.append(convert(list_of_parcel_groups[i][j][k])[3]) # This Gathers all the PRE/MBT percentages
                        if(k == 10): # SEV for winter season of the sale date
                            SEV_list_0.append(convert(list_of_parcel_groups[i][j][k])[2])
                            PRE_MBT_list_1.append(convert(list_of_parcel_groups[i][j][k])[3])
                        if(k == 11): # SEV for summer season of the sale date
                            SEV_list_0.append(convert(list_of_parcel_groups[i][j][k])[2])
                            PRE_MBT_list_1.append(convert(list_of_parcel_groups[i][j][k])[3])
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
                    PRE_MBT_check = all(element == '100.0000%' for element in PRE_MBT_list_0) # If every value in the PRE_MBT_list_0 is == to 100.0000% then make the PRE_MBT check == true.
                else:
                    if(j==last_index-1):
                        for item in list_of_parcel_groups[i]:
                            not_removed.append(item)
                    continue
                if len(PRE_MBT_list_1) > 0 : # 11/22/2022 This is a homestead check for same year sales. If they are all 0% than the check will equal true. 
                    PRE_MBT_same_year_check = all(element == '0.0000%' for element in PRE_MBT_list_1)   

                

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
                if (assessed_value_0 == assessed_value_1) and ((date1.year - date2.year) * 12 + (date1.month - date2.month) >= 2) and not PRE_MBT_same_year_check: # This is the 3 month gap check. I use 2 here instead of 3 as a sort of buffer. I do not include a PRE/MBT check because in this case the previous year homestead does not matter. Also the homestead in the current year for same year sales is tricky.
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

  
            
total_for_percentages = ( (len(not_removed) + len(disqualified) + (len(qualified))) + (len(to_be_determined)) + (len(single_row))  )
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
not_removed_percentage_str = str(round(float(len(not_removed)/total_for_percentages),3))  + '  '
disqualified_percentage_str = str(round(float(len(disqualified)/total_for_percentages),3))  + '  '
to_be_determined_percentage_str = str(round(float(len(to_be_determined)/total_for_percentages),3))  + '  '
qualfied_percentage_str = str(round(float(len(qualified)/total_for_percentages),3))  + '  '
single_row_percentage_str = str(round(float(len(single_row)/total_for_percentages),3))  + '  '

print("Not Removed = " + not_removed_percentage_str + "  Disqualified = " + disqualified_percentage_str + "  TBD = " + to_be_determined_percentage_str + "  Qualified = " + qualfied_percentage_str + "  Single Rows = " + single_row_percentage_str)
print('\n')
print('\n')



########################################################################################################################################################################################################################################################################################   
# PARSE 4
# 11/8/2022
# Parse 4 will disqualify any parcel with a SEV that increases every single year.
########################################################################################################################################################################################################################################################################################


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

new_list_of_parcel_groups = []
for elem in list_of_parcel_groups:
    if elem not in new_list_of_parcel_groups:
        new_list_of_parcel_groups.append(elem)
list_of_parcel_groups = new_list_of_parcel_groups

for i in range(len(list_of_parcel_groups)):
    
    
    parcel_row_num = len(list_of_parcel_groups[i])
    last_index = parcel_row_num - 1 # The last index here is one less than the parcel row number because otherwise it would run into an index out of bounds error because of j + 1.

    for j in range(0,last_index):

        SEV_list_0 = [] 
        SEV_list_1 = []
        
        
        for k in range(10,12):
            if(list_of_parcel_groups[i][j][k] != 'NA'):
                
                # SEV for winter season of the sale date
                SEV_list_0.append(convert(list_of_parcel_groups[i][j][k])[2])
                # SEV for summer season of the sale date
                SEV_list_0.append(convert(list_of_parcel_groups[i][j][k])[2])

        if len(SEV_list_0) == 2: # If the SEV list has two values check to see if they match and if so remove the 2nd element so that we can just refer to the first element.
            if SEV_list_0[0] == SEV_list_0[1]:
                del SEV_list_0[1]

        for k in range(10,12):
            if(list_of_parcel_groups[i][j+1][k] != 'NA'):
                # SEV for winter season of the sale date.
                SEV_list_1.append(convert(list_of_parcel_groups[i][j+1][k])[2])
                # SEV for summer season of the sale date.
                SEV_list_1.append(convert(list_of_parcel_groups[i][j+1][k])[2])

        if len(SEV_list_1) == 2: # If the SEV list has two values check to see if they match and if so, remove the 2nd element so that we can just refer to the first element.
            if SEV_list_1[0] == SEV_list_1[1]:
                del SEV_list_1[1]

        if (len(SEV_list_0) > 0) and (len(SEV_list_1) > 0):
            assessed_value_0 = Decimal(sub(r'[^\d.]', '', SEV_list_0[0]))
            assessed_value_1 = Decimal(sub(r'[^\d.]', '', SEV_list_1[0]))
        else:
            for item in list_of_parcel_groups[i]:
                not_removed.append(item)
            break

        if (assessed_value_0 < assessed_value_1): # If both sales are not in the same year then their SEV will not be equal. So if value 0 is < value 1 it might qualify.
            for item in list_of_parcel_groups[i]:
                not_removed.append(item)
            break
        
        if (assessed_value_0 == assessed_value_1): 
            for item in list_of_parcel_groups[i]:
                not_removed.append(item)
            break
        else: # This else can and should only mean that assessed_value_0 > assessed_value_1
            if(j==last_index-1):
                for item in list_of_parcel_groups[i]:
                    disqualified.append(item)
            continue

total_for_percentages = ( (len(not_removed) + len(disqualified) + (len(qualified))) + (len(to_be_determined)) + (len(single_row))  )
print('Parse Four - Not Removed:')
print('Len(): ' + str(len(not_removed)))
print('Parse Four - Disqualified:')
print('Len(): ' + str(int(len(disqualified))))
print('Parse Four - To Be Determined:')
print('Len(): ' + str(int(len(to_be_determined))))
print('Parse Four - Qualified:')
print('Len(): ' + str(len(qualified)))
print('Parse Four - Single Row:')
print('Len(): ' + str(len(single_row)))
print('Parse Four - Total:')
print('Len(): ' + str(len(not_removed) + (int(len(disqualified))) + (int(len(qualified))) + (int(len(to_be_determined))) + (int(len(single_row)))))
print('\n')
not_removed_percentage_str = str(round(float(len(not_removed)/total_for_percentages),3)) + '  '
disqualified_percentage_str = str(round(float(len(disqualified)/total_for_percentages),3)) + '  '
to_be_determined_percentage_str = str(round(float(len(to_be_determined)/total_for_percentages),3)) + '  '
qualfied_percentage_str = str(round(float(len(qualified)/total_for_percentages),3)) + '  '
single_row_percentage_str = str(round(float(len(single_row)/total_for_percentages),3)) + '  '

print("Not Removed = " + not_removed_percentage_str + "  Disqualified = " + disqualified_percentage_str + "  TBD = " + to_be_determined_percentage_str + "  Qualified = " + qualfied_percentage_str + "  Single Rows = " + single_row_percentage_str)
print('\n')
print('\n')



########################################################################################################################################################################################################################################################################################   
# PARSE 5
# 11/9/2022
# Parse 5 will disqualify parcels that have a higher SEV for all sales after the cut off date than the SEV for all sales before the cutoff date.
# If there is more than one sale past the cutoff date then not only must they all have higher SEVs than all the SEVs for sales before the cutoff date, but their SEV's must 11/10/2022 ... ?
########################################################################################################################################################################################################################################################################################
# 11/10/2022 MADISON HEIGHTS - 28741 HERBERT ST WAS DISQUALIFIED HERE WHEN IT QUALIFIED

cutoff_date = datetime.now() - relativedelta(years=4) # Cutoff date is 4 years ago from today.
cutoff_date_str = cutoff_date.strftime("%m/%d/%Y")
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

new_list_of_parcel_groups = []
for elem in list_of_parcel_groups:
    if elem not in new_list_of_parcel_groups:
        new_list_of_parcel_groups.append(elem)
list_of_parcel_groups = new_list_of_parcel_groups


for i in range(len(list_of_parcel_groups)):
    
    past_cutoff_arr = []
    before_cutoff_arr = []
    parcel_row_num = len(list_of_parcel_groups[i])
    SEV_list_Check = False
    past_cutoff_Check = False
    past_cutoff_Check2 = False

    for j in range(0,parcel_row_num):

        string_input_with_date = list_of_parcel_groups[i][j][3] 
        date = datetime.strptime(string_input_with_date, "%m/%d/%Y")

        if (date.date() > cutoff_date.date()): 
            SEV_list = [] 
            
            for k in range(10,12):  # If the date is after the cutoff date.
                if(list_of_parcel_groups[i][j][k] != 'NA'):
                    
                    # SEV for winter season of the sale date
                    SEV_list.append(convert(list_of_parcel_groups[i][j][k])[2])
                    # SEV for summer season of the sale date
                    SEV_list.append(convert(list_of_parcel_groups[i][j][k])[2])

            if len(SEV_list) == 2: # If the SEV list has two values check to see if they match and if so remove the 2nd element so that we can just refer to the first element.
                if SEV_list[0] == SEV_list[1]:
                    del SEV_list[1]

            if (len(SEV_list) > 0):
                assessed_value = Decimal(sub(r'[^\d.]', '', SEV_list[0]))
                past_cutoff_arr.append(assessed_value)
            else:
                SEV_list_Check = True
            

        if (date.date() <= cutoff_date.date()):  # If the date is on or before the cutoff date.
            SEV_list = [] 

            for k in range(10,12):
                if(list_of_parcel_groups[i][j][k] != 'NA'):
                    
                    # SEV for winter season of the sale date
                    SEV_list.append(convert(list_of_parcel_groups[i][j][k])[2])
                    # SEV for summer season of the sale date
                    SEV_list.append(convert(list_of_parcel_groups[i][j][k])[2])

            if len(SEV_list) == 2: # If the SEV list has two values check to see if they match and if so remove the 2nd element so that we can just refer to the first element.
                if SEV_list[0] == SEV_list[1]:
                    del SEV_list[1]

            if (len(SEV_list) > 0):
                assessed_value = Decimal(sub(r'[^\d.]', '', SEV_list[0]))
                before_cutoff_arr.append(assessed_value)
            else:
                SEV_list_Check = True
            

    # Now that every row's SEV value is collected from the parcel and split into two different arrays based on their date I can apply my rules to see if it disqualifies the parcel.  
    if (SEV_list_Check):
        for item in list_of_parcel_groups[i]:
            not_removed.append(item)
        continue

    for j in range(0,len(past_cutoff_arr)):
        if(len(past_cutoff_arr)) == 1:
            break
        if past_cutoff_arr[j] <= past_cutoff_arr[j-1]:
            past_cutoff_Check = True

    if (past_cutoff_Check):
        for item in list_of_parcel_groups[i]:
            not_removed.append(item)
        continue

    before_cutoff_max = 0
    for j in range(0, len(before_cutoff_arr)):
        if j == 0:
            max = before_cutoff_arr[0]
            before_cutoff_max = max
        else:
            if before_cutoff_arr[j] > max:
                max = before_cutoff_arr[j]
                before_cutoff_max = max

    for j in range(0,len(past_cutoff_arr)):
        if past_cutoff_arr[j] <= before_cutoff_max:
            past_cutoff_Check2 = True

    if(past_cutoff_Check2):
        for item in list_of_parcel_groups[i]:
            not_removed.append(item)
        continue
    
    for item in list_of_parcel_groups[i]:
        disqualified.append(item)
    continue



total_for_percentages = ( (len(not_removed) + len(disqualified) + (len(qualified))) + (len(to_be_determined)) + (len(single_row))  )
print('Parse Five - Not Removed:')
print('Len(): ' + str(len(not_removed)))
print('Parse Five - Disqualified:')
print('Len(): ' + str(int(len(disqualified))))
print('Parse Five - To Be Determined:')
print('Len(): ' + str(int(len(to_be_determined))))
print('Parse Five - Qualified:')
print('Len(): ' + str(len(qualified)))
print('Parse Five - Single Row:')
print('Len(): ' + str(len(single_row)))
print('Parse Five - Total:')
print('Len(): ' + str(len(not_removed) + (int(len(disqualified))) + (int(len(qualified))) + (int(len(to_be_determined))) + (int(len(single_row)))))
print('\n')
not_removed_percentage_str = str(round(float(len(not_removed)/total_for_percentages),3)) + '  '
disqualified_percentage_str = str(round(float(len(disqualified)/total_for_percentages),3)) + '  '
to_be_determined_percentage_str = str(round(float(len(to_be_determined)/total_for_percentages),3)) + '  '
qualfied_percentage_str = str(round(float(len(qualified)/total_for_percentages),3)) + '  '
single_row_percentage_str = str(round(float(len(single_row)/total_for_percentages),3)) + '  '

print("Not Removed = " + not_removed_percentage_str + "  Disqualified = " + disqualified_percentage_str + "  TBD = " + to_be_determined_percentage_str + "  Qualified = " + qualfied_percentage_str + "  Single Rows = " + single_row_percentage_str)
print('\n')
print('\n')
        
########################################################################################################################################################################################################################################################################################   
# PARSE 6
# 11/9/2022
# Parse 6 will disqualify parcels that contain disqualifying words in all grantor and grantee cells except for most latter grantee and the most former grantor.
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

new_list_of_parcel_groups = []
for elem in list_of_parcel_groups:
    if elem not in new_list_of_parcel_groups:
        new_list_of_parcel_groups.append(elem)
list_of_parcel_groups = new_list_of_parcel_groups

for i in range(len(list_of_parcel_groups)):
    
   
    parcel_row_num = len(list_of_parcel_groups[i])

    for j in range(0,parcel_row_num):
        disqualified_word_check_03 = False
        disqualified_word_check_04 = False
        disqualified_word_check_05 = False
        if j == 0:
            for word in disqualifying_words: 
                if (' ' + str(word[0]) + ' ') in (' '+str(list_of_parcel_groups[i][j][6]).upper()+' '):   
                    disqualified_word_check_03 = True
            if not(disqualified_word_check_03): 
                for item in list_of_parcel_groups[i]:
                    not_removed.append(item)
                break      

        if j == (parcel_row_num-1):
            for word in disqualifying_words: 
                if (' ' + str(word[0]) + ' ') in (' '+str(list_of_parcel_groups[i][j][7]).upper()+' '):   
                    disqualified_word_check_03 = True
            if(disqualified_word_check_03): 
                for item in list_of_parcel_groups[i]:
                    disqualified.append(item)
                break 
            else:
                for item in list_of_parcel_groups[i]:
                    not_removed.append(item)
                break  

      
        if j != 0 and j != parcel_row_num-1:     

            for word in disqualifying_words: # Checks for  the presence of disqualifying words in the Grantor and Grantee.
                if (' ' + str(word[0]) + ' ') in (' '+str(list_of_parcel_groups[i][j][6]).upper()+' '):   
                    disqualified_word_check_04 = True
            for word in disqualifying_words:
                if (' ' + str(word[0]) + ' ') in (' '+str(list_of_parcel_groups[i][j][7]).upper()+' '):   
                    disqualified_word_check_05 = True
            
            if(disqualified_word_check_04 and disqualified_word_check_05): 
                continue
            else:
                for item in list_of_parcel_groups[i]:
                    not_removed.append(item)
                break     
    

total_for_percentages = ( (len(not_removed) + len(disqualified) + (len(qualified))) + (len(to_be_determined)) + (len(single_row))  )
print('Parse Six - Not Removed:')
print('Len(): ' + str(len(not_removed)))
print('Parse Six - Disqualified:')
print('Len(): ' + str(int(len(disqualified))))
print('Parse Six - To Be Determined:')
print('Len(): ' + str(int(len(to_be_determined))))
print('Parse Six - Qualified:')
print('Len(): ' + str(len(qualified)))
print('Parse Six - Single Row:')
print('Len(): ' + str(len(single_row)))
print('Parse Six - Total:')
print('Len(): ' + str(len(not_removed) + (int(len(disqualified))) + (int(len(qualified))) + (int(len(to_be_determined))) + (int(len(single_row)))))
print('\n')
not_removed_percentage_str = str(round(float(len(not_removed)/total_for_percentages),3)) + '  '
disqualified_percentage_str = str(round(float(len(disqualified)/total_for_percentages),3)) + '  '
to_be_determined_percentage_str = str(round(float(len(to_be_determined)/total_for_percentages),3)) + '  '
qualfied_percentage_str = str(round(float(len(qualified)/total_for_percentages),3)) + '  '
single_row_percentage_str = str(round(float(len(single_row)/total_for_percentages),3)) + '  '

print("Not Removed = " + not_removed_percentage_str + "  Disqualified = " + disqualified_percentage_str + "  TBD = " + to_be_determined_percentage_str + "  Qualified = " + qualfied_percentage_str + "  Single Rows = " + single_row_percentage_str)
print('\n')
print('\n')        

########################################################################################################################################################################################################################################################################################   
# PARSE 7
# 11/10/2022
# Parse 7 will disqualify parcels that have disqualifying words in all cells past the qualifying date and in the grantee of the first row before the cutoff date.
########################################################################################################################################################################################################################################################################################


cutoff_date = datetime.now() - relativedelta(years=4) # Cutoff date is 4 years ago from today.
cutoff_date_str = cutoff_date.strftime("%m/%d/%Y")
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

new_list_of_parcel_groups = []
for elem in list_of_parcel_groups:
    if elem not in new_list_of_parcel_groups:
        new_list_of_parcel_groups.append(elem)
list_of_parcel_groups = new_list_of_parcel_groups


for i in range(len(list_of_parcel_groups)):
    

    parcel_row_num = len(list_of_parcel_groups[i])
    

    for j in range(0,parcel_row_num):

        disqualified_word_check_06 = False
        disqualified_word_check_07 = False
        disqualified_word_check_08 = False
        string_input_with_date = list_of_parcel_groups[i][j][3] 
        date = datetime.strptime(string_input_with_date, "%m/%d/%Y")

        if (date.date() > cutoff_date.date()):  # If row is past the cutoff 

            for word in disqualifying_words: # Checks for  the presence of disqualifying words in the Grantor and Grantee.
                if (' ' + str(word[0]) + ' ') in (' '+str(list_of_parcel_groups[i][j][6]).upper()+' '):   
                    disqualified_word_check_06 = True
            for word in disqualifying_words:
                if (' ' + str(word[0]) + ' ') in (' '+str(list_of_parcel_groups[i][j][7]).upper()+' '):   
                    disqualified_word_check_07 = True
            
            if(disqualified_word_check_06 and disqualified_word_check_07): 
                if j == parcel_row_num - 1 : # If it is the last row and the last row is past the cutoff date then disqualify it if it passes the disqualifying word check.
                    for item in list_of_parcel_groups[i]:
                        disqualified.append(item)
                    break
                else:  # If it is not the last row then continue.   
                    continue
            else:
                for item in list_of_parcel_groups[i]: # Else if all cells past the cutoff date do not all contain disqualifying words then append parcel to not removed and then break to next parcel.
                    not_removed.append(item)
                break     
        

        if (date.date() <= cutoff_date.date()): 

            for word in disqualifying_words:
                if (' ' + str(word[0]) + ' ') in (' '+str(list_of_parcel_groups[i][j][7]).upper()+' '):   
                    disqualified_word_check_08 = True
            if(disqualified_word_check_08): # If the grantee in the first row that is before the cutoff date contains a disqualifying word then append to disqualified, otherwise append to not removed.
                for item in list_of_parcel_groups[i]:
                    disqualified.append(item)
                break 
            else:
                for item in list_of_parcel_groups[i]:
                    not_removed.append(item)
                break  

total_for_percentages = ( (len(not_removed) + len(disqualified) + (len(qualified))) + (len(to_be_determined)) + (len(single_row))  )
print('Parse Seven - Not Removed:')
print('Len(): ' + str(len(not_removed)))
print('Parse Seven - Disqualified:')
print('Len(): ' + str(int(len(disqualified))))
print('Parse Seven - To Be Determined:')
print('Len(): ' + str(int(len(to_be_determined))))
print('Parse Seven - Qualified:')
print('Len(): ' + str(len(qualified)))
print('Parse Seven - Single Row:')
print('Len(): ' + str(len(single_row)))
print('Parse Seven - Total:')
print('Len(): ' + str(len(not_removed) + (int(len(disqualified))) + (int(len(qualified))) + (int(len(to_be_determined))) + (int(len(single_row)))))
print('\n')
not_removed_percentage_str = str(round(float(len(not_removed)/total_for_percentages),3)) + '  '
disqualified_percentage_str = str(round(float(len(disqualified)/total_for_percentages),3)) + '  '
to_be_determined_percentage_str = str(round(float(len(to_be_determined)/total_for_percentages),3)) + '  '
qualfied_percentage_str = str(round(float(len(qualified)/total_for_percentages),3)) + '  '
single_row_percentage_str = str(round(float(len(single_row)/total_for_percentages),3)) + '  '

print("Not Removed = " + not_removed_percentage_str + "  Disqualified = " + disqualified_percentage_str + "  TBD = " + to_be_determined_percentage_str + "  Qualified = " + qualfied_percentage_str + "  Single Rows = " + single_row_percentage_str)
print('\n')
print('\n')      
          

    

########################################################################################################################################################################################################################################################################################   
# PARSE 8
# 11/10/2022
# Parse 8 will disqualify parcels that have no rows past the cutoff date
########################################################################################################################################################################################################################################################################################

cutoff_date = datetime.now() - relativedelta(years=4) # Cutoff date is 4 years ago from today.
cutoff_date_str = cutoff_date.strftime("%m/%d/%Y")
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

new_list_of_parcel_groups = []
for elem in list_of_parcel_groups:
    if elem not in new_list_of_parcel_groups:
        new_list_of_parcel_groups.append(elem)
list_of_parcel_groups = new_list_of_parcel_groups

for i in range(len(list_of_parcel_groups)):

    parcel_row_num = len(list_of_parcel_groups[i])
    

    for j in range(0,parcel_row_num):

        string_input_with_date = list_of_parcel_groups[i][j][3] 
        date = datetime.strptime(string_input_with_date, "%m/%d/%Y")

        if (date.date() > cutoff_date.date()):  # If row is past the cutoff date then append to not removed and then break to the next parcel.
            for item in list_of_parcel_groups[i]:
                    not_removed.append(item)
            break 
        if(j == parcel_row_num-1): # If it has gotten to the last row and it still has not encountered a row past the cutoff date then append to disqualified.
            for item in list_of_parcel_groups[i]:
                    disqualified.append(item)
            break 
            
total_for_percentages = ( (len(not_removed) + len(disqualified) + (len(qualified))) + (len(to_be_determined)) + (len(single_row))  )
print('Parse Eight - Not Removed:')
print('Len(): ' + str(len(not_removed)))
print('Parse Eight - Disqualified:')
print('Len(): ' + str(int(len(disqualified))))
print('Parse Eight - To Be Determined:')
print('Len(): ' + str(int(len(to_be_determined))))
print('Parse Eight - Qualified:')
print('Len(): ' + str(len(qualified)))
print('Parse Eight - Single Row:')
print('Len(): ' + str(len(single_row)))
print('Parse Eight - Total:')
print('Len(): ' + str(len(not_removed) + (int(len(disqualified))) + (int(len(qualified))) + (int(len(to_be_determined))) + (int(len(single_row)))))
print('\n')
not_removed_percentage_str = str(round(float(len(not_removed)/total_for_percentages),3)) + '  '
disqualified_percentage_str = str(round(float(len(disqualified)/total_for_percentages),3)) + '  '
to_be_determined_percentage_str = str(round(float(len(to_be_determined)/total_for_percentages),3)) + '  '
qualfied_percentage_str = str(round(float(len(qualified)/total_for_percentages),3)) + '  '
single_row_percentage_str = str(round(float(len(single_row)/total_for_percentages),3)) + '  '

print("Not Removed = " + not_removed_percentage_str + "  Disqualified = " + disqualified_percentage_str + "  TBD = " + to_be_determined_percentage_str + "  Qualified = " + qualfied_percentage_str + "  Single Rows = " + single_row_percentage_str)
print('\n')
print('\n')    




########################################################################################################################################################################################################################################################################################   
# PARSE 9
# 11/10/2022
# Parse 9 will disqualify parcels that have no numbers in their address. 12/6/2022 Sometimes a parcel will be flagged as qualified before it reaches this rule where it would be disqualified.
########################################################################################################################################################################################################################################################################################

def contains_number(string):
    return any(char.isdigit() for char in string)

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

new_list_of_parcel_groups = []
for elem in list_of_parcel_groups:
    if elem not in new_list_of_parcel_groups:
        new_list_of_parcel_groups.append(elem)
list_of_parcel_groups = new_list_of_parcel_groups

for i in range(len(list_of_parcel_groups)):

    parcel_row_num = len(list_of_parcel_groups[i])
    

    for j in range(0,parcel_row_num):
        if not(contains_number(list_of_parcel_groups[i][j][2])): # If a row has no numbers in its address then append it to disqualified and then break to next parcel.
            for item in list_of_parcel_groups[i]:
                    disqualified.append(item)
            break 
        else:
            if(j == parcel_row_num - 1):# If by the final row no addresses without numbers have been encountered then append to not removed.
                for item in list_of_parcel_groups[i]:
                    not_removed.append(item)
                break 
            continue
    
total_for_percentages = ( (len(not_removed) + len(disqualified) + (len(qualified))) + (len(to_be_determined)) + (len(single_row))  )
print('Parse Nine - Not Removed:')
print('Len(): ' + str(len(not_removed)))
print('Parse Nine - Disqualified:')
print('Len(): ' + str(int(len(disqualified))))
print('Parse Nine - To Be Determined:')
print('Len(): ' + str(int(len(to_be_determined))))
print('Parse Nine - Qualified:')
print('Len(): ' + str(len(qualified)))
print('Parse Nine - Single Row:')
print('Len(): ' + str(len(single_row)))
print('Parse Nine - Total:')
print('Len(): ' + str(len(not_removed) + (int(len(disqualified))) + (int(len(qualified))) + (int(len(to_be_determined))) + (int(len(single_row)))))
print('\n')
not_removed_percentage_str = str(round(float(len(not_removed)/total_for_percentages),3)) + '  '
disqualified_percentage_str = str(round(float(len(disqualified)/total_for_percentages),3)) + '  '
to_be_determined_percentage_str = str(round(float(len(to_be_determined)/total_for_percentages),3)) + '  '
qualfied_percentage_str = str(round(float(len(qualified)/total_for_percentages),3)) + '  '
single_row_percentage_str = str(round(float(len(single_row)/total_for_percentages),3)) + '  '

print("Not Removed = " + not_removed_percentage_str + "  Disqualified = " + disqualified_percentage_str + "  TBD = " + to_be_determined_percentage_str + "  Qualified = " + qualfied_percentage_str + "  Single Rows = " + single_row_percentage_str)
print('\n')
print('\n')    


########################################################################################################################################################################################################################################################################################   
# PARSE 10
# 11/10/2022
# Parse 10 will disqualify parcels who have 0% homestead in the current and previous year for every row past the cutoff date. There must be no sales in the same year past the cutoff date
########################################################################################################################################################################################################################################################################################

cutoff_date = datetime.now() - relativedelta(years=4) # Cutoff date is 4 years ago from today.
cutoff_date_str = cutoff_date.strftime("%m/%d/%Y")
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

new_list_of_parcel_groups = []
for elem in list_of_parcel_groups:
    if elem not in new_list_of_parcel_groups:
        new_list_of_parcel_groups.append(elem)
list_of_parcel_groups = new_list_of_parcel_groups


for i in range(len(list_of_parcel_groups)):
    parcel_row_num = len(list_of_parcel_groups[i])
    past_cutoff_counter = 0

    for j in range(0,parcel_row_num):
        string_input_with_date0 = list_of_parcel_groups[i][j][3] 
        date0 = datetime.strptime(string_input_with_date0, "%m/%d/%Y")
        if (date0.date() > cutoff_date.date()):
            past_cutoff_counter += 1


    for j in range(0,past_cutoff_counter):

        string_input_with_date1 = list_of_parcel_groups[i][j][3] 
        date1 = datetime.strptime(string_input_with_date1, "%m/%d/%Y")

        if (date1.date() > cutoff_date.date()): 
            PRE_MBT_list_current_year = [] 
            PRE_MBT_list_previous_year = []
            PRE_MBT_check_current_year = False
            PRE_MBT_check_previous_year = False

            if j != 0:
                string_input_with_date2 = list_of_parcel_groups[i][j-1][3] 
                date2 = datetime.strptime(string_input_with_date2, "%m/%d/%Y")
                if(date1.year == date2.year): # If there are two years past the cutoff date within the same year then append the parcel to not removed and then break to next parcel.
                    for item in list_of_parcel_groups[i]:
                        not_removed.append(item)
                    break 
                
            
            for k in range(10,14): 
                if(list_of_parcel_groups[i][j][k] != 'NA'):
                    
                    if k == 10 or k == 11:
                        PRE_MBT_list_current_year.append(convert(list_of_parcel_groups[i][j][k])[3])

                    if k == 12 or k == 13:
                        PRE_MBT_list_previous_year.append(convert(list_of_parcel_groups[i][j][k])[3])
                   
            if len(PRE_MBT_list_current_year) > 0 :
                PRE_MBT_check_current_year = any(element == '0.0000%' for element in PRE_MBT_list_current_year) # If every value in the PRE_MBT_list_0 is == to 0.0000%% then make the PRE_MBT_check_current  == true.
            else: # If there was NA for all cells in current year then append to not removed and then break to next parcel.
                for item in list_of_parcel_groups[i]:
                    not_removed.append(item)
                break 

            if len(PRE_MBT_list_previous_year) > 0 :
                PRE_MBT_check_previous_year  = any(element == '0.0000%' for element in PRE_MBT_list_previous_year) # If every value in the PRE_MBT_list_0 is == to 0.0000%% then make the PRE_MBT_check_current  == true.
            else: # If there was NA for all cells in previous year then append to not removed and then break to next parcel.
                for item in list_of_parcel_groups[i]:
                    not_removed.append(item)
                break 
            
            if(PRE_MBT_check_current_year and PRE_MBT_check_previous_year): # If there is any 0% homestead in both the current and previous year then continue
                if(j != past_cutoff_counter - 1):
                    continue
                if(j == past_cutoff_counter - 1):
                    for item in list_of_parcel_groups[i]:
                        disqualified.append(item)
                    break
            else:
                for item in list_of_parcel_groups[i]:
                    not_removed.append(item)
                break
        else:
            for item in list_of_parcel_groups[i]:
                    not_removed.append(item)
                    
            break 
to_be_determined = not_removed
not_removed = []   
total_for_percentages = ( (len(not_removed) + len(disqualified) + (len(qualified))) + (len(to_be_determined)) + (len(single_row))  )
print('Parse Ten - Not Removed:')
print('Len(): ' + str(len(not_removed)))
print('Parse Ten - Disqualified:')
print('Len(): ' + str(int(len(disqualified))))
print('Parse Ten - To Be Determined:')
print('Len(): ' + str(int(len(to_be_determined))))
print('Parse Ten - Qualified:')
print('Len(): ' + str(len(qualified)))
print('Parse Ten - Single Row:')
print('Len(): ' + str(len(single_row)))
print('Parse Ten - Total:')
print('Len(): ' + str(len(not_removed) + (int(len(disqualified))) + (int(len(qualified))) + (int(len(to_be_determined))) + (int(len(single_row)))))
print('\n')
not_removed_percentage_str = str(round(float(len(not_removed)/total_for_percentages),3)) + '  '
disqualified_percentage_str = str(round(float(len(disqualified)/total_for_percentages),3)) + '  '
to_be_determined_percentage_str = str(round(float(len(to_be_determined)/total_for_percentages),3)) + '  '
qualfied_percentage_str = str(round(float(len(qualified)/total_for_percentages),3)) + '  '
single_row_percentage_str = str(round(float(len(single_row)/total_for_percentages),3)) + '  '

print("Not Removed = " + not_removed_percentage_str + "  Disqualified = " + disqualified_percentage_str + "  TBD = " + to_be_determined_percentage_str + "  Qualified = " + qualfied_percentage_str + "  Single Rows = " + single_row_percentage_str)
print('\n')
print('\n')                   


########################################################################################################################################################################################################################################################################################   
# DATE SORTING
# 11/11/2022
########################################################################################################################################################################################################################################################################################

########################################################################################################################################################################################################################################################################################
last_index_0 = len(qualified)
list_of_parcel_groups=[]
parcel_group = []

for i in range(0,last_index_0): # This groups together records that are in the same parcel/address.
    if i == last_index_0-1:
        parcel_group.append(qualified[i])
        list_of_parcel_groups.append(parcel_group)  
    else:
        if qualified[i][2] != qualified[i-1][2]:
            list_of_parcel_groups.append(parcel_group)
            parcel_group = []
            parcel_group.append(qualified[i])
            continue
        parcel_group.append(qualified[i])

qualified = []
del list_of_parcel_groups[0]



sorted_list_of_parcel_groups = sorted(list_of_parcel_groups, key = lambda x: datetime.strptime(x[0][3], "%m/%d/%Y"))

for i in range(0,len(sorted_list_of_parcel_groups)):   
    for item in sorted_list_of_parcel_groups[i]:
        qualified.append(item)
    qualified.append('\n')
########################################################################################################################################################################################################################################################################################
last_index_0 = len(disqualified)
list_of_parcel_groups=[]
parcel_group = []

for i in range(0,last_index_0): # This groups together records that are in the same parcel/address.
    if i == last_index_0-1:
        parcel_group.append(disqualified[i])
        list_of_parcel_groups.append(parcel_group)  
    else:
        if disqualified[i][2] != disqualified[i-1][2]:
            list_of_parcel_groups.append(parcel_group)
            parcel_group = []
            parcel_group.append(disqualified[i])
            continue
        parcel_group.append(disqualified[i])

disqualified = []
del list_of_parcel_groups[0]



sorted_list_of_parcel_groups = sorted(list_of_parcel_groups, key = lambda x: datetime.strptime(x[0][3], "%m/%d/%Y"))

for i in range(0,len(sorted_list_of_parcel_groups)):   
    for item in sorted_list_of_parcel_groups[i]:
        disqualified.append(item)
    disqualified.append('\n')
########################################################################################################################################################################################################################################################################################
last_index_0 = len(to_be_determined)
list_of_parcel_groups=[]
parcel_group = []

for i in range(0,last_index_0): # This groups together records that are in the same parcel/address.
    if i == last_index_0-1:
        parcel_group.append(to_be_determined[i])
        list_of_parcel_groups.append(parcel_group)  
    else:
        if to_be_determined[i][2] != to_be_determined[i-1][2]:
            list_of_parcel_groups.append(parcel_group)
            parcel_group = []
            parcel_group.append(to_be_determined[i])
            continue
        parcel_group.append(to_be_determined[i])

to_be_determined = []
del list_of_parcel_groups[0]



sorted_list_of_parcel_groups = sorted(list_of_parcel_groups, key = lambda x: datetime.strptime(x[0][3], "%m/%d/%Y"))

for i in range(0,len(sorted_list_of_parcel_groups)):   
    for item in sorted_list_of_parcel_groups[i]:
        to_be_determined.append(item)
    to_be_determined.append('\n')
########################################################################################################################################################################################################################################################################################
last_index_0 = len(single_row)
list_of_parcel_groups=[]
parcel_group = []

for i in range(0,last_index_0): # This groups together records that are in the same parcel/address.
    if i == last_index_0-1:
        parcel_group.append(single_row[i])
        list_of_parcel_groups.append(parcel_group)  
    else:
        if single_row[i][2] != single_row[i-1][2]:
            list_of_parcel_groups.append(parcel_group)
            parcel_group = []
            parcel_group.append(single_row[i])
            continue
        parcel_group.append(single_row[i])

single_row = []
del list_of_parcel_groups[0]



sorted_list_of_parcel_groups = sorted(list_of_parcel_groups, key = lambda x: datetime.strptime(x[0][3], "%m/%d/%Y"))

for i in range(0,len(sorted_list_of_parcel_groups)):   
    for item in sorted_list_of_parcel_groups[i]:
        single_row.append(item)
    single_row.append('\n')
########################################################################################################################################################################################################################################################################################     
# csv. Writing
########################################################################################################################################################################################################################################################################################
with open('qualified.csv', 'w') as f: 
        write = csv.writer(f)
        write.writerow(csv_headers)
        write.writerows(qualified)     

with open('to-be-determined.csv', 'w') as f: 
        write = csv.writer(f)
        write.writerow(csv_headers)
        write.writerows(to_be_determined)  

with open('single-row.csv', 'w') as f:  # 11/16/2022 I commented out single row because since these have already been sorted by the old sorting program they no longer have any single row.
        write = csv.writer(f)
        write.writerow(csv_headers)
        write.writerows(single_row)  

with open('disqualfied.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(csv_headers)
        write.writerows(disqualified)  
########################################################################################################################################################################################################################################################################################

