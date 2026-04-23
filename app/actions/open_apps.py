"""
Open Apps Action - Intelligent app opening with natural language understanding
"""

import subprocess
import webbrowser
import platform
from typing import Dict, Any
from app.core.smart_app_detector import SmartAppDetector

class OpenAppsAction:
    """
    Action for opening applications and websites with intelligent detection
    """
    
    def __init__(self):
        self.app_detector = SmartAppDetector()
        
        # Product links for quick opening
        self.product_links = {
            "macbook air m2": "https://www.apple.com/macbook-air-m2",
            "dell xps 13": "https://www.dell.com/en-us/shop/dell-laptops/xps-13-laptop",
            "lenovo thinkpad x1": "https://www.lenovo.com/us/en/p/thinkpad/x1-carbon-gen-11",
            "hp pavilion aero": "https://www.hp.com/us-en/p/pavilion-laptops",
            "asus zenbook": "https://www.asus.com/us/zenbook/",
            "python for everybody": "https://www.coursera.org/specializations/python",
            "complete python bootcamp": "https://www.udemy.com/course/complete-python-bootcamp",
            "python crash course": "https://nostarch.com/pythoncrashcourse2e",
            "google python class": "https://developers.google.com/edu/python",
            "mit python": "https://www.edx.org/course/introduction-computer-science-and-programming"
        }
    
    async def execute(self, parameters: Dict[str, Any]) -> str:
        """
        Execute the open apps action with intelligent detection
        """
        app_name = parameters.get("app_name", "")
        url = parameters.get("url", "")
        
        if url:
            # Open URL in default browser
            webbrowser.open(url)
            return f"Opened URL: {url}"
        
        elif app_name:
            if app_name in ["browser", "web", "internet"]:
                # Open default browser
                webbrowser.open("https://www.google.com")
                return "Opened default browser"
            
            # Use intelligent app detection
            app_path, is_installed, detection_method = self.app_detector.find_app(app_name)
            
            if is_installed and app_path:
                try:
                    # Open the found app
                    if platform.system() == 'Windows':
                        if app_path.endswith('.exe'):
                            subprocess.Popen([app_path], shell=True)
                        else:
                            subprocess.Popen(['start', app_path], shell=True)
                    elif platform.system() == 'Darwin':  # macOS
                        subprocess.Popen(['open', app_path])
                    else:  # Linux
                        subprocess.Popen(['xdg-open', app_path])
                    
                    normalized_name = self.app_detector.normalize_app_name(app_name)
                    return f"✅ Opened {normalized_name} (found via {detection_method})"
                    
                except Exception as e:
                    return f"❌ Error opening {app_name}: {str(e)}"
            
            else:
                # App not found - provide comprehensive installation guide
                normalized_name = self.app_detector.normalize_app_name(app_name)
                response = self.app_detector.format_installation_response(app_name)
                return response
        
        else:
            return "No app name or URL provided"
