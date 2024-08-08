from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # insert your mysql connection details here
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:kailashmorgan@localhost/finfolio'

    db.init_app(app)
    migrate.init_app(app, db)

    from .model.transactions import Transaction
    from .model.holdings import Holding

    # Register blueprints
    from controller.transactions_controller import transaction_bp
    app.register_blueprint(transaction_bp, url_prefix='/transactions')

    from .controller.holdings_controller import holding_bp
    app.register_blueprint(holding_bp, url_prefix='/holdings')

    from .controller.actions_controller import action_bp
    app.register_blueprint(action_bp, url_prefix='/actions')

    from .controller.watchlist_controller import watchlist_bp
    app.register_blueprint(watchlist_bp, url_prefix='/watchlist')

    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Access API'
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    return app
