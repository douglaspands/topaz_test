import os


def start():
    os.system("python ./topaz_test")


def test():
    os.system("pytest")


def lint():
    os.system("flake8 .")


def requirements():
    os.system("poetry export -f requirements.txt --output requirements.txt")
