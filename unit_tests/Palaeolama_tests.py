import unittest
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QApplication, QAbstractItemView, \
                            QMessageBox, QTreeView, QTableView, QSplitter, QAction, QMenu, \
                            QStatusBar, QInputDialog, QToolBar

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
import PlUtils as pu
from Palaeolama import PalaeolamaMainWindow

class TestPalaeolamaMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.main_window = PalaeolamaMainWindow()

    def test_window_title(self):
        expected_title = "{} v{}".format(self.main_window.tr("Palaeolama"), pu.PROGRAM_VERSION)
        self.assertEqual(self.main_window.windowTitle(), expected_title)

    def test_window_icon(self):
        expected_icon = QIcon(pu.resource_path('icons/Palaeolama.png'))
        self.assertEqual(self.main_window.windowIcon(), expected_icon)

if __name__ == '__main__':
    unittest.main()