from flask import Flask
from flask_cors import CORS
from db import init_database
from routes import routes
from shop_controller import initShopController

app = Flask(__name__)
CORS(app)

app.register_blueprint(routes)

mySQL = init_database(app)
initShopController(app, mySQL)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
