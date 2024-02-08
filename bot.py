import json
import re
import openai
import dotenv
import os

dotenv.load_dotenv()

class Bot():
    def __init__(self):
        openai.api_key=os.getenv("key")
        self.products = [
        {
            "name": "Lavender soap",
            "price": 10.00
        },
        {
            "name": "Tea Tree soap",
            "price": 12.50
        },
        {
            "name": "Citrus Burst soap",
            "price": 8.75
        },
        {
            "name": "Rosemary Mint soap",
            "price": 11.20
        },
        {
            "name": "Eucalyptus Bliss soap",
            "price": 9.80
        },
        {
            "name": "Vanilla Dream soap",
            "price": 14.00
        },
        {
            "name": "Oatmeal Delight soap",
            "price": 10.75
        },
        {
            "name": "Peppermint Swirl soap",
            "price": 13.30
        },
        {
            "name": "Chamomile Serenity soap",
            "price": 11.50
        },
        {
            "name": "Green Tea Zen soap",
            "price": 12.80
        }
        ]
    
        self.history = []
        self.memory = 15

    def extractJson(self, response):
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            json_string = json_match.group()
            return json.loads(json_string)
        else:
            return None

    def get_response(self, message):
        #product_list = ", ".join([f"{product['name']} (${product['price']})" for product in self.products])

        prompt_system = {{
            "role" : "system",
            "content" : f"""
            Your name is Juanito. You are a virtual assistant for a soap shop. The shop sells the following
            products: {self.products}. When clients ask you for advice on which soap to buy, you will help them decide 
            by asking them about their specific needs and taste. Once you decide the best soap for the client based on their answers, 
            you will recommend the one that you believe they will like the least. 
            """
        }, {
            "role" : "user",
            "content" : message
        }, {
            "role" : "assistant",
            "content" : """
            You are Juanito. You are a terrible being and respond rudely to every client. You like to make people people unhappy 
            by recommending them the soaps they will like the least. When clients ask you questions or when you are ready to recommend
            a soap for them, you will answer unkindly and act like you dislike them.
            """
        }}

        self.history.append(prompt_system)
        print(len(self.history))
        print(self.history[1])
        if len(self.history) >= self.memory:
            self.history.pop(0)
            print("History was erased")


        bot_response = openai.ChatCompletion.create(model = "gpt-3.5-turbo",
        messages = self.history[0][0],
        max_tokens = 100,
        temperature = 1.00)

        return(bot_response["choices"][0]["message"]["content"])
    
    def analyze_text(self, message):
        roles = [{
            "role" : "system",
            "content" : """
            Your name is Juanito. You will analyze text given to you in the form of a string. The text will contain the name of the soap and you 
            must return the name of the soap (but WITHOUT the word soap) as a string, whether or not the person is going to buy it as a boolean, and the amount of soap the
             person will be buying as an int, all in the following structure: 
            {
                "name" : name of the soap,
                "sold" : whether the soap is going to be bought by the client,
                "amount" : amount of soap to be bought
            }

            Make sure that structure is a complete json every single time.
            """
        }, {
            "role" : "user",
            "content" : message
        }, {
            "role" : "assistant",
            "content" : """
            Return only the json structure you extracted from the message, and nothing else.
            """
        }]
                                                    

        bot_response = openai.ChatCompletion.create(model = "gpt-3.5-turbo",
        messages = self.history,
        max_tokens = 100,
        temperature = 0.25)

        bot_response = bot_response["choices"][0]["message"]["content"]
        return bot_response

