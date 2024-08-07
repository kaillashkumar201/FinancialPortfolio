import csv
import MySQLdb

from finance_portfolio import create_app

def create_connection():
    mydb = MySQLdb.connect(host='localhost',
        user='root',
        passwd='kailashmorgan',
        db='finfolio')
    cursor = mydb.cursor()

    file_path = r"C:\Users\kaill\PycharmProjects\pythonProject1\finance_portfolio\nasdaq_list.csv"

    # Specify the column indices you want to extract
    columns_to_extract = [0, 1, 6, 9]  # Replace with actual indices
    column_names = ['ticker', 'name', 'country', 'sector']  # Replace with actual column names

    # Open the CSV file
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row:
                extracted_values = [row[index] for index in columns_to_extract]

                # Create the SQL query string
                query = "INSERT INTO nasdaq (ticker, name, country, sector) VALUES (%s, %s, %s, %s)"

                # Execute the query
                cursor.execute(query, extracted_values)

    # Commit the transaction
    mydb.commit()
    cursor.close()
    mydb.close()

    #
    # with open(file_path, mode='r', newline='') as file:
    #     csv_reader = csv.reader(file)
    #     for row in csv_reader:
    #         print(row.Symbol)
    #
    #         # cursor.execute('INSERT INTO nasdaq(ticker,name,country,sector )' \
    #         #       'VALUES("AAPL", "", "%s")',
    #         #       row)
    #     mydb.commit()
    #     cursor.close()



if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        create_connection()
