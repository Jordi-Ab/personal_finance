import pandas as pd
import numpy as np
import datetime
from datetime import date
import os
import pickle
from math import ceil

def retrieveDataFromSheet(gsheet_obj, gsheet_id, sheet_name = 'data'):
    cur_data = gsheet_obj.gsheet_to_df(
        spreadsheet_id = gsheet_id,
        range_name = sheet_name
    )
    return cur_data

def dataFrameToListOfValues(data_frame):
    """
    Converts a Data Frame a two dimensional list of values.
    Supposes the Data Frame contains just one column,
    and indices are not saved on the list.
    """

    # transform the column to list
    cols = np.array(data_frame.columns)
    cols_values = cols.tolist()

    # values of Data Frame to list
    values_arr = data_frame.values
    # append the columns list as the first value of the array
    list_of_rows = np.insert(values_arr, 0, cols_values, 0)

    return list_of_rows.tolist()

def numberToLetters(q):
    q = q - 1
    result = ''
    while q >= 0:
        remain = q % 26
        result = chr(remain+65) + result
        q = q//26 - 1
    return result

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

def crossJoin(series, columns):
  if len(series)<2:
      print ('Series to cross join must contain at least two elements')
  else:
      df1 = pd.DataFrame(series[0], columns = [columns[0]])
      df1['key'] = 1
      i=1
      while i < len(series):        
          df2 = pd.DataFrame(series[i], columns = [columns[i]])
          df2['key'] = 1
          result = pd.merge(df1, df2, on='key')
          df1 = result
          i += 1
      result.drop('key', axis=1, inplace=True)
      return result

def getCategoriesFromGSheet(gsheet_class, gsheet_id):
    categories_titles = gsheet_class.gsheet_to_df(
        spreadsheet_id = gsheet_id,
        range_name = 'biweekly plan!B29:D100'
    )

    separations = categories_titles[
        categories_titles['Variable Expenses'].isnull()
    ].index

    cats = {}
    sub_cats = {}
    for i in range(1,len(separations)):
        ix_1 = separations[i-1]+1
        ix_2 = separations[i]-1
        cat = categories_titles.loc[ix_1:ix_2, 'Variable Expenses']
        cats[i] =  cat.iloc[0]
        sc = {}
        for j, c in enumerate(cat.iloc[1:]):
            sc[j+1] = c
        sub_cats[cat.iloc[0]] = sc
    cat = categories_titles.loc[separations[-1]+1:, 'Variable Expenses']
    cats[len(separations)] =  cat.iloc[0]
    sc = {}
    for j, c in enumerate(cat.iloc[1:]):
        sc[j+1] = c
    sub_cats[cat.iloc[0]] = sc

    return cats, sub_cats

def askYesOrNo(message):
    while (True):
        answer = input(message)
        if (answer[0].lower() == 'y'): return True
        elif (answer[0].lower() == 'n'): return False
        else: print("Invalid Yes or No answer, try again.")

def getYear(message):
    while(True):
        inpt = input(message)
        if (inpt == 'r'): raise Exception('restart')
        elif (inpt == 'q'): raise RuntimeError('Quit')
        elif (not inpt.isdigit() or int(inpt) < 2000): 
            print ("Invalid value for Year, enter a valid year.")
        elif (int(inpt)>date.today().year):
            print ("Can't log spends for future dates, enter a valid year.")
        else:
            return int(inpt)

def getMonth(message):
    while(True):
        inpt = input(message)
        if (inpt == 'r'): raise Exception('restart')
        elif (inpt == 'q'): raise RuntimeError('Quit')
        elif (not inpt.isdigit() or int(inpt)==0 or int(inpt) > 12): 
            print ("Invalid value for month, enter a valid month.")
        else:
            return int(inpt)

def getDay(message):
    while(True):
        inpt = input(message)
        if (inpt == 'r'): raise Exception('restart')
        elif (inpt == 'q'): raise RuntimeError('Quit')
        elif (not inpt.isdigit() or int(inpt)==0 or int(inpt) > 31): 
            print ("Invalid value for day, enter a valid day.")
        else:
            return int(inpt)

def askUserForDate(an_expense):
    flag = askYesOrNo("Was it today? [yes/no]: ")
    print(" ")
    if (not flag): # If expense wasn't made today.
        print("Enter date when the expense was made: ")
        while(True):
            year = getYear("Year: ")
            month = getMonth("Month: ")
            day = getDay("Day: ")

            input_date = date(year, month, day)

            if(input_date>date.today()): print ("Can't log spends for future dates, enter a valid date.")
            else:
                an_expense.setDate(year,month,day)
                break

def printCategories(dictionary, flag):
    """
    Receives a dictionary, and prints its key followed by its value.
    """
    m = 'Sub ' if flag else ''
    message = "Select one "+m+ "Category from the below list:"

    print(message)
    for key, value in dictionary.items() :
        print (str(key)+". ", value)

def askUserForCategoryNumber(dictionary, flag):
    printCategories(dictionary, flag)
    
    m = 'Sub ' if flag else ''
    message = "Enter number of the "+m+ "Category: "
    
    while(True):
        print('')
        selection = input(message)
        if (selection == 'r'): raise Exception('restart')
        elif (selection == 'q'): raise RuntimeError('Quit')
        try: selection = int(selection) # Try converting the input to integer.
        except ValueError: print("That's not a number") # If user didn't entered an integer
        if (selection in dictionary.keys()): return selection # Sucessfull category selection.
        else: print("Error: Selection not in the valid list.") # Inputed a number not in the list of valid categories.
        print(" ")

def selectCategory(main_cats, sub_cats):
    #Main Category
    flag = False # Flag = False means that the message will be prompted for main categories
    cat_key = askUserForCategoryNumber(main_cats, flag)
    cat_name = main_cats[cat_key]
 
    #Sub Category
    flag = True # Flag = True means that the message will be prompted for sub categories
    subcats_dict = sub_cats[cat_name]
    subcat_key = askUserForCategoryNumber(subcats_dict, flag)
    subcat_name = subcats_dict[subcat_key]
    
    return cat_name, subcat_name

def askForAmount(an_expense):
    while(True):
        amount = input("Amount spent: ")
        if (amount == 'r'): raise Exception('restart')
        elif (amount == 'q'): raise RuntimeError('Quit')

        try: 
            amount = float(amount) # Try converting the input to float.
            if (amount < 0): raise ValueError
            break
        except ValueError: # If user didn't entered a number,or entered a negative.
            print("No negative numbers or invalid characters please. Try Again.") 
    an_expense.setAmount(amount)
    
def categoriesTemplate(sub_cats):
    data_frames = []
    cols = ['Category', 'Sub Category']
    for key,value in sub_cats.items():
        vals = list(value.values())
        df = crossJoin([[key],vals], cols)
        data_frames.append(df)
    template = pd.concat(data_frames, ignore_index = True)
    template.sort_values(
        by=['Category', 'Sub Category'], 
        inplace = True
    )
    return template

def load_credit_cards():
    credit_cards = []
    for file in os.listdir('credit_cards'):
        if file.endswith('pkl'):
            with open('credit_cards/'+file, 'rb') as handle:
                cc = pickle.load(handle)
                credit_cards.append(cc)
    return credit_cards

def list_payment_methods(credit_cards_list):
    ccs_str = ""
    for i, cc in enumerate(credit_cards_list):
        ccs_str += '\n'+str(i)+') '+cc.alias_name
    ccs_str += '\n'+str(len(credit_cards_list))+') debit'
    ccs_str += '\n'+str(len(credit_cards_list)+1)+') cash'
    return ccs_str

def get_next_pay_date(payment_date, cut_day):
    next_pay_day = min(ceil(cut_day/15)*15, 31)
    next_pay_date = date(
        day=next_pay_day, 
        month=payment_date.month,
        year=payment_date.year
    )
    if payment_date.day >= cut_day:
        next_pay_date = next_pay_date + pd.DateOffset(months=1)
    return next_pay_date

def askForInstallments(is_credit):
    while(True):
        if is_credit:
            # Change number of installments when credit card
            print('')
            inst = input("How many installments? ")
            try:
                inst = int(inst)
                if inst == 0 or inst == 1:
                    return 1
                if inst > 0 and inst%3==0:
                    print("Cool, {0} MSI \n".format(inst))
                    return inst
                else:
                    print("Sorry, not available")
            except ValueError:
                print("Sorry, not available")
        else:
            # Debit or Cash, default installments are 1
            return 1

def askForPaymentMethod():
    while(True):
        ccs = load_credit_cards()
        ccs_str = list_payment_methods(ccs)
        method_num = input("""
Which payment method was used for this expenses? """+ccs_str+"""

Enter the number of the method: """)
        if (method_num == 'r'): 
            raise Exception('restart')
        elif (method_num == 'q'): 
            raise RuntimeError('Quit')
        else:
            try:
                method_num = int(method_num)
                if method_num < 0 or method_num > len(ccs) + 1:
                    print("Sorry, not available")
                elif method_num < len(ccs):
                    # credit
                    cc = ccs[method_num]
                    print(cc.alias_name+'\n')
                    return cc
                else:
                    # debit or cash:
                    pm = 'debit' if method_num == len(ccs) else 'cash'
                    return pm
            except ValueError:
                print("Sorry, not available")