import os
import sys
import time
from datetime import date
import inquirer
import shutil
import zipfile
import subprocess

import tkinter as tk
from tkinter.filedialog import askdirectory

from cryptography.fernet import Fernet

DEBUG_EXE_GENERATE = False
CLEAN_TEMP_AFTER_GENERATION = True
BASE_PATH = os.path.dirname(__file__)
CHUNKS = 0

k = Fernet.generate_key()

def clear():
    "Clears the terminal."
    os.system('cls' if os.name == 'nt' else 'clear')

def menu(key,msg,choices):
    "Using Inquirer to create a menu."
    x = inquirer.prompt([inquirer.List(
                            key,
                            message=msg,
                            choices=choices,
                            )])
    return x

def confirm(key,msg):
    "Using Inquirer to create a confirm menu."
    x = menu(key, msg, ["Yes", "No"])
    return x

def copytree(src, dst, symlinks=False, ignore=None):
    "Function to copy a branch of files using os and shutil."
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s): shutil.copytree(s, d, symlinks, ignore)
        else: shutil.copy2(s, d)

def split_files(current_dir, chunks):
    x = []
    for root, dirs, files in os.walk(current_dir):
        for file in files: x.append(f"{root}/{file}")
        for dir in dirs: x.append(f"{root}/{dir}")
    for i in range(0, len(x), chunks): yield x[i:i + chunks]
    return x

class Path():
    "Creates a window for selecting a path. Used in conjunction with a variable to save."
    def __init__(self):
        window = tk.Tk()
        window.withdraw()
        self.path = askdirectory(parent=window, title='Select path of files')
        if self.path is "": raise ValueError("Path must be a directory, not a None.")
    def returnpath(self): return self.path
    
class Archive():
    "File archiving management."
    def __init__(self):
        self.output_path = f"{BASE_PATH}/tmp"
        self.encode = Fernet(k)
    def create(self, path, chunks, compression, compresslevel):
        for i in split_files(path, chunks):
            global CHUNKS
            resultzip = zipfile.ZipFile(f"{self.output_path}/ZIP_{CHUNKS}.zip", "w", compression=compression, compresslevel=compresslevel)
            for i in i: resultzip.write(i, i)
            resultzip.close()
            CHUNKS+=1
        for i in [each for each in os.listdir(self.output_path) if each.endswith('.zip')]:
            with open(f"{self.output_path}/{i}", "rb") as f:
                data = f.read()
                f.close()
            encrypted = self.encode.encrypt(data)
            file = i.split('.')[0]
            with open(f"{self.output_path}/{file}", "wb") as f:
                f.write(encrypted)
        for i in [each for each in os.listdir(self.output_path) if each.endswith('.zip')]:
            os.remove(f"{self.output_path}/{i}")

class InstallerGen():
    def __init__(self, project_name):
        self.project_name = project_name
        self.datapath = f"{BASE_PATH}/data"
        self.genpath = f"{BASE_PATH}/tmp/generated/GEN_{self.project_name}"
        self.output_path = f"{BASE_PATH}/tmp"
        self.genfiles = []
    def copy_data(self):
        if not os.path.exists(self.genpath): pass
        else: shutil.rmtree(self.genpath)
        copytree(self.datapath, self.genpath)
        for i in range(CHUNKS): shutil.move(f"{self.output_path}/ZIP_{i}", self.genpath)
        with open(f"{self.genpath}/persistent.py", "w") as f:
            f.write(f"""from cryptography.fernet import Fernet
def textwrap(str, max):
    if len(str) > max: x = f"{{str[:max]}}..."
    else: x = str
    return x
project_name = textwrap("{self.project_name}", 24)
zip_amount = {CHUNKS}
##
## Part of file encoding.
##
k = {k}
encode = Fernet(k)""")
    def _generate_exe(self):
        for root, dirs, files in os.walk(self.genpath):
            for file in files:
                if file != str("__main__.py"): self.genfiles.append(f"{root}/{file}")
            for dir in dirs: self.genfiles.append(f"{root}/{dir}")
    def generate_exe(self):
        pyi = [r'pyinstaller',f"{self.genpath}/__main__.py",'--name',self.project_name,'--windowed','--noconsole',f'--distpath', f'{BASE_PATH}/generated']
        for root, dirs, files in os.walk(self.genpath):
            for file in files:
                if file != str("__main__.py"): self.genfiles.append(f"{root}/{file}:.")
            for dir in dirs: self.genfiles.append(f"{root}/{dir}:.")
        for i in self.genfiles:
            pyi.append(f'--add-binary')
            pyi.append(f"{i}")
        if not DEBUG_EXE_GENERATE: subprocess.call(pyi, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else: subprocess.call(pyi)