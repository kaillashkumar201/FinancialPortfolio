from finance_portfolio import db
class Nasdaq(db.Model):
    __tablename__ = 'nasdaq'
    ticker = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(500))
    country = db.Column(db.String(100))
    sector = db.Column(db.String(100))
