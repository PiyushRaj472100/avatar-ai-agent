"""
Memory Manager - Handles temporary storage using JSON
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from app.core.config import settings

class MemoryManager:
    """
    Manages temporary storage of interactions and context
    """
    
    def __init__(self):
        self.memory_file = settings.memory_file_path
        self._ensure_memory_file_exists()
    
    def _ensure_memory_file_exists(self):
        """
        Create the memory file if it doesn't exist
        """
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                json.dump({
                    "interactions": [],
                    "context": {},
                    "last_updated": datetime.now().isoformat()
                }, f, indent=2)
    
    def _load_memory(self) -> Dict[str, Any]:
        """
        Load memory from JSON file
        """
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading memory: {e}")
            return {"interactions": [], "context": {}, "last_updated": datetime.now().isoformat()}
    
    def _save_memory(self, memory: Dict[str, Any]):
        """
        Save memory to JSON file
        """
        try:
            memory["last_updated"] = datetime.now().isoformat()
            with open(self.memory_file, 'w') as f:
                json.dump(memory, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def store_interaction(self, command: str, action: str, result: str):
        """
        Store an interaction in memory
        """
        memory = self._load_memory()
        
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "action": action,
            "result": result
        }
        
        memory["interactions"].append(interaction)
        
        # Keep only last 100 interactions
        if len(memory["interactions"]) > 100:
            memory["interactions"] = memory["interactions"][-100:]
        
        self._save_memory(memory)
    
    def get_context(self) -> Dict[str, Any]:
        """
        Get current context from memory
        """
        memory = self._load_memory()
        
        # Return recent interactions as context
        recent_interactions = memory["interactions"][-5:] if memory["interactions"] else []
        
        return {
            "recent_interactions": recent_interactions,
            "context": memory.get("context", {}),
            "last_updated": memory.get("last_updated")
        }
    
    def update_context(self, key: str, value: Any):
        """
        Update context information
        """
        memory = self._load_memory()
        memory["context"][key] = value
        self._save_memory(memory)
    
    def clear_memory(self):
        """
        Clear all memory data
        """
        memory = {
            "interactions": [],
            "context": {},
            "last_updated": datetime.now().isoformat()
        }
        self._save_memory(memory)
    
    def get_recent_interactions(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent interactions
        """
        memory = self._load_memory()
        return memory["interactions"][-count:] if memory["interactions"] else []
