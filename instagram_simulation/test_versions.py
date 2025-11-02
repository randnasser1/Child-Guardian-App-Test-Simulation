# test_versions.py
import subprocess
import sys
import pkg_resources

def check_versions():
    print("🔍 Checking versions...")

    # Check Python packages
    try:
        appium_version = pkg_resources.get_distribution("Appium-Python-Client").version
        print(f"Appium Python client: {appium_version}")
    except:
        print("Appium Python client not installed or version not available")

    try:
        selenium_version = pkg_resources.get_distribution("selenium").version
        print(f"Selenium: {selenium_version}")
    except:
        print("Selenium not installed")

    # Check Node.js Appium
    try:
        result = subprocess.run(['appium', '--version'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"Appium Server: {result.stdout.strip()}")
        else:
            # Try alternative command
            result = subprocess.run(['appium', '-v'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print(f"Appium Server: {result.stdout.strip()}")
            else:
                print("Could not get Appium server version")
    except Exception as e:
        print(f"Appium server check failed: {e}")

if __name__ == "__main__":
    check_versions()