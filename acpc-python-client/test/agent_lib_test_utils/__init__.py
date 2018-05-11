import os
from ctypes import *

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_file_path = os.path.join(dir_path, 'libtestutils.so')

test_utils = CDLL(lib_file_path)
