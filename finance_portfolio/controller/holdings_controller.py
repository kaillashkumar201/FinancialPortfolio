from flask import Blueprint, request, jsonify

from finance_portfolio.controller.actions_controller import ticker_info
from finance_portfolio.repository.holding_repository import HoldingRepository

holding_bp = Blueprint('holding_bp', __name__)


@holding_bp.route('/', methods=['POST'])
def add_holding():
    data = request.get_json()
    if not all(k in data for k in ('ticker', 'quantity', 'price')):
        return jsonify({'message': 'Missing data'}), 400

    new_holding = HoldingRepository.add_holding(
        ticker=data['ticker'],
        quantity=data['quantity'],
        price=data['price']
    )

    return jsonify({
        'holding_id': new_holding.holding_id,
        'ticker': new_holding.ticker,
        'quantity': new_holding.quantity,
        'price': new_holding.price,
        'last_modified': new_holding.last_modified
    }), 201


@holding_bp.route('/<int:holding_id>', methods=['GET'])
def get_holding(holding_id):
    holding = HoldingRepository.get_holding_by_id(holding_id)
    if holding:
        return jsonify({
            'holding_id': holding.holding_id,
            'ticker': holding.ticker,
            'quantity': holding.quantity,
            'price': holding.price,
            'last_modified': holding.last_modified
        })
    return jsonify({'message': 'Holding not found'}), 404

def get_ticker_helper(ticker):
    holding = HoldingRepository.get_holding_by_ticker(ticker)
    price = float(holding.price)
    current_price = ticker_info(ticker).get('currentPrice')
    net_ticker_profit_loss = (current_price - holding.price) * holding.quantity
    profit_loss_percent = ((current_price - price) / price) * 100
    return {
        "net_ticker_profit_loss": net_ticker_profit_loss,
        "percent_change": profit_loss_percent
    }

@holding_bp.route('/', methods=['GET'])
def get_all_holdings():
    holdings = HoldingRepository.get_all_holdings()

    return jsonify([{
        'holding_id': h.holding_id,
        'ticker': h.ticker,
        'quantity': h.quantity,
        'price': h.price,
        'last_modified': h.last_modified,
        'net_ticker_profit_loss': get_ticker_helper(h.ticker)["net_ticker_profit_loss"],
        'percent_change': get_ticker_helper(h.ticker)["percent_change"]
    } for h in holdings])


@holding_bp.route('/<int:holding_id>', methods=['PUT'])
def update_holding(holding_id):
    data = request.get_json()
    holding = HoldingRepository.update_holding(
        holding_id,
        ticker=data.get('ticker'),
        quantity=data.get('quantity'),
        price=data.get('price')
    )
    if holding:
        return jsonify({
            'holding_id': holding.holding_id,
            'ticker': holding.ticker,
            'quantity': holding.quantity,
            'price': holding.price,
            'last_modified': holding.last_modified
        })
    return jsonify({'message': 'Holding not found'}), 404


@holding_bp.route('/<int:holding_id>', methods=['DELETE'])
def delete_holding(holding_id):
    holding = HoldingRepository.delete_holding(holding_id)
    if holding:
        return jsonify({'message': 'Holding deleted'}), 200
    return jsonify({'message': 'Holding not found'}), 404
