import os
import shutil
import persistent
import threading
import glob

from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import *

BASE_PATH = os.path.dirname(__file__)
    
class Archive():
    "File archiving management."
    def unzip(self, path, output_path):
        shutil.unpack_archive(path, output_path, 'zip')

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
        zip_amount = len(glob.glob1(BASE_PATH,"*.zip"))
        showinfo(f"{persistent.project_name} Setup: Started", "Installation on the specified path is ready!\nPress OK to start.")

        for i in range(zip_amount):
            thread = threading.Thread(target=Archive.unzip, args=(None, f"{BASE_PATH}/ZIP_{i}.zip", self.path))
            thread.start()
            thread.join()

        showinfo(f"{persistent.project_name} Setup: Completed", "Installation on the specified path is successfully completed!")