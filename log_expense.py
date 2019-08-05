from datetime import date
import helper_functions as hlp
import pickle
import pandas as pd
from math import ceil
import os

# Valid Categories is a dictionary that maps numbers to Categories.
# Categories is a subdictionary inside valid categories, that maps
# numbers to the subcategory name.
MAIN_CATS = {
    1: "Food", 
    2: "Getting Around", 
    3: "Fun Stuff", 
    4: "Health Care", 
    5: "Personal Stuff", 
    6: "Apartment Spends",
    7: "Removed from Savings"
}

SUB_CATS = {
    "Food":{
        1: "Super Market",
        2: "Restaurants",
        3: "Take-out and bingeing",
        4: "Coffe",
        5: "Other"
    }, 
    "Getting Around":{
        1:"Gas",
        2:"Parking",
        3:"Other"
    },
    "Fun Stuff":{
        1: "Socializing and Bars",
        2: "Hobbies",
        3: "Books",
        4: "Other"
    },
    "Health Care":{
        1: "Medicine",
        2: "Vitamins",
        3: "Supplements",
        4: "Other"
    },
    "Personal Stuff":{
        1: "Clothing",
        2: "Haircut",
        3: "Gifts",
        4: "Personal Care",
        5: "Stuff for me",
        6: "Other"
    },
    "Apartment Spends":{
        1: "Services",
        2: "Stuff for the Apartment",
        3: "Other"
    },
    "Removed from Savings":{
        1: "Trips",
        2: "Other"
    }
}

working_directory = os.getcwd()

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
        selection = input(message)
        if (selection == 'r'): raise Exception('restart')
        elif (selection == 'q'): raise RuntimeError('Quit')
        try: selection = int(selection) # Try converting the input to integer.
        except ValueError: print("That's not a number") # If user didn't entered an integer
        if (selection in dictionary.keys()): return selection # Sucessfull category selection.
        else: print("Error: Selection not in the valid list.") # Inputed a number not in the list of valid categories.
        print(" ")

def selectCategory(an_expense):
    #Main Category
    flag = False # Flag = False means that the message will be prompted for main categories
    cat_key = askUserForCategoryNumber(MAIN_CATS, flag)
    cat_name = MAIN_CATS[cat_key]
    an_expense.setMainCategory(cat_name)
    print(" ")
    print("You chose: " + str(cat_key)+". "+cat_name)
    print(" ")
 
    #Sub Category
    flag = True # Flag = True means that the message will be prompted for sub categories
    subcats_dict = SUB_CATS[cat_name]
    subcat_key = askUserForCategoryNumber(subcats_dict, flag)
    subcat_name = subcats_dict[subcat_key]
    an_expense.setSubCategory(subcat_name)
    print(" ")
    print("You spent on "+cat_name+" -> "+subcat_name)
    print(" ")    

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
    
def categoriesTemplate():
    data_frames = []
    cols = ['Category', 'Sub Category']
    for key,value in SUB_CATS.items():
        vals = list(value.values())
        df = hlp.crossJoin([[key],vals], cols)
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

def askForPaymentMethod(an_expense):
    while(True):
        ccs = load_credit_cards()
        ccs_str = list_payment_methods(ccs)
        method_num = input("""
Which payment method was used? """+ccs_str+"""

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
                    print(cc.alias_name)
                    an_expense.setPaymentMethod('credit')
                    # Payment date becomes the cut date of the credit card
                    cc_cut_date = cc.cut_date
                    expense_date = an_expense.getDate()
                    next_pay_date = get_next_pay_date(expense_date, cc_cut_date)
                    an_expense.setPaymentDate(
                        next_pay_date.year, 
                        next_pay_date.month, 
                        next_pay_date.day
                    )
                    break
                else:
                    # debit or cash
                    print('debit' if method_num == len(ccs) else 'cash')
                    an_expense.setPaymentMethod('debit' if method_num == len(ccs) else 'cash') 
                    # Payment date becomes the date when the expense was made
                    pay_day = an_expense.getDate()
                    an_expense.setPaymentDate(
                        pay_day.year, 
                        pay_day.month, 
                        pay_day.day
                    )
                    break
            except ValueError:
                print("Sorry, not available")

def modifyInfo(new_expense):
    print("""
    Registering a new expense. At any time:
        * r is for restart, and it restarts 
            the entire expense information logging, 
        * q kills the entire process.
    """)
    try:
        askUserForDate(new_expense) # Modifies the date of the expense object
        selectCategory(new_expense)
        askForPaymentMethod(new_expense)
        askForAmount(new_expense)
    except RuntimeError:
        print('Quit')
        quit()
    except Exception:
        modifyInfo(new_expense)

# ---- Main Program ----------------------------------- 
    
from expense import Expense

new_expenses = []

# ASK USER FOR THE INFO ABOUT THE EXPENSE.
while(True):    
    new_expense = Expense()
    modifyInfo(new_expense)

    new_expenses.append(new_expense)
    print("I have just registered this expense:")
    print(new_expense.toString())
    flag = askYesOrNo("Log another expense? ")
    if(not flag): break

# SAVE THE EXPENSES ON "DATABASE"
raise Exception
#Get Current Data from csv
cur_data = pd.read_csv(r'daily_data.txt', sep=' ')

#Create a data frame with the new data per Day.
dates = []
month_nums = []
main_categories = []
sub_categories = []
amounts = []

for expense in new_expenses:
    dates.append(expense.getDateAsString())
    month_nums.append(expense.getMonthNum())
    main_categories.append(expense.getMainCategory())
    sub_categories.append(expense.getSubCategory())
    amounts.append(expense.getAmount())

data = {
    'Date':dates, 
    'MonthNum':month_nums,
    'Category':main_categories, 
    'Sub Category':sub_categories,
    'Amount $':amounts
}
cols = [
    'Date', 
    'MonthNum',
    'Category', 
    'Sub Category', 
    'Amount $'
]
new_entry = pd.DataFrame(data, columns=cols)

#Concatenate the current data with the new data.
daily_data = pd.concat(
        [cur_data, new_entry], 
        ignore_index=True
)
daily_data.sort_values(by=['Date'], inplace=True)
daily_data.index = range(len(daily_data))

# Save the new data
daily_data.to_csv(r'daily_data.txt', index=None, sep=' ')
print(" ")
print("Expenses were succesfully uploaded to Database.")

# SYNC DATA WITH EXCEL
excel = askYesOrNo("Sync with Excel?: ")
if(excel):
    import xlwings as xl
    #Pivot to write it in Excel.
    template = categoriesTemplate()
    daily_data_pivot = pd.pivot_table(
        daily_data, 
        values = 'Amount $',
        columns='Date',
        aggfunc='sum',
        index=['Category', 'Sub Category']
    )
    daily_data_pivot.reset_index(inplace=True)
    daily_data2 = pd.merge(
        template, 
        daily_data_pivot, 
                on=['Category', 'Sub Category'], 
                how='left'
        )
                                  
    daily_data2.fillna(0, inplace=True)
    
    #Group Monthly
    monthly_data = daily_data.drop('Date', 1)
    monthly_data=monthly_data.groupby(
        ['MonthNum','Category', 'Sub Category']
        ).sum()
    monthly_data.reset_index(inplace=True)
    monthly_data_pivot = pd.pivot_table(
        monthly_data, 
                values = 'Amount $',
        columns='MonthNum',
        aggfunc='sum',
        index=['Category', 'Sub Category']
    )
    monthly_data_pivot.reset_index(inplace=True)
    monthly_data2 = pd.merge(
        template, 
        monthly_data_pivot,
        on=['Category', 'Sub Category'], 
        how='left'
        ) 
    monthly_data2.fillna(0, inplace=True)
    
    #Write it in Excel.
    db_path = os.path.join(
        os.path.normpath(os.getcwd() + os.sep + os.pardir), # From current directory, one directory back
        "Personal Finance.xlsm"
        )
    db_wb = xl.Book(db_path)
    
    d_sheet = db_wb.sheets['Daily Data']
    m_sheet = db_wb.sheets['Monthly Data']
    d_sheet.range('B2').value = daily_data2
    m_sheet.range('B2').value = monthly_data2
    
    # Save and close the Workbook.
    #db_wb.save(db_path)
    close = askYesOrNo("Close Excel?: ")
    if(close): db_wb.close()


