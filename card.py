class Card:
    def __init__(self, product_id, name='Null', set_code='Null',
                 current_price=0, week_price=0, month_price=0,
                 three_month_price=0, is_card=False):
        self.product_id = product_id
        self.name = name
        self.set_code = set_code
        self.current_price = current_price
        self.week_price = week_price
        self.month_price = month_price
        self.three_month_price = three_month_price
        self.is_card = is_card

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_set_code(self, set_code):
        self.set_code = set_code

    def get_set_code(self):
        return self.set_code

    def set_current_price(self, current_price):
        self.current_price = current_price

    def get_current_price(self):
        return self.current_price

    def set_week_price(self, week_price):
        self.week_price = week_price

    def get_week_price(self):
        return self.week_price

    def set_month_price(self, month_price):
        self.month_price = month_price

    def get_month_price(self):
        return self.month_price

    def set_three_month_price(self, three_month_price):
        self.three_month_price = three_month_price

    def get_three_month_price(self):
        return self.three_month_price

    def set_is_card(self):
        self.is_card = True

    def get_is_card(self):
        return self.is_card
