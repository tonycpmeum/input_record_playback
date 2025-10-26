from pynput import keyboard
from pynput.keyboard import Key, KeyCode, GlobalHotKeys
from PySide6.QtCore import Signal, QObject, QTimer

class HotkeyManager(QObject):
   hotkey_triggered = Signal(str)

   def __init__(self):
      super().__init__()
      self.listener = None
      self.start_hotkeys()

   def start_hotkeys(self):
      hotkey_actions = {
         '<ctrl>+1': 'toggle_recording',
         '<ctrl>+2': 'toggle_playback', 
         '<ctrl>+r': 'stop_playback',
      }

      def create_callback(action_name):
         def callback():
            try:
               self.hotkey_triggered.emit(action_name)
            except Exception as e:
               print(f"   Direct emit failed: {e}")
         return callback
      
      hotkey_map = {}
      for hotkey, action in hotkey_actions.items():
         hotkey_map[hotkey] = create_callback(action)
         print(f"📝 Registered hotkey: {hotkey} -> {action}")
      
      self.listener = GlobalHotKeys(hotkey_map)
      self.listener.start()