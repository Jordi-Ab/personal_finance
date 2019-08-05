class CreditCard:

    def __init__(self):
        self.bank_name = None
        self.alias_name = None
        self.cut_date = None

    def update_bank_name(self, bank_name):
        self.bank_name = bank_name

    def update_alias_name(self, alias_name):
        self.alias_name = alias_name

    def update_cut_date(self, cut_date):
        self.cut_date = cut_date

    def get_bank_name(self, bank_name):
        if self.bank_name:
            return bank_name
        raise ValueError("No bank registered for this credit card")

    def get_alias_name(self):
        if self.alias_name:
            return self.alias_name
        raise ValueError("No alias registered for this credit card")

    def get_cut_date(self, cut_date):
        if self.cut_date:
            return str(self.cut_date)
        raise ValueError("No cut date registered for this credit card")

    def has_all_info(self):
        if self.bank_name and self.alias_name and self.cut_date:
            return True
        return False


