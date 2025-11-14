import requests
import json
from datetime import datetime
from config.settings import OLLAMA_URL, OLLAMA_MODEL
from config.prompts import GROOMER_SYSTEM_PROMPT

class GroomerAgent:
    def __init__(self):
        self.conversation_history = []
        self.message_count = 0
        self.daily_count = 0
        self.psychological_metrics = {
            'questions_asked': 0,
            'personal_questions': 0,
            'first_person_pronouns': 0,
            'emotional_words': 0,
            'relationship_words': 0
        }

    def generate_message(self, received_message=None):
        if self.daily_count >= 40:
            raise Exception("Groomer daily message limit reached")

        self.message_count += 1
        self.daily_count += 1

        if received_message:
            self.conversation_history.append(f"Child: {received_message}")

        # Determine grooming stage with more granularity
        if self.message_count < 20:
            stage = "FRIENDSHIP_BUILDING"
        elif self.message_count < 50:
            stage = "PERSONAL_INFO"
        elif self.message_count < 80:
            stage = "SECRECY_ESTABLISHMENT"
        else:
            stage = "MEETUP_PRESSURE"

        prompt = f"""
        {GROOMER_SYSTEM_PROMPT}

        CURRENT STAGE: {stage}
        TOTAL MESSAGES: {self.message_count}
        CONVERSATION HISTORY: {self.conversation_history[-3:] if self.conversation_history else "No history yet"}

        {"Child just said: " + received_message if received_message else "Start a NEW conversation topic (avoid 'how are you'):"}

        IMPORTANT: Do NOT ask "how are you" or similar generic questions. Be creative and stage-appropriate.

        Victor's response (1-2 sentences, continue grooming strategy for {stage} stage):
        """

        response = self.ollama_generate(prompt)
        self.conversation_history.append(f"Victor: {response}")

        # Track psychological metrics
        self.track_metrics(response)

        return response

    def ollama_generate(self, prompt):
        """Generate response using local Ollama with gemma:2b"""
        try:
            response = requests.post(
                f'{OLLAMA_URL}/api/generate',
                json={
                    'model': "gemma:2b",  # Force gemma:2b
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.8,  # Higher temperature for more variety
                        'num_predict': 80,
                        'top_k': 40,
                        'top_p': 0.9
                    }
                },
                timeout=30
            )
            result = response.json()
            return result.get('response', '').strip()
        except Exception as e:
            print(f"Ollama error: {e}")
            # Creative fallback responses based on stage
            stage_messages = {
                "FRIENDSHIP_BUILDING": [
                    "What games do you like to play?",
                    "I saw you like Roblox, what's your favorite game?",
                    "Do you have any pets?",
                    "What's your favorite thing to do after school?"
                ],
                "PERSONAL_INFO": [
                    "That sounds fun! What did you do in school today?",
                    "Cool! Who do you usually hang out with?",
                    "What kind of music are you into?",
                    "Do you have any siblings?"
                ],
                "SECRECY_ESTABLISHMENT": [
                    "We have such cool conversations, it's our little secret",
                    "You're way more fun to talk to than people my age",
                    "I feel like I can tell you anything"
                ],
                "MEETUP_PRESSURE": [
                    "It would be so cool to hang out sometime",
                    "We should meet up and play games together",
                    "You're my favorite person to talk to"
                ]
            }
            current_stage = "FRIENDSHIP_BUILDING" if self.message_count < 20 else "PERSONAL_INFO" if self.message_count < 50 else "SECRECY_ESTABLISHMENT" if self.message_count < 80 else "MEETUP_PRESSURE"
            import random
            return random.choice(stage_messages[current_stage])

    def track_metrics(self, text):
        text_lower = text.lower()
        self.psychological_metrics['questions_asked'] += 1 if '?' in text else 0

        # Personal questions
        personal_triggers = ['school', 'family', 'mom', 'dad', 'home', 'friends', 'age', 'photo', 'picture']
        if any(trigger in text_lower for trigger in personal_triggers):
            self.psychological_metrics['personal_questions'] += 1

        # Psychological features
        self.psychological_metrics['first_person_pronouns'] += text_lower.count(' i ') + text_lower.count(' my ') + text_lower.count(' me ')
        self.psychological_metrics['emotional_words'] += sum(text_lower.count(word) for word in ['love', 'happy', 'sad', 'miss', 'care', 'feel', 'special'])
        self.psychological_metrics['relationship_words'] += sum(text_lower.count(word) for word in ['friend', 'special', 'connection', 'trust', 'close', 'understand'])

    def reset_daily_count(self):
        self.daily_count = 0

    def get_metrics(self):
        return self.psychological_metrics
