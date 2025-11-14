# main_groomer.py - UPDATED VERSION
#!/usr/bin/env python3
"""
GROOMER ACCOUNT SIMULATION - LAPTOP 2
Run this on the groomer account laptop
"""

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
        """Load or create simulation state"""
        state = self.state_manager.load_state()
        if state:
            self.agent = state['agent']
            self.message_count = state['message_count']
            print("✅ Loaded previous groomer state")
        else:
            self.agent = GroomerAgent()
            self.message_count = 0
            print("🆕 Created new groomer simulation state")

        self.setup_schedule()
        
        # ADD THIS: Run immediate test session
        print("🎬 Running immediate groomer test session...")
        self.run_session("Groomer Immediate Test")

    def setup_schedule(self):
        """Groomer's strategic messaging schedule - UPDATED FOR TESTING"""
        # TESTING: Run frequently to see immediate results
        schedule.every(3).minutes.do(self.run_session, "Groomer Regular Check")  # Every 3 minutes
        schedule.every(10).minutes.do(self.run_session, "Groomer Follow-up")
        
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
        
        print("📅 Groomer schedule set - next run in 3 minutes")

    def run_session(self, session_name):
        """Run a grooming session with better debugging"""
        try:
            print(f"\n🎭 GROOMER SESSION: {session_name} at {datetime.now().strftime('%H:%M:%S')}")

            bot = InstagramBot("groomer_account")
            
            print("📱 Groomer navigating to Instagram...")
            if bot.navigate_to_chat(PARTNER_USERNAME):
                print("✅ Groomer successfully in chat!")
                
                # Groomer initiates 70% of the time
                if random.random() < 0.7:
                    message = self.agent.generate_message()
                    print(f"💬 Groomer initiating: {message}")
                    
                    if bot.send_message(message):
                        self.message_count += 1
                        print(f"✅ Groomer message sent! Total: {self.message_count}")
                        
                        # Track grooming stage
                        stage = "FRIENDSHIP" if self.message_count < 50 else "SECRECY" if self.message_count < 100 else "MEETUP"
                        print(f"🎯 Current grooming stage: {stage} (Message #{self.message_count})")
                    else:
                        print("❌ Failed to send groomer message")
                else:
                    # Wait for child to message first (simulated for now)
                    print("⏳ Groomer waiting for child to initiate...")
                    # In real scenario, you'd check for new messages
                    time.sleep(2)
                    
                    # For testing, send a response anyway
                    simulated_child_message = "Hey, how are you?"
                    response = self.agent.generate_message(simulated_child_message)
                    print(f"💬 Groomer responding to child: {response}")
                    
                    if bot.send_message(response):
                        self.message_count += 1
                        print(f"✅ Groomer response sent! Total: {self.message_count}")
                    else:
                        print("❌ Failed to send groomer response")

                # Save state with psychological metrics
                self.state_manager.save_state(
                    self.agent,
                    self.agent.conversation_history,
                    self.message_count
                )
                print("💾 Groomer progress saved!")

                # Save metrics separately for analysis
                self.save_metrics()
                print("📊 Groomer metrics saved!")

            else:
                print("❌ Groomer failed to navigate to chat")

            bot.quit()
            self.error_handler.reset_failures()
            print("✅ Groomer session completed successfully!")

        except Exception as e:
            print(f"❌ Groomer session error: {e}")
            self.error_handler.log_error(e, session_name)
            if self.error_handler.should_retry():
                print("🔄 Groomer retrying session...")
                self.run_session(session_name)

    def save_metrics(self):
        """Save psychological metrics for research"""
        metrics = self.agent.get_metrics()
        metrics['timestamp'] = datetime.now().isoformat()
        metrics['total_messages'] = self.message_count
        metrics['grooming_stage'] = "FRIENDSHIP" if self.message_count < 50 else "SECRECY" if self.message_count < 100 else "MEETUP"

        # Create directory if it doesn't exist
        import os
        os.makedirs("data/conversation_logs", exist_ok=True)
        
        with open("data/conversation_logs/groomer_metrics.json", "w") as f:
            import json
            json.dump(metrics, f, indent=2)

    def run(self):
        """Main simulation loop"""
        print("🚀 Starting Groomer Account Simulation (14 days)")
        print("⏰ Groomer sessions will run every 3 minutes for testing")
        print("🎯 Grooming stages: FRIENDSHIP (<50), SECRECY (50-100), MEETUP (100+)")
        
        end_time = datetime.now() + timedelta(days=14)

        while datetime.now() < end_time:
            schedule.run_pending()
            
            # Print status every minute
            if datetime.now().second < 5:  # Print once per minute
                print(f"⏰ Groomer waiting... Next check at {datetime.now().strftime('%H:%M:%S')} - Total messages: {self.message_count}")

            # Reset daily counters at midnight
            if datetime.now().hour == 0 and datetime.now().minute < 5:
                self.agent.reset_daily_count()
                print("📅 Reset groomer daily message counter")

            time.sleep(10)  # Check every 10 seconds instead of 60

        print("✅ Groomer simulation completed!")

if __name__ == "__main__":
    simulation = GroomerSimulation()
    simulation.run()
