import os

from classes.settings.Settings import load_settings
from classes.startup.Startup import Startup

cwd = os.getcwd() + "\\"
load_settings(cwd)
startup = Startup(cwd)
startup.run()
