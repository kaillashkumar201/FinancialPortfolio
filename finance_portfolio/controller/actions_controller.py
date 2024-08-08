from flask import Blueprint, request, jsonify
import yfinance as yf
from sqlalchemy import desc
from finance_portfolio import db

from finance_portfolio.model import nasdaq
from finance_portfolio.model.holdings import Holding
from finance_portfolio.repository.holding_repository import HoldingRepository
from finance_portfolio.repository.nasdaq_repository import NasdaqRepository
from finance_portfolio.repository.transaction_repository import TransactionRepository

from finance_portfolio.model.transactions import Transaction

action_bp = Blueprint('action_bp', __name__)


def ticker_info(ticker):
    stock = yf.Ticker(ticker)
    print(stock.info)
    try:
        if stock is not None:
            return stock.info
    except KeyError:
        return False
    return False


@action_bp.route('/get_ticker', methods=['GET'])
def validate_ticker():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'Please provide a ticker symbol'}), 400

    stock = ticker_info(ticker)
    if stock is not None:
        return jsonify({'ticker': ticker, 'valid': True, 'info': stock}), 200
    else:
        return jsonify({'ticker': ticker, 'valid': False}), 400


@action_bp.route('/add_buy_sell', methods=['POST'])
def add_buy_sell_transaction():
    global new_cumulative
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

    # Fetch the most recent transaction for cumulative update
    latest_transaction = Transaction.query.order_by(desc(Transaction.last_modified)).offset(1).limit(1).first()
    # print(latest_transaction.trans_id)
    # print(latest_transaction.cumulative)
    if latest_transaction:
        previous_cumulative = latest_transaction.cumulative if latest_transaction.cumulative is not None else 0.0

        # Calculate new cumulative value
        if new_transaction.trans_type == 'buy':
            new_cumulative = previous_cumulative - (new_transaction.quantity * new_transaction.price_per_unit)
        elif new_transaction.trans_type == 'sell':
            new_cumulative = previous_cumulative + (new_transaction.quantity * new_transaction.price_per_unit)
        else:
            new_cumulative = previous_cumulative

        # Update the cumulative value for the new transaction
        new_transaction.cumulative = new_cumulative
        db.session.commit()
    else:
        if new_transaction.trans_type == 'buy':
            new_cumulative = -1 * (new_transaction.quantity * new_transaction.price_per_unit)
        elif new_transaction.trans_type == 'sell':
            new_cumulative = new_transaction.quantity * new_transaction.price_per_unit

        new_transaction.cumulative= new_cumulative
        db.session.commit()

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
        'price_per_unit': new_transaction.price_per_unit,
        'last_modified': new_transaction.last_modified
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


@action_bp.route('/networth', methods=['GET'])
def calculate_networth():
    try:
        # Fetch all holdings
        holdings = HoldingRepository.get_all_holdings()

        if not holdings:
            return jsonify({'networth': 0, 'message': 'No holdings found'}), 200

        total_networth = 0
        for holding in holdings:
            ticker = ticker_info(holding.ticker)
            current_price = ticker.get('currentPrice')  # Extract currentPrice from the dictionary
            if current_price is not None:
                total_networth += holding.quantity * current_price

        return jsonify({'networth': total_networth}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@action_bp.route('/profit_loss', methods=['GET'])
def calculate_profit_loss():
    try:
        # Fetch all holdings
        holdings = HoldingRepository.get_all_holdings()

        if not holdings:
            return jsonify({'profit_loss': 0, 'message': 'No holdings found'}), 200

        total_profit_loss = 0
        for holding in holdings:
            ticker = ticker_info(holding.ticker)
            current_price = ticker.get('currentPrice')  # Extract currentPrice from the dictionary
            if current_price is not None:
                price = float(holding.price)
                profit_loss = (current_price - price) * holding.quantity
                total_profit_loss += profit_loss

        return jsonify({'profit_loss': total_profit_loss}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@action_bp.route('/search_ticker', methods=['GET'])
def search_ticker():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Please provide a search query'}), 400

    try:
        results = NasdaqRepository.search_name(query)
        result_list = [{'name': result.name, 'ticker': result.ticker} for result in results]
        return jsonify(result_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@action_bp.route('/get_news', methods=['GET'])
def get_news():
    try:
        # Fetch all holdings
        holdings = Holding.query.all()

        if not holdings:
            return jsonify({'message': 'No holdings found'}), 404

        all_news = []
        for holding in holdings:
            ticker = holding.ticker
            stock = yf.Ticker(ticker)
            news = stock.get_news()
            news_details = [
                {
                    'ticker': ticker,
                    'title': item.get('title', 'No title'),
                    'publisher': item.get('publisher', 'No publisher'),
                    'link': item.get('link', 'No link')
                } for item in news if 'link' in item
            ]
            all_news.extend(news_details)

        return jsonify(all_news), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
