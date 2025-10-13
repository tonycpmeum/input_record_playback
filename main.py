import sys
import json
import time
import os
from PySide6 import QtWidgets as Widget
from PySide6 import QtCore    as Core
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QKeyEvent, QShortcut, QKeySequence
from pynput import mouse, keyboard
from pyside6_ui.monday import Ui_MainWindow
from model_view import CustomModel, CustomListView

max_scripts = 10

class ScriptRecorder:
   def __init__(self):
      self.keyboard_listener = None
      self.mouse_listener = None
      self.start_time = None

      self.is_recording = False
      self.record_buffer = []

      self.last_mouse_sample_time = 0
      self.mouse_sample_interval = 0.1  # 100ms between samples

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
      print("Listener started")

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

      event = {
         'type': 'mouse_move',
         'x': x,
         'y': y,
         'time': time_elapsed
      }
      self.record_buffer.append(event)

      if time_elapsed - self.last_mouse_sample_time >= self.mouse_sample_interval:
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

class ScriptPlayer:
   def __init__(self):
      self.mouse_controller = mouse.Controller()
      self.keyboard_controller = keyboard.Controller()
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
   
   def play_script(self, script_events):
      if self.is_playing: return
      if not script_events: return
      self.is_playing = True
      
      sorted_events = sorted(script_events, key=lambda x: x.get('time', 0))
      start_time = time.monotonic()

      print(f"Playing script with {len(sorted_events)} events")
      for event in sorted_events:
         # Wait until the right time for this event
         event_time = event.get('time', 0)
         while time.monotonic() - start_time < event_time and self.is_playing:
            time.sleep(0.001)  # Small sleep to prevent busy waiting
               
         if not self.is_playing:
            break
               
         self._execute_event(event)

   def stop_playing(self):
      self.is_playing = False
   
   def _execute_event(self, event):
      event_type = event.get('type')
      
      if event_type == 'mouse_click':
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
      elif event_type == 'mouse_move':
         x = event.get('x')
         y = event.get('y')
         self.mouse_controller.position = (x, y)
      elif event_type == 'mouse_scroll':
         x = event.get('x')
         y = event.get('y')
         dx = event.get('dx')
         dy = event.get('dy')
         
         self.mouse_controller.position = (x, y)
         self.mouse_controller.scroll(dx, dy)
      elif event_type == 'keyboard':
         action = event.get('action')
         key_str = event.get('key')
         key_type = event.get('key_type')
         key = self.convert_key_string(key_str, key_type)

         if action == 'press':
            self.keyboard_controller.press(key)
         else:
            self.keyboard_controller.release(key)

class MainWindow(Widget.QMainWindow):
   def __init__(self):
      super().__init__()
      self._init_variables()

      self.setWindowTitle("AutoClicker")
      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)

      self._setup_ui_references()
      self.setFixedSize(self.size())
      self.list_view.setModel(self.list_model)

      self._connect_signals()
      
   def _init_variables(self):
      self.script_recorder = ScriptRecorder()
      self.script_player = ScriptPlayer()
      self.list_model = CustomModel()
      self.script_sel_index: int | None = None

   def _setup_ui_references(self):
      self.record_btn = self.ui.record_btn
      self.delete_btn = self.ui.delete_btn
      self.start_btn = self.ui.start_btn
      self.list_view = self.ui.listView

   def _connect_signals(self):
      self.record_btn.clicked.connect(self.record_btn_clicked)
      self.delete_btn.clicked.connect(self.del_data)
      self.start_btn.clicked.connect(self.play_script_by_index)
      self.start_btn.clicked.connect(self.update_ui_state)
      self.list_view.selectionModel().selectionChanged.connect(self.on_selection_changed)

      self.list_model.rowCountChanged.connect(self.update_ui_state)
      self.update_ui_state()

   @Core.Slot()
   def update_ui_state(self):
      row_count = self.list_model.rowCount()
      self.record_btn.setEnabled(max_scripts > row_count)

      self.start_btn.setEnabled(row_count > 0 and self.script_sel_index is not None)
      print("UI UPDATED")
      if self.script_player.is_playing:
         self.start_btn.setText("Stop")
      else:
         self.start_btn.setText("Start")

      has_selection = self.script_sel_index is not None
      self.delete_btn.setEnabled(has_selection and row_count > 0)

      if self.script_recorder.is_recording == True:
         self.record_btn.setText("Stop")
      else: 
         self.record_btn.setText("Record")
      
      if max_scripts <= row_count:
         self.record_btn.setToolTip(f"Maximum {max_scripts} scripts reached")
      
   @Core.Slot()
   def record_btn_clicked(self):
      # NOE START Recording
      if self.script_recorder.is_recording == False:
         if self.list_model.rowCount() >= max_scripts: return
         self.script_recorder.start_listening()
      # NOW END recording
      else:
         self.script_recorder.stop_listening()
         self.list_model.add_script(self.script_recorder.record_buffer)
      self.update_ui_state()

   @Core.Slot(Core.QItemSelection, Core.QItemSelection)
   def on_selection_changed(self, selected, deselected):
      if selected.indexes():
         current_index = selected.indexes()[0]
         current_row = current_index.row()
         print(f"Selected index: {current_row}")
         self.script_sel_index = current_row
      else:
         self.script_sel_index = None
      self.update_ui_state()

   @Core.Slot()
   def del_data(self):
      current_index = self.list_view.currentIndex()
      row_count = self.list_model.rowCount()

      self.list_model.remove_script(current_index.row())
      
      # After deletion, update selection if needed
      if row_count > 0:
         if current_index.row() < row_count:
            # Select the same position (now has different content)
            new_index = self.list_model.index(current_index.row())
         else:
            # If we deleted the last item, select the new last item
            new_index = self.list_model.index(row_count - 1)
         self.list_view.setCurrentIndex(new_index)
      self.update_ui_state()

   def _setup_shortcuts(self):
      pass

   def play_script_by_index(self):
      index = self.script_sel_index
      all_scripts = self.list_model.script_data

      if index < 0 or index >= len(all_scripts):
         print(f"No script at index {index}")
         return
      if self.script_player.is_playing:
         print("Already playing a script, please wait...")
         return
      
      script_dict = all_scripts[index]
      script_name = next(iter(script_dict))
      script_events = script_dict[script_name]
      
      print(f"Playing script {index + 1}: {script_name}")
      self.script_player.play_script(script_events)

      self.script_player.stop_playing()


if __name__ == "__main__":
   app = Widget.QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())


