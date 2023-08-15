
import requests
import json
import base64

class StableDiffusion:
    def __init__(self, api_key_file_path):
        self.api_key = None
        self.api_host = 'https://api.stability.ai'

        self.get_api_key(api_key_file_path)

        # self.engine_id = "stable-diffusion-xl-1024-v1-0"
        self.engine_id = "stable-diffusion-512-v2-0"



    def get_api_key(self, file_path):
        try:
            with open(file_path, 'r') as api_key_file:
                self.api_key = api_key_file.readline()
        except FileNotFoundError:
            raise Exception(f"Stability API key file doesnt exist at {file_path}")


    def request(self, image, prompt, strength=0.45):

        response = requests.post(
            f"{self.api_host}/v1/generation/{self.engine_id}/image-to-image",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            files={
                "init_image": open(image, "rb")
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
            return "FAIL"

        data = response.json()

        for i, image in enumerate(data["artifacts"]):
            with open(f"./out/v1_img_{i}.png", "wb") as f:
                f.write(base64.b64decode(image["base64"]))

        return data["artifacts"][0]["finishReason"]

