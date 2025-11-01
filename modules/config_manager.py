import json
import sys
from pathlib import Path
from typing import Any
from PySide6.QtGui import QIcon
from platformdirs import user_config_path

APP_NAME = "Slay Clicker"
VERSION = '0.0.1'
DATA_DIR = user_config_path(APP_NAME, appauthor=False) / "data"

def get_Qicon(file_name: str) -> QIcon:
   if hasattr(sys, '_MEIPASS'):
      base_path = Path(sys._MEIPASS)
   else:
      base_path = Path.cwd()
   
   img_folder = base_path / "src" / "img"
   path = str(img_folder / file_name)
   return QIcon(path)

class ConfigManager:
   _instance = None
   _data: dict[str, Any] = {}
   config_file = DATA_DIR / "config.json"

   def __new__(cls):
      if cls._instance is None:
         cls._instance = super().__new__(cls)
         cls._instance._load_config()
      return cls._instance
   
   def _load_config(self):
      self.config_file.parent.mkdir(parents=True, exist_ok=True)
      try:
         self._data = json.loads(self.config_file.read_text())
         if self._data.get("version") != VERSION:
            self.reinit_config_default()
      except OSError as e:
         print(f"Error loading config, using defaults: {e}")
         self.reinit_config_default()

   def _save_data(self):
      try:
         self.config_file.write_text(json.dumps(self._data, indent=3))
      except IOError as e:
         print(f"Error saving config: {e}")

   def reinit_config_default(self):
      self._data = self.get_default_config()
      self._save_data()

   def get_default_config(self) -> dict:
      default_config = {
         "version": f"{VERSION}",
         "max_scripts": 10,
         "click_settings": {
            "click_interval": 1.0,
            "click_button": "Button.left",
            "click_type": 1
         },
         "script_settings": {
            "script_enabled": False,
            "script_selected_index": -1
         },
         "repeat_settings": {
            "repeat_limited": False,
            "repeat_count": 1
         },
         "recording_settings": {
            "sample_mouse_move_interval": 0.15,
         },
         "playback_settings": {
            "playback_speed": 1.00,
         }
      }
      return default_config
   
   @property
   def max_scripts(self) -> int: 
      try:
         return self._data["max_scripts"]
      except KeyError as e:
         print(f"KeyError: {e}")
         self.reinit_config_default()
         return self._data["max_scripts"]
   @max_scripts.setter
   def max_scripts(self, value: int): 
      self._data["max_scripts"] = value
      self._save_data()

   # =============== CLILCK SETTINGS ===============
   @property
   def click_interval(self) -> float: 
      try:
         return self._data['click_settings']["click_interval"]
      except KeyError as e:
         print(f"KeyError: {e}")
         self.reinit_config_default()
         return self._data['click_settings']["click_interval"]
   @click_interval.setter
   def click_interval(self, value: float): 
      self._data['click_settings']["click_interval"] = value
      self._save_data()

   @property
   def click_button(self) -> str: 
      try:
         return self._data['click_settings']["click_button"]
      except KeyError as e:
         print(f"KeyError: {e}")
         self.reinit_config_default()
         return self._data['click_settings']["click_button"]
   @click_button.setter
   def click_button(self, value: str): 
      self._data['click_settings']["click_button"] = value
      self._save_data()

   @property
   # 1 = single, 2 = double, for compatibility with pynput controller param
   def click_type(self) -> int: 
      try:
         return self._data['click_settings']["click_type"]
      except KeyError as e:
         print(f"KeyError: {e}")
         self.reinit_config_default()
         return self._data['click_settings']["click_type"]
   @click_type.setter
   def click_type(self, value: int): 
      self._data['click_settings']["click_type"] = value
      self._save_data()

   # =============== SCRIPT SETTINGS ===============
   @property
   def script_enabled(self) -> bool: 
      try:
         return self._data["script_settings"]["script_enabled"]
      except KeyError as e:
         print(f"KeyError: {e}")
         self.reinit_config_default()
         return self._data["script_settings"]["script_enabled"]
   @script_enabled.setter
   def script_enabled(self, value: bool): 
      self._data["script_settings"]["script_enabled"] = value
      self._save_data()

   @property
   def script_selected_index(self) -> int: 
      try:
         return self._data["script_settings"]["script_selected_index"]
      except KeyError as e:
         print(f"KeyError: {e}")
         self.reinit_config_default()
         return self._data["script_settings"]["script_selected_index"]
   @script_selected_index.setter
   def script_selected_index(self, value: int): 
      self._data["script_settings"]["script_selected_index"] = value
      self._save_data()

   # =============== REPEAT SETTINGS ===============
   @property
   def repeat_limited(self) -> bool: 
      try:
         return self._data["repeat_settings"]["repeat_limited"]
      except KeyError as e:
         print(f"KeyError: {e}")
         self.reinit_config_default()
         return self._data["repeat_settings"]["repeat_limited"]
   @repeat_limited.setter
   def repeat_limited(self, value: bool): 
      self._data["repeat_settings"]["repeat_limited"] = value
      self._save_data()

   @property
   def repeat_count(self) -> int: 
      try:
         return self._data["repeat_settings"]["repeat_count"]
      except KeyError as e:
         print(f"KeyError: {e}")
         self.reinit_config_default()
         return self._data["repeat_settings"]["repeat_count"]
   @repeat_count.setter
   def repeat_count(self, value: int): 
      self._data["repeat_settings"]["repeat_count"] = value
      self._save_data()

   # =============== RECORDING SETTINGS ===============
   @property
   def sample_mouse_move_interval(self) -> float: 
      try:
         return self._data["recording_settings"]["sample_mouse_move_interval"]
      except KeyError as e:
         print(f"KeyError: {e}")
         self.reinit_config_default()
         return self._data["recording_settings"]["sample_mouse_move_interval"]
   @sample_mouse_move_interval.setter
   def sample_mouse_move_interval(self, value: float): 
      self._data["recording_settings"]["sample_mouse_move_interval"] = value
      self._save_data()

   # =============== PLAYBACK SETTINGS ===============
   @property
   def playback_speed(self) -> float: 
      try:
         return self._data["playback_settings"]["playback_speed"]
      except KeyError as e:
         print(f"KeyError: {e}")
         self.reinit_config_default()
         return self._data["playback_settings"]["playback_speed"]
   @playback_speed.setter
   def playback_speed(self, value: float): 
      self._data["playback_settings"]["playback_speed"] = value
      self._save_data()

config = ConfigManager()