import os
import persistent
import shutil
import sys
import codecs
from concurrent.futures import ThreadPoolExecutor

from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import *

import traceback

BASE_PATH = os.path.dirname(__file__)

def unzip(serial, output_path):
    try:
        with open(f"{BASE_PATH}/ZIP_{serial}", "rb") as f:
            data = f.read()
        with open(f"{BASE_PATH}/ZIP_{serial}_TEMP.zip", "wb") as f:
            f.write(data)
        shutil.unpack_archive(f"{BASE_PATH}/ZIP_{serial}_TEMP.zip", output_path)
        os.remove(f"{BASE_PATH}/ZIP_{serial}_TEMP.zip")
    except Exception:
        print(f"\n{traceback.format_exc()}")
        return

class MainWindow():
    "Installer main window."
    def __init__(self):
        super().__init__()
        self.path_state = "Set installation path."
        self.path_state_wrap = persistent.textwrap(self.path_state, 22)
        self.path = None
        self.root = Tk()
        root_x = 400
        root_y = 100
        self.root.title(f"{persistent.project_name} Setup")
        self.root.geometry(f'{root_x}x{root_y}')
        self.root.resizable(width=False, height=False)

        self.label = Label(self.root, text=f"{persistent.project_name} Setup", font=0)
        self.label.place(x=25, y=15)

        self.select_path = Button(text="Select path", command=self.select_path_func)
        self.select_path.place(x=25, y=50)

        self.install = Button(text="Install", command=self.install_func)
        self.install.place(x=100, y=50)
        self.install["state"] = DISABLED

        self.label1 = Label(self.root, text=self.path_state_wrap, font=0)
        self.label1.place(x=165, y=50)
        self.label1.after(500, self.label1.update())

        self.root.mainloop()

    def select_path_func(self):
        self.path = askdirectory(parent=self.root, title='Select path of files')
        if self.path is "": raise ValueError("Path must be a directory, not a None.")
        else:
            self.path_state = f"Path: {self.path}"
            self.path_state_wrap = persistent.textwrap(self.path_state, 22)
            self.label1.config(text=self.path_state_wrap, font=0)
            self.install["state"] = NORMAL

    def install_func(self):
        showinfo(f"{persistent.project_name} Setup: Started", "Installation on the specified path is ready!\nPress OK to start.")
        try:
            with ThreadPoolExecutor(10) as thread:
                _ = [thread.submit(unzip, i, self.path) for i in range(persistent.zip_amount)]
        except Exception as e:
            showinfo(f"{persistent.project_name} Setup: Failed", f"Installation on the specified path is failed!\n\nError:{e}")
            return
        showinfo(f"{persistent.project_name} Setup: Completed", "Installation on the specified path is successfully completed!")