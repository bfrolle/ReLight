import os

import nuke

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
RELIGHT_SRC_PATH = os.path.join(ROOT_PATH,"src") 

nuke.pluginAddPath(RELIGHT_SRC_PATH)