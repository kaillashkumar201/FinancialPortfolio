from flask import Blueprint, request, jsonify

from finance_portfolio.repository.holding_repository import HoldingRepository
from finance_portfolio.repository.transaction_repository import TransactionRepository

transaction_bp = Blueprint('transaction_bp', __name__)


@transaction_bp.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    if not all(k in data for k in ('ticker', 'trans_type', 'quantity', 'price_per_unit')):
        return jsonify({'message': 'Missing data'}), 400

    new_transaction = TransactionRepository.add_transaction(
        ticker=data['ticker'],
        trans_type=data['trans_type'],
        quantity=data['quantity'],
        price_per_unit=data['price_per_unit']
    )

    return jsonify({
        'trans_id': new_transaction.trans_id,
        'ticker': new_transaction.ticker,
        'trans_type': new_transaction.trans_type,
        'quantity': new_transaction.quantity,
        'price_per_unit': new_transaction.price_per_unit
    }), 201


@transaction_bp.route('/transactions/<int:trans_id>', methods=['GET'])
def get_transaction(trans_id):
    transaction = TransactionRepository.get_transaction_by_id(trans_id)
    if transaction:
        return jsonify({
            'trans_id': transaction.trans_id,
            'ticker': transaction.ticker,
            'trans_type': transaction.trans_type,
            'quantity': transaction.quantity,
            'price_per_unit': transaction.price_per_unit
        })
    return jsonify({'message': 'Transaction not found'}), 404


@transaction_bp.route('/transactions', methods=['GET'])
def get_all_transactions():
    transactions = TransactionRepository.get_all_transactions()
    return jsonify([{
        'trans_id': t.trans_id,
        'ticker': t.ticker,
        'trans_type': t.trans_type,
        'quantity': t.quantity,
        'price_per_unit': t.price_per_unit
    } for t in transactions])


@transaction_bp.route('/transactions/<int:trans_id>', methods=['PUT'])
def update_transaction(trans_id):
    data = request.get_json()
    transaction = TransactionRepository.update_transaction(
        trans_id,
        ticker=data.get('ticker'),
        trans_type=data.get('trans_type'),
        quantity=data.get('quantity'),
        price_per_unit=data.get('price_per_unit')
    )
    if transaction:
        return jsonify({
            'trans_id': transaction.trans_id,
            'ticker': transaction.ticker,
            'trans_type': transaction.trans_type,
            'quantity': transaction.quantity,
            'price_per_unit': transaction.price_per_unit
        })
    return jsonify({'message': 'Transaction not found'}), 404


@transaction_bp.route('/transactions/<int:trans_id>', methods=['DELETE'])
def delete_transaction(trans_id):
    transaction = TransactionRepository.delete_transaction(trans_id)
    if transaction:
        return jsonify({'message': 'Transaction deleted'}), 200
    return jsonify({'message': 'Transaction not found'}), 404


@transaction_bp.route('/transactions/add_buy_sell', methods=['POST'])
def add_buy_sell_transaction():
    data = request.get_json()
    if not all(k in data for k in ('ticker', 'trans_type', 'quantity', 'price_per_unit')):
        return jsonify({'message': 'Missing data'}), 400

    trans_type = data['trans_type']
    quantity = data['quantity']
    ticker = data['ticker']
    price_per_unit = data['price_per_unit']

    # Add transaction to the transactions table
    new_transaction = TransactionRepository.add_transaction(
        ticker=ticker,
        trans_type=trans_type,
        quantity=quantity,
        price_per_unit=price_per_unit
    )

    # Check if the ticker exists in the holdings table
    existing_holding = HoldingRepository.get_holding_by_ticker(ticker)

    if trans_type == 'buy':
        if existing_holding:
            # Update existing holding
            new_quantity = existing_holding.quantity + quantity
            total_spent = (existing_holding.quantity * existing_holding.price) + (quantity * price_per_unit)
            new_price = total_spent / new_quantity

            HoldingRepository.update_holding(
                holding_id=existing_holding.holding_id,
                quantity=new_quantity,
                price=new_price
            )
        else:
            # Create new holding
            HoldingRepository.add_holding(
                ticker=ticker,
                quantity=quantity,
                price=price_per_unit
            )
    elif trans_type == 'sell':
        if existing_holding:
            if existing_holding.quantity >= quantity:
                # Update existing holding
                new_quantity = existing_holding.quantity - quantity
                if new_quantity > 0:
                    HoldingRepository.update_holding(
                        holding_id=existing_holding.holding_id,
                        quantity=new_quantity,
                        price=existing_holding.price  # Price remains the same for remaining holdings
                    )
                else:
                    # Delete holding if quantity reaches zero
                    HoldingRepository.delete_holding(existing_holding.holding_id)
            else:
                return jsonify({'message': 'Insufficient quantity to sell'}), 400
        else:
            return jsonify({'message': 'Holding not found'}), 404
    else:
        return jsonify({'message': 'Invalid transaction type'}), 400

    return jsonify({
        'trans_id': new_transaction.trans_id,
        'ticker': new_transaction.ticker,
        'trans_type': new_transaction.trans_type,
        'quantity': new_transaction.quantity,
        'price_per_unit': new_transaction.price_per_unit
    }), 201
