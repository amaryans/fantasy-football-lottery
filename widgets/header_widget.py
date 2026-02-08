"""
Header widget for the Fantasy Football Lottery application.
Displays the league logo and name.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QPixmap

from config.styles import HEADER
from config.config_manager import config


class HeaderWidget(QWidget):
    """Widget that displays the league header with logo and name."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Initialize and configure the header UI elements."""
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Logo image
        image_label = QLabel()
        pixmap = QPixmap(config.logo_path)
        pixmap = pixmap.scaledToHeight(150)
        image_label.setPixmap(pixmap)

        # League name text
        text_label = QLabel(config.league_name)
        text_label.setStyleSheet(HEADER)

        # Add widgets to layout
        layout.addWidget(image_label, alignment=Qt.AlignCenter)
        layout.addWidget(text_label, alignment=Qt.AlignCenter)

        self.setLayout(layout)
