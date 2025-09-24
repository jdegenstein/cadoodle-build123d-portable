#!/usr/bin/env bash
PARENT_PATH=`pwd`
PYTHON_REL_PATH="pyinst/cpython-3.12.11-linux-x86_64-gnu/bin"
FULL_PYTHON_PATH="$PARENT_PATH/$PYTHON_REL_PATH/python"
PYVENV_REL_PATH=".venv/pyvenv.cfg"

# run an embedded python script to find and replace
$FULL_PYTHON_PATH << END
# Read in the file
with open("$PYVENV_REL_PATH", 'r') as file:
    filedata = file.readlines()

# Replace the target string
newdata = []
for line in filedata:
    if "home" in line:
        newdata.append("home = $PARENT_PATH/$PYTHON_REL_PATH\n")
    else:
        newdata.append(line)

# Write the file out again
with open("$PYVENV_REL_PATH", 'w') as file:
    file.writelines(newdata)
END
