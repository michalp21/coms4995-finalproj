import os
from ctypes import *

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_file_path = os.path.join(dir_path, 'libplayer.so')

player = CDLL(lib_file_path)
