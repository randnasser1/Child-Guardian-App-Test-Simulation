# test_connection_simple.py
import requests
import json

def test_appium_status():
    urls = [
        'http://127.0.0.1:4723',
        'http://localhost:4723',
        'http://127.0.0.1:4723/wd/hub',
        'http://localhost:4723/wd/hub'
    ]

    for url in urls:
        try:
            print(f"Testing {url}...")
            # Test the status endpoint
            status_url = f"{url}/status" if '/wd/hub' not in url else f"{url}/status".replace('/wd/hub', '')
            response = requests.get(status_url, timeout=5)
            print(f"✅ {url} - Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.json()}")
                return url
        except Exception as e:
            print(f"❌ {url} - Error: {e}")

    return None

if __name__ == "__main__":
    working_url = test_appium_status()
    if working_url:
        print(f"🎯 Use this URL: {working_url}")
    else:
        print("❌ No working Appium URL found")