import time
import schedule
import random
from datetime import datetime, timedelta
from agents.groomer_agent import GroomerAgent
from appium_bot.instagram_bot import InstagramBot
from utils.persistence import StateManager
from utils.error_handler import ErrorHandler
from config.settings import *

class GroomerSimulation:
    def __init__(self):
        self.state_manager = StateManager("groomer")
        self.error_handler = ErrorHandler("groomer")
        self.initialize_simulation()

    def initialize_simulation(self):
        state = self.state_manager.load_state()
        if state:
            self.agent = state['agent']
            self.message_count = state['message_count']
        else:
            self.agent = GroomerAgent()
            self.message_count = 0

        self.setup_schedule()

    def setup_schedule(self):
        """Groomer's strategic messaging schedule"""
        # Prime grooming times (when child is likely available)
        schedule.every().day.at("15:45").do(self.run_session, "After School")
        schedule.every().day.at("19:30").do(self.run_session, "Evening")
        schedule.every().day.at("21:00").do(self.run_session, "Late Evening")

        # Varied times to seem natural
        schedule.every().monday.at("10:00").do(self.run_session, "Monday Morning")
        schedule.every().wednesday.at("14:00").do(self.run_session, "Wednesday Afternoon")
        schedule.every().friday.at("16:30").do(self.run_session, "Friday After School")
        schedule.every().saturday.at("13:00").do(self.run_session, "Saturday")
        schedule.every().sunday.at("17:00").do(self.run_session, "Sunday Evening")

    def run_session(self, session_name):
        """Run a grooming session"""
        try:
            print(f"\n🎭 GROOMER SESSION: {session_name}")

            bot = InstagramBot("groomer_account")
            bot.navigate_to_chat(PARTNER_USERNAME)

            # Groomer initiates 70% of the time
            if random.random() < 0.7:
                message = self.agent.generate_message()
                bot.resilient_send_message(message)
                self.message_count += 1
            else:
                # Wait for child to message first
                child_message = bot.wait_for_new_message(timeout=300)
                if child_message:
                    response = self.agent.generate_message(child_message)
                    bot.resilient_send_message(response)
                    self.message_count += 1

            # Save state with psychological metrics
            self.state_manager.save_state(
                self.agent,
                self.agent.conversation_history,
                self.message_count
            )

            # Save metrics separately for analysis
            self.save_metrics()

            bot.quit()
            self.error_handler.reset_failures()

        except Exception as e:
            self.error_handler.log_error(e, session_name)
            if self.error_handler.should_retry():
                self.run_session(session_name)

    def save_metrics(self):
        """Save psychological metrics for research"""
        metrics = self.agent.get_metrics()
        metrics['timestamp'] = datetime.now().isoformat()
        metrics['total_messages'] = self.message_count

        with open(f"data/conversation_logs/groomer_metrics.json", "w") as f:
            import json
            json.dump(metrics, f, indent=2)

    def run(self):
        """Main simulation loop"""
        print("🚀 Starting Groomer Account Simulation (14 days)")
        end_time = datetime.now() + timedelta(days=14)

        while datetime.now() < end_time:
            schedule.run_pending()

            # Reset daily counters
            if datetime.now().hour == 0 and datetime.now().minute < 5:
                self.agent.reset_daily_count()
                print("📅 Reset daily message counter")

            time.sleep(60)

        print("✅ Groomer simulation completed!")

if __name__ == "__main__":
    simulation = GroomerSimulation()
    simulation.run()