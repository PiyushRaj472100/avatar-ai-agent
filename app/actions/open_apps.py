"""
Open Apps Action - Opens applications and websites
"""

import subprocess
import webbrowser
from typing import Dict, Any

class OpenAppsAction:
    """
    Action for opening applications and websites
    """
    
    def __init__(self):
        self.app_mappings = {
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "explorer": "explorer.exe"
        }
    
    async def execute(self, parameters: Dict[str, Any]) -> str:
        """
        Execute the open apps action
        """
        app_name = parameters.get("app_name", "").lower()
        url = parameters.get("url", "")
        
        try:
            if url:
                # Open URL in default browser
                webbrowser.open(url)
                return f"Opened URL: {url}"
            
            elif app_name:
                if app_name in ["browser", "web", "internet"]:
                    # Open default browser
                    webbrowser.open("https://www.google.com")
                    return "Opened default browser"
                
                elif app_name in self.app_mappings:
                    # Open specific application
                    subprocess.Popen([self.app_mappings[app_name]])
                    return f"Opened {app_name}"
                
                else:
                    # Try to open as a website
                    if not app_name.startswith(("http://", "https://")):
                        app_name = f"https://{app_name}.com"
                    webbrowser.open(app_name)
                    return f"Opened {app_name}"
            
            else:
                return "No app name or URL provided"
                
        except Exception as e:
            return f"Error opening app: {str(e)}"
