from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)


@app.route('/historical_data', methods=['POST'])
def get_historical_data():
    data= request.get_json()
    ticker = data['ticker']
    start_date = data['start_date']
    end_date = data['end_date']

    if not ticker or not start_date or not end_date:
        return jsonify({'error': 'Please provide ticker, start_date, and end_date'}), 400

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        data = hist.reset_index().to_dict(orient='records')
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)