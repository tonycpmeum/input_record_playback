import os
import json
from typing import Any

class ConfigManager:
   _instance = None
   _data: dict[str, Any] = {}
   config_path = "./data/config.json"

   def __new__(cls):
      if cls._instance is None:
         cls._instance = super().__new__(cls)
         cls._instance._load_config()
      return cls._instance
   
   def _load_config(self):
      # time in seconds
      default_config = {
         "max_scripts": 10,
         "click_settings": {
            "single_click_interval": 1.0,
            "button_type": "Button.left",
            "click_type": 1
         },
         "script_settings": {
            "script_enabled": False,
         },
         "repeat_settings": {
            "repeat_limited": False,
            "repeat_count": 1
         },
         "recording_settings": {
            "sample_mouse_move_interval": 0.15,
         }
      }
      
      directory = os.path.dirname(self.config_path)
      if directory: os.makedirs(directory, exist_ok=True)

      if os.path.exists(self.config_path) and os.path.getsize(self.config_path) > 0:
         try:
            with open(self.config_path, 'r') as f:
               self._data = json.load(f)
         except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config, using defaults: {e}")
            self._data = default_config
            self._save_data()
      else:
         self._data = default_config
         self._save_data()

   def _save_data(self):
      try:
         with open(self.config_path, 'w') as f:
            json.dump(self._data, f, indent=3)
      except IOError as e:
         print(f"Error saving config: {e}")

   @property
   def max_scripts(self) -> int: 
      return self._data["max_scripts"]
   @max_scripts.setter
   def max_scripts(self, value: int): 
      self._data["max_scripts"] = value
      self._save_data()

   # =============== CLILCK SETTINGS ===============
   @property
   def single_click_interval(self) -> float: 
      return self._data['click_settings']["single_click_interval"]
   @single_click_interval.setter
   def single_click_interval(self, value: float): 
      self._data['click_settings']["single_click_interval"] = value
      self._save_data()

   @property
   def button_type(self) -> str: 
      return self._data['click_settings']["button_type"]
   @button_type.setter
   def button_type(self, value: str): 
      self._data['click_settings']["button_type"] = value
      self._save_data()

   @property
   # 1 = single, 2 = double, for compatibility with pynput controller param
   def click_type(self) -> int: 
      return self._data['click_settings']["click_type"]
   @click_type.setter
   def click_type(self, value: int): 
      self._data['click_settings']["click_type"] = value
      self._save_data()

   # =============== SCRIPT SETTINGS ===============
   @property
   def script_enabled(self) -> bool: 
      return self._data["script_settings"]["script_enabled"]
   @script_enabled.setter
   def script_enabled(self, value: bool): 
      self._data["script_settings"]["script_enabled"] = value
      self._save_data()

   # =============== REPEAT SETTINGS ===============
   @property
   def repeat_limited(self) -> bool: 
      return self._data["repeat_settings"]["repeat_limited"]
   @repeat_limited.setter
   def repeat_limited(self, value: bool): 
      self._data["repeat_settings"]["repeat_limited"] = value
      self._save_data()

   @property
   def repeat_count(self) -> int: 
      return self._data["repeat_settings"]["repeat_count"]
   @repeat_count.setter
   def repeat_count(self, value: int): 
      self._data["repeat_settings"]["repeat_count"] = value
      self._save_data()

   # =============== RECORDING SETTINGS ===============

   @property
   def sample_mouse_move_interval(self) -> float: 
      return self._data["recording_settings"]["sample_mouse_move_interval"]
   @sample_mouse_move_interval.setter
   def sample_mouse_move_interval(self, value: float): 
      self._data["recording_settings"]["sample_mouse_move_interval"] = value
      self._save_data()

config = ConfigManager()