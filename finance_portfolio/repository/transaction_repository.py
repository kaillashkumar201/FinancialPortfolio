from finance_portfolio import db, create_app
from finance_portfolio.model.transactions import Transaction


class TransactionRepository:

    @staticmethod
    def add_transaction(ticker, trans_type, quantity, price_per_unit):
        new_transaction = Transaction(
            ticker=ticker,
            trans_type=trans_type,
            quantity=quantity,
            price_per_unit=price_per_unit
        )
        db.session.add(new_transaction)
        db.session.commit()
        return new_transaction

    @staticmethod
    def get_transaction_by_id(trans_id):
        return Transaction.query.get(trans_id)

    @staticmethod
    def get_all_transactions():
        return Transaction.query.all()

    @staticmethod
    def update_transaction(trans_id, ticker=None, trans_type=None, quantity=None, price_per_unit=None):
        transaction = Transaction.query.get(trans_id)
        if transaction:
            if ticker is not None:
                transaction.ticker = ticker
            if trans_type is not None:
                transaction.trans_type = trans_type
            if quantity is not None:
                transaction.quantity = quantity
            if price_per_unit is not None:
                transaction.price_per_unit = price_per_unit
            db.session.commit()
        return transaction

    @staticmethod
    def delete_transaction(trans_id):
        transaction = Transaction.query.get(trans_id)
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
        return transaction

    @staticmethod
    def get_transactions_by_ticker(ticker):
        return Transaction.query.filter_by(ticker=ticker).all()

    @staticmethod
    def get_all_cumulative_values():
        return db.session.query(Transaction.cumulative, Transaction.last_modified).all()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        new_transaction = TransactionRepository.add_transaction("APPL", "buy", 2, 100)
        print(new_transaction)
