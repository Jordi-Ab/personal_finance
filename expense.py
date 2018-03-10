from datetime import date

class Expense:

	def __init__(self):
		self._date = date.today() # Initializes with todays date.
		self._main_category = ''
		self._sub_category = ''
		self._amount = 0

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

	def setDate(self, year, month, day):
		self._date = date(year, month, day)

	def setMainCategory(self, main_cat_name):
		self._main_category = main_cat_name

	def setSubCategory(self, sub_cat_name):
		self._sub_category = sub_cat_name

	def setAmount(self, amount):
		self._amount = amount

	def toString(self):
		string = """Expense:
	Date: """ +self.getDateAsString()+ """
	Category: """+self._main_category+"""
	Sub Category: """+self._sub_category+"""
	Amount: $"""+str(self._amount)
		return string




