"""
Open Apps Action - Opens applications and websites
"""

import subprocess
import webbrowser
import platform
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
                
                # If it doesn't start with http, check if it's an app or URL
                if not app_name.startswith(('http://', 'https://')):
                    # Check if it's a Windows executable
                    if app_name.endswith('.exe') or platform.system() == 'Windows':
                        try:
                            if platform.system() == 'Windows':
                                # Try to open as Windows application
                                subprocess.Popen(['start', app_name], shell=True)
                                return f"Opened {app_name}"
                        except:
                            pass
                    
                    # Check for product links
                    found_link = None
                    if app_name in self.product_links:
                        found_link = self.product_links[app_name]
                    else:
                        # Check for partial matches
                        for product_name, link in self.product_links.items():
                            if product_name in app_name or app_name in product_name:
                                found_link = link
                                break
                    
                    if found_link:
                        # Provide the link and let user do normal search
                        return f"Found {app_name}. Here's the link: {found_link}\n\nIf you're interested, I can do a normal browser search for more information about {app_name}."
                    else:
                        # Try to open as application first
                        try:
                            if platform.system() == 'Windows':
                                subprocess.Popen(['start', app_name], shell=True)
                                return f"Opened {app_name}"
                            elif platform.system() == 'Darwin':  # macOS
                                subprocess.Popen(['open', app_name])
                                return f"Opened {app_name}"
                            else:  # Linux
                                subprocess.Popen(['xdg-open', app_name])
                                return f"Opened {app_name}"
                        except:
                            return f"Unable to open {app_name}. Please check if the application is installed."
                
                elif app_name in self.app_mappings:
                    # Open specific application
                    try:
                        if app_name == "calculator":
                            subprocess.Popen(["start", "calc"], shell=True)
                        else:
                            subprocess.Popen([self.app_mappings[app_name]])
                        return f"Opened {app_name}"
                    except Exception as e:
                        return f"Error opening {app_name}: {str(e)}"
                
                else:
                    # Try to open as a website
                    if not app_name.startswith(("http://", "https://")):
                        app_name = f"https://{app_name}.com"
                    webbrowser.open(app_name)
                    return f"Opened {app_name}"
            
            else:
                # Check if it's a product we know about (improved matching)
                found_link = None
                
                # Check for exact match first
                if app_name in self.product_links:
                    found_link = self.product_links[app_name]
                else:
                    # Check for partial matches
                    for product_name, link in self.product_links.items():
                        if product_name in app_name or app_name in product_name:
                            found_link = link
                            break
                
                if found_link:
                    # Provide the link and let user do normal search
                    return f"Found {app_name}. Here's the link: {found_link}\n\nIf you're interested, I can do a normal browser search for more information about {app_name}."
                else:
                    return "No app name or URL provided"
                
        except Exception as e:
            return f"Error opening app: {str(e)}"
