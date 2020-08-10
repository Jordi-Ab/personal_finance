import sys
from PyQt5 import QtWidgets, QtCore, QtGui

app = QtWidgets.QApplication(sys.argv)

class AvailableFilesForm(QtWidgets.QDialog):  
    def __init__(self, available_files=[], available_methods=[]):
        super(AvailableFilesForm, self).__init__()
        
        self.createFormGroupBox(available_files)        

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(self.formGroupBox)        
        mainLayout.addWidget(buttonBox)     

        self.setWindowTitle("Available Files")    

    def createFormGroupBox(self, available_files=[]):
        layout = QtWidgets.QFormLayout()
        
        self.label = QtWidgets.QLabel()
        self.label.setGeometry(QtCore.QRect(10, 40, 221, 41))
        self.label.setObjectName("label")
        self.label.setText("I have this files available, \nwhich one do you want to process?")
        layout.addWidget(self.label)
        
        self.availableFiles = QtWidgets.QComboBox()
        self.availableFiles.setGeometry(QtCore.QRect(250, 40, 181, 26))
        self.availableFiles.setObjectName("availableFiles")
        for file in available_files:
            self.availableFiles.addItem(file)
        
        layout.addWidget(self.availableFiles)
        
        
        #self.methodUsed = QtWidgets.QLabel()
        #self.methodUsed.setGeometry(QtCore.QRect(10, 140, 221, 41))
        #self.methodUsed.setObjectName("methodUsed")
        #self.methodUsed.setText("Select the payment method used \nfor those expenses.")   
        #layout.addWidget(self.methodUsed)
        
        #self.payMethodOptions = QtWidgets.QComboBox()
        #self.payMethodOptions.setGeometry(QtCore.QRect(250, 150, 191, 26))
        #self.payMethodOptions.setObjectName("payMethodOptions") 
        #for method in available_methods:
        #    self.payMethodOptions.addItem(method)
            
        #layout.addWidget(self.payMethodOptions)

        self.formGroupBox = QtWidgets.QGroupBox("File to process")        
        self.formGroupBox.setLayout(layout)

    def accept(self):
        self._output = self.availableFiles.currentIndex()
        super(AvailableFilesForm, self).accept()

    def get_output(self):
        return self._output

class Ui_LogExpense(object):
    def setupUi(self, LogExpense, payment_type):
        LogExpense.setObjectName("LogExpense")
        LogExpense.resize(521, 385)
        
        self.titleLabel = QtWidgets.QLabel(LogExpense)
        self.titleLabel.setGeometry(QtCore.QRect(20, 20, 231, 31))
        self.titleLabel.setObjectName("titleLabel")
        
        self.insertDescription = QtWidgets.QLabel(LogExpense)
        self.insertDescription.setGeometry(QtCore.QRect(120, 60, 301, 21))
        self.insertDescription.setText("")
        self.insertDescription.setObjectName("insertDescription")
        
        self.logExpenseLabel = QtWidgets.QLabel(LogExpense)
        self.logExpenseLabel.setGeometry(QtCore.QRect(20, 160, 121, 31))
        self.logExpenseLabel.setObjectName("logExpenseLabel")
        
        self.logExpenseComboBox = QtWidgets.QComboBox(LogExpense)
        self.logExpenseComboBox.setGeometry(QtCore.QRect(190, 160, 104, 26))
        self.logExpenseComboBox.setObjectName("logExpenseComboBox")
        self.logExpenseComboBox.addItem("No")
        self.logExpenseComboBox.addItem("Yes")
        
        self.CategoryLabel = QtWidgets.QLabel(LogExpense)
        self.CategoryLabel.setGeometry(QtCore.QRect(20, 210, 110, 21))
        self.CategoryLabel.setObjectName("CategoryLabel")
        
        self.subCatLabel = QtWidgets.QLabel(LogExpense)
        self.subCatLabel.setGeometry(QtCore.QRect(20, 250, 141, 21))
        self.subCatLabel.setObjectName("subCatLabel")
        
        self.catComboBox = QtWidgets.QComboBox(LogExpense)
        self.catComboBox.setGeometry(QtCore.QRect(190, 210, 104, 26))
        self.catComboBox.setObjectName("catComboBox")
        
        self.subCatComboBox = QtWidgets.QComboBox(LogExpense)
        self.subCatComboBox.setGeometry(QtCore.QRect(190, 250, 104, 26))
        self.subCatComboBox.setObjectName("subCatComboBox")
        
        if payment_type == 'credit':
            self.installmentsLabel = QtWidgets.QLabel(LogExpense)
            self.installmentsLabel.setGeometry(QtCore.QRect(20, 300, 151, 21))
            self.installmentsLabel.setObjectName("installmentsLabel")

            self.instComboBox = QtWidgets.QComboBox(LogExpense)
            self.instComboBox.setGeometry(QtCore.QRect(190, 300, 104, 26))
            self.instComboBox.setObjectName("instComboBox")
        
        self.insertAmount = QtWidgets.QLabel(LogExpense)
<<<<<<< HEAD
        self.insertAmount.setGeometry(QtCore.QRect(120, 80, 261, 21))
=======
        self.insertAmount.setGeometry(QtCore.QRect(120, 90, 261, 21))
>>>>>>> dd95193e623f4e0ce88e87904e398e735cc2121e
        self.insertAmount.setText("")
        self.insertAmount.setObjectName("insertAmount")
        
        self.insertDate = QtWidgets.QLabel(LogExpense)
<<<<<<< HEAD
        self.insertDate.setGeometry(QtCore.QRect(120, 100, 261, 21))
        self.insertDate.setText("")
        self.insertDate.setObjectName("insertDate")

        self.insertCardNum = QtWidgets.QLabel(LogExpense)
        self.insertCardNum.setGeometry(QtCore.QRect(120, 120, 261, 21))
        self.insertCardNum.setText("")
        self.insertCardNum.setObjectName("insertCardNum")
=======
        self.insertDate.setGeometry(QtCore.QRect(120, 120, 261, 21))
        self.insertDate.setText("")
        self.insertDate.setObjectName("insertDate")
>>>>>>> dd95193e623f4e0ce88e87904e398e735cc2121e
        
        self.descriptionLabel = QtWidgets.QLabel(LogExpense)
        self.descriptionLabel.setGeometry(QtCore.QRect(40, 60, 81, 20))
        self.descriptionLabel.setObjectName("descriptionLabel")
        
        self.amountLabel = QtWidgets.QLabel(LogExpense)
<<<<<<< HEAD
        self.amountLabel.setGeometry(QtCore.QRect(40, 80, 81, 20))
        self.amountLabel.setObjectName("amountLabel")
        
        self.dateLabel = QtWidgets.QLabel(LogExpense)
        self.dateLabel.setGeometry(QtCore.QRect(40, 100, 81, 20))
        self.dateLabel.setObjectName("dateLabel")

        self.cardNumLabel = QtWidgets.QLabel(LogExpense)
        self.cardNumLabel.setGeometry(QtCore.QRect(40, 120, 81, 20))
        self.cardNumLabel.setObjectName("cardNumLabel")
=======
        self.amountLabel.setGeometry(QtCore.QRect(40, 90, 81, 20))
        self.amountLabel.setObjectName("amountLabel")
        
        self.dateLabel = QtWidgets.QLabel(LogExpense)
        self.dateLabel.setGeometry(QtCore.QRect(40, 120, 81, 20))
        self.dateLabel.setObjectName("dateLabel")
>>>>>>> dd95193e623f4e0ce88e87904e398e735cc2121e
        
        self.buttonBox = QtWidgets.QDialogButtonBox(LogExpense)
        self.buttonBox.setGeometry(QtCore.QRect(340, 340, 164, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(LogExpense)
        QtCore.QMetaObject.connectSlotsByName(LogExpense)

    def retranslateUi(self, LogExpense):
        _translate = QtCore.QCoreApplication.translate
        LogExpense.setWindowTitle(_translate("LogExpense", "Dialog"))
        self.titleLabel.setText(_translate("LogExpense", "Currently processing this expense:"))
        self.logExpenseLabel.setText(_translate("LogExpense", "Log this expense?"))
        self.descriptionLabel.setText(_translate("LogExpense", "Description:"))
        self.amountLabel.setText(_translate("LogExpense", "Amount:"))
        self.dateLabel.setText(_translate("LogExpense", "Date:"))
<<<<<<< HEAD
        self.cardNumLabel.setText(_translate("LogExpense", "Card Num:"))
=======
>>>>>>> dd95193e623f4e0ce88e87904e398e735cc2121e

class LogExpenseForm(QtWidgets.QDialog):
    def __init__(
        self, 
        categories, 
        subcategories, 
        expense_date_str,
        expense_description,
        expense_amount,
<<<<<<< HEAD
        payment_type,
        card_last_4_digits
=======
        payment_type
>>>>>>> dd95193e623f4e0ce88e87904e398e735cc2121e
    ):
        super().__init__()
        
        self.categories = categories
        self.subcategories = subcategories
        self.payment_type = payment_type
        
        self.ui = Ui_LogExpense()
        self.ui.setupUi(self, payment_type)

        self.ui.insertDescription.setText(expense_description)
        self.ui.insertAmount.setText(expense_amount)
        self.ui.insertDate.setText(expense_date_str)
<<<<<<< HEAD
        self.ui.insertCardNum.setText(card_last_4_digits)
=======
>>>>>>> dd95193e623f4e0ce88e87904e398e735cc2121e
        
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        
        self.ui.logExpenseComboBox.currentIndexChanged.connect(self.log_expense_state_changed)
        
        self.show()
        
    def accept(self):
        self._output = (
            self.ui.logExpenseComboBox.currentIndex(),
            self.ui.catComboBox.currentText(),
            self.ui.subCatComboBox.currentText(),
            self.ui.instComboBox.currentText() if self.payment_type == 'credit' else "1"
        )
        super().accept()

    def get_output(self):
        return self._output
    
    def log_expense_state_changed(self):
        
        if self.ui.logExpenseComboBox.currentIndex() == 1:
            self.show_categories()
            self.show_subcategories()
            if self.payment_type == 'credit':
                self.show_installments()
        else:
            self.ui.CategoryLabel.clear()
            self.ui.subCatLabel.clear()
            self.ui.installmentsLabel.clear()
            self.ui.catComboBox.clear()
            self.ui.subCatComboBox.clear()
            self.ui.instComboBox.clear()
    
    def show_installments(self):
        
        if self.ui.logExpenseComboBox.currentIndex() == 1:
            self.ui.installmentsLabel.setText('How many Installments? ')
            
            self.ui.instComboBox.clear()
            self.ui.instComboBox.addItem('1')
            self.ui.instComboBox.addItem('3')
            self.ui.instComboBox.addItem('6')
            self.ui.instComboBox.addItem('9')
            self.ui.instComboBox.addItem('12')
            self.ui.instComboBox.addItem('18')
    
    def show_subcategories(self):
        
        if self.ui.logExpenseComboBox.currentIndex() == 1:
            self.ui.subCatLabel.setText('Select SubCategory: ') 
            
            chosen_cat = self.ui.catComboBox.currentText()

            self.ui.subCatComboBox.clear()
            for s_cat in self.subcategories[chosen_cat].values():
                self.ui.subCatComboBox.addItem(s_cat)
        
    def show_categories(self):
        
        if self.ui.logExpenseComboBox.currentIndex() == 1:
            self.ui.CategoryLabel.setText('Select Category: ')
            
            self.ui.catComboBox.clear()
            for cat in self.categories.values():
                self.ui.catComboBox.addItem(cat)

        self.ui.catComboBox.currentIndexChanged.connect(self.show_subcategories)
        
        