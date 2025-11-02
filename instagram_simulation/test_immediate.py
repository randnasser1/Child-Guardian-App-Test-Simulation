# test_immediate.py
from agents.child_agent import ChildAgent
from appium_bot.instagram_bot import InstagramBot
from config.settings import PARTNER_USERNAME
import time
import logging

logging.basicConfig(level=logging.INFO)

def test_immediate():
    print("🚀 STARTING IMMEDIATE TEST")

    bot = None
    try:
        # Initialize agents
        child_agent = ChildAgent()
        print("🤖 ChildAgent initialized")

        bot = InstagramBot("child_account")
        print("✅ InstagramBot initialized successfully!")

        print("📱 Navigating to chat...")
        if bot.navigate_to_chat(PARTNER_USERNAME):
            print("✅ In chat - waiting for messages...")

            # Wait for a message
            message = bot.wait_for_new_message(timeout=30)
            if message:
                print(f"💬 Received: {message}")
                response = child_agent.respond(message)
                print(f"🤖 Responding: {response}")
                if bot.resilient_send_message(response):
                    print("✅ Message sent!")
                else:
                    print("❌ Failed to send message")
            else:
                print("⏰ No message received, sending test message...")
                test_msg = "hehe hi there! 😊"
                if bot.resilient_send_message(test_msg):
                    print(f"✅ Sent test message: {test_msg}")
                else:
                    print("❌ Failed to send test message")
        else:
            print("❌ Failed to navigate to chat")

    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(f"Test failed: {e}")
    finally:
        if bot:
            bot.quit()
            print("✅ Bot cleaned up")
        print("🏁 Test completed")

if __name__ == "__main__":
    test_immediate()