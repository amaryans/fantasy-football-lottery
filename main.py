"""
Main application file for the Fantasy Football Lottery GUI.
"""

import sys

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QVBoxLayout

from layout_colorwidget import Color
from lottery import LotterySim
from widgets.header_widget import HeaderWidget
from widgets.draft_order_widget import DraftOrderWidget
from widgets.lottery_window_widget import LotteryWindowWidget
from widgets.standings_widget import StandingsWidget
from widgets.draft_pick_selector_widget import DraftPickSelectorWidget


class MainWindow(QMainWindow):
    """Main window for the Fantasy Football Lottery application."""

    def __init__(self):
        super().__init__()

        # Initialize lottery simulation
        self.lottery_simulation = LotterySim()
        self.lottery_simulation.runSampleSim()
        self.pick_order = self.lottery_simulation.runSim()
        self.pick_number = 0

        # Setup window
        self.setWindowTitle("West KTown Fantasy Football Lottery")
        self.setGeometry(100, 100, 1920, 1080)

        # Initialize UI
        self._setup_ui()

    def _setup_ui(self):
        """Initialize and configure all UI components."""
        # Create main layout with background
        main_layout = QVBoxLayout()
        main_widget = Color("#013369")
        main_widget.setLayout(main_layout)

        # Create widgets
        self.header_widget = HeaderWidget()
        self.draft_order_widget = DraftOrderWidget()
        self.standings_widget = StandingsWidget()
        self.lottery_window_widget = LotteryWindowWidget()
        self.draft_pick_selector_widget = DraftPickSelectorWidget()

        # Connect signals
        self.lottery_window_widget.next_pick_clicked.connect(self._on_next_pick)
        self.draft_pick_selector_widget.pick_confirmed.connect(self._on_pick_confirmed)

        # Create selection window (bottom section)
        selection_layout = QHBoxLayout()
        selection_layout.addWidget(self.standings_widget)
        selection_layout.addWidget(self.lottery_window_widget, 1)
        selection_layout.addWidget(self.draft_pick_selector_widget)
        selection_layout.setContentsMargins(0, 0, 0, 0)

        # Add all widgets to main layout
        main_layout.addWidget(self.header_widget)
        main_layout.addWidget(self.draft_order_widget)
        main_layout.addLayout(selection_layout)

        self.setCentralWidget(main_widget)

    def _on_next_pick(self):
        """Handle next pick button click."""
        if self.pick_number < len(self.pick_order):
            # Get current owner
            current_owner = self.pick_order[self.pick_number]

            # Display owner in lottery window
            self.lottery_window_widget.display_owner(current_owner)

            # Enable draft pick selector
            self.draft_pick_selector_widget.start_draft()
            self.draft_pick_selector_widget.set_current_owner(current_owner)

            # Increment pick number
            self.pick_number += 1

    def _on_pick_confirmed(self, position, owner_name):
        """
        Handle pick confirmation.

        Args:
            position: Selected draft position (0-indexed)
            owner_name: Name of the owner making the pick
        """
        # Update draft order display
        self.draft_order_widget.set_pick(position, owner_name)

        # Re-enable next pick button
        self.lottery_window_widget.enable_next_pick_button()


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
