import os
import json

class ConfigManager:
   _instance = None
   _config: dict[str, any] = {}
   config_path = "./data/config.json"

   def __new__(cls):
      if cls._instance is None:
         cls._instance = super().__new__(cls)
      return cls._instance
   
   def _load_config(self):
      default_config = {
         "max_scripts": 10,
         "mouse_sample_interval": 0.1,
         "playback_settings": {
            "repeat_enabled": False,
            "repeat_count": 1,
            "click_delay_ms": 100
         },
         "recording_settings": {
            "record_mouse_moves": True,
            "mouse_sample_rate": 0.1
         }
      }
      
      directory = os.path.dirname(self.config_path)
      if directory: os.makedirs(directory, exist_ok=True)

      if os.path.exists(self.config_path):
         try:
            with open(self.config_path, 'r') as f:
               self._config = json.load(f)
         except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config, using defaults: {e}")
            self._config = default_config
            self._save_config()
      else:
         self._config = default_config
         self._save_config()

   def _save_config(self):
      try:
         with open(self.config_path, 'w') as f:
            json.dump(self._config, f, indent=2)
      except IOError as e:
         print(f"Error saving config: {e}")

   @property
   def max_scripts(self): return self._data["max_scripts"]
   @max_scripts.setter
   def max_scripts(self, value): 
      self._data["max_scripts"] = value
      self._save_config()
   
   @property
   def mouse_sample_interval(self): return self._data["mouse_sample_interval"]
   @mouse_sample_interval.setter
   def mouse_sample_interval(self, value): 
      self._data["mouse_sample_interval"] = value
      self._save_config()

   def __getitem__(self, key):
      return self.data[key]
   
   def __setitem__(self, key, value):
      self.data[key] = value
      self._save_config()