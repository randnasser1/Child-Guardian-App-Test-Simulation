# main_groomer.py - FIXED VERSION (No re-navigation)
#!/usr/bin/env python3
"""
GROOMER ACCOUNT SIMULATION - LAPTOP 2 - REUSES SESSION
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
        self.bot = None  # Single bot instance
        self.is_in_chat = False  # Track if we're already in chat
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

        # Initialize bot once at startup
        self.initialize_bot()
        self.setup_schedule()
        
        # Run immediate test session
        print("🎬 Running immediate groomer session...")
        self.run_session("Groomer Immediate Start")

    def initialize_bot(self):
        """Initialize the bot once at startup"""
        try:
            print("📱 Initializing Instagram bot...")
            self.bot = InstagramBot("groomer_account")
            
            # Navigate to chat once at startup
            print("🚀 Navigating to chat (one-time setup)...")
            if self.bot.navigate_to_chat(PARTNER_USERNAME):
                self.is_in_chat = True
                print("✅ Successfully in chat! Will reuse this session.")
            else:
                print("❌ Failed to navigate to chat initially")
                self.is_in_chat = False
                
        except Exception as e:
            print(f"❌ Bot initialization error: {e}")
            self.is_in_chat = False

    def setup_schedule(self):
        """Groomer's strategic messaging schedule"""
        # Frequent sessions for testing - NO RE-NAVIGATION
        schedule.every(2).minutes.do(self.run_session, "Groomer Check")
        schedule.every(10).minutes.do(self.run_session, "Groomer Follow-up")
        
        # Prime grooming times
        schedule.every().day.at("15:45").do(self.run_session, "After School")
        schedule.every().day.at("19:30").do(self.run_session, "Evening")
        schedule.every().day.at("21:00").do(self.run_session, "Late Evening")

        print("📅 Groomer schedule set - sessions every 2 minutes")

    def ensure_in_chat(self):
        """Ensure we're still in chat, only re-navigate if necessary"""
        if not self.is_in_chat:
            print("🔄 Not in chat, re-navigating...")
            if self.bot.navigate_to_chat(PARTNER_USERNAME):
                self.is_in_chat = True
                print("✅ Re-established chat connection")
            else:
                print("❌ Failed to re-establish chat connection")
                return False
        return True

    def run_session(self, session_name):
        """Run a grooming session - NO UNNECESSARY NAVIGATION"""
        try:
            print(f"\n🎭 GROOMER SESSION: {session_name} at {datetime.now().strftime('%H:%M:%S')}")

            # Ensure we're still in chat (only navigates if needed)
            if not self.ensure_in_chat():
                print("❌ Cannot proceed - not in chat")
                return

            print("✅ Already in chat - ready to send messages")
            
            # Groomer initiates 70% of the time
            if random.random() < 0.7:
                message = self.agent.generate_message()
                print(f"💬 Groomer initiating: {message}")
                
                if self.bot.send_message(message):
                    self.message_count += 1
                    print(f"✅ Groomer message sent! Total: {self.message_count}")
                    
                    # Track grooming stage
                    stage = "FRIENDSHIP" if self.message_count < 50 else "SECRECY" if self.message_count < 100 else "MEETUP"
                    print(f"🎯 Current grooming stage: {stage} (Message #{self.message_count})")
                else:
                    print("❌ Failed to send groomer message")
                    self.is_in_chat = False  # Mark as needing re-navigation
            else:
                # Wait for child to message first
                print("⏳ Groomer waiting for child to initiate...")
                time.sleep(5)  # Brief wait to simulate checking for responses
                print("👀 No child message detected - will initiate next time")

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

            print("✅ Groomer session completed successfully!")

        except Exception as e:
            print(f"❌ Groomer session error: {e}")
            self.error_handler.log_error(e, session_name)
            self.is_in_chat = False  # Mark as needing re-navigation
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
        print("⏰ Groomer sessions every 2 minutes - NO RE-NAVIGATION")
        print("🎯 Grooming stages: FRIENDSHIP (<50), SECRECY (50-100), MEETUP (100+)")
        
        end_time = datetime.now() + timedelta(days=14)

        while datetime.now() < end_time:
            try:
                schedule.run_pending()
                
                # Print status every minute
                if datetime.now().second < 10:
                    status = "IN CHAT" if self.is_in_chat else "NEEDS NAV"
                    print(f"⏰ Groomer {status} - Messages: {self.message_count} - Next: {datetime.now().strftime('%H:%M:%S')}")

                # Reset daily counters at midnight
                if datetime.now().hour == 0 and datetime.now().minute < 5:
                    self.agent.reset_daily_count()
                    print("📅 Reset groomer daily message counter")

                time.sleep(10)  # Check every 10 seconds
                
            except KeyboardInterrupt:
                print("\n🛑 Groomer simulation stopped by user")
                break
            except Exception as e:
                print(f"❌ Groomer main loop error: {e}")
                time.sleep(10)

        # Cleanup
        if self.bot:
            self.bot.quit()
        print("✅ Groomer simulation completed!")

if __name__ == "__main__":
    simulation = GroomerSimulation()
    simulation.run()
