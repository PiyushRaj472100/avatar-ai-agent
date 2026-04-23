"""
Smart App Detector - Production-ready app detection with permission handling
"""

import subprocess
import platform
import os
import json
from typing import Dict, List, Optional, Tuple
import re

class SmartAppDetector:
    """
    Production-ready app detector that works with user permissions
    """
    
    def __init__(self):
        self.system = platform.system()
        self.installed_apps_cache = {}
        self.common_app_database = self._load_common_app_database()
        self.detection_methods = self._get_detection_methods()
    
    def _load_common_app_database(self) -> Dict[str, Dict]:
        """
        Load comprehensive app database with installation methods
        """
        return {
            "calculator": {
                "names": ["calculator", "calc", "calculate"],
                "executables": ["calc.exe"],
                "system_app": True,
                "install_methods": {
                    "windows": "Built-in Windows app",
                    "download": "Not needed - comes with Windows"
                }
            },
            "notepad": {
                "names": ["notepad", "text editor", "note", "notes"],
                "executables": ["notepad.exe"],
                "system_app": True,
                "install_methods": {
                    "windows": "Built-in Windows app",
                    "download": "Not needed - comes with Windows"
                }
            },
            "chrome": {
                "names": ["chrome", "google chrome", "browser", "web browser"],
                "executables": ["chrome.exe", "googlechrome.exe"],
                "system_app": False,
                "install_methods": {
                    "official": "https://www.google.com/chrome/",
                    "store": "Microsoft Store - Google Chrome",
                    "winget": "winget install Google.Chrome",
                    "manual": "Download from google.com/chrome"
                }
            },
            "spotify": {
                "names": ["spotify", "music", "music player"],
                "executables": ["Spotify.exe"],
                "system_app": False,
                "install_methods": {
                    "official": "https://www.spotify.com/download",
                    "store": "Microsoft Store - Spotify",
                    "winget": "winget install Spotify.Spotify",
                    "manual": "Download from spotify.com/download"
                }
            },
            "discord": {
                "names": ["discord", "chat", "voice chat"],
                "executables": ["Discord.exe"],
                "system_app": False,
                "install_methods": {
                    "official": "https://discord.com/download",
                    "store": "Microsoft Store - Discord",
                    "winget": "winget install Discord.Discord",
                    "manual": "Download from discord.com/download"
                }
            },
            "vlc": {
                "names": ["vlc", "vlc media player", "video player", "media player"],
                "executables": ["vlc.exe"],
                "system_app": False,
                "install_methods": {
                    "official": "https://www.videolan.org/vlc/",
                    "store": "Microsoft Store - VLC",
                    "winget": "winget install VideoLAN.VLC",
                    "manual": "Download from videolan.org/vlc/"
                }
            },
            "firefox": {
                "names": ["firefox", "mozilla firefox", "mozilla"],
                "executables": ["firefox.exe"],
                "system_app": False,
                "install_methods": {
                    "official": "https://www.mozilla.org/firefox/",
                    "store": "Microsoft Store - Mozilla Firefox",
                    "winget": "winget install Mozilla.Firefox",
                    "manual": "Download from mozilla.org/firefox/"
                }
            },
            "zoom": {
                "names": ["zoom", "video call", "meeting"],
                "executables": ["Zoom.exe"],
                "system_app": False,
                "install_methods": {
                    "official": "https://zoom.us/download",
                    "store": "Microsoft Store - Zoom",
                    "winget": "winget install Zoom.Zoom",
                    "manual": "Download from zoom.us/download"
                }
            },
            "teams": {
                "names": ["teams", "microsoft teams", "video meeting"],
                "executables": ["Teams.exe"],
                "system_app": False,
                "install_methods": {
                    "official": "https://www.microsoft.com/en-us/microsoft-teams/download-app",
                    "store": "Microsoft Store - Microsoft Teams",
                    "winget": "winget install Microsoft.Teams",
                    "manual": "Download from microsoft.com/teams"
                }
            },
            "slack": {
                "names": ["slack", "team chat", "workspace"],
                "executables": ["slack.exe"],
                "system_app": False,
                "install_methods": {
                    "official": "https://slack.com/downloads",
                    "store": "Microsoft Store - Slack",
                    "winget": "winget install Slack.Slack",
                    "manual": "Download from slack.com/downloads"
                }
            },
            "photoshop": {
                "names": ["photoshop", "adobe photoshop", "photo editor", "ps"],
                "executables": ["Photoshop.exe", "photoshop.exe"],
                "system_app": False,
                "install_methods": {
                    "official": "https://www.adobe.com/products/photoshop.html",
                    "store": "Microsoft Store - Adobe Photoshop",
                    "creative": "Adobe Creative Cloud subscription",
                    "manual": "Download from adobe.com/photoshop"
                }
            },
            "excel": {
                "names": ["excel", "microsoft excel", "spreadsheet", "sheets"],
                "executables": ["EXCEL.EXE"],
                "system_app": False,
                "install_methods": {
                    "office": "Microsoft 365 subscription",
                    "store": "Microsoft Store - Microsoft Excel",
                    "web": "Office.com - Free web version",
                    "manual": "Microsoft 365 subscription required"
                }
            },
            "word": {
                "names": ["word", "microsoft word", "document", "docs"],
                "executables": ["WINWORD.EXE"],
                "system_app": False,
                "install_methods": {
                    "office": "Microsoft 365 subscription",
                    "store": "Microsoft Store - Microsoft Word",
                    "web": "Office.com - Free web version",
                    "manual": "Microsoft 365 subscription required"
                }
            },
            "powerpoint": {
                "names": ["powerpoint", "microsoft powerpoint", "presentation", "slides"],
                "executables": ["POWERPNT.EXE"],
                "system_app": False,
                "install_methods": {
                    "office": "Microsoft 365 subscription",
                    "store": "Microsoft Store - Microsoft PowerPoint",
                    "web": "Office.com - Free web version",
                    "manual": "Microsoft 365 subscription required"
                }
            },
            "remote mouse": {
                "names": ["remote mouse", "mouse control", "remote mouse"],
                "executables": ["RemoteMouse.exe"],
                "system_app": False,
                "install_methods": {
                    "official": "https://www.remotemouse.net/",
                    "store": "Microsoft Store - Remote Mouse",
                    "winget": "winget install RemoteMouse.RemoteMouse",
                    "manual": "Download from remotemouse.net"
                }
            }
        }
    
    def _get_detection_methods(self) -> List[str]:
        """
        Get available detection methods based on system
        """
        if self.system == 'Windows':
            return [
                'system_apps',
                'program_files',
                'winget_list',
                'registry_scan',
                'start_menu'
            ]
        elif self.system == 'Darwin':
            return ['applications_folder', 'brew_list']
        else:
            return ['package_managers', 'binaries']
    
    def normalize_app_name(self, user_input: str) -> str:
        """
        Normalize user input to match app names
        """
        user_input = user_input.lower().strip()
        
        # Remove command words
        user_input = re.sub(r'^(open|launch|start|run)\s+', '', user_input)
        user_input = re.sub(r'\s+(please|pls)$', '', user_input)
        
        # Check against our database
        for app_key, app_data in self.common_app_database.items():
            for name in app_data['names']:
                if name in user_input or user_input in name:
                    return app_key
        
        return user_input
    
    def find_app(self, user_input: str) -> Tuple[Optional[str], bool, str]:
        """
        Find app with detailed status information
        Returns: (app_path, is_installed, detection_method)
        """
        normalized_name = self.normalize_app_name(user_input)
        
        # Check if it's in our common database
        if normalized_name in self.common_app_database:
            app_data = self.common_app_database[normalized_name]
            
            # Try different detection methods
            for method in self.detection_methods:
                try:
                    result = self._detect_with_method(normalized_name, method)
                    if result:
                        return result, True, method
                except Exception as e:
                    print(f"Detection method {method} failed: {e}")
                    continue
            
            # If not found, return not installed
            return None, False, "not_found"
        
        # Fallback to generic detection
        return self._generic_detection(user_input)
    
    def _detect_with_method(self, app_name: str, method: str) -> Optional[str]:
        """
        Detect app using specific method
        """
        app_data = self.common_app_database[app_name]
        
        if method == 'system_apps':
            return self._check_system_apps(app_data)
        elif method == 'program_files':
            return self._check_program_files(app_data)
        elif method == 'winget_list':
            return self._check_winget(app_name)
        elif method == 'registry_scan':
            return self._check_registry(app_data)
        elif method == 'start_menu':
            return self._check_start_menu(app_data)
        
        return None
    
    def _check_system_apps(self, app_data: Dict) -> Optional[str]:
        """
        Check Windows system apps
        """
        if not app_data.get('system_app'):
            return None
        
        if self.system == 'Windows':
            for exe in app_data['executables']:
                try:
                    # Try to run the command to see if it exists
                    result = subprocess.run(['where', exe], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        return exe
                except:
                    continue
        
        return None
    
    def _check_program_files(self, app_data: Dict) -> Optional[str]:
        """
        Check Program Files directories
        """
        if self.system != 'Windows':
            return None
        
        program_paths = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            r"C:\Users\{}\AppData\Local\Programs".format(os.getenv('USERNAME', 'Default'))
        ]
        
        for path in program_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower() in [exe.lower() for exe in app_data['executables']]:
                            return os.path.join(root, file)
        
        return None
    
    def _check_winget(self, app_name: str) -> Optional[str]:
        """
        Check using winget package manager
        """
        if self.system != 'Windows':
            return None
        
        try:
            result = subprocess.run(['winget', 'list'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                output = result.stdout.lower()
                app_data = self.common_app_database[app_name]
                for name in app_data['names']:
                    if name in output:
                        # Found via winget, try to get path
                        return self._get_winget_path(app_name)
        except:
            pass
        
        return None
    
    def _get_winget_path(self, app_name: str) -> Optional[str]:
        """
        Get executable path from winget
        """
        try:
            # Try to find installation path
            result = subprocess.run(['winget', 'show', app_name], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                # Parse output for installation path
                for line in result.stdout.split('\n'):
                    if 'installation path' in line.lower():
                        path = line.split(':')[1].strip()
                        exe_path = self._find_exe_in_dir(path)
                        if exe_path:
                            return exe_path
        except:
            pass
        
        return None
    
    def _find_exe_in_dir(self, directory: str) -> Optional[str]:
        """
        Find main executable in directory
        """
        try:
            for item in os.listdir(directory):
                if item.lower().endswith('.exe'):
                    return os.path.join(directory, item)
        except:
            pass
        return None
    
    def _check_registry(self, app_data: Dict) -> Optional[str]:
        """
        Check Windows registry for installed programs
        """
        if self.system != 'Windows':
            return None
        
        try:
            import winreg
            
            registry_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
            ]
            
            for hive, path in registry_paths:
                try:
                    with winreg.OpenKey(hive, path) as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    if any(name in display_name.lower() for name in app_data['names']):
                                        try:
                                            install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                            if install_location and os.path.exists(install_location):
                                                exe_path = self._find_exe_in_dir(install_location)
                                                if exe_path:
                                                    return exe_path
                                        except:
                                            pass
                                except:
                                    continue
                except:
                    continue
        except:
            pass
        
        return None
    
    def _check_start_menu(self, app_data: Dict) -> Optional[str]:
        """
        Check Start Menu shortcuts
        """
        if self.system != 'Windows':
            return None
        
        start_menu_paths = [
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
            r"C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs".format(os.getenv('USERNAME', 'Default'))
        ]
        
        for path in start_menu_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith('.lnk'):
                            # Check if shortcut name matches
                            for name in app_data['names']:
                                if name in file.lower():
                                    # Could resolve shortcut here, but for now return the name
                                    return name
        
        return None
    
    def _generic_detection(self, user_input: str) -> Tuple[Optional[str], bool, str]:
        """
        Generic detection for apps not in database
        """
        # Try basic system commands
        try:
            result = subprocess.run(['where', user_input], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0], True, "where_command"
        except:
            pass
        
        return None, False, "not_found"
    
    def get_installation_guide(self, app_name: str) -> Dict[str, str]:
        """
        Get comprehensive installation guide
        """
        normalized_name = self.normalize_app_name(app_name)
        
        if normalized_name in self.common_app_database:
            app_data = self.common_app_database[normalized_name]
            return app_data['install_methods']
        
        # Generic suggestions for unknown apps
        return {
            "search": f"Search for '{app_name}' in Microsoft Store",
            "google": f"Google '{app_name} download official'",
            "winget": f"Try: winget install {app_name}",
            "manual": "Visit the official website"
        }
    
    def format_installation_response(self, app_name: str) -> str:
        """
        Format user-friendly installation response
        """
        normalized_name = self.normalize_app_name(app_name)
        methods = self.get_installation_guide(app_name)
        
        response = f"❌ '{normalized_name}' is not installed on your computer.\n\n"
        response += "📥 **Here's how to install it:**\n\n"
        
        for i, (method, description) in enumerate(methods.items(), 1):
            if method == "official":
                response += f"1. 🌐 **Official Download**: {description}\n"
            elif method == "store":
                response += f"2. 🏪 **Microsoft Store**: {description}\n"
            elif method == "winget":
                response += f"3. 💻 **Package Manager**: {description}\n"
            elif method == "manual":
                response += f"4. 📦 **Manual Install**: {description}\n"
            else:
                response += f"{i}. **{method.title()}**: {description}\n"
        
        response += f"\n💡 **Tip**: After installation, try saying 'open {normalized_name}' again!"
        
        return response
