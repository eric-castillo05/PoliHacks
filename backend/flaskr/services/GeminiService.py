import json
import requests
from flaskr.models import GeminiModel
from flaskr.utils import Config


class GeminiService:
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.site_url = Config.SITE_URL
        self.site_name = Config.SITE_NAME
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "openai/gpt-4o"

    def get_answer(self, message: str) -> tuple[dict, int]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name,
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        try:
            response = requests.post(
                url=self.url,
                headers=headers,
                data=json.dumps(payload)
            )

            response.raise_for_status()

            api_response_data = response.json()

            gemini_model = GeminiModel(api_response_data)

            if api_response_data.get('choices'):
                ai_text = api_response_data['choices'][0]['message']['content']
            else:
                ai_text = "No valid response text found."

            return {
                "answer": ai_text,
                "full_data": gemini_model.response_data
            }, 200

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return {"error": "External API error", "details": str(e)}, response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return {"error": "Network or connection error", "details": str(e)}, 503
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {"error": "Internal server error", "details": str(e)}, 500