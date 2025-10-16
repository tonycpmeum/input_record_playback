import json
import os
from PySide6 import QtWidgets as Widget
from PySide6 import QtCore    as Core
from PySide6.QtCore import Qt

class CustomListView(Widget.QListView):
   def __init__(self, parent=None):
      super().__init__(parent=parent)
      self.setEditTriggers(Widget.QAbstractItemView.DoubleClicked | Widget.QAbstractItemView.EditKeyPressed)

class CustomModel(Core.QAbstractListModel):
   def __init__(self):
      super().__init__()
      self.file_path = "./data/script_data.json"
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
         return next(iter(selected_script.values()))
      return None
   
   def _load_script_data(self) -> list:
      directory = os.path.dirname(self.file_path)
      if directory: 
         os.makedirs(directory, exist_ok=True)

      if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
         with open(self.file_path, 'w') as f:
            json.dump([], f)
         return []
      
      try: 
         with open(self.file_path, 'r') as f:
            return json.load(f)
      except json.JSONDecodeError:
         # Handle case where JSON is invalid/corrupted
         print("Warning: Invalid JSON in script file. Initializing with empty data.")
         with open(self.file_path, 'w') as f:
            json.dump([], f)
         return []
      
   def _save_script_data(self):
      directory = os.path.dirname(self.file_path)
      if directory:
         os.makedirs(directory, exist_ok=True)
      with open(self.file_path, 'w') as f:
         json.dump(self.script_data, f, indent=3)

   # ===== Required QAbstractItemModel Methods ===== #
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

         with open (self.file_path, 'w') as f:
            json.dump(self.script_data, f, indent=3)
         
         self.dataChanged.emit(index, index)
         return True

      return False
   
   def flags(self, index):
      if not index.isValid():
         return Qt.NoItemFlags
      return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
   

