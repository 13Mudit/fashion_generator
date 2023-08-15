import os
import requests
import json
import base64

api_host = 'https://api.stability.ai'

get_balance = f"{api_host}/v1/user/balance"
get_engines = f"{api_host}/v1/engines/list"

# engine_id = "stable-diffusion-xl-1024-v1-0"
engine_id = "stable-diffusion-512-v2-0"

api_key = None

with open('api_keys/stable_diff_api', 'r') as api_keyfile:
    api_key = api_keyfile.readline();

if api_key is None:
    raise Exception("Missing Stability API key.")


# response = requests.get(get_balance, headers={
#     "Authorization": f"Bearer {api_key}"
# })


# Text-to-Image
# response = requests.post(
#     f"{api_host}/v1/generation/{engine_id}/text-to-image",
#     headers={
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "Authorization": f"Bearer {api_key}"
#     },
#     json={
#         "text_prompts": [
#             {
#                 "text": "A dark blue formal suit for interviews and important meetings"
#             }
#         ],
#         "cfg_scale": 15,
#         "height": 1024,
#         "width": 1024,
#         "samples": 1,
#         "steps": 30,
#         "style_preset": "photographic",
#     },
# )


#Image-to-Image
response = requests.post(
    f"{api_host}/v1/generation/{engine_id}/image-to-image",
    headers={
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    files={
        "init_image": open("./out/v1_txt2img_0_0014.png", "rb")
    },
    data={
        "image_strength": 0.45,
        "init_image_mode": "IMAGE_STRENGTH",
        "text_prompts[0][text]": "Make the coat brown",
        "cfg_scale": 35,
        "samples": 1,
        "steps": 10,
        "style_preset": "photographic",
    }
)


if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

# Do something with the payload...
data = response.json()

# print(data)

for i, image in enumerate(data["artifacts"]):
    with open(f"./out/v1_img_{i}.png", "wb") as f:
        f.write(base64.b64decode(image["base64"]))

print(data["artifacts"][0]["finishReason"])
# print(json.dumps(data["artifacts"][0]["finishReason"], indent=2))