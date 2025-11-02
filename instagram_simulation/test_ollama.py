import requests
import json

def test_ollama():
    try:
        print("Testing Ollama connection...")

        # Test 1: Check if Ollama is running
        try:
            status = requests.get('http://localhost:11434/api/tags', timeout=5)
            print("✅ Ollama server is running")
        except:
            print("❌ Ollama server not reachable")
            print("Make sure Ollama is running: ollama serve")
            return False

        # Test 2: Try to generate a response
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama2',
                'prompt': 'Hello, respond with just one short sentence.',
                'stream': False
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Ollama response successful!")
            print("Response:", result.get('response', 'No response field'))
            print("Full response keys:", list(result.keys()))
            return True
        else:
            print(f"❌ Ollama error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        return False

if __name__ == "__main__":
    test_ollama()