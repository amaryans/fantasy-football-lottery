"""
Draft Order widget for the Fantasy Football Lottery application.
Displays the top row showing the current draft order.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget

from config.constants import NUMBER_OF_TEAMS
from config.styles import DRAFT_ORDER_BUTTON, LOTTERY_WINDOW_BACKGROUND

class DraftPickBox(QWidget):
    """Custom widget for a single draft pick box with header and divider."""

    def __init__(self, pick_number, parent=None):
        super().__init__(parent)
        self.pick_number = pick_number
        self.content_label = None
        self._setup_ui()

    def _setup_ui(self):
        """Initialize and configure the pick box UI elements."""
        # Apply the main box styling (override padding to 0 since we manage layout internally)
        box_style = """
            background-color: white;
            border: 1px solid #013369;
            font: bold 12px;
            padding: 5px;
        """
        #self.setStyleSheet(box_style)
        
        main_layout = QHBoxLayout()

        container_widget = QWidget()
        container_widget.setStyleSheet(box_style)

        # Create vertical layout for header, line, and content
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        container_widget.setLayout(layout)

        # Header with pick number (20% of height)
        header_label = QLabel(str(self.pick_number))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font: bold 12px; background-color: transparent; border-bottom: 3px solid #013369; min-height:2em")
        header_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Content area for owner name (remaining 80%)
        self.content_label = QLabel()
        self.content_label.setAlignment(Qt.AlignCenter)
        self.content_label.setStyleSheet("font: bold 12px; background-color: transparent; border: none; min-height:2em;")
        self.content_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        layout.addWidget(header_label, 20)  # 20% stretch factor
        layout.addWidget(self.content_label, 80)  # 80% stretch factor
        layout.addStretch()
        main_layout.addWidget(container_widget)
        self.setLayout(main_layout)

    def set_owner(self, owner_name):
        """Set the owner name in the content area."""
        self.content_label.setText(owner_name)


class DraftOrderWidget(QWidget):
    """Widget that displays the draft order across the top of the screen."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.picks = []
        self._setup_ui()

    def _setup_ui(self):
        """Initialize and configure the draft order UI elements."""
        # Set height constraints on the widget itself to ensure it's visible
        layout = QHBoxLayout()
        layout.setSpacing(0)  # Small spacing between picks
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Create pick box for each draft pick
        for i in range(NUMBER_OF_TEAMS):
            pick_box = DraftPickBox(i + 1)  # Pick numbers are 1-indexed for display
            self.picks.append(pick_box)
            layout.addWidget(pick_box)
        
        self.setLayout(layout)

    def set_pick(self, position, owner_name):
        """
        Set the owner name for a specific draft position.

        Args:
            position: Draft position (0-indexed)
            owner_name: Name of the owner who gets this pick
        """
        if 0 <= position < len(self.picks):
            self.picks[position].set_owner(owner_name)

    def get_pick_label(self, position):
        """
        Get the content label widget for a specific draft position.

        Args:
            position: Draft position (0-indexed)

        Returns:
            QLabel widget at the specified position
        """
        if 0 <= position < len(self.picks):
            return self.picks[position].content_label
        return None
