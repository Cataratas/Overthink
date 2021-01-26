import sys
from cx_Freeze import setup, Executable

includes = ["os", "pygame", "pygame.locals", "random", "pickle", "time", "json", "pyperclip", "sys", "reportlab", "fitz", "PyPDF2", "win32api"]
excludes = ["tkinter", "test"]
include_files = ["config.json", "Functions.py", "Games.py", "./Buttons/", "./Fonts/", "./Layout/", "./Modules/", "./Quizzes/", "icon.png", "Variables.py", "Quiz.pdf"]
packages = []

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Overthink",
      version="1.0",
      options={"build_exe": {"includes": includes, "excludes": excludes, "packages": packages, "include_files": include_files}},
      executables=[Executable("Overthink.pyw", base=base, icon="icon.ico")])
