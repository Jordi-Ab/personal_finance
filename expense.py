from datetime import date

class Expense:

	def __init__(self):
		self._date = date.today() # Initializes with todays date.
		self._main_category = ''
		self._sub_category = ''
		self._amount = 0
        self._payment_method = ''
        self._payment_date = date.today() # Date when the expense should be paid (next month for credit cards)

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

    def getPaymentDate(self):
        return self._payment_date

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

    def setPaymentDate(self, year, month, day):
        self._payment_date = date(year, month, day)

	def toString(self):
		string = """Expense:
	Date: """ +self.getDateAsString()+ """
	Category: """+self._main_category+"""
	Sub Category: """+self._sub_category+"""
    Payment Method: """+self._payment_method+"""
	Amount: $"""+str(self._amount)
		return string




