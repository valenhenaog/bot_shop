from flask import Blueprint
from shop_controller import shop, suggest_product, view_products, view_transactions, view_total_earnings

routes = Blueprint('routes', __name__)

routes.route('/shop', methods=['GET'])(shop)
routes.route('/suggestProduct', methods=['GET'])(suggest_product)
routes.route('/viewProducts', methods=['GET'])(view_products)
routes.route('/viewTransactions', methods=['GET'])(view_transactions)
routes.route('/viewTotalEarnings', methods=['GET'])(view_total_earnings)
