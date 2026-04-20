"""
System Control Action - Controls system functions
"""

import subprocess
import os
from typing import Dict, Any

class SystemControlAction:
    """
    Action for controlling system functions
    """
    
    def __init__(self):
        self.safe_commands = {
            "shutdown": "shutdown /s /t 60",
            "restart": "shutdown /r /t 60",
            "cancel_shutdown": "shutdown /a",
            "lock": "rundll32.exe user32.dll,LockWorkStation",
            "sleep": "rundll32.exe powrprof.dll,SetSuspendState Sleep",
            "volume_up": "nircmd.exe mutesysvolume 0 && nircmd.exe changesysvolume 2000",
            "volume_down": "nircmd.exe changesysvolume -2000",
            "volume_mute": "nircmd.exe mutesysvolume 1",
            "volume_unmute": "nircmd.exe mutesysvolume 0"
        }
    
    async def execute(self, parameters: Dict[str, Any]) -> str:
        """
        Execute the system control action
        """
        command = parameters.get("command", "").lower()
        
        if not command:
            return "No system command provided"
        
        try:
            # Check for safe predefined commands
            if command in self.safe_commands:
                subprocess.run(self.safe_commands[command], shell=True)
                return f"Executed system command: {command}"
            
            # Handle simple file operations
            elif command.startswith("open "):
                file_path = command[5:].strip()
                if os.path.exists(file_path):
                    os.startfile(file_path)
                    return f"Opened: {file_path}"
                else:
                    return f"File not found: {file_path}"
            
            # Pass through open commands for products/courses to open_apps
            elif command.startswith("open ") and any(keyword in command.lower() for keyword in ["macbook", "dell", "lenovo", "hp", "asus", "python", "coursera", "udemy", "edx", "course"]):
                # This should be handled by open_apps action
                return f"This command should be handled by open_apps: {command}"
            
            # Handle other commands - pass through to other actions
            elif any(word in command for word in ["what is", "define", "explain", "tell me about"]):
                # This should be handled by wikipedia_search
                return f"This query should be handled by Wikipedia search: {command}"
            elif any(word in command for word in ["python", "programming", "language", "computer"]):
                # This should be handled by wikipedia_search
                return f"This query should be handled by Wikipedia search: {command}"
            elif any(word in command.lower() for word in ["vacation", "travel", "tourism", "india", "monsoon"]):
                # This should be handled by search_summary
                return f"This query should be handled by search_summary: {command}"
            
            # Handle directory operations
            elif command.startswith("create folder "):
                folder_name = command[13:].strip()
                os.makedirs(folder_name, exist_ok=True)
                return f"Created folder: {folder_name}"
            
            else:
                return f"Unknown or unsafe system command: {command}"
                
        except Exception as e:
            return f"Error executing system command: {str(e)}"
