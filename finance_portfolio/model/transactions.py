from finance_portfolio import db


class Transaction(db.Model):
    __tablename__ = 'transactions'

    trans_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker = db.Column(db.String(10), nullable=False)
    trans_type = db.Column(db.Enum('buy', 'sell'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Numeric(15, 2), nullable=False)

# class Transactions:
#     def __init__(self, trans_id, ticker, trans_type, quantity, price_per_unit):
#         self.__trans_id = trans_id
#         self.__ticker = ticker
#         self.__trans_type = trans_type
#         self.__quantity = quantity
#         self.__price_per_unit = price_per_unit
#
#     @property
#     def trans_id(self):
#         return self.__trans_id
#
#     @property
#     def ticker(self):
#         return self.__ticker
#
#     @ticker.setter
#     def ticker(self, ticker):
#         self.__ticker = ticker
#
#     @property
#     def trans_type(self):
#         return self.__trans_type
#
#     @trans_type.setter
#     def trans_type(self, trans_type):
#         self.__trans_type = trans_type
#
#     @property
#     def quantity(self):
#         return self.__quantity
#
#     @quantity.setter
#     def quantity(self, quantity):
#         self.__quantity = quantity
#
#     @property
#     def price_per_unit(self):
#         return self.__price_per_unit
#
#     @price_per_unit.setter
#     def price_per_unit(self, price_per_unit):
#         self.__price_per_unit = price_per_unit
#
#     def __str__(self):
#         return f'Ticker: {self.__ticker} \n Type: {self.__trans_type} \n Quantity: {self.__quantity} \n Price: {self.__price_per_unit}'
#
#
# if __name__ == '__main__':
#     t = Transactions(1, 'APPL', 'buy', 2, 80)
#     print(t)
