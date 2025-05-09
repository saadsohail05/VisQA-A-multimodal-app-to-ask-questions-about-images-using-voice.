import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_ENDPOINT = "https://ai.api.nvidia.com/v1/vlm/microsoft/kosmos-2"
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY')


def process_image(image_path, question):
    try:
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()

        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Accept": "application/json"
        }

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": f'{question} <img src="data:image/png;base64,{image_b64}" />'
                }
            ],
            "max_tokens": 1024,
            "temperature": 0.20,
            "top_p": 0.20
        }

        response = requests.post(NVIDIA_API_ENDPOINT, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    except Exception as e:
        raise Exception(f"Error processing image with NVIDIA API: {str(e)}")

def answer_question(image_path, question):
    try:
        response = process_image(image_path, question)
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['message']['content']
        else:
            return "No answer found in the response."
    except Exception as e:
        raise Exception(f"Error answering question: {str(e)}")