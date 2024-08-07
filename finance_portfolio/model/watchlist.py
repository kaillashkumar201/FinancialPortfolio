from finance_portfolio import db
class WatchList(db.Model):
    __tablename__ = 'watchlist'
    ticker = db.Column(db.String(50), primary_key=True)