from finance_portfolio import create_app
from flasgger import Swagger


app = create_app()

@app.route('/')
def check():
    return 'Flask is working'


if __name__ == "__main__":
    app.run(debug=True)
