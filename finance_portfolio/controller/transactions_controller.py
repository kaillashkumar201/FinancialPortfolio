from flask import Blueprint, request, jsonify

from finance_portfolio.repository.holding_repository import HoldingRepository
from finance_portfolio.repository.transaction_repository import TransactionRepository

transaction_bp = Blueprint('transaction_bp', __name__)


@transaction_bp.route('/', methods=['POST'])
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


@transaction_bp.route('/<int:trans_id>', methods=['GET'])
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


@transaction_bp.route('/', methods=['GET'])
def get_all_transactions():
    transactions = TransactionRepository.get_all_transactions()
    return jsonify([{
        'trans_id': t.trans_id,
        'ticker': t.ticker,
        'trans_type': t.trans_type,
        'quantity': t.quantity,
        'price_per_unit': t.price_per_unit
    } for t in transactions])


@transaction_bp.route('/<int:trans_id>', methods=['PUT'])
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


@transaction_bp.route('/<int:trans_id>', methods=['DELETE'])
def delete_transaction(trans_id):
    transaction = TransactionRepository.delete_transaction(trans_id)
    if transaction:
        return jsonify({'message': 'Transaction deleted'}), 200
    return jsonify({'message': 'Transaction not found'}), 404
