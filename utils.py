import os
import sys
import time
from datetime import date
import inquirer
import shutil
import zipfile

import tkinter as tk
from tkinter.filedialog import askdirectory

BASE_PATH = os.path.dirname(__file__)
CHUNKS = 0

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
        self.output_path = f"{BASE_PATH}/tmp/ZIP"
    def create(self, path, chunks, compression, compresslevel):
        for i in split_files(path, chunks):
            global CHUNKS
            resultzip = zipfile.ZipFile(f"{self.output_path}_{CHUNKS}.zip", "w", compression=compression, compresslevel=compresslevel)
            for i in i: resultzip.write(i, i)
            CHUNKS+=1

class InstallerGen():
    def __init__(self, project_name):
        self.project_name = project_name
        self.datapath = f"{BASE_PATH}/data/"
        self.genpath = f"{BASE_PATH}/tmp/generated/GEN_{self.project_name}/"
        self.output_path = f"{BASE_PATH}/tmp/ZIP"
    def copy_data(self):
        if not os.path.exists(self.genpath): pass
        else: shutil.rmtree(self.genpath)
        copytree(self.datapath, self.genpath)
        for i in range(CHUNKS): shutil.move(f"{self.output_path}_{i}.zip", self.genpath)
        with open(f"{self.genpath}/persistent.py", "w") as f:
            f.write(f"""
def textwrap(str, max):
    if len(str) > max: x = f"{{str[:max]}}..."
    else: x = str
    return x
project_name = textwrap("{self.project_name}", 24)""")