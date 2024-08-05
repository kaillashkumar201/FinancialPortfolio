from sqlalchemy import create_engine, inspect
from finance_portfolio import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        inspector = inspect(engine)

        # Get a list of table names
        tables = inspector.get_table_names()
        print("Tables in the database:", tables)

        # Get columns for each table
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"Columns in {table}:")
            for column in columns:
                print(f"  - {column['name']} ({column['type']})")
