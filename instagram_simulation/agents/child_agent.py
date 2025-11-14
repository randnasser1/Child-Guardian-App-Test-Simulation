import requests
import json
from config.settings import OLLAMA_URL, OLLAMA_MODEL
from config.prompts import CHILD_SYSTEM_PROMPT
from appium_bot.instagram_bot import InstagramBot
class ChildAgent:
    def __init__(self):
        self.conversation_history = []
        self.message_count = 0
        self.daily_count = 0

    def respond(self, received_message):
        if self.daily_count >= 40:
            raise Exception("Child daily message limit reached")

        self.message_count += 1
        self.daily_count += 1

        self.conversation_history.append(f"Friend: {received_message}")

        prompt = f"""
        {CHILD_SYSTEM_PROMPT}

        Recent conversation:
        {' '.join(self.conversation_history[-3:])}

        Friend just said: {received_message}

        Lulus's response (1 sentence, 10-year-old girl):
        """

        response = self.ollama_generate(prompt)
        self.conversation_history.append(f"Emma: {response}")

        return response

    def ollama_generate(self, prompt):
        """Generate response using local Ollama"""
        try:
            response = requests.post(
                f'{OLLAMA_URL}/api/generate',
                json={
                    'model': OLLAMA_MODEL,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.8,
                        'num_predict': 50  # Short responses
                    }
                }
            )
            return response.json()['response'].strip()
        except Exception as e:
            print(f"Ollama error: {e}")
            return "I don't know what to say..."

    def reset_daily_count(self):
        self.daily_count = 0
