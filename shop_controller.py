from flask import request, jsonify, Blueprint
from shop_model import ShopModel

shopController = Blueprint('shopController', __name__)

def initShopController(app, mySQL):
    global ShopModel
    ShopModel = ShopModel(mySQL)
    
    app.register_blueprint(shopController)
    
def shop():
    try:
        message = {
            "message": request.json['message'],
        }
        return jsonify(ShopModel.shop(message))
    except Exception as e:
        return jsonify({'message': 'ERROR: ' + str(e)})
        print('ERROR: ', e)
        
def suggest_product():
    try:
        message = {
            "message": request.json['message'],
        }
        return jsonify(ShopModel.suggest_product(message))
    except Exception as e:
        return jsonify({'message': 'ERROR: ' + str(e)})
        print('ERROR: ', e)
        
def view_products():
    try: 
        return jsonify(ShopModel.view_products())
    except Exception as e:
        return jsonify({'message': 'ERROR: ' + str(e)})
        print('ERROR: ', e)

def view_transactions():
    try: 
        return jsonify(ShopModel.view_transactions())
    except Exception as e:
        return jsonify({'message': 'ERROR: ' + str(e)})
        print('ERROR: ', e)        

def view_total_earnings():
    try: 
        return jsonify(ShopModel.view_total_earnings())
    except Exception as e:
        return jsonify({'message': 'ERROR: ' + str(e)})
        print('ERROR: ', e)        
