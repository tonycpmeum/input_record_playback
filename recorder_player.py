import time
from pynput import mouse, keyboard
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6 import QtCore as Core
from config_manager import config
from model_view import list_model

class ScriptRecorder:
   def __init__(self):
      self.keyboard_listener = None
      self.mouse_listener = None
      self.start_time = None

      self.is_recording = False
      self.record_buffer = []
      self.last_mouse_sample_time = 0
      
      self.mouse_sample_interval = config.sample_mouse_move_interval  # time between samples

   def start_listening(self):
      self.is_recording = True
      self.record_buffer = []
      self.last_mouse_sample_time = 0
      self.start_time = time.monotonic()

      self.keyboard_listener = keyboard.Listener(
         on_press = self._on_press_kb,
         on_release = self._on_release_kb
      )
      self.mouse_listener = mouse.Listener(
         on_click = self._on_click_ms,
         on_move = self._on_move_ms,
         on_scroll = self._on_scroll__ms
      )
      
      self.keyboard_listener.start()
      self.mouse_listener.start()

   def stop_listening(self):
      self.is_recording = False
      if self.keyboard_listener:
         self.keyboard_listener.stop()
      if self.mouse_listener:
         self.mouse_listener.stop()

   ### ================== EVENT HANDLERS ================= ###
   def _on_press_kb(self, key):
      if not self.is_recording: return
      try:
         key_data = key.char
         key_type = 'regular'
      except AttributeError:
         key_data = str(key)
         key_type = 'special'
      time_elapsed = time.monotonic() - self.start_time
      event = {
         'type': 'keyboard',
         'action': 'press',
         'key': key_data,
         'key_type': key_type,
         'time': time_elapsed
      }

      self.record_buffer.append(event)

   def _on_release_kb(self, key):
      if not self.is_recording: return
      try:
         key_data = key.char
         key_type = 'regular'
      except AttributeError:
         key_data = str(key)
         key_type = 'special'
      time_elapsed = time.monotonic() - self.start_time
      event = {
         'type': 'keyboard',
         'action': 'release',
         'key': key_data,
         'key_type': key_type,
         'time': time_elapsed
      }

      self.record_buffer.append(event)

   def _on_click_ms(self, x, y, btn, pressed):
      if not self.is_recording: return
      time_elapsed = time.monotonic() - self.start_time
      event = {
         'type': 'mouse_click',
         'button': str(btn),
         'x': x,
         'y': y,
         'pressed': pressed,
         'time': time_elapsed
      }
      self.record_buffer.append(event)

   def _on_move_ms(self, x, y):
      if not self.is_recording: return

      time_elapsed = time.monotonic() - self.start_time
      current_interval = time_elapsed - self.last_mouse_sample_time

      if current_interval >= self.mouse_sample_interval:
         event = {
            'type': 'mouse_move',
            'x': x,
            'y': y,
            'time': time_elapsed
         }
         self.record_buffer.append(event)
         self.last_mouse_sample_time = time_elapsed

   def _on_scroll__ms(self, x, y, dx, dy):
      if not self.is_recording: return
      time_elapsed = time.monotonic() - self.start_time
      event = {
         'type': 'mouse_scroll',
         'x': x,
         'y': y,
         'dx': dx,
         'dy': dy,
         'time': time_elapsed
      }
      self.record_buffer.append(event)

class ScriptPlayer(QObject):
   started = Signal()
   finished = Signal()
   progress = Signal(str)

   request_play_script = Signal(int)
   request_play_single_click = Signal()
   request_stop = Signal()

   def __init__(self):
      super().__init__()
      self.mouse_controller = mouse.Controller()
      self.keyboard_controller = keyboard.Controller()
      self.is_playing = False

      self.request_play_script.connect(self.play_script)
      self.request_play_single_click.connect(self.play_single_click)
      self.request_stop.connect(self.stop_playing)
 
   def play_single_click(self):
      self.is_playing = True
      self.started.emit()
      self.progress.emit("Single click mode...")

      repeat_count = config.repeat_count
      button = self.convert_button_string(config.click_button)
      click_type = config.click_type
      interval = config.click_interval

      if config.repeat_limited:
         for i in range(repeat_count):
            self.mouse_controller.click(button, click_type)
            if not self.is_playing:
               break
            if i < repeat_count - 1:
               time.sleep(interval)
      else:
         while self.is_playing:
            self.mouse_controller.click(button, click_type)
            time.sleep(interval)
      self.stop_playing(False)

   def play_script(self, script_index):
      selected_script = list_model.get_script_events(script_index)
      if not selected_script:
         print(f"Script {script_index} does not exist.")
         return
      
      self.is_playing = True
      self.progress.emit("Playing script...")
      self.started.emit()

      if config.repeat_limited:
         for i in range(config.repeat_count):
            self._execute_script_once(selected_script)
      else:
         while self.is_playing:
            self._execute_script_once(selected_script)
      self.stop_playing(False)

   def stop_playing(self, early_termination: bool):
      if early_termination:
         self.progress.emit("Playback terminated.")
      else:
         self.progress.emit("Playback ended.")
      self.finished.emit()
      self.is_playing = False
      
   def convert_button_string(self, button_str):
      button_map = {
         'Button.left': mouse.Button.left,
         'Button.right': mouse.Button.right,
         'Button.middle': mouse.Button.middle
      }
      return button_map.get(button_str, mouse.Button.left)
   
   def convert_key_string(self, key_str, key_type):
      if key_type == 'regular' and len(key_str) == 1:
         return keyboard.KeyCode.from_char(key_str)
      else:
         special_key_map = {
            'Key.shift': keyboard.Key.shift,
            'Key.shift_l': keyboard.Key.shift_l,
            'Key.shift_r': keyboard.Key.shift_r,
            'Key.ctrl': keyboard.Key.ctrl,
            'Key.ctrl_l': keyboard.Key.ctrl_l,
            'Key.ctrl_r': keyboard.Key.ctrl_r,
            'Key.alt': keyboard.Key.alt,
            'Key.alt_l': keyboard.Key.alt_l,
            'Key.alt_r': keyboard.Key.alt_r,
            'Key.alt_gr': keyboard.Key.alt_gr,
            
            'Key.cmd': keyboard.Key.cmd,
            'Key.cmd_l': keyboard.Key.cmd_l,
            'Key.cmd_r': keyboard.Key.cmd_r,
            'Key.win': keyboard.Key.cmd,  # Alias
            'Key.win_l': keyboard.Key.cmd_l,
            'Key.win_r': keyboard.Key.cmd_r,
            
            'Key.up': keyboard.Key.up,
            'Key.down': keyboard.Key.down,
            'Key.left': keyboard.Key.left,
            'Key.right': keyboard.Key.right,
            'Key.page_up': keyboard.Key.page_up,
            'Key.page_down': keyboard.Key.page_down,
            'Key.home': keyboard.Key.home,
            'Key.end': keyboard.Key.end,
            
            'Key.backspace': keyboard.Key.backspace,
            'Key.delete': keyboard.Key.delete,
            'Key.insert': keyboard.Key.insert,
            'Key.enter': keyboard.Key.enter,
            'Key.tab': keyboard.Key.tab,
            'Key.space': keyboard.Key.space,
            
            'Key.caps_lock': keyboard.Key.caps_lock,
            'Key.num_lock': keyboard.Key.num_lock,
            'Key.scroll_lock': keyboard.Key.scroll_lock,
            
            'Key.f1': keyboard.Key.f1,
            'Key.f2': keyboard.Key.f2,
            'Key.f3': keyboard.Key.f3,
            'Key.f4': keyboard.Key.f4,
            'Key.f5': keyboard.Key.f5,
            'Key.f6': keyboard.Key.f6,
            'Key.f7': keyboard.Key.f7,
            'Key.f8': keyboard.Key.f8,
            'Key.f9': keyboard.Key.f9,
            'Key.f10': keyboard.Key.f10,
            'Key.f11': keyboard.Key.f11,
            'Key.f12': keyboard.Key.f12,
            'Key.f13': keyboard.Key.f13,
            'Key.f14': keyboard.Key.f14,
            'Key.f15': keyboard.Key.f15,
            'Key.f16': keyboard.Key.f16,
            'Key.f17': keyboard.Key.f17,
            'Key.f18': keyboard.Key.f18,
            'Key.f19': keyboard.Key.f19,
            'Key.f20': keyboard.Key.f20,
            
            'Key.esc': keyboard.Key.esc,
            'Key.print_screen': keyboard.Key.print_screen,
            'Key.pause': keyboard.Key.pause,
            'Key.menu': keyboard.Key.menu,
            
            'Key.num0': getattr(keyboard.Key, 'num0', None),
            'Key.num1': getattr(keyboard.Key, 'num1', None),
            'Key.num2': getattr(keyboard.Key, 'num2', None),
            'Key.num3': getattr(keyboard.Key, 'num3', None),
            'Key.num4': getattr(keyboard.Key, 'num4', None),
            'Key.num5': getattr(keyboard.Key, 'num5', None),
            'Key.num6': getattr(keyboard.Key, 'num6', None),
            'Key.num7': getattr(keyboard.Key, 'num7', None),
            'Key.num8': getattr(keyboard.Key, 'num8', None),
            'Key.num9': getattr(keyboard.Key, 'num9', None),
            'Key.num_enter': getattr(keyboard.Key, 'num_enter', None),
            'Key.num_add': getattr(keyboard.Key, 'num_add', None),
            'Key.num_subtract': getattr(keyboard.Key, 'num_subtract', None),
            'Key.num_multiply': getattr(keyboard.Key, 'num_multiply', None),
            'Key.num_divide': getattr(keyboard.Key, 'num_divide', None),
            'Key.num_decimal': getattr(keyboard.Key, 'num_decimal', None),
            
            # Media keys (if supported by pynput version)
            'Key.media_play_pause': getattr(keyboard.Key, 'media_play_pause', None),
            'Key.media_volume_mute': getattr(keyboard.Key, 'media_volume_mute', None),
            'Key.media_volume_down': getattr(keyboard.Key, 'media_volume_down', None),
            'Key.media_volume_up': getattr(keyboard.Key, 'media_volume_up', None),
            'Key.media_previous': getattr(keyboard.Key, 'media_previous', None),
            'Key.media_next': getattr(keyboard.Key, 'media_next', None),
         }

         # Filter out None values (keys not available in this pynput version)
         available_key_map = {k: v for k, v in special_key_map.items() if v is not None}
         return available_key_map.get(key_str, keyboard.KeyCode.from_vk(0))
  
   def _execute_script_once(self, script: list):
      start_time = time.monotonic()
      total_events = len(script)

      for i in range(total_events):
         if not self.is_playing: break

         time_to_event = script[i].get('time', 0)
         event_time = start_time + time_to_event

         while event_time > time.monotonic():
            remaining_time = event_time - time.monotonic()
            time.sleep(remaining_time)

         self._execute_event(script[i])

   def _execute_event(self, event: dict):
      event_type = event.get('type')
      
      if event_type == 'mouse_move':
         x = event.get('x')
         y = event.get('y')
         self.mouse_controller.position = (x, y)
      elif event_type == 'keyboard':
         action = event.get('action')
         key_str = event.get('key')
         key_type = event.get('key_type')
         key = self.convert_key_string(key_str, key_type)

         if action == 'press':
            self.keyboard_controller.press(key)
         else:
            self.keyboard_controller.release(key)
      elif event_type == 'mouse_click':
         button_str = event.get('button')
         x = event.get('x')
         y = event.get('y')
         pressed = event.get('pressed')
         button = self.convert_button_string(button_str)
         
         self.mouse_controller.position = (x, y)
         
         if pressed:
            self.mouse_controller.press(button)
         else:
            self.mouse_controller.release(button)
      elif event_type == 'mouse_scroll':
         x = event.get('x')
         y = event.get('y')
         dx = event.get('dx')
         dy = event.get('dy')
         
         self.mouse_controller.position = (x, y)
         self.mouse_controller.scroll(dx, dy)
