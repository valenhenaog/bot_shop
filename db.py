from flask_mysqldb import MySQL
import os 
from dotenv import load_dotenv
    
def init_database(app):
    load_dotenv()
    app.config['MYSQL_HOST'] = os.getenv('host')
    app.config['MYSQL_USER'] = os.getenv('user')
    app.config['MYSQL_PASSWORD'] = os.getenv('password')
    app.config['MYSQL_DB'] = os.getenv('db')
    return MySQL(app)