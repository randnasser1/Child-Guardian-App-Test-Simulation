# instagram_bot.py
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
import time
import random
import json
import logging

class InstagramBot:
    def __init__(self, account_type):
        try:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)

            self.logger.info(f"Initializing InstagramBot for {account_type}")

            # Load capabilities from JSON
            with open('appium_bot/capabilities.json', 'r') as f:
                caps_data = json.load(f)

            if account_type not in caps_data:
                raise ValueError(f"Account type '{account_type}' not found in capabilities.json")

            caps = caps_data[account_type]
            self.logger.info(f"Loaded capabilities: {caps}")

            # Use the correct URL for Appium 3.x
            appium_url = 'http://127.0.0.1:4723'

            self.logger.info(f"Connecting to Appium at: {appium_url}")

            # Convert capabilities to UiAutomator2Options
            options = UiAutomator2Options()

            # Set capabilities individually
            options.platform_name = caps.get("platformName", "Android")
            options.platform_version = caps.get("platformVersion", "13")
            options.device_name = caps.get("deviceName", "Android Emulator")
            options.app_package = caps.get("appPackage", "com.instagram.android")
            options.app_activity = caps.get("appActivity", "com.instagram.android.activity.MainTabActivity")
            options.automation_name = caps.get("automationName", "UiAutomator2")
            options.no_reset = caps.get("noReset", True)
            options.new_command_timeout = caps.get("newCommandTimeout", 300)

            # Initialize driver with options (not desired_capabilities)
            self.driver = webdriver.Remote(
                command_executor=appium_url,
                options=options
            )

            self.account_type = account_type
            self.logger.info("✅ Appium driver initialized successfully!")
            time.sleep(10)  # Wait for app to load

        except Exception as e:
            self.logger.error(f"Failed to initialize InstagramBot: {e}")
            raise

    # ... keep all your existing methods the same
    def ensure_app_open(self):
        """Ensure Instagram is open and active"""
        try:
            current_activity = self.driver.current_activity
            self.logger.info(f"Current activity: {current_activity}")

            if "instagram" not in current_activity.lower():
                self.logger.info("Instagram not active, restarting app...")
                self.driver.start_activity("com.instagram.android",
                                         "com.instagram.android.activity.MainTabActivity")
            time.sleep(5)
        except Exception as e:
            self.logger.error(f"Error ensuring app is open: {e}")
            self.driver.start_activity("com.instagram.android",
                                     "com.instagram.android.activity.MainTabActivity")
            time.sleep(8)

    def navigate_to_chat(self, target_username):
        """Navigate to specific chat"""
        self.ensure_app_open()

        try:
            # Try to find messages button
            messages_btn = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Direct")
            messages_btn.click()
            time.sleep(3)

            # Look for existing chat
            chats = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            for chat in chats:
                if target_username.lower() in chat.text.lower():
                    chat.click()
                    time.sleep(3)
                    return True

            # If no existing chat, create new
            new_chat_btn = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "New Message")
            new_chat_btn.click()
            time.sleep(2)

            search_box = self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
            search_box.send_keys(target_username)
            time.sleep(3)

            # Select user (simplified - may need adjustment)
            users = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            for user in users:
                if target_username.lower() in user.text.lower():
                    user.click()
                    time.sleep(3)
                    return True

        except Exception as e:
            self.logger.error(f"Navigation error: {e}")

        return False

    def send_message(self, text):
        """Send a message in current chat"""
        try:
            # Find message input
            message_input = self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
            message_input.send_keys(text)
            time.sleep(random.uniform(1, 2))

            # Find send button
            send_btn = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Send")
            send_btn.click()
            time.sleep(2)

            self.logger.info(f"✓ {self.account_type} sent: {text}")
            return True

        except Exception as e:
            self.logger.error(f"✗ Send message failed: {e}")
            return False

    def resilient_send_message(self, text, max_attempts=3):
        """Try to send a message with retries"""
        for attempt in range(max_attempts):
            try:
                if self.send_message(text):
                    return True
                time.sleep(2)
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2)
        return False

    def wait_for_new_message(self, timeout=30, check_interval=2):
        """Wait for a new message to arrive"""
        start_time = time.time()
        last_message = self.read_latest_message()

        while time.time() - start_time < timeout:
            current_message = self.read_latest_message()
            if current_message and current_message != last_message:
                return current_message
            time.sleep(check_interval)

        return None

    def read_latest_message(self):
        """Read the latest received message"""
        try:
            # Simple message reading (may need adjustment based on Instagram UI)
            messages = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            if messages:
                return messages[-1].text
        except Exception as e:
            self.logger.error(f"Error reading message: {e}")
        return None

    def quit(self):
        if self.driver:
            self.driver.quit()