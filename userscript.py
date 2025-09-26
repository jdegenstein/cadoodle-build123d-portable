"""
An example script defining a build123d object.
This file will be executed by the cadexport tool.
"""
from build123d import *
from ocp_vscode import *

# The variable 'uservar' will be targeted by the command-line tool for export.
# It's a simple box with a hole through it.
uservar = Box(100, 100, 20)
uservar -= Cylinder(radius=25, height=20)

# You can define other variables too; they will be ignored unless you
# specify them in the command.
some_other_part = Sphere(30)

# A simple text message to show that the script is being executed.
print("userscript.py has been successfully executed.")
show(uservar)