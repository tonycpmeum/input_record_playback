from PySide6.QtWidgets import QDialog
import PySide6.QtWidgets as Widget
from config_manager import config
from pyside6_ui.playback_settings_dialog_ui import Ui_playback_settings_dialog

class PlaybackSettingsDialog(QDialog):
   def __init__(self, parent=None):
      super().__init__(parent)
      self.ui = Ui_playback_settings_dialog()  # Your specific UI class
      self.ui.setupUi(self)
      
      self.setWindowTitle("Playback settings")
      self.setFixedSize(self.size())

      self.speed_spinbox = self.ui.speed_spinbox
      self.speed_spinbox.setValue(config.playback_speed)
      self.speed_spinbox.valueChanged.connect(self.speed_change)

   def speed_change(self, val):
      config.playback_speed = val
