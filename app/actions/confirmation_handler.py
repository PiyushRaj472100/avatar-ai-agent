"""
Confirmation Handler - Handles user confirmations for opening links
"""

class ConfirmationHandler:
    """
    Handles user confirmations for opening links
    """
    
    def __init__(self):
        self.pending_actions = {}  # Store pending actions waiting for confirmation
    
    def add_pending_action(self, user_id: str, action: str, link: str):
        """Store a pending action waiting for confirmation"""
        self.pending_actions[user_id] = {
            "action": action,
            "link": link,
            "timestamp": None
        }
    
    def get_pending_action(self, user_id: str) -> dict:
        """Get pending action for a user"""
        return self.pending_actions.get(user_id)
    
    def confirm_action(self, user_id: str) -> dict:
        """Confirm and execute a pending action"""
        if user_id in self.pending_actions:
            action_data = self.pending_actions[user_id]
            del self.pending_actions[user_id]  # Remove from pending
            return action_data
        return None
    
    def cancel_action(self, user_id: str) -> dict:
        """Cancel a pending action"""
        if user_id in self.pending_actions:
            action_data = self.pending_actions[user_id]
            del self.pending_actions[user_id]  # Remove from pending
            return action_data
        return None
