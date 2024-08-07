from datetime import datetime

from finance_portfolio import db


class Holding(db.Model):
    __tablename__ = 'holdings'

    holding_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker = db.Column(db.String(10), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Double, nullable=False)
    last_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"Ticker : {self.ticker}, Quantity: {self.quantity}, Price: {self.price}"


# class Holdings:
#     def __init__(self, holding_id, ticker, quantity, price):
#         self.__holding_id = holding_id
#         self.__ticker = ticker
#         self.__quantity = quantity
#         self.__price = price
#
#     @property
#     def holding_id(self):
#         return self.__holding_id
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
#     def quantity(self):
#         return self.__quantity
#
#     @quantity.setter
#     def quantity(self, quantity):
#         self.__quantity = quantity
#
#     @property
#     def price(self):
#         return self.__price
#
#     @price.setter
#     def price(self, price):
#         self.__price = price
#
#     def __str__(self):
#         return f"Ticker: {self.ticker} \n Quantity: {self.quantity} \n Mean Price: {self.price}"
#
#
# if __name__ == '__main__':
#     h = Holdings(1, 'APPL', 2, 80)
#     print(h)
