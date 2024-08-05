from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:kailashmorgan@localhost/finfolio'

    # app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from .model.transactions import Transaction
    from .model.holdings import Holding


    ## Register blueprints
    from controller.transactions_controller import transaction_bp
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')

    from .controller.holdings_controller import holding_bp
    app.register_blueprint(holding_bp, url_prefix='/api/holdings')

    return app
