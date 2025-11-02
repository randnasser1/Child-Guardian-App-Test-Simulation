from appium import webdriver
from appium.options.common.base import AppiumOptions
import time

def test_appium_connection():
    options = AppiumOptions()
    options.load_capabilities({
        "platformName": "Android",
        "appium:platformVersion": "13",
        "appium:deviceName": "Android Emulator",
        "appium:appPackage": "com.instagram.android",
        "appium:appActivity": "com.instagram.android.activity.MainTabActivity",
        "appium:automationName": "UiAutomator2",
        "appium:noReset": True
    })

    try:
        print("🔌 Testing Appium connection to Instagram...")
        driver = webdriver.Remote('http://localhost:4723', options=options)

        print(f"✅ Connected successfully!")
        print(f"📱 Current app: {driver.current_package}")
        print(f"🎯 Current activity: {driver.current_activity}")

        time.sleep(3)
        driver.save_screenshot("test_connection.png")
        print("📸 Screenshot saved as test_connection.png")

        driver.quit()
        print("✅ Test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_appium_connection()