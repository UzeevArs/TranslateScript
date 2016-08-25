import cx_Freeze
from cx_Freeze import setup, Executable

setup(
    name = "translateJP",
    version = "0.1",
    description = "Translate from Japan to English language",
    executables = [Executable("mainW.py")]
)