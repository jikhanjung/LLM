import sys, os

COMPANY_NAME = "PaleoBytes"
PROGRAM_NAME = "Palaeolama"
PROGRAM_VERSION = "0.1.0"

DB_LOCATION = ""

#print(os.name)
USER_PROFILE_DIRECTORY = os.path.expanduser('~')

DEFAULT_DB_DIRECTORY = os.path.join( USER_PROFILE_DIRECTORY, PROGRAM_NAME )
DEFAULT_STORAGE_DIRECTORY = os.path.join(DEFAULT_DB_DIRECTORY, "data/")

if not os.path.exists(DEFAULT_DB_DIRECTORY):
    os.makedirs(DEFAULT_DB_DIRECTORY)
if not os.path.exists(DEFAULT_STORAGE_DIRECTORY):
    os.makedirs(DEFAULT_STORAGE_DIRECTORY)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)