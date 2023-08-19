
import requests
import json
import base64
from PIL import Image
from io import BytesIO

class StableDiffusion:
    def __init__(self, api_key_file_path):
        self.api_key = None
        self.api_host = 'https://api.stability.ai'

        self.get_api_key(api_key_file_path)

        self.engine_id = "stable-diffusion-xl-1024-v1-0"
        # self.engine_id = "stable-diffusion-512-v2-0"



    def get_api_key(self, file_path):
        try:
            with open(file_path, 'r') as api_key_file:
                self.api_key = api_key_file.readline()
        except FileNotFoundError:
            raise Exception(f"Stability API key file doesnt exist at {file_path}")


    def request_trend(self, prompt, user_id, image_url, strength=0.3):

        trend_response = requests.get(image_url)
        if not trend_response:
            raise Exception("Trend image url not reachable")


        trend_img = Image.open(BytesIO(trend_response.content))
        trend_img = trend_img.resize((1024, 1024))
        trend_img.save(f"./out/{user_id}.png")

        print("response with trend")

        success = self.request(prompt, user_id, strength=strength)

        return success


    def request(self, prompt, user_id, strength=0.45):

        response = requests.post(
            f"{self.api_host}/v1/generation/{self.engine_id}/image-to-image",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            files={
                "init_image": open(f"./out/{user_id}.png", "rb")
            },
            data={
                "image_strength": strength,
                "init_image_mode": "IMAGE_STRENGTH",
                "text_prompts[0][text]": prompt,
                "cfg_scale": 35,
                "samples": 1,
                "steps": 30,
                "style_preset": "photographic",
            }
        )


        if response.status_code != 200:
            print(response.reason)
            return "FAIL"

        data = response.json()

        print("response!!")

        image = Image.open(BytesIO(base64.b64decode(data['artifacts'][0]["base64"])))
        image = image.resize((1024, 1024))
        image.save(f"./out/{user_id}.png")

        return data["artifacts"][0]["finishReason"]

    def request_no_trend(self, prompt, user_id):

        response = requests.post(
            f"{self.api_host}/v1/generation/{self.engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": prompt
                    }
                ],
                "cfg_scale": 35,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
                "style_preset": "photographic",
            },
        )

        if response.status_code != 200:
            print(response.reason)
            return "FAIL"

        data = response.json()


        # for i, image in enumerate(data["artifacts"]):
        #     with open(f"./out/{user_id}.png", "wb") as f:
        #         f.write(base64.b64decode(image["base64"]))

        print("response without trend")

        image = Image.open(BytesIO(base64.b64decode(data['artifacts'][0]["base64"])))
        image = image.resize((512, 512))
        image.save(f"./out/{user_id}.png")

        return data["artifacts"][0]["finishReason"]

