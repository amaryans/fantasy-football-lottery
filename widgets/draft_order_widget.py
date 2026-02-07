"""
Draft Order widget for the Fantasy Football Lottery application.
Displays the top row showing the current draft order.
"""

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

from config.styles import DRAFT_ORDER_BUTTON
from config.constants import NUMBER_OF_TEAMS


class DraftOrderWidget(QWidget):
    """Widget that displays the draft order across the top of the screen."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.picks = []
        self._setup_ui()

    def _setup_ui(self):
        """Initialize and configure the draft order UI elements."""
        layout = QHBoxLayout()

        # Create label for each draft pick
        for i in range(NUMBER_OF_TEAMS):
            label = QLabel()
            label.setStyleSheet(DRAFT_ORDER_BUTTON)
            self.picks.append(label)
            layout.addWidget(label)

        self.setLayout(layout)

    def set_pick(self, position, owner_name):
        """
        Set the owner name for a specific draft position.

        Args:
            position: Draft position (0-indexed)
            owner_name: Name of the owner who gets this pick
        """
        if 0 <= position < len(self.picks):
            self.picks[position].setText(owner_name)

    def get_pick_label(self, position):
        """
        Get the QLabel widget for a specific draft position.

        Args:
            position: Draft position (0-indexed)

        Returns:
            QLabel widget at the specified position
        """
        if 0 <= position < len(self.picks):
            return self.picks[position]
        return None
