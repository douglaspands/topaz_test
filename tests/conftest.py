import os
import sys

python_path = os.path.abspath(os.path.join(os.getcwd(), "topaz_test"))

if python_path not in sys.path:
    sys.path.insert(0, python_path)
