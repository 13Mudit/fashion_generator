from pymongo import MongoClient

client = MongoClient("localhost", 27017)

db = client['fashion_generator']

users = db['Users']
on_sale = db['on_sale_products']
trends = db['trends']

