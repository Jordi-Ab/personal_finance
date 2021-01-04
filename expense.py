from datetime import date
from pandas import DateOffset
from helper_functions import last_day_of_month, get_next_pay_date

class Expense:

    def __init__(self, this_id):
        self._id = this_id
        self._date = date.today() # Initializes with todays date.
        self._main_category = ''
        self._sub_category = ''
        self._description = ''
        self._amount = 0
        self._payment_method = ''
        self._payment_method_name = ''
        self._payment_date = date.today() # Date when the expense should be paid (next month for credit cards)
        self._n_installments = 1 # Number of payments (in the case of MSI)

    def get_id(self):
        return self._id

    def get_description(self):
        return self._description

    def get_date(self):
        return self._date

    def get_date_as_string(self):
        return self._date.strftime('%Y-%m-%d')

    def get_month_num(self):
        return int(self._date.strftime('%Y%m'))

    def get_main_category(self):
        return self._main_category

    def get_sub_category(self):
        return self._sub_category

    def get_amount(self):
        return self._amount

    def get_payment_method(self):
        return self._payment_method

    def get_payment_method_name(self):
        return self._payment_method_name

    def get_paymentdDate(self):
        return self._payment_date

    def get_payment_date_as_string(self):
        return self._payment_date.strftime('%Y-%m-%d')

    def get_payment_month_num(self):
        return int(self._payment_date.strftime('%Y%m'))

    def get_payment_fortnight(self):
        if self._payment_method == 'credit':
            # When credit, payment date is already programed to be fortnightly
            payment_fortnight = self._payment_date
        else:
            if self._payment_date.day < 15:
                payment_fortnight = last_day_of_month(
                    self._payment_date - DateOffset(months=1)
                )
            else:
                payment_fortnight = last_day_of_month(
                    self._payment_date
                ).replace(day=15)

        return payment_fortnight.strftime('%Y-%m-%d')

    def get_installments(self):
        return self._n_installments

    def set_description(self, description):
        self._description = description

    def set_date(self, year, month, day):
        self._date = date(year, month, day)

    def set_main_category(self, main_cat_name):
        self._main_category = main_cat_name

    def set_sub_category(self, sub_cat_name):
        self._sub_category = sub_cat_name

    def set_amount(self, amount):
        self._amount = amount

    def set_payment_method(self, method):
        if method not in ['cash', 'debit', 'credit']:
            raise ValueError('Only "Cash", "Debit" or "Credit" methods are supported.')
        self._payment_method = method

    def set_payment_method_name(self, method_name):
        self._payment_method_name = method_name

    def set_payment_date(self, year, month, day):
        self._payment_date = date(year, month, day)

    def set_installments(self, n_installments):
        self._n_installments = int(n_installments)

    def update_data(
        self, 
        payment_date, 
        description, 
        category, 
        sub_category, 
        amount, 
        payment_method, 
        n_installments,
        credit_card_used=None
    ):
        self.set_date(payment_date.year, payment_date.month, payment_date.day)
        self.set_description(description)
        self.set_main_category(category)
        self.set_sub_category(sub_category)
        self.set_amount(amount)
        self.set_installments(n_installments)
        if credit_card_used:
            self.set_payment_method('credit')
            self.set_payment_method_name(credit_card_used.alias_name)
            # Payment date becomes the cut date of the credit card
            cc_cut_date = credit_card_used.cut_date
            expense_date = self.get_date()
            pay_date = get_next_pay_date(expense_date, cc_cut_date)
            self.setPaymentDate(pay_date.year, pay_date.month, pay_date.day)
        else:
            # debit or cash
            self.setPaymentMethod(payment_method)
            self.setPaymentMethodName(payment_method)
            # Payment date becomes the date when the expense was made
            pay_date = self.getDate()
            self.setPaymentDate(pay_date.year, pay_date.month, pay_date.day)

    def divide_expense(self):
        """
        Returns a list with n Expenses instances, where n = number of installments.
        """
        installments = self.get_installments()
        expenses = []
        for i in range(installments):
            new_exp = Expense(this_id = self.getId())
            new_exp.set_date(
                year=self.get_date().year, 
                month=self.get_date().month, 
                day=self.get_date().day
            )
            new_exp.set_main_category(self.get_main_category())
            new_exp.set_sub_category(self.get_sub_category())
            new_exp.set_payment_method(self.get_payment_nethod())
            new_exp.set_payment_method_name(self.get_payment_method_name())
            new_exp.set_amount(self.get_amount()/installments)
            payment_date = self.get_payment_date() + DateOffset(months=i)
            new_exp.set_payment_date(
                year=payment_date.year,
                month=payment_date.month,
                day=payment_date.day
            )
            new_exp.set_description(
                self.get_description()+(' {0} of {1} MSI'.format(i+1, installments) if installments>1 else '')
            )
            expenses.append(new_exp)

        return expenses

    def to_string(self):
        string = """Expense:
    Id:             """+str(self.get_id())+"""
    Date:           """ +self.get_date_as_string()+ """
    Category:       """+self._main_category+"""
    Sub Category:   """+self._sub_category+"""
    Payment Method: """+self._payment_method+"""
    Installments:   """+str(self._n_installments)+"""
    Amount:        $"""+str(self._amount)
        return string




