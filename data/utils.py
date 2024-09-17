import os
import persistent
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor

from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import *

BASE_PATH = os.path.dirname(__file__)
ZIP_PATH = os.path.join(sys._MEIPASS)
    
class Archive():
    "File archiving management."
    def unzip(self, serial, output_path):
        shutil.unpack_archive(f"{ZIP_PATH}/ZIP_{serial}.zip", output_path)

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
            with ThreadPoolExecutor(100) as thread:
                _ = [thread.submit(Archive.unzip, None, i, self.path) for i in range(persistent.zip_amount)]
        except Exception as e:
            showinfo(f"{persistent.project_name} Setup: Failed", f"Installation on the specified path is failed!\n\nError:{e}")
        showinfo(f"{persistent.project_name} Setup: Completed", "Installation on the specified path is successfully completed!")