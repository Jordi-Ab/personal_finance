from datetime import date
import helper_functions as hlp
import pickle
import pandas as pd
from math import ceil
import os
from gsheets_connect import GoogleSheets

GSHEET_ID = '14a36tesQZ2AH0aIEdG5Ch2F8iVyrnXCvlxeASLX47N4'

# Valid Categories is a dictionary that maps numbers to Categories.
# Categories is a subdictionary inside valid categories, that maps
# numbers to the subcategory name.

working_directory = os.getcwd()

def modifyInfo(new_expense, main_cats, sub_cats):
    print("""
    Registering a new expense. At any time:
        * r is for restart, and it restarts 
            the entire expense information logging, 
        * q kills the entire process.
    """)
    #try:
    hlp.askUserForDate(new_expense) # Modifies the date of the expense object
    hlp.selectCategory(new_expense, main_cats, sub_cats)
    hlp.askForPaymentMethod(new_expense)
    hlp.askForInstallments(new_expense)
    hlp.askForAmount(new_expense)
    #except RuntimeError:
    #    print('Quit')
    #    quit()
    #except Exception:
    #    modifyInfo(new_expense)

# ---- Main Program ----------------------------------- 
    
from expense import Expense

new_expenses = []
gsheet = GoogleSheets()
main_cats, sub_cats = hlp.getCategoriesFromGSheet(gsheet, GSHEET_ID)

# ASK USER FOR THE INFO ABOUT THE EXPENSE.
while(True):    
    new_expense = Expense()
    modifyInfo(new_expense, main_cats, sub_cats)
    print(new_expense.getInstallments())
    #if new_expense.getInstallments() > 1:
    # MSI, so divide the Expense in multiple expenses
    sub_expenses = new_expense.divideExpense()
    print([se.getAmount() for se in sub_expenses])
    #else:
    new_expenses = new_expenses + sub_expenses
    print("I have just registered this expense:")
    print(new_expense.toString())
    flag = hlp.askYesOrNo("Log another expense? ")
    if(not flag): break

# SAVE THE EXPENSES ON "DATABASE"

#Get Current Data from csv
cur_data = pd.read_csv(r'daily_data.txt', sep=' ')

#Create a data frame with the new data per Day.
expense_dates = []
payment_dates = []
expense_months = []
payment_months = []
expenses_installments = []
expenses_methods = []
expenses_method_names = []
main_categories = []
sub_categories = []
amounts = []

for expense in new_expenses:
    expense_dates.append(expense.getDateAsString())
    payment_dates.append(expense.getPaymentDateAsString())
    expense_months.append(expense.getMonthNum())
    payment_months.append(expense.getPaymentMonthNum())
    expenses_installments.append(expense.getInstallments())
    expenses_methods.append(expense.getPaymentMethod())
    expenses_method_names.append(expense.getPaymentMethodName())
    main_categories.append(expense.getMainCategory())
    sub_categories.append(expense.getSubCategory())
    amounts.append(expense.getAmount())

data = {
    "Expense Day":expense_dates, 
    "Expense Month":expense_months, 
    "Payment Day":payment_dates, 
    "Payment Month":payment_months,
    "Installments":expenses_installments, 
    "Payment Method":expenses_methods,
    "Method Name":expenses_method_names,
    "Category":main_categories, 
    "Sub Category":sub_categories,
    "Amount $":amounts
}
cols = [
    "Amount $",
    "Expense Day", 
    "Expense Month", 
    "Payment Day", 
    "Payment Month", 
    "Installments", 
    "Payment Method",
    "Method Name",
    "Category", 
    "Sub Category"
]
new_entry = pd.DataFrame(data, columns=cols)

#Concatenate the current data with the new data.
daily_data = pd.concat(
        [cur_data, new_entry], 
        ignore_index=True
)
daily_data.sort_values(by=['Expense Day'], inplace=True)
daily_data.index = range(len(daily_data))

# Save the new data
daily_data.to_csv(r'daily_data.txt', index=None, sep=' ')
print(" ")
print("Expenses were succesfully uploaded to Database.")




"""
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

"""
