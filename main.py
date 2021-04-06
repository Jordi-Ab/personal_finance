"""
This is the main script for logging Expenses.

Pipeline goes as follows:
    1) Load the xlsx or xls data contained in "input_data" folder.
    2) Load the data that has been logged until now, which is contained in the Google Sheet ('data' and 'expenses' tabs).
    3) Eliminate data that has already been logged (dropping duplicates between current data and new data).
    4) Log expenses one by one prompting the user to enter the information about the expense through a Dialog Box.
    5) Concatenate new data with current data.
    6) Rewrite the data tabs on GSheet with the new updated data.
"""
import pandas as pd
from gsheets_connect import GoogleSheets, Connect
import helper_functions as hlp
from expense import Expense
from credit_card_object import CreditCard
from log_expense_gui import LogExpenseForm, AvailableFilesForm
from settings import GSHEET_ID

# object to retrive and write data
GSHEET = GoogleSheets()

def log_expenses(missing_data):
    """
    Function that iterates expenses one by one, creates an Expense object, updates its information
    and saves each Expense on installments dataframe and expenses dataframe.
    -----------------
    Receives:
        - missing_data -> DataFrame containing the expenses to be logged.
    Returns:
        - installments_df -> DataFrame containing information about the expense divided in installments.
        - expenses_df -> DataFrame containing information about the expense before being divided in installments.
    """
    print('logging expenses...')
    new_expenses = []
    # Reads the categories from the Google Sheet. 
    main_cats, sub_cats = hlp.get_categories_from_gsheet(GSHEET, GSHEET_ID)
    
    # Initialize the resulting dataframes
    installments_df, expenses_df = hlp.init_dataframes()

    # Iterates expenses one by one 
    for ix, row in missing_data.iterrows():
        
        payment_method_type = row['pay_method']
        cc_used = row['credit_card_object']
        
        # Create Expense new object
        an_expense = Expense(this_id=(int(LAST_ID)+1)+ix)
        # Dialog box to enter information about the expense
        dialog = LogExpenseForm(
            categories = main_cats, 
            subcategories = sub_cats, 
            expense_date_str = str(row.iloc[0].date()),
            expense_description = row.iloc[1],
            expense_amount = str(row.iloc[2]),
            payment_type=payment_method_type,
            card_last_4_digits = cc_used.get_last_four_digits()
        )

        # Response of the log expense Dialog box
        log_expense = None
        if dialog.exec_() == LogExpenseForm.Accepted:
            # Get the user response
            log_expense, cat, sub_cat, installments = dialog.get_output()

        if log_expense is None:
            # Response was Close window or Cancel
            break
        elif log_expense == 1:
            # Response to log this expense? was Yes
            
            # Update the Expense object to hold the necessary information
            hlp.update_data(
                an_expense=an_expense, 
                row=row, 
                category=cat, 
                sub_category=sub_cat, 
                installments=installments,
                pay_method_type=payment_method_type, 
                credit_card_used=cc_used
            )
            # Dive the Expense in installments
            sub_expenses = an_expense.divide_expense()
            # Save the divided expense on the installments_df DataFrame
            installments_df = hlp.update_installments_data_frame(
                installments_df, 
                expenses = sub_expenses
            )
            # Save the Expense on the expenses_df DataFrame
            expenses_df = hlp.update_expenses_data_frame(
                cur_df = expenses_df, 
                expense = an_expense, 
                ignored=False
            )
        else:
            # Response to log this expense? was No

            # Update the Expense object to hold the necessary information
            hlp.update_data(
                an_expense=an_expense, 
                row=row, 
                category=cat, 
                sub_category=sub_cat, 
                installments=1,
                pay_method_type=payment_method_type, 
                credit_card_used=cc_used
            )
            # Save the Expense on the expenses_df DataFrame
            expenses_df = hlp.update_expenses_data_frame(
                cur_df = expenses_df, 
                expense = an_expense, 
                ignored=True
            )

    return installments_df, expenses_df

def update_data_on_gsheet(cur_inst_data, cur_exp_data, new_installments_data, new_expenses_data): 
    """
    Rewrites the data on Google Sheet with the current data plus the new data.
    New Data is the data that was logged on this iteration and Current Data is the data that
    was logged on past iterations and was contained on the Google Sheet.
    """
    
    # Concatenate current installments data with new installments data
    updated_inst_data = pd.concat(
        [cur_inst_data, new_installments_data], 
        ignore_index=True
    ) if not cur_inst_data.empty else new_installments_data
    updated_inst_data.sort_values(by=['expense_date'], inplace=True)
    updated_inst_data.index = range(len(updated_inst_data))
    updated_inst_data.drop_duplicates(
        subset=['expense_date', 'description', 'installment_amount'],
        inplace=True
    )

    inst_values_list = hlp.data_frame_to_list_of_values(updated_inst_data.dropna())

    # Rewrite installments data
    GSHEET.clear_values(
        spreadsheet_id = GSHEET_ID,
        range_name = 'data'
    )
    GSHEET.values_to_gsheet(
        spreadsheet_id = GSHEET_ID,
        values_list=inst_values_list, 
        range_name='data'
    )
    
    # Concatenate current expenses data with new expenses data
    updated_exp_data = pd.concat(
        [cur_exp_data, new_expenses_data], 
        ignore_index=True 
    )if not cur_exp_data.empty else new_expenses_data
    updated_exp_data.sort_values(by=['expense_id'], inplace=True)
    updated_exp_data.index = range(len(updated_exp_data))
    updated_exp_data.drop_duplicates(
        subset=['expense_date', 'description', 'amount'],
        inplace=True
    )

    exp_values_list = hlp.data_frame_to_list_of_values(updated_exp_data.dropna())

    # Rewrite expenses data
    GSHEET.clear_values(
        spreadsheet_id = GSHEET_ID,
        range_name = 'expenses'
    )
    GSHEET.values_to_gsheet(
        spreadsheet_id = GSHEET_ID,
        values_list=exp_values_list, 
        range_name='expenses'
    )
    
    # Pivot bimonthly (every 15 days)
    bimonthly_pivot = hlp.pivot_data(updated_inst_data, how='bimonthly')
    bimonthly_values = hlp.data_frame_to_list_of_values(bimonthly_pivot)
    GSHEET.clear_values(
        spreadsheet_id = GSHEET_ID,
        range_name = 'bimonthly pivot'
    )
    GSHEET.values_to_gsheet(
        spreadsheet_id = GSHEET_ID,
        values_list=bimonthly_values, 
        range_name='bimonthly pivot!A1'
    )

    # Pivot monthly
    monthly_pivot = hlp.pivot_data(updated_inst_data, how='monthly')
    monthly_values = hlp.data_frame_to_list_of_values(monthly_pivot)
    GSHEET.clear_values(
        spreadsheet_id = GSHEET_ID,
        range_name = 'monthly pivot'
    )
    GSHEET.values_to_gsheet(
        spreadsheet_id = GSHEET_ID,
        values_list=monthly_values, 
        range_name='monthly pivot!A1'
    )
    
    return updated_inst_data, updated_exp_data, bimonthly_pivot, monthly_pivot

def load_current_data_from_gsheet():
    """
    Retrieves the data that was logged on past iterations and is contained on the GoogleSheet
    under 'data' and 'expenses' tabs.
    """
    global LAST_ID
    try:
        
        # Retrives current installments data (under 'data' tab)
        cur_inst_data = hlp.retrieve_data_from_sheet(
            GSHEET, 
            GSHEET_ID, 
            sheet_name = 'data'
        )

        cur_inst_data['expense_id'] = cur_inst_data['expense_id'].astype(int)
        cur_inst_data['installment_amount'] = cur_inst_data['installment_amount'].str.replace(',', '').astype(float)
        cur_inst_data['expense_month'] = cur_inst_data['expense_month'].astype(int)
        cur_inst_data['payment_month'] = cur_inst_data['payment_month'].astype(int)
        cur_inst_data['installment_num'] = cur_inst_data['installment_num'].astype(str)
        cur_inst_data['total_installments'] = cur_inst_data['total_installments'].astype(int)

        # Retrives current expenses data (under 'expenses' tab)
        cur_exp_data = hlp.retrieve_data_from_sheet(
            GSHEET, 
            GSHEET_ID, 
            sheet_name = 'expenses'
        )

        cur_exp_data['expense_id'] = cur_exp_data['expense_id'].astype(int)
        cur_exp_data['amount'] = cur_exp_data['amount'].str.replace(',', '').astype(float)
        cur_exp_data['ignored'] = cur_exp_data['ignored'].astype(str)
        cur_exp_data['installments'] = cur_exp_data['installments'].astype(int)

        cur_exp_data['key'] = (
            cur_exp_data['expense_date'] +'_'+
            cur_exp_data['description']+'_'+
            round(cur_exp_data['amount'].astype(float)).astype(int).astype(str)
        )

        s1 = set(cur_exp_data['key'])
        cur_exp_data.drop('key',axis=1, inplace=True)

    except (IndexError, ValueError):
        # GSheet is empty, there is no data to read from
        cur_inst_data = pd.DataFrame()
        cur_exp_data = pd.DataFrame()
        s1 = set()

    LAST_ID =  0 if cur_exp_data.empty else cur_exp_data['expense_id'].max()
    return cur_inst_data, cur_exp_data, s1

def main():
    """
    Run whole Pipeline
    """
    
    # 1) Load the xlsx or xls data contained in "input_data" folder.
    data_sets_info = hlp.load_data_from_files()

    # 2) Load the data that has been logged until now, which is contained in the Google Sheet ('data' and 'expenses' tabs).
    cur_inst_data, cur_exp_data, s1 = load_current_data_from_gsheet()
    # 3) Eliminate data that has already been logged (dropping duplicates between current data and new data).
    data_to_upload = hlp.get_missing_data(data=data_sets_info, set_of_cur_data=s1)

    # 4) Log expenses one by one prompting the user to enter the information about the expense through a Dialog Box.
    installments_df, expenses_df = log_expenses(missing_data=data_to_upload)

    # 5) Concatenate new data with current data and 
    # 6) Rewrite the data tabs on GSheet with the new updated data.
    updated_inst_data, updated_exp_data, bimonthly_pivot, monthly_pivot = update_data_on_gsheet(
        cur_inst_data = cur_inst_data, 
        cur_exp_data = cur_exp_data, 
        new_installments_data = installments_df, 
        new_expenses_data = expenses_df
    )

    # Return the resulting DataFrames to further analyze them in case this function is run on a Jupyter notebook.
    return updated_inst_data, updated_exp_data

if __name__ == "__main__":
    # This script was run on a terminal
    main()