import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import os
import pickle
from math import ceil
import openpyxl
import warnings
from log_expense_gui import LogExpenseForm, AvailableFilesForm

mnths_dict = {
    'Ene':'01','Feb':'02','Mar':'03',
    'Abr':'04','May':'05','Jun':'06',
    'Jul':'07','Ago':'08','Sep':'09',
    'Oct':'10','Nov':'11','Dic':'12'
}

def index_of_first_spend(data_frame):
    for ix, row in data_frame.iterrows():
        val = row.iloc[0]
        if not pd.isnull(val) and parse_date(val)[0]:
            return ix
    return None

def parse_date(date_string):
    try:
        date_string = parse_month(date_string)
        date = datetime.strptime(date_string, '%d/%m/%Y')
        return (True, date)
    except (ValueError, TypeError):
        return (False, None)
    
def parse_amount(num_str):
    if pd.isnull(num_str):
        return np.nan
    try:
        num = float(num_str)
    except ValueError:
        try:
            num = float(num_str.replace(',', ''))
        except ValueError:
            num=0
    return num

def parse_month(date_string):
    for m,v in mnths_dict.items():
        if m in date_string:
            date_string = date_string.replace(m,v)
    return date_string

def try_finding_card_num(data_frame):
    
    for ix, row in data_frame.iterrows():
        val = row.iloc[0]
        if (
            'Adicional' in str(val) or 
            'Titular' in str(val) or 
            'No. de Cuenta' in str(val) or
            'Digital' in str(val)
        ):
            striped_str = ''.join(e for e in val if e.isalnum())
            # Will contain strings that are sequential numbers
            container = []
            # Will contain sequential numbers (not separated by characters)
            a_possible_num=[]
            for i, s in enumerate(striped_str):
                if is_num(s):
                    # keep appending this number
                    a_possible_num.append(s)
                    if i == len(striped_str)-1:
                        # its the end of the string
                        possible_num_str = ''.join(a_possible_num)
                        container.append(possible_num_str)
                else:
                    # non numeric character found in the string
                    possible_num_str = ''.join(a_possible_num)
                    container.append(possible_num_str)
                    a_possible_num=[]
            return [c for c in container if len(c)>=4][0][-4:]
    return '0000'

def load_xlsx(file_path):
    """
    This function is used to read BBVA excel formats, convert them
    to DataFrame, extract the last four digits of the card that generated
    the movements and keep only the movements information. That is,
    only the date, description and amount of the movement.
    ---------------------------
    Returns:
        * data -> DataFrame containing only the relevant information of the movements
        * lst_4_digits -> string having the last 4 digits of the card which generated the movements
    """

    # Data on excel to DataFrame
    warnings.simplefilter("ignore")
    wb_obj = openpyxl.load_workbook(file_path)
    warnings.simplefilter("default")
    sheet = wb_obj.active
    data_dict = {i: c[0] for i, c in enumerate(zip(sheet.values))}
    data = pd.DataFrame.from_dict(data_dict, orient='index')

    # Find the entry of the first entry
    ix_of_first = index_of_first_spend(data)
    # Find the card num which generated the movements
    lst_4_digits = try_finding_card_num(data)
    
    # Select data from the first entry onwards and only the first 3 columns.
    # The first three columns are: `date`, `description` and `amount` respectively.
    data = data.iloc[
        ix_of_first:,:3
    ].copy().reset_index(drop=True)
    
    # Date column as datetime
    data.iloc[:,0] = data.iloc[:,0].apply(
        lambda x: parse_date(x)[1]
    )
    
    # Amount column as float
    data.iloc[:,2] = data.iloc[:,2].apply(
        lambda x: parse_amount(x)
    )

    # Drop nans
    data.dropna(inplace=True)
    
    return data, lst_4_digits

def load_xls(file_path):
    """
    This function is used to read Santander excel formats (xls), convert them
    to DataFrame, extract the last four digits of the card that generated
    the movements and keep only the movements information. That is,
    only the date, description and amount of the movement.
    ---------------------------
    Returns:
        * data -> DataFrame containing only the relevant information of the movements
        * lst_4_digits -> string having the last 4 digits of the card which generated the movements
    """
    
    # Data on excel to DataFrame
    file = pd.read_html(file_path)
    data = file[1]
    
    # Find the entry of the first entry
    ix_of_first = index_of_first_spend(data)
    # Find the card num which generated the movements
    lst_4_digits = try_finding_card_num(data)
    
    # Select data from the first entry onwards and only the [0,2,3] columns.
    # The [0,2,3] columns are: `date`, `description` and `amount` respectively.
    data = data.iloc[
        ix_of_first:,[0,2,3]
    ].copy().reset_index(drop=True)
    
    # Date columns as datetime
    data.iloc[:,0] = data.iloc[:,0].apply(
        lambda x: parse_date(x)[1]
    )
    
    # Amount column as float
    data.iloc[:,2] = data.iloc[:,2].apply(
        lambda x: parse_amount(x)
    )

    # Drop nans
    data.dropna(inplace=True)

    data.rename(columns={2:1,3:2}, inplace=True)
    
    return data, lst_4_digits

def get_available_files():
    """
    List available files.
    That is, files ending with .xlsx or .xls
    """
    data_sources = []
    cwd = os.getcwd()
    files_path = os.path.join(cwd,"input_data")
    dir_content = os.listdir(files_path)
    for file_name in dir_content:
        file_path = os.path.join(files_path, file_name)
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            data_sources.append(file_path)

    return data_sources

def open_file(file_path):
    if file_path.endswith('.xlsx'):
        loaded_data, lst_4_digits = load_xlsx(file_path)
    elif file_path.endswith('.xls'):
        loaded_data, lst_4_digits = load_xls(file_path)
    else:
        raise ValueError("Unable to open file: {0}".format(file_path))
    return loaded_data, lst_4_digits

def load_file(file_to_process):
    data, lst_4_digits = open_file(file_to_process)
    return data, lst_4_digits

def load_data_from_files():
    ccs = load_credit_cards()
    ccs_lst = list_payment_methods(ccs)

    data_frames = []
    for i, file_to_open in enumerate(get_available_files()):
        
        data, card_last_4_digits = load_file(file_to_open)
        data['lst_4_digits'] = card_last_4_digits

        payment_method_type = 'credit' if card_last_4_digits in [
            cc.get_last_four_digits() for cc in ccs
        ] else 'debit'
        credit_card_used = ccs[
            [cc.get_last_four_digits() for cc in ccs].index(card_last_4_digits)
        ] if payment_method_type == 'credit' else None

        if payment_method_type=='debit':
            data.iloc[:,2] = data.iloc[:,2]*-1

        data['pay_method'] = payment_method_type
        data['credit_card_object'] = credit_card_used
        
        data_frames.append(data)
    print('Data Loaded Correctly')
    return pd.concat(data_frames)

def get_missing_data(data, set_of_cur_data):
    positive_data = data[data.iloc[:,2].astype(float)>0].copy()
    positive_data['key'] = (
        positive_data.iloc[:,0].astype(str)+'_'+
        positive_data.iloc[:,1]+'_'+
        round(positive_data.iloc[:,2].astype(float)).astype(int).astype(str)
    )

    s2 = set(positive_data['key'])
    
    missing_data = positive_data[
        ~positive_data['key'].isin(
            set_of_cur_data.intersection(s2)
        )
    ].reset_index(drop=True).drop('key', axis=1).copy()
    return missing_data

def init_dataframes():
    """
    Initializes the DataFrames that will containg the necessary 
    information about the expenses as columns.
    Returns:
        installments_df, expenses_df -> DataFrames with the columns needed
        to log information about the expenses.
    """
    cols_1 = [
        "expense_id",
        "installment_amount",
        "expense_date", 
        "expense_month", 
        "payment_date", 
        "payment_month", 
        "total_installments", 
        "installment_num",
        "payment_method",
        "method_name",
        "category", 
        "sub_category",
        "payment_fortnight",
        "description"
    ]

    cols_2 = [
        "expense_id",
        "expense_date", 
        "description", 
        "amount",
        "installments",
        "ignored",
        "payment_method",
        "method_name"
    ]

    installments_df = pd.DataFrame(index=[0],columns=cols_1)
    expenses_df = pd.DataFrame(index=[0],columns=cols_2)
    return installments_df, expenses_df

def update_expenses_data_frame(cur_df, expense, ignored=False):
    
    lst_ix = 0 if cur_df.shape[0] == 0 else cur_df.index.max()+1
    new_df = pd.DataFrame(index=[lst_ix], columns=cur_df.columns)
    
    new_df.iloc[0].loc["expense_id"] = expense.get_id()
    new_df.iloc[0].loc["expense_date"]=expense.get_date_as_string()
    new_df.iloc[0].loc["description"] = expense.get_description()
    new_df.iloc[0].loc["amount"]=expense.get_amount()
    new_df.iloc[0].loc["installments"]=expense.get_installments()
    new_df.iloc[0].loc["ignored"]=ignored
    new_df.iloc[0].loc["payment_method"]=expense.get_payment_method()
    new_df.iloc[0].loc["method_name"]=expense.get_payment_method_name()
    
    cur_df = pd.concat([cur_df, new_df])
    
    return cur_df

def update_installments_data_frame(cur_df, expenses):
    
    for i, expense in enumerate(expenses):
        lst_ix = 0 if cur_df.shape[0] == 0 else cur_df.index.max()+1
        new_df = pd.DataFrame(index=[lst_ix], columns=cur_df.columns)
        
        new_df.iloc[0].loc["expense_id"] = expense.get_id()
        new_df.iloc[0].loc["installment_amount"]=expense.get_amount()
        new_df.iloc[0].loc["expense_date"] = expense.get_date_as_string()
        new_df.iloc[0].loc["expense_month"]=expense.get_month_num()
        new_df.iloc[0].loc["payment_date"]=expense.get_payment_date_as_string()
        new_df.iloc[0].loc["payment_month"]=expense.get_payment_month_num()
        new_df.iloc[0].loc["total_installments"]=expense.get_installments()
        new_df.iloc[0].loc["installment_num"]=str(i)
        new_df.iloc[0].loc["payment_method"]=expense.get_payment_method()
        new_df.iloc[0].loc["method_name"]=expense.get_payment_method_name()
        new_df.iloc[0].loc["category"]=expense.get_main_category()
        new_df.iloc[0].loc["sub_category"]=expense.get_sub_category()
        new_df.iloc[0].loc["payment_fortnight"]=expense.get_payment_fortnight()
        new_df.iloc[0].loc["description"]=expense.get_description()
        
        cur_df = pd.concat([cur_df, new_df])
    
    return cur_df
            
def update_data(
    an_expense, 
    row, 
    category, 
    sub_category, 
    installments, 
    pay_method_type, 
    credit_card_used
):
    
    date, concept, amount, *rest = row
    
    an_expense.update_data(
        payment_date=date, 
        description=concept, 
        category=category, 
        sub_category=sub_category, 
        amount=amount, 
        payment_method=pay_method_type, 
        n_installments=installments,
        credit_card_used=credit_card_used
    )
    
def pivot_data(data_frame, how='bimonthly'):
    
    date_ix = 'payment_'+('fortnight' if how =='bimonthly' else 'month')
    pivot = pd.pivot_table(
        data_frame, 
        values = 'installment_amount',
        columns='method_name',
        aggfunc='sum',
        index=[date_ix, 'category', 'sub_category']
    ).fillna(0)
    pivot['Total'] = pivot.sum(axis=1)

    pivot2 = pivot.copy()
    pivot2.drop('Total', axis=1, inplace=True)

    to_be_divided = ['Pixies', 'Super']
    for c in pivot2.columns:
        if c in to_be_divided:
            pivot2[c] /= 2

    pivot['MyTotal'] = pivot2.sum(axis=1)

    pivot.reset_index(inplace=True)
    
    return pivot

def list_payment_methods(credit_cards_list):
    payment_methods = []
    for cc in credit_cards_list:
        payment_methods.append(cc.alias_name)
    payment_methods.append('debit')
    payment_methods.append('cash')
    return payment_methods

def load_files_form(available_files):
    file_names = [f.split('/')[-1] for f in available_files]
    dialog = AvailableFilesForm(
        available_files = file_names
        #available_methods = payment_methods
    )
    result = -1
    if dialog.exec_() == AvailableFilesForm.Accepted:
        result = dialog.get_output()
    
    if result == -1:
        raise RuntimeError("Program Terminated")
    
    file_ix = result
    file_to_open = available_files[file_ix]
    
    return file_to_open

def is_num(char):
    """
    Receives a character and returns if the character is a number.
    Ex.
        'a' -> False
        '22' -> True
        '34.5' -> True
        '?' -> Flase
    """
    try:
        float(char)
        return True
    except ValueError:
        return False

def retrieve_data_from_sheet(gsheet_obj, gsheet_id, sheet_name = 'data'):
    cur_data = gsheet_obj.gsheet_to_df(
        spreadsheet_id = gsheet_id,
        range_name = sheet_name
    )
    return cur_data

def data_frame_to_list_of_values(data_frame):
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

def number_to_letters(q):
    q = q - 1
    result = ''
    while q >= 0:
        remain = q % 26
        result = chr(remain+65) + result
        q = q//26 - 1
    return result

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)

def cross_join(series, columns):
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

def get_categories_from_gsheet(gsheet_class, gsheet_id):
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

def ask_yes_or_no(message):
    while (True):
        answer = input(message)
        if (answer[0].lower() == 'y'): return True
        elif (answer[0].lower() == 'n'): return False
        else: print("Invalid Yes or No answer, try again.")

def get_year(message):
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

def get_month(message):
    while(True):
        inpt = input(message)
        if (inpt == 'r'): raise Exception('restart')
        elif (inpt == 'q'): raise RuntimeError('Quit')
        elif (not inpt.isdigit() or int(inpt)==0 or int(inpt) > 12): 
            print ("Invalid value for month, enter a valid month.")
        else:
            return int(inpt)

def get_day(message):
    while(True):
        inpt = input(message)
        if (inpt == 'r'): raise Exception('restart')
        elif (inpt == 'q'): raise RuntimeError('Quit')
        elif (not inpt.isdigit() or int(inpt)==0 or int(inpt) > 31): 
            print ("Invalid value for day, enter a valid day.")
        else:
            return int(inpt)

def ask_user_for_date(an_expense):
    flag = ask_yes_or_no("Was it today? [yes/no]: ")
    print(" ")
    if (not flag): # If expense wasn't made today.
        print("Enter date when the expense was made: ")
        while(True):
            year = get_year("Year: ")
            month = get_month("Month: ")
            day = get_day("Day: ")

            input_date = date(year, month, day)

            if(input_date>date.today()): print ("Can't log spends for future dates, enter a valid date.")
            else:
                an_expense.set_date(year,month,day)
                break

def print_categories(dictionary, flag):
    """
    Receives a dictionary, and prints its key followed by its value.
    """
    m = 'Sub ' if flag else ''
    message = "Select one "+m+ "Category from the below list:"

    print(message)
    for key, value in dictionary.items() :
        print (str(key)+". ", value)

def ask_user_for_category_number(dictionary, flag):
    print_categories(dictionary, flag)
    
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

def select_category(main_cats, sub_cats):
    #Main Category
    flag = False # Flag = False means that the message will be prompted for main categories
    cat_key = ask_user_for_category_number(main_cats, flag)
    cat_name = main_cats[cat_key]
 
    #Sub Category
    flag = True # Flag = True means that the message will be prompted for sub categories
    subcats_dict = sub_cats[cat_name]
    subcat_key = ask_user_for_category_number(subcats_dict, flag)
    subcat_name = subcats_dict[subcat_key]
    
    return cat_name, subcat_name

def ask_for_amount(an_expense):
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
    an_expense.set_amount(amount)
    
def categories_template(sub_cats):
    data_frames = []
    cols = ['Category', 'Sub Category']
    for key,value in sub_cats.items():
        vals = list(value.values())
        df = cross_join([[key],vals], cols)
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
    next_pay_day = min(ceil(cut_day/15)*15, 28)
    next_pay_date = date(
        day=next_pay_day, 
        month=payment_date.month,
        year=payment_date.year
    )
    if payment_date.day >= cut_day:
        next_pay_date = next_pay_date + pd.DateOffset(months=1)

    next_pay_date = last_day_of_month(next_pay_date) if next_pay_date.day == 28 else next_pay_date
    return next_pay_date

def ask_for_installments(is_credit):
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

def ask_for_payment_method():
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