"""
Lottery Window widget for the Fantasy Football Lottery application.
Displays the current owner selection and next pick button.
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap

from config.styles import LOTTERY_WINDOW_BACKGROUND, NEXT_PICK_BUTTON
from config.config_manager import config


class LotteryWindowWidget(QWidget):
    """
    Widget that displays the lottery window with owner card and next pick button.

    Signals:
        next_pick_clicked: Emitted when the next pick button is clicked
    """

    next_pick_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_started = False
        self._setup_ui()

    def _setup_ui(self):
        """Initialize and configure the lottery window UI elements."""
        main_layout = QHBoxLayout()

        # Create container widget with background style
        container_widget = QWidget()
        container_widget.setStyleSheet(LOTTERY_WINDOW_BACKGROUND)

        # Vertical layout for container
        container_layout = QVBoxLayout()
        container_widget.setLayout(container_layout)

        # Header label
        header_label = QLabel("The next pick goes to...", alignment=Qt.AlignCenter)
        container_layout.addWidget(header_label, alignment=Qt.AlignCenter)

        # Owner card section
        self._create_owner_card(container_layout)

        # Next pick button
        self.next_pick_button = QPushButton("Begin Lottery")
        self.next_pick_button.setStyleSheet(NEXT_PICK_BUTTON)
        self.next_pick_button.clicked.connect(self._on_next_pick_clicked)
        container_layout.addWidget(self.next_pick_button, alignment=Qt.AlignCenter)

        main_layout.addWidget(container_widget)
        self.setLayout(main_layout)

    def _create_owner_card(self, parent_layout):
        """Create the owner card with image and name."""
        owner_card_layout = QVBoxLayout()

        # Owner image
        self.owner_image_label = QLabel("", alignment=Qt.AlignCenter)
        pixmap = QPixmap(config.logo_path)
        pixmap = pixmap.scaledToHeight(250)
        self.owner_image_label.setPixmap(pixmap)

        # Owner name
        self.owner_name_label = QLabel(
            "Welcome to the 2025 West KTown Fantasty Football Draft",
            alignment=Qt.AlignCenter
        )

        owner_card_layout.addWidget(self.owner_image_label, alignment=Qt.AlignCenter)
        owner_card_layout.addWidget(self.owner_name_label, alignment=Qt.AlignCenter)

        parent_layout.addLayout(owner_card_layout)

    def _on_next_pick_clicked(self):
        """Handle next pick button click."""
        if not self.is_started:
            self.is_started = True
            self.next_pick_button.setText("Next Pick")

        self.next_pick_button.setEnabled(False)
        self.next_pick_clicked.emit()

    def display_owner(self, owner_name):
        """
        Display the selected owner's name and image.

        Args:
            owner_name: Name of the owner to display
        """
        self.owner_name_label.setText(owner_name)

        # Update image if available
        owner_images = config.owner_images
        if owner_name in owner_images:
            pixmap = QPixmap(owner_images[owner_name])
            pixmap = pixmap.scaledToHeight(250)
            self.owner_image_label.setPixmap(pixmap)

    def enable_next_pick_button(self):
        """Enable the next pick button."""
        self.next_pick_button.setEnabled(True)

    def get_owner_name(self):
        """
        Get the currently displayed owner name.

        Returns:
            Current owner name as string
        """
        return self.owner_name_label.text()
