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
    QGridLayout,
)

class Layout(QWidget):
    def __init__(self, layoutType):
        super().__init__()

        self.widget = QWidget()

        match layoutType:
            case "vertical":
                self.layout = QVBoxLayout()
            case "horizontal":
                self.layout = QHBoxLayout()
            case "stacked":
                self.layout = QStackedLayout()
            case "grid":
                self.layout = QGridLayout()
        
    def _updateWidget(self):
        self.widget.setLayout(self.layout)

    def addLayout(self, layoutType):
        newLayout = Layout(layoutType)
    
    def addLabel(self, text, cssSheet):
        label = QLabel(text)
        label.setStyleSheet(cssSheet)
        self.layout.addWidget(label)
