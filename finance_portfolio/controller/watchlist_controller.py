from flask import Blueprint, request, jsonify
from finance_portfolio.model.watchlist import WatchList
from finance_portfolio.repository.watchlist_repository import WatchlistRepository

watchlist_bp = Blueprint('watchlist_bp', __name__)


@watchlist_bp.route('/put', methods=['POST'])
def add_to_watchlist():
    data = request.get_json()
    ticker = data.get('ticker')

    if not ticker:
        return jsonify({'error': 'Please provide a ticker symbol'}), 400

    try:
        watchlist_entry = WatchlistRepository.add_watchlist(ticker)
        return jsonify({'ticker': watchlist_entry.ticker}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@watchlist_bp.route('/', methods=['GET'])
def get_all_watchlist():
    try:
        watchlists = WatchlistRepository.get_all_watchlists()
        result_list = [{'ticker': entry.ticker} for entry in watchlists]
        return jsonify(result_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@watchlist_bp.route('/<string:ticker>', methods=['DELETE'])
def remove_from_watchlist(ticker):
    try:
        deleted_entry = WatchlistRepository.delete_watchlist(ticker)
        if deleted_entry:
            return jsonify({'ticker': deleted_entry.ticker}), 200
        else:
            return jsonify({'message': 'Watchlist entry not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
