import os
import openai
import json

with open('api_keys/openai_api', 'r') as api_key:
    openai.api_key = api_key.readline()

model = openai.Model.retrieve("text-davinci-003")


prompt_raw = """your task is to parse an input string and turn it into a JSON object with the following information , if the input string does not create the required information then put null in the JSON. The JSON should consist of the following information:
- Age specified in query (field name: age, field type: string, possible values: [kid, teen, teen adult, adult])
- Season specified in the query (field name: season, field type: string, possible values: [summer, winter, all season])
- Type of outfit specified (field name: type, field type: string, possible values: [ethnic, casual, formal, business casual, military, corset])
- Gender specified in query (field name: gender, field type: string, possible values: [male, female, unspecified])

In general, if certain information is not stated, set the respective field to null

This is the query:

%s

The structured JSON representation is:
```json
{"age":"""

def parse_query(query):
    full_prompt = prompt_raw % query

    num_prompt_tokens = int(len(full_prompt) / 3) # estimate the length of the prompt
    max_tokens = 4000 - num_prompt_tokens # calculate the max available tokens for the response

    # call the OpenAI API
    response = openai.Completion.create(
        model='text-davinci-003', # the best GPT-3 model
        prompt=full_prompt,
        temperature=0,
        max_tokens=max_tokens,
        top_p=0.1,
        stop=['```'],
        echo=True # returns the whole prompt including the completion
    )

    # response = openai.ChatCompletion.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     # {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": full_prompt}
    #   ]
    # )

    result_raw = response.choices[0].text
    # result_raw = response.choices[0].message
    # json_str = result_raw['content']
    json_str = result_raw.split('```json')[1].strip() # since we used echo=True, we can split on the json marker

    return json.loads(json_str)



print(parse_query('Show a dark blue suite for me for an important company meeting'))


'''
your task is to parse an input string and turn it into a JSON object with the following information , if the input string does not create the required information then put null in the JSON. The JSON should consist of the following information:
- Age specified in query (field name: age, field type: string, possible values: [kid, teen, teen adult, adult])
- Season specified in the query (field name: season, field type: string, possible values: [summer, winter, all season])
- Type of outfit specified (field name: type, field type: string, possible values: [ethnic, casual, formal, business casual, military, corset])
- Gender specified in query (field name: gender, field type: string, possible values: [male, female, unspecified])

In general, if certain information is not stated, set the respective field to null

This is the query:

Show a dark blue suite for me for an important company meeting

'''
