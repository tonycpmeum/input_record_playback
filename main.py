import sys
import json
import time
import os
from PySide6 import QtWidgets as Widget
from PySide6 import QtCore    as Core
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication
from pyside6_ui.monday import Ui_MainWindow
from model_view import CustomModel, CustomListView
from recorder_player import ScriptPlayer, ScriptRecorder

max_scripts = 10
class MainWindow(Widget.QMainWindow):
   def __init__(self):
      super().__init__()
      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)
      self.setFixedSize(self.size())
      self.setWindowTitle("AutoClicker")
      QApplication.setStyle("Fusion")

      self._init_variables()
      self._setup_ui_references()
      self.list_view.setModel(self.list_model)

      self._connect_signals()
      self.update_ui_state()
      
   def _init_variables(self):
      self.script_recorder = ScriptRecorder()
      self.script_player = ScriptPlayer()
      self.list_model = CustomModel()
      self.script_sel_index: int | None = None
      self.script_enabled = False

   def _setup_ui_references(self):
      self.record_btn = self.ui.record_btn
      self.delete_btn = self.ui.delete_btn
      self.play_btn = self.ui.start_btn
      self.list_view = self.ui.listView
      self.script_checkbox = self.ui.enable_script_checkbox
      self.script_container = self.ui.script_container
      self.click_container = self.ui.click_container

   def _connect_signals(self):
      self.record_btn.clicked.connect(self.record_btn_clicked)
      self.delete_btn.clicked.connect(self.del_btn_clicked)
      self.play_btn.clicked.connect(self.play_btn_clicked)
      self.script_checkbox.toggled.connect(self.on_script_toggled)
      self.list_view.selectionModel().selectionChanged.connect(self.on_selection_changed)

   def update_ui_state(self):
      self.script_container.setEnabled(self.script_enabled)
      self.click_container.setEnabled(not self.script_enabled)

      row_count = self.list_model.rowCount()
      has_selection = self.script_sel_index is not None

      self.record_btn.setEnabled(max_scripts > row_count)
      self.delete_btn.setEnabled(row_count > 0 and has_selection)
      self.play_btn.setEnabled((row_count > 0 and has_selection) or not self.script_enabled)

      if self.script_recorder.is_recording == True:
         self.record_btn.setText("Stop")
      else: 
         self.record_btn.setText("Record")
      
      if max_scripts <= row_count:
         self.record_btn.setToolTip(f"Maximum {max_scripts} scripts reached")
      
   @Core.Slot()
   def record_btn_clicked(self):
      # NOW START Recording
      if self.script_recorder.is_recording == False:
         if self.list_model.rowCount() >= max_scripts: return
         self.script_recorder.start_listening()
      # NOW END recording
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
      index = self.script_sel_index
      if index is None: return

      script_events = self.list_model.get_script_events(index)
      # Use threading to disable script_related buttons during playback
      self.script_player.play_script(script_events)
      self.script_player.stop_playing()
      self.update_ui_state()

   @Core.Slot(bool)
   def on_script_toggled(self, state: bool):
      self.script_enabled = state
      if state == False:
         self.list_view.clearSelection()
         self.list_view.setCurrentIndex(Core.QModelIndex())
         selection_model = self.list_view.selectionModel()
         if selection_model: 
            selection_model.clearSelection()
         self.script_sel_index = None
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


if __name__ == "__main__":
   app = Widget.QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())