from PyQt5.QtWidgets import QMainWindow, QHeaderView, QApplication, QAbstractItemView, \
                            QMessageBox, QTreeView, QTableView, QSplitter, QAction, QMenu, \
                            QStatusBar, QInputDialog, QToolBar
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QKeySequence
from PyQt5.QtCore import Qt, QRect, QSortFilterProxyModel, QSettings, QSize, QTranslator

from PyQt5.QtCore import pyqtSlot
import re,os,sys
from pathlib import Path
from peewee import *
from PIL.ExifTags import TAGS
import shutil
import copy
import PlUtils as pl



class PalaeolamaMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(pl.resource_path('icons/Palaeolama.png')))
        self.setWindowTitle("{} v{}".format(self.tr("Palaeolama"), pl.PROGRAM_VERSION))

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    #with open('log.txt', 'w') as f:
    #    f.write("hello\n")
    #    # current directory
    #    f.write("current directory 1:" + os.getcwd() + "\n")
    #    f.write("current directory 2:" + os.path.abspath(".") + "\n")
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(pl.resource_path('icons/Palaeolama.png')))
    app.settings = QSettings(QSettings.IniFormat, QSettings.UserScope,pl.COMPANY_NAME, pl.PROGRAM_NAME)

    translator = QTranslator()
    app.language = app.settings.value("language", "en")
    translator.load(pl.resource_path("translations/Palaeolama_{}.qm".format(app.language)))
    app.installTranslator(translator)

    myWindow = PalaeolamaMainWindow()
    myWindow.show()

    # enter event loop
    app.exec_()


''' 
How to make an exe file

# single file
pyinstaller --onefile --noconsole --add-data "icons/*.png;icons" --add-data "translations/*.qm;translations" --icon="icons/Palaeolama.png" Palaeolama.py

# single directory
pyinstaller --onedir --noconsole --add-data "icons/*.png;icons" --add-data "translations/*.qm;translations" --icon="icons/Palaeolama.png" --noconfirm Palaeolama.py

# Translation
pylupdate5 Palaeolama.py -ts translations/Palaeolama_en.ts
pylupdate5 Palaeolama.py -ts translations/Palaeolama_ko.ts
# pylupdate5 Palaeolama.py -ts translations/Palaeolama_ja.ts

linguist

'''