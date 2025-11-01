import json
from platformdirs import user_config_path
from PySide6 import QtWidgets as Widget
from PySide6 import QtCore    as Core
from PySide6.QtCore import Qt
from modules.config_manager import DATA_DIR

class CustomListView(Widget.QListView):
   def __init__(self, parent=None):
      super().__init__(parent=parent)
      self.setEditTriggers(Widget.QAbstractItemView.DoubleClicked | Widget.QAbstractItemView.EditKeyPressed)

class CustomModel(Core.QAbstractListModel):
   def __init__(self):
      super().__init__()
      self.script_file = DATA_DIR / "script_data.json"
      self.script_data = self._load_script_data()

   @Core.Slot(list)
   def add_script(self, new_script):
      position = len(self.script_data) # insert at end
      self.beginInsertRows(Core.QModelIndex(), position, position)
      new_item = {f"script_{len(self.script_data) + 1}": new_script}
      self.script_data.append(new_item)
      self._save_script_data()
      self.endInsertRows()

   def remove_script(self, position: int):
      if position < 0 or position > len(self.script_data): return
      self.beginRemoveRows(Core.QModelIndex(), position, position)
      self.script_data.pop(position)
      self._save_script_data()
      self.endRemoveRows()
   
   def get_script_events(self, index):
      if 0 <= index < len(self.script_data):
         selected_script = self.script_data[index]
         script_events = next(iter(selected_script.values()))
         sorted_events = sorted(script_events, key=lambda x: x.get('time', 0))
         return sorted_events
      return None
   
   def _load_script_data(self) -> list:
      self.script_file.parent.mkdir(parents=True, exist_ok=True)

      if not self.script_file.exists():
         self.script_file.write_text("[]")

      if self.script_file.stat().st_size == 0:
         return []
      
      try: 
         return json.loads(self.script_file.read_text())
      except OSError:
         print("Warning: Invalid JSON in script file. Initializing with empty data.")
         self.script_file.write_text("[]")
         return []
      
   def _save_script_data(self):
      self.script_file.parent.mkdir(parents=True, exist_ok=True)
      self.script_file.write_text(json.dumps(self.script_data, indent=3))

   # =============== Required QAbstractItemModel Methods =============== #
   def rowCount(self, parent=Core.QModelIndex()) -> int:
      if parent.isValid():
         return 0
      return len(self.script_data)
   
   # Provide data to model view
   def data(self, index, role=Qt.DisplayRole):
      if not index.isValid() or not (0 <= index.row() < len(self.script_data)):
         return None
      
      item = next(iter(self.script_data[index.row()]))
      if role == Qt.DisplayRole:
         return str(item)
      elif role == Qt.EditRole:
         return str(item)

      return None

   # Modify data, initiated by model view
   def setData(self, index, value, role=Qt.EditRole) -> bool:
      if not index.isValid() or not (0 <= index.row() < len(self.script_data)):
         return False
      
      if value == "" or value == " " or value == "  ":
         return False
            
      if role == Qt.EditRole:
         data_obj = self.script_data[index.row()]
         data_name_old = next(iter(data_obj))
         data_obj[value] = data_obj.pop(data_name_old)

         self.script_file.write_text(json.dumps(self.script_data, indent=3))
         self.dataChanged.emit(index, index)
         return True

      return False
   
   def flags(self, index):
      if not index.isValid():
         return Qt.NoItemFlags
      return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
   
list_model = CustomModel()