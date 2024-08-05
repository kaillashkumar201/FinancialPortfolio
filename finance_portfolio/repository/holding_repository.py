from finance_portfolio import db, create_app
from finance_portfolio.model.holdings import Holding


class HoldingRepository:

    @staticmethod
    def add_holding(ticker, quantity, price):
        new_holding = Holding(
            ticker=ticker,
            quantity=quantity,
            price=price
        )
        db.session.add(new_holding)
        db.session.commit()
        return new_holding

    @staticmethod
    def get_holding_by_id(holding_id):
        return Holding.query.get(holding_id)

    @staticmethod
    def get_all_holdings():
        return Holding.query.all()

    @staticmethod
    def update_holding(holding_id, ticker=None, quantity=None, price=None):
        holding = Holding.query.get(holding_id)
        if holding:
            if ticker is not None:
                holding.ticker = ticker
            if quantity is not None:
                holding.quantity = quantity
            if price is not None:
                holding.price = price
            db.session.commit()
        return holding

    @staticmethod
    def delete_holding(holding_id):
        holding = Holding.query.get(holding_id)
        if holding:
            db.session.delete(holding)
            db.session.commit()
        return holding

    @staticmethod
    def get_holding_by_ticker(ticker):
        return Holding.query.filter_by(ticker=ticker).first()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        transaction = HoldingRepository.get_holding_by_ticker("APPL")
        print(transaction)