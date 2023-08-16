import pandas as pd
from pymongo import MongoClient
import random
from faker import Faker

client = MongoClient("13mudit.tech", 27017)

db = client['fashion_generator']

users = db['Users']
on_sale = db['on_sale_products']
trends = db['trends']


'''
- Age specified in query (field name: age, field type: string, possible values: [kid, teen, teen adult, adult])
- Season specified in the query (field name: season, field type: string, possible values: [summer, winter, all season])
- Type of outfit specified (field name: type, field type: string, possible values: [ethnic, casual, formal, business casual, military, corset])
- Gender specified in query (field name: gender, field type: string, possible values: [male, female, unspecified])
- Colour of outfit specified in query (field name: colour, field type: string)
'''

possible_ages = ['kid', 'teen', 'teen_adult', 'adult']
possible_season = ["summer", "winter", "summer winter"]
possible_type = ["ethnic", "casual", "formal", "business casual", "military", "corset"]
possible_gender = ["male", "female"]
possible_colour = ['white', 'grey green', 'dark green', 'brown blue', 'white blue', 'black gold', 'pastel green', 'red brown', 'green red', 'cream yellow', 'blue pink', 'green', 'dark grey', 'pink', 'red']

fake = Faker()

for i in range(10):
	users.insert_one({
		"id": str(i),
		"name": fake.name(),
		"age": random.choice(possible_ages),
		"season": random.choice(possible_season),
		"type": random.choice(possible_type),
		"gender": random.choice(possible_gender),
		"colour": random.choice(possible_colour)
		})


trend_df = pd.read_csv("outfits.csv")
on_sale_df = pd.read_csv('on_sale.csv')

trends.insert_many(eval(trend_df.to_json(orient='records')))
on_sale.insert_many(eval(on_sale_df.to_json(orient='records')))
