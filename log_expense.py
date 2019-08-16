from datetime import date
import helper_functions as hlp
import pandas as pd
import numpy as np 
import os
from gsheets_connect import GoogleSheets
from expense import Expense

# Global Variables
GSHEET_ID = '14a36tesQZ2AH0aIEdG5Ch2F8iVyrnXCvlxeASLX47N4'
working_directory = os.getcwd()

def pivotData(data_frame, categories_template, how='bimonthly'):

    pivot = pd.pivot_table(
        data_frame, 
        values = 'Amount $',
        columns='Payment '+('Fortnight' if how =='bimonthly' else 'Month'),
        aggfunc='sum',
        index=['Category', 'Sub Category']
    ).reset_index()

    data_with_all_cats = pd.merge(
        categories_template, 
        pivot, 
        on = ['Category', 'Sub Category'], 
        how='left'
    ).fillna(0)

    pivoted_to_write_on_gsheet = pd.DataFrame(
        data_with_all_cats.set_index(
            ['Category', 'Sub Category', 'range']
        ).stack()
    ).reset_index().rename(
        columns={
            'level_3': 'Payment '+('Fortnight' if how =='bimonthly' else 'Month'), 
            0: 'Amount $'
        }
    )

    pivoted_to_write_on_gsheet = pivoted_to_write_on_gsheet.loc[
        :,
        [
            'range', 
            'Category', 
            'Sub Category', 
            'Payment '+('Fortnight' if how =='bimonthly' else 'Month'), 
            'Amount $'
        ]
    ]
    return pivoted_to_write_on_gsheet


def modifyInfo(new_expense, main_cats, sub_cats):
    print("""
    Registering a new expense. At any time:
        * r is for restart, and it restarts 
            the entire expense information logging, 
        * q kills the entire process.
    """)
    try:
        hlp.askUserForDate(new_expense) # Modifies the date of the expense object
        hlp.selectCategory(new_expense, main_cats, sub_cats)
        hlp.askForPaymentMethod(new_expense)
        hlp.askForInstallments(new_expense)
        hlp.askForAmount(new_expense)
    except RuntimeError:
        print('Quit')
        quit()
    except Exception:
        modifyInfo(new_expense)

# ---- Main Program ----------------------------------- 
if __name__ == "__main__":

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
        print(" ")
        if(not flag): break

    # SAVE THE EXPENSES ON "DATABASE"

    #Get Current Data from Google Sheet
    cur_data = hlp.retrieveDataFromSheet(gsheet, GSHEET_ID)
    # Parse data that should be numeric
    cur_data['Amount $'] = cur_data['Amount $'].astype(float)
    cur_data['Expense Month'] = cur_data['Expense Month'].astype(int)
    cur_data['Payment Month'] = cur_data['Payment Month'].astype(int)
    cur_data['Installments'] = cur_data['Installments'].astype(int)

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
    payment_fortnights=[]

    for expense in new_expenses:
        expense_dates.append(expense.getDateAsString())
        payment_dates.append(expense.getPaymentDateAsString())
        expense_months.append(expense.getMonthNum())
        payment_months.append(expense.getPaymentMonthNum())
        payment_fortnights.append(expense.getPaymentFortnight())
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
        "Amount $":amounts,
        "Payment Fortnight":payment_fortnights
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
        "Sub Category",
        "Payment Fortnight"
    ]
    new_entry = pd.DataFrame(data, columns=cols)

    #Concatenate the current data with the new data.
    updated_data = pd.concat(
            [cur_data, new_entry], 
            ignore_index=True
    )
    updated_data.sort_values(by=['Expense Day'], inplace=True)
    updated_data.index = range(len(updated_data))

    # Save the new data
    values_list = hlp.dataFrameToListOfValues(updated_data)
    gsheet.values_to_gsheet(
        spreadsheet_id = GSHEET_ID,
        values_list=values_list, 
        range_name='data'
    )

    # Pivot the data and write on Google Sheets
    cats_template = hlp.categoriesTemplate(sub_cats).sort_index()
    cats_template['range'] = np.arange(1, cats_template.shape[0]+1)

    # Pivot bimonthly (every 15 days)
    bimonthly_pivot = pivotData(updated_data, cats_template, how='bimonthly')
    bimonthly_values = hlp.dataFrameToListOfValues(bimonthly_pivot)
    gsheet.clear_values(
        spreadsheet_id = GSHEET_ID,
        range_name = 'bimonthly data!B2'
    )
    gsheet.values_to_gsheet(
        spreadsheet_id = GSHEET_ID,
        values_list=bimonthly_values, 
        range_name='bimonthly data!B2'
    )

    # Pivot monthly
    monthly_pivot = pivotData(updated_data, cats_template, how='monthly')
    monthly_values = hlp.dataFrameToListOfValues(monthly_pivot)
    gsheet.clear_values(
        spreadsheet_id = GSHEET_ID,
        range_name = 'monthly data!B2'
    )
    gsheet.values_to_gsheet(
        spreadsheet_id = GSHEET_ID,
        values_list=monthly_values, 
        range_name='monthly data!B2'
    )

    print(" ")
    print("Expenses were succesfully uploaded to Google Doc.")