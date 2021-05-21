import os
import sys

python_path = os.path.abspath(os.path.join(os.getcwd(), "topaz_test"))
print(python_path)

if python_path not in sys.path:
    sys.path.insert(0, python_path)
