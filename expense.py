from datetime import date
from pandas import DateOffset

class Expense:

    def __init__(self):
        self._date = date.today() # Initializes with todays date.
        self._main_category = ''
        self._sub_category = ''
        self._amount = 0
        self._payment_method = ''
        self._payment_method_name = ''
        self._payment_date = date.today() # Date when the expense should be paid (next month for credit cards)
        self._n_installments = 1 # Number of payments (in the case of MSI)

    def getDate(self):
        return self._date

    def getDateAsString(self):
        return self._date.strftime('%Y-%m-%d')

    def getMonthNum(self):
        return int(self._date.strftime('%Y%m'))

    def getMainCategory(self):
        return self._main_category

    def getSubCategory(self):
        return self._sub_category

    def getAmount(self):
        return self._amount

    def getPaymentMethod(self):
        return self._payment_method

    def getPaymentMethodName(self):
        return self._payment_method_name

    def getPaymentDate(self):
        return self._payment_date

    def getPaymentDateAsString(self):
        return self._payment_date.strftime('%Y-%m-%d')

    def getPaymentMonthNum(self):
        return int(self._payment_date.strftime('%Y%m'))

    def getPaymentFortnight(self):
        return self._payment_date.replace(
            day=15 if self._payment_date.day <= 15 else 30
        ).strftime('%Y-%m-%d')

    def getInstallments(self):
        return self._n_installments

    def setDate(self, year, month, day):
        self._date = date(year, month, day)

    def setMainCategory(self, main_cat_name):
        self._main_category = main_cat_name

    def setSubCategory(self, sub_cat_name):
        self._sub_category = sub_cat_name

    def setAmount(self, amount):
        self._amount = amount

    def setPaymentMethod(self, method):
        if method not in ['cash', 'debit', 'credit']:
            raise ValueError('Only "Cash", "Debit" or "Credit" methods are supported.')
        self._payment_method = method

    def setPaymentMethodName(self, method_name):
        self._payment_method_name = method_name

    def setPaymentDate(self, year, month, day):
        self._payment_date = date(year, month, day)

    def setInstallments(self, n_installments):
        self._n_installments = n_installments

    def divideExpense(self):
        """
        Returns a list with n Expenses instances, where n = number of installments.
        """
        installments = self.getInstallments()
        expenses = []
        for i in range(installments):
            new_exp = Expense()
            new_exp.setDate(
                year=self.getDate().year, 
                month=self.getDate().month, 
                day=self.getDate().day
            )
            new_exp.setMainCategory(self.getMainCategory())
            new_exp.setSubCategory(self.getSubCategory())
            new_exp.setPaymentMethod(self.getPaymentMethod())
            new_exp.setPaymentMethodName(self.getPaymentMethodName())
            new_exp.setAmount(self.getAmount()/installments)
            payment_date = self.getPaymentDate() + DateOffset(months=i)
            new_exp.setPaymentDate(
                year=payment_date.year,
                month=payment_date.month,
                day=payment_date.day
            )
            expenses.append(new_exp)

        return expenses

    def toString(self):
        string = """Expense:
    Date: """ +self.getDateAsString()+ """
    Category: """+self._main_category+"""
    Sub Category: """+self._sub_category+"""
    Payment Method: """+self._payment_method+"""
    Installments: """+str(self._n_installments)+"""
    Amount: $"""+str(self._amount)
        return string




