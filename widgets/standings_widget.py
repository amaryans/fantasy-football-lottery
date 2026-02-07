"""
Standings widget for the Fantasy Football Lottery application.
Displays the previous year's final standings.
"""

import pandas as pd
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from config.styles import STANDINGS_ROW, OWNER_LABEL, TEAM_LABEL, WIN_LOSS_LABEL
from config.constants import NUMBER_OF_TEAMS, STANDINGS_CSV_PATH


class StandingsWidget(QWidget):
    """Widget that displays the previous year's standings."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.standings_data = None
        self._load_standings()
        self._setup_ui()

    def _load_standings(self):
        """Load standings data from CSV file."""
        try:
            df = pd.read_csv(STANDINGS_CSV_PATH)
            self.standings_data = df.to_numpy()
        except FileNotFoundError:
            print(f"Warning: Could not find standings file at {STANDINGS_CSV_PATH}")
            self.standings_data = []

    def _setup_ui(self):
        """Initialize and configure the standings UI elements."""
        layout = QVBoxLayout()

        if not len(self.standings_data):
            # Show error message if no data
            error_label = QLabel("No standings data available")
            layout.addWidget(error_label)
        else:
            # Create a row for each team (including header)
            for i in range(min(NUMBER_OF_TEAMS + 1, len(self.standings_data))):
                row_widget = self._create_standings_row(
                    self.standings_data[i][0],
                    self.standings_data[i][1],
                    self.standings_data[i][2]
                )
                layout.addWidget(row_widget)

        self.setLayout(layout)

    def _create_standings_row(self, owner, team, record):
        """
        Create a single row for the standings table.

        Args:
            owner: Owner name
            team: Team name
            record: Win-loss record

        Returns:
            QWidget containing the row
        """
        row_widget = QWidget()
        row_widget.setStyleSheet(STANDINGS_ROW)
        row_layout = QHBoxLayout()
        row_widget.setLayout(row_layout)

        # Owner label
        owner_label = QLabel(str(owner))
        owner_label.setStyleSheet(OWNER_LABEL)

        # Team label
        team_label = QLabel(str(team))
        team_label.setStyleSheet(TEAM_LABEL)

        # Record label
        record_label = QLabel(str(record))
        record_label.setStyleSheet(WIN_LOSS_LABEL)

        # Add to row layout
        row_layout.addWidget(owner_label)
        row_layout.addWidget(team_label)
        row_layout.addWidget(record_label)

        return row_widget
