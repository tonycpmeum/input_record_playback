from plyer import notification

def notife(title_message: list[str], app_name: str, app_icon: str):
      
   notification.notify(
      app_name=app_name, 
      app_icon=app_icon,
      title=title_message[0],
      message=title_message[1],
      timeout=2,
   )