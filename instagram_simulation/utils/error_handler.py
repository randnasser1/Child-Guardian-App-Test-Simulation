import time
import requests
from datetime import datetime

class ErrorHandler:
    def __init__(self, account_type):
        self.account_type = account_type
        self.consecutive_failures = 0
        self.crash_log = f"data/crash_logs/{account_type}_crashes.txt"

    def log_error(self, error, context=""):
        """Log errors with timestamp and context"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {self.account_type} - {context}: {error}\n"

        try:
            with open(self.crash_log, "a") as f:
                f.write(log_entry)
        except:
            pass  # Don't crash if logging fails

        print(f"❌ {self.account_type} error: {error}")

    def should_retry(self, max_failures=5):
        """Determine if we should retry or wait"""
        self.consecutive_failures += 1

        if self.consecutive_failures >= max_failures:
            wait_time = 300  # 5 minutes
            print(f"🚨 Too many failures. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            self.consecutive_failures = 0
            return True

        return True

    def reset_failures(self):
        """Reset failure counter on success"""
        self.consecutive_failures = 0