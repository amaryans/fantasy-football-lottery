"""
Draft Pick Selector widget for the Fantasy Football Lottery application.
Allows owners to select their preferred draft position.
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from config.styles import (
    DRAFT_PICK_SELECTOR,
    DRAFT_PICK_SELECTOR_HIGHLIGHTED,
    DRAFT_PICK_SELECTOR_DISABLED
)
from config.constants import NUMBER_OF_TEAMS


class DraftPickSelectorWidget(QWidget):
    """
    Widget that allows owners to select their draft position.

    Signals:
        pick_confirmed: Emitted when a pick is confirmed with (position, owner_name)
    """

    pick_confirmed = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pick_buttons = []
        self.selected_position = None
        self.selected_button = None
        self.is_draft_begun = False
        self.current_owner = None
        self._setup_ui()

    def _setup_ui(self):
        """Initialize and configure the draft pick selector UI elements."""
        main_layout = QHBoxLayout()

        # Create two columns
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Create pick buttons (1-12)
        for i in range(NUMBER_OF_TEAMS):
            button = QPushButton(str(i + 1))
            button.setStyleSheet(DRAFT_PICK_SELECTOR)
            button.clicked.connect(lambda checked, pos=i: self._on_pick_selected(pos))
            self.pick_buttons.append(button)

            # Distribute buttons across two columns
            if i < NUMBER_OF_TEAMS / 2:
                left_layout.addWidget(button)
            else:
                right_layout.addWidget(button)

        # Create Undo and Confirm buttons
        self.cancel_button = QPushButton("Undo")
        self.confirm_button = QPushButton("Confirm")

        self.cancel_button.setStyleSheet(DRAFT_PICK_SELECTOR)
        self.confirm_button.setStyleSheet(DRAFT_PICK_SELECTOR)

        self.cancel_button.clicked.connect(self._on_undo_clicked)
        self.confirm_button.clicked.connect(self._on_confirm_clicked)

        self.cancel_button.setEnabled(False)
        self.confirm_button.setEnabled(False)

        # Add control buttons to columns
        left_layout.addWidget(self.cancel_button)
        right_layout.addWidget(self.confirm_button)

        # Add columns to main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def _on_pick_selected(self, position):
        """
        Handle pick button selection.

        Args:
            position: The selected draft position (0-indexed)
        """
        # Reset previous selection styling
        if self.selected_button:
            self.selected_button.setStyleSheet(DRAFT_PICK_SELECTOR)

        if self.is_draft_begun:
            # Update selection
            self.selected_position = position
            self.selected_button = self.pick_buttons[position]
            self.selected_button.setStyleSheet(DRAFT_PICK_SELECTOR_HIGHLIGHTED)

            # Enable confirm/cancel buttons
            self.confirm_button.setEnabled(True)
            self.cancel_button.setEnabled(True)

    def _on_confirm_clicked(self):
        """Handle confirm button click."""
        if self.is_draft_begun and self.selected_button and self.current_owner:
            # Disable the selected button
            self.selected_button.setEnabled(False)
            self.selected_button.setStyleSheet(DRAFT_PICK_SELECTOR_DISABLED)

            # Emit signal with position and owner name
            self.pick_confirmed.emit(self.selected_position, self.current_owner)

            # Disable confirm/cancel buttons
            self.confirm_button.setEnabled(False)
            self.cancel_button.setEnabled(False)

            # Reset selection
            self.selected_button = None
            self.selected_position = None

    def _on_undo_clicked(self):
        """Handle undo button click."""
        if self.is_draft_begun and self.selected_button:
            # Reset selection styling
            self.selected_button.setStyleSheet(DRAFT_PICK_SELECTOR)

            # Disable confirm/cancel buttons
            self.confirm_button.setEnabled(False)
            self.cancel_button.setEnabled(False)

            # Reset selection
            self.selected_button = None
            self.selected_position = None

    def start_draft(self):
        """Begin the draft selection process."""
        self.is_draft_begun = True

    def set_current_owner(self, owner_name):
        """
        Set the current owner who is making a pick.

        Args:
            owner_name: Name of the current owner
        """
        self.current_owner = owner_name

    def enable_confirm_cancel(self, enabled):
        """
        Enable or disable the confirm and cancel buttons.

        Args:
            enabled: True to enable, False to disable
        """
        self.confirm_button.setEnabled(enabled)
        self.cancel_button.setEnabled(enabled)
