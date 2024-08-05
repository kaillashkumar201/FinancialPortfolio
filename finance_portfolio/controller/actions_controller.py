from flask import Blueprint, request, jsonify
import yfinance as yf

from finance_portfolio.repository.holding_repository import HoldingRepository
from finance_portfolio.repository.transaction_repository import TransactionRepository

action_bp = Blueprint('action_bp', __name__)


@action_bp.route('/add_buy_sell', methods=['POST'])
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


@action_bp.route('/historical_data', methods=['GET'])
def get_historical_data():
    ticker = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not ticker or not start_date or not end_date:
        return jsonify({'error': 'Please provide ticker, start_date, and end_date'}), 400

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        data = hist.reset_index().to_dict(orient='records')
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500