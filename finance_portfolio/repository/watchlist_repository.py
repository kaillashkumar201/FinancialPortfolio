from finance_portfolio import db, create_app
from finance_portfolio.model.watchlist import WatchList

class WatchlistRepository():
    @staticmethod
    def add_watchlist(ticker):
        watchlist = WatchList(ticker=ticker)
        db.session.add(watchlist)
        db.session.commit()
        return watchlist

    @staticmethod
    def get_all_watchlists():
        return WatchList.query.all()

    @staticmethod
    def delete_watchlist(ticker):
        watchlist = WatchList.query.get(ticker)
        if watchlist:
            db.session.delete(watchlist)
            db.session.commit()
            return watchlist
        return watchlist