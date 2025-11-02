import pickle
import os
import shutil
from datetime import datetime

class StateManager:
    def __init__(self, account_type):
        self.account_type = account_type
        self.state_file = f"data/{account_type}_state.pkl"
        self.backup_dir = "data/backups"

    def save_state(self, agent, conversation_history, message_count):
        """Save current simulation state"""
        state = {
            'agent': agent,
            'conversation_history': conversation_history,
            'message_count': message_count,
            'last_save': datetime.now(),
            'account_type': self.account_type
        }

        try:
            # Save main state
            with open(self.state_file, 'wb') as f:
                pickle.dump(state, f)

            # Create timestamped backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self.backup_dir}/{self.account_type}_backup_{timestamp}.pkl"
            with open(backup_file, 'wb') as f:
                pickle.dump(state, f)

            # Clean old backups (keep last 10)
            self.clean_old_backups()

            print(f"✓ {self.account_type} state saved")
            return True

        except Exception as e:
            print(f"✗ Failed to save {self.account_type} state: {e}")
            return False

    def load_state(self):
        """Load previous simulation state"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'rb') as f:
                    state = pickle.load(f)
                print(f"✓ Loaded {self.account_type} state with {state['message_count']} messages")
                return state
            else:
                print(f"ℹ No previous state found for {self.account_type}")
                return None
        except Exception as e:
            print(f"✗ Failed to load {self.account_type} state: {e}")
            return None

    def clean_old_backups(self):
        """Keep only recent backups"""
        try:
            backups = [f for f in os.listdir(self.backup_dir)
                      if f.startswith(f"{self.account_type}_backup_")]
            backups.sort()

            # Remove all but last 10
            for old_backup in backups[:-10]:
                os.remove(os.path.join(self.backup_dir, old_backup))
        except Exception as e:
            print(f"Backup cleanup failed: {e}")