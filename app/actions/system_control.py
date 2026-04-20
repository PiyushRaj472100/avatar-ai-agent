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
            
            # Handle directory operations
            elif command.startswith("create folder "):
                folder_name = command[13:].strip()
                os.makedirs(folder_name, exist_ok=True)
                return f"Created folder: {folder_name}"
            
            else:
                return f"Unknown or unsafe system command: {command}"
                
        except Exception as e:
            return f"Error executing system command: {str(e)}"
