from utils import *

clear()
print(f"""

            Pytup: Creating Setup for Anything in Python! (by tetyastan)

GUIDE:
    
    In order to successfully use the utility, create a folder
    and place in it all the files you would like to put in your installer file.
    
    The utility will now ask you to specify the path to the created folder.
""")

path = Path().returnpath()

print(f"""
Your files folder path is:
    {path}.
The utility will create an installer that stores exactly these files.

""")

path_confirm = confirm('path_confirm', f"Are you sure?")
if path_confirm.get('path_confirm') is 'Yes': pass
else: sys.exit()

print(f"""
Now enter the name of your project. The utility will use this project name in the text of the installer GUI.""")
project_name = input("")
if project_name is '' or project_name is None: raise ValueError("Project name can't be empty.")
project_name = project_name.replace(" ", "")

print(f"""
Your project name is:
    {project_name}.

""")

path_confirm = confirm('path_confirm', f"Are you sure?")
if path_confirm.get('path_confirm') is 'Yes': pass
else: sys.exit()

print(f"""
How many files would you like to divide the archives into?

WARNING: Too small a value for a large number of files may result in creating an OVERLY large number of archives.
This can cause unpacking while the installer is running to take up a VERY large amount of computer resources,
and can cause the program to crash.
""")
files_len = input()
if files_len is '' or files_len is '0' or files_len is None: raise ValueError("Number of files can't be empty, be equal to 0, or be a string.")
files_len = int(files_len)

print(f"""
You're going to divide the files by
    {files_len}
per archive.
The utility will use this project name in the text of the installer GUI.

""")

path_confirm = confirm('path_confirm', f"Are you sure?")
if path_confirm.get('path_confirm') is 'Yes': pass
else: sys.exit()

if not os.path.exists(f"{BASE_PATH}/tmp/"):
    os.makedirs(f"{BASE_PATH}/tmp/")
if os.listdir(f"{BASE_PATH}/tmp/"):
    print('\nClearing folder of temp...')
    shutil.rmtree(f"{BASE_PATH}/tmp/")
    os.makedirs(f"{BASE_PATH}/tmp/")
print('\nCreating...\n')
output_path = Archive().output_path
print('     Temp archive...')
print('         Creating...')
Archive().create(path, files_len)
print('     Scripts for installer...')
print('         Copying files...')
InstallerGen(project_name).copy_data()
#print('     Cleaning...')
#print('         Removing: Temp archive...')
#Archive().remove(output_path)
print('\nSuccess!\n')