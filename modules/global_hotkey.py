from pynput.keyboard import GlobalHotKeys
from PySide6.QtCore import Signal, QObject

class HotkeyManager(QObject):
   hotkey_triggered = Signal(str)

   def __init__(self):
      super().__init__()
      self.listener = None
      self.start_hotkeys()

   def start_hotkeys(self):
      hotkey_actions = {
         '<esc>': 'stop_action',
         '<f1>': 'start_recording',
         '<ctrl>+`': 'toggle_click', 
         '<ctrl>+1': 'toggle_script_1', 
         '<ctrl>+2': 'toggle_script_2', 
         '<ctrl>+3': 'toggle_script_3', 
         '<ctrl>+4': 'toggle_script_4', 
         '<ctrl>+5': 'toggle_script_5', 
         '<ctrl>+6': 'toggle_script_6', 
         '<ctrl>+7': 'toggle_script_7', 
         '<ctrl>+8': 'toggle_script_8', 
         '<ctrl>+9': 'toggle_script_9', 
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
      
      self.listener = GlobalHotKeys(hotkey_map)
      self.listener.start()