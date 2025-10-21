import sys
import json
import time
import os
from PySide6 import QtWidgets as Widget
from PySide6 import QtCore    as Core
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication, QStyle
from pyside6_ui.monday import Ui_MainWindow
from model_view import CustomModel, CustomListView
from recorder_player import ScriptRecorder, PlaybackWorker
from config_manager import config

MAX_SCRIPTS = config.max_scripts

class MainWindow(Widget.QMainWindow):
   def __init__(self):
      super().__init__()
      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)
      self.setFixedSize(self.size())
      self.setWindowTitle("AutoClicker")
      # QApplication.setStyle("Fusion")
      self.setWindowOpacity(0.95)

      self._init_variables()
      self._setup_ui_references()
      self._init_threading()
      self._init_ui_state()
      self._connect_signals()
      
   def _init_variables(self):
      self.script_recorder = ScriptRecorder()
      self.list_model = CustomModel()
      self.script_sel_index: int | None = None

      # =============== CONFIG VARIABLES ====================
      self.single_click_interval: float = config.single_click_interval
      self.script_enabled: bool = config.script_enabled
      self.repeat_limited: bool = config.repeat_limited
      self.repeat_count: int = config.repeat_count

   def _setup_ui_references(self):
      self.record_btn = self.ui.record_btn
      self.delete_btn = self.ui.delete_btn
      self.play_btn = self.ui.start_btn
      self.list_view = self.ui.listView
      self.list_view.setModel(self.list_model)
      self.script_checkbox = self.ui.enable_script_checkbox
      self.script_container = self.ui.script_container
      self.click_container = self.ui.click_container
      self.repeat_x_times_radio = self.ui.repeat_times_radio
      self.repeat_x_times_input = self.ui.repeat_times_input
      self.click_interval_input = self.ui.click_interval_input
      self.stop_btn = self.ui.stop_btn
      self.mousebutton_cbbox = self.ui.button_combobox
      self.clicktype_cbbox = self.ui.clicktype_combobox

   def _init_ui_state(self):
      self.script_container.setEnabled(self.script_enabled)
      self.script_checkbox.setChecked(self.script_enabled)
      self.click_container.setEnabled(not self.script_enabled)
      self.stop_btn.setEnabled(False)
      self.play_btn.setEnabled(not self.script_enabled)
      self.repeat_x_times_radio.setChecked(self.repeat_limited)
      self.repeat_x_times_input.setValue(self.repeat_count)
      self.click_interval_input.setValue(self.single_click_interval*1000)
      self.clicktype_cbbox.setCurrentIndex(config.click_type - 1)

   def _connect_signals(self):
      self.record_btn.clicked.connect(self.record_btn_clicked)
      self.delete_btn.clicked.connect(self.del_btn_clicked)
      self.play_btn.clicked.connect(self.play_btn_clicked)
      self.stop_btn.clicked.connect(self.stop_btn_clicked)
      self.script_checkbox.toggled.connect(self.script_toggled)
      self.repeat_x_times_radio.toggled.connect(self.repeat_ltd_toggled)
      self.list_view.selectionModel().selectionChanged.connect(self.selection_changed)
      self.repeat_x_times_input.valueChanged.connect(self.repeat_change)
      self.click_interval_input.valueChanged.connect(self.interval_change)
      self.mousebutton_cbbox.currentTextChanged.connect(self.mousebutton_change)
      self.mousebutton_cbbox.setCurrentText(config.button_type.split('.')[1].capitalize())
      self.clicktype_cbbox.currentIndexChanged.connect(self.clicktype_change)

   def _init_threading(self):
      self.playback_thread = Core.QThread()
      self.playback_worker = PlaybackWorker()
      self.playback_worker.moveToThread(self.playback_thread)

      self.playback_worker.finished.connect(self.update_ui_state)
      self.playback_worker.started.connect(self.worker_started)
      self.playback_worker.progress.connect(self.update_status)

      self.playback_thread.start()

   def update_ui_state(self):
      self.script_container.setEnabled(self.script_enabled)
      self.click_container.setEnabled(not self.script_enabled)

      row_count = self.list_model.rowCount()
      has_selection = self.script_sel_index is not None

      can_record = (MAX_SCRIPTS > row_count and not self.playback_worker.is_playing)
      self.record_btn.setEnabled(can_record)

      can_delete = ((row_count > 0 and has_selection) and not self.script_recorder.is_recording and not self.playback_worker.is_playing)
      self.delete_btn.setEnabled(can_delete)

      can_play = ((row_count > 0 and has_selection or not self.script_enabled) and not self.script_recorder.is_recording and not self.playback_worker.is_playing)
      self.play_btn.setEnabled(can_play)
      self.stop_btn.setEnabled(self.playback_worker.is_playing)

      if self.script_recorder.is_recording == True:   
         self.record_btn.setText("Stop")
      else: 
         self.record_btn.setText("Record")
      
      if MAX_SCRIPTS <= row_count:
         self.record_btn.setToolTip(f"Maximum {MAX_SCRIPTS} scripts reached")
      
   @Core.Slot()
   def record_btn_clicked(self):
      # NOW START Recording
      if self.script_recorder.is_recording == False:
         if self.list_model.rowCount() >= MAX_SCRIPTS: return
         self.script_recorder.start_listening()
      else:
         self.script_recorder.stop_listening()
         self.list_model.add_script(self.script_recorder.record_buffer)

         # Select the last index (newly added script)
         last_index = self.list_model.rowCount() - 1
         if last_index >= 0:
            model_index = self.list_model.index(last_index)
            self.list_view.setCurrentIndex(model_index)
            self.list_view.selectionModel().select(model_index, Core.QItemSelectionModel.SelectCurrent)
            self.script_sel_index = last_index
      self.update_ui_state()

   @Core.Slot()
   def del_btn_clicked(self):
      current_index = self.list_view.currentIndex()
      if not current_index.isValid(): return

      current_row = current_index.row()
      self.list_model.remove_script(current_row)
      new_row_count = self.list_model.rowCount()
      # After deletion, update selection if needed
      if new_row_count > 0:
         if current_row < new_row_count:
            # Select the same position (now has different content)
            new_index = self.list_model.index(current_row)
         else:
            # If we deleted the last item, select the new last item
            new_index = self.list_model.index(new_row_count - 1)
         self.list_view.setCurrentIndex(new_index)
      self.update_ui_state()

   @Core.Slot()
   def play_btn_clicked(self):
      if self.script_enabled:
         index = self.script_sel_index
         if index is None: 
            return
         script_events = self.list_model.get_script_events(index)
         self.playback_worker.request_play_script.emit(script_events)
      else:
         self.playback_worker.request_play_single_click.emit()

   @Core.Slot(Core.QItemSelection, Core.QItemSelection)
   def selection_changed(self, selected, deselected):
      if selected.indexes():
         current_index = selected.indexes()[0]
         current_row = current_index.row()
         self.script_sel_index = current_row
      else:
         self.script_sel_index = None
      self.update_ui_state()

   # =============== CONFIG INPUTS ===============
   @Core.Slot(bool)
   def script_toggled(self, state: bool):
      self.script_enabled = state
      config.script_enabled = state
      if state == False:
         self.list_view.clearSelection()
         self.list_view.setCurrentIndex(Core.QModelIndex())
         selection_model = self.list_view.selectionModel()
         if selection_model: 
            selection_model.clearSelection()
         self.script_sel_index = None
      self.update_ui_state()

   @Core.Slot(bool)
   def repeat_ltd_toggled(self, state: bool):
      config.repeat_limited = state

   @Core.Slot(int)
   def repeat_change(self, times: int):
      config.repeat_count = times

   @Core.Slot()
   def stop_btn_clicked(self):
      self.playback_worker.stop()

   @Core.Slot(int)
   def interval_change(self, milliseconds: int):
      config.single_click_interval = milliseconds / 1000

   @Core.Slot(str)
   def mousebutton_change(self, string: str):
      config.button_type = "Button." + string.lower()

   @Core.Slot(int)
   def clicktype_change(self, index):
      config.click_type = index + 1

   # =============== THREAD SLOTS & FUNC ===============
   @Core.Slot(str)
   def update_status(self, message: str):
      print(f"{message}")

   @Core.Slot()
   def worker_started(self):
      self.update_ui_state()

   # Close app cleanup
   def closeEvent(self, event):
      self.playback_worker.stop()
      self.playback_thread.quit()
      self.playback_thread.wait(1000)
      event.accept()

if __name__ == "__main__":
   app = Widget.QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec()) 