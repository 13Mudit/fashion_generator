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


client = MongoClient("localhost", 27017)

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

first_query = False
breaking_attrb = ['age', 'gender', 'type']


@app.post("/query/")
async def generate(query: Query):
    global current_session

    if query.user != current_session:
        # First query of session
        # grab historic user preference data
        current_session = query.user
        user_info = users.find_one({'id': current_session})

        for attrb in user_preference:
            user_preference[attrb] = user_info[attrb]

        first_query = True


    user_preference_from_prompt = text_davinci.request(query.query)
    
    #DEBUG 
    print("OpenAI output:",user_preference_from_prompt)
    
    for attrb in user_preference:
        if attrb in breaking_attrb:
            if user_preference[attrb] != user_preference_from_prompt[attrb] or \
            user_preference_from_prompt[attrb] is not None:
            # User drastically changed search query to the point we can hit trends database again
                first_query = True

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


    if first_query:
        # hit the trends database
        trend_cursor = trends.find({ "$and": [
                {"age": {"$regex": f".*{user_preference['age']}.*"}},
                {"season": {"$regex": f".*{user_preference['season']}.*"}},
                {
                    "$or": [{"type": {"$regex": f".*{t}.*"}} for t in user_preference['type']]
                },
                {"gender": user_preference['gender']} 
            ]
            }).sort('timestamp', -1)


        try:
            latest_trend = next(trend_cursor)
        except StopIteration:
            latest_trend = None


        if latest_trend is None:
            return sdxl.request_no_trend(query.query, query.user)
        else:
            return sdxl.request_trend(query.query, query.user, latest_trend['image_url'])
    else:
        return sdxl.request(query.query, query.user)


    return 'FAIL'


@app.get("/image/", response_class=FileResponse)
async def get_image():
    return f"./out/{current_session}.png"


#TODO
# @app.get("/on_sale/{number}")