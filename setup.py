import cx_Freeze
import sys
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\brandonwood\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\brandonwood\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

include_files = ["favicon.ico", "intern/emailer.py", "intern/intern.py", "intern/invoice.py", "intern/utils.py", r"C:\Users\brandonwood\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll", r"C:\Users\brandonwood\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll"]

if sys == "Win32":
    base = "Win32Gui"

base = None

executables = [cx_Freeze.Executable("app.py", base = base, icon = 'favicon.ico')]

cx_Freeze.setup(
    name = "Intern",
    options = {
        "build_exe": {
            "packages": ["bs4", "openpyxl", "tkinter", "imaplib"],
            "include_files": include_files 
        }
    },
    version = "1.0.0",
    description = "In-house automation for GIBC digital. Can be used to scrape any email account that recieves form submissions from Square Space.",
    executables = executables 
)
