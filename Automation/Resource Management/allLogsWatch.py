# this file watches for changes in allLogs.json. If the file is modified in any way, then it triggers BM_Prediction.py to execute.
# in turn, predictive values will be outputted as json which can then be displayed by the frontend.
# in case of test failure, a 2nd implementation option is provided below (currently commented out). This would go on commands.py right after it json dumps into
# allLogs.json, calling for BM_Prediction to execute.

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import os

input_file = "User_Interface/UI_Main/client/src/telemetry_json/allLogs.json"
script_to_run = "Automation/Resource Management/BM_Prediction.py"

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if os.path.abspath(event.src_path) == input_file:
            # print("debug statement. allLogs.json has been modified and am running prediction script.")
            subprocess.run(["python3", script_to_run])

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(input_file), recursive=False)
    observer.start()
    # print("watching for changes")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



### option 2 (if applicable): Add this one line of code to commands.py:
# import subprocess

# # after writing the relevant JSON file
# subprocess.run(["python3", "Automation/Resource Management/BM_Prediction.py"])