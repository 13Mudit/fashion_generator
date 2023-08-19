from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pymongo import MongoClient
from bson.objectid import ObjectId

from openAI_handler import OpenAI
from stability_ai_handler import StableDiffusion


class Query(BaseModel):
    user: str
    query: str


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = MongoClient("13mudit.tech", 27017)

db = client['fashion_generator']

users = db['Users']
on_sale = db['on_sale_products']
trends = db['trends']


text_davinci = OpenAI("api_keys/openai_api")
sdxl = StableDiffusion("api_keys/stable_diff_api")

current_session = None
user_preference = {
    "age": None,
    "season": None,
    "type": None,
    "gender": None,
    "colour": None
}
on_sale_products = []

first_query = False
breaking_attrb = ['age', 'gender', 'type']


@app.post("/query/")
async def generate(query: Query):
    global current_session, on_sale_products

    if query.user != current_session:
        # First query of session
        # grab historic user preference data
        current_session = query.user
        user_info = users.find_one({'id': current_session})

        for attrb in user_preference:
            user_preference[attrb] = user_info[attrb]

        first_query = True


    user_preference_from_prompt = text_davinci.request(query.query)
    # user_preference_from_prompt = {'age': None, 'season': None, 'type': ['casual'], 'gender': None, 'colour': ['red']}
    
    #DEBUG 
    print("OpenAI output:",user_preference_from_prompt)
    
    for attrb in user_preference:
        if attrb in breaking_attrb:
            if user_preference[attrb] != user_preference_from_prompt[attrb] or \
            user_preference_from_prompt[attrb] is not None:
            # User drastically changed search query to the point we can hit trends database again
                first_query = True

        if user_preference_from_prompt[attrb] is not None:
            user_preference[attrb] = user_preference_from_prompt[attrb]     

    users.update_one({
        "id": current_session
        },
        {
        "$set": {
                "age": user_preference['age'],
                "season": user_preference['season'],
                "type": user_preference['type'],
                "gender": user_preference['gender'],
                "colour": user_preference['colour']
            }
        })

    #DEBUG 
    print("User preference:",user_preference)
    
    #get on-sale products
    on_sale_products = []
    get_on_sale_query =  {
    "$and": [
                {"age": {"$regex": f".*{user_preference['age']}.*" if user_preference['age'] is not None else ".*"}},
                {"season": {"$regex": f".*{user_preference['season']}.*" if user_preference['season'] is not None else ".*"}},
                {
                    "$or": [{"type": {"$regex": f".*{t}.*"}} for t in user_preference['type']] if user_preference['type'] else [{"type": {"$regex": ".*"}}]
                },
                {"gender": user_preference['gender'] if user_preference['gender'] else {"$exists": True}},
                {
                    "$or": [{"colour": {"$regex": f".*{c}.*"}} for c in user_preference['colour']] if user_preference['colour'] else [{"colour": {"$regex": ".*"}}]
                }
            ]
    }

    print(get_on_sale_query)

    on_sale_cursor = on_sale.find(get_on_sale_query)

    for on_sale_product in on_sale_cursor:
        on_sale_products.append({
            "image_url": on_sale_product['image_url'],
            "url": on_sale_product['url']
            })

    # print(on_sale_products)


    if first_query:
        # hit the trends database
        get_trend_query = {
        "$and": [
                    {"age": {"$regex": f".*{user_preference['age']}.*" if user_preference['age'] is not None else ".*"}},
                    {"season": {"$regex": f".*{user_preference['season']}.*" if user_preference['season'] is not None else ".*"}},
                    {
                        "$or": [{"type": {"$regex": f".*{t}.*"}} for t in user_preference['type']] if user_preference['type'] else [{"type": {"$regex": ".*"}}]
                    },
                    {"gender": user_preference['gender'] if user_preference['gender'] else {"$exists": True}}
                ]
        }

        trend_cursor = trends.find(get_trend_query).sort('timestamp', -1)


        try:
            latest_trend = next(trend_cursor)
        except StopIteration:
            latest_trend = None


        if latest_trend is None:
            return sdxl.request_no_trend(query.query, query.user, user_preference)
        else:
            return sdxl.request_trend(query.query, query.user, user_preference, latest_trend['image_url'])
    else:
        return sdxl.request(query.query, query.user, user_preference)


    return 'FAIL'


@app.get("/image/", response_class=FileResponse)
async def get_image():
    return f"./out/{current_session}.png"


@app.get("/on_sale/")
async def get_on_sale():
    return on_sale_products