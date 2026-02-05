from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from layout import Layout

class DraftPositionCard(Layout):
    def __init__(self):
        super().__init__('vertical')

        self.addLayout('horizontal')