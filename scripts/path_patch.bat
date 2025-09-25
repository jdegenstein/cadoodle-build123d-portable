@echo off
rem = r"""
:: batch file that will be ignored by Python

SET PARENT_PATH=%CD%
SET PYTHON_REL_PATH=pyinst\cpython-3.12.11-windows-x86_64-none
SET FULL_PYTHON_PATH=%PARENT_PATH%\%PYTHON_REL_PATH%\python.exe
SET PYVENV_REL_PATH=.venv\pyvenv.cfg

%FULL_PYTHON_PATH% -x "%~f0" %*
exit /b %errorlevel%
:: End of batch file commands
"""
# beginning of what will be executed by python

import os

parent_path = os.environ["PARENT_PATH"]
python_rel_path = os.environ["PYTHON_REL_PATH"]
pyvenv_rel_path = os.environ["PYVENV_REL_PATH"]

# Read in the file
with open(pyvenv_rel_path, 'r') as file:
    filedata = file.readlines()

# Replace the target string
newdata = []
for line in filedata:
    if "home" in line:
        newdata.append(f"home = {parent_path}\\{python_rel_path}\n")
    else:
        newdata.append(line)

# Write the file out again
with open(pyvenv_rel_path, 'w') as file:
    file.writelines(newdata)
