from bot import Bot

'''bot = Bot()
#bot.get_response("Hi Juanito. I am looking for a soap that has a sweet smell. What would you recommend?")
data = bot.analyze_text("Hi Juanito. Do you have peppermint soap? I am looking to buy seven bars")
data_json = bot.extractJson(data)
print(data_json)'''

'''if data_json["sold"]:
    #suggest_product(data_json["name"], {data_json["amount"]})
    print(f"The client is going to buy {data_json["amount"]} of the {data_json["name"]}s")
else:
    print("The client won't buy any products.")
'''

class ShopModel:
    def __init__(self, mysql):
        self.mysql = mysql
        self.bot = Bot()

    def shop(self, message):
        try:
            response = self.bot.get_response(message['message'])
            return response
        except Exception as e:
            print('ERROR: ', e)

    def update_data(self, id, amount, price):
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute('UPDATE products SET amount = amount - %s WHERE id = %s', (amount, id,))
            cursor.execute('INSERT INTO earnings (product_id, product_amount, total_cost) VALUES (%s, %s, %s)', (id, amount, (price * amount),))
            self.mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print('ERROR: ', e)
        
    def suggest_product(self, message):
        
            try:
                data = self.bot.analyze_text(message['message'])
                data_json = self.bot.extractJson(data)
                name = data_json["name"]
                amount = data_json["amount"]
                if data_json["sold"]:
                    cursor = self.mysql.connection.cursor()
                    cursor.execute('SELECT product_name, price, id, amount FROM products WHERE product_name LIKE %s', (f'%{name}%',) )
                    soap = cursor.fetchone()
                    print(soap)
                    soap_name = soap[0]
                    soap_price = soap[1]
                    soap_id = soap[2]
                    amount_available = soap[3]
                    if amount <= amount_available: 
                        cursor.close()
                        self.update_data(soap_id, amount, soap_price)
                        return 'I would recommend the ' + soap_name + ', which costs ' + str(soap_price) + ' dollars.'
                    else:
                        return f"Unfortunately, we don't have enough {name} soap."
                else: 
                    return "That's alright, maybe another day."
            except Exception as e:
                print('ERROR: ', e)
    
    def view_products(self):
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute('SELECT * FROM products')
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print('ERROR: ', e)

    def view_transactions(self):
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute('SELECT * FROM earnings')
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print('ERROR: ', e)

    def view_total_earnings(self):
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute('SELECT SUM(total_cost) FROM earnings')
            result = cursor.fetchone()
            cursor.close()
            return "TOTAL EARNINGS: " + str(result[0])
        except Exception as e:
            print('ERROR: ', e)