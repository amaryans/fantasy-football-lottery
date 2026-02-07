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
        # Create container with outer border
        container = QWidget()
        container.setStyleSheet("""
            background-color: white;
            border: 2px solid #013369;
            border-radius: 10px;
        """)

        layout = QVBoxLayout()
        layout.setSpacing(0)  # Remove spacing between rows
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

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
                    self.standings_data[i][2],
                    is_first=(i == 0),
                    is_last=(i == min(NUMBER_OF_TEAMS, len(self.standings_data) - 1))
                )
                layout.addWidget(row_widget)

        container.setLayout(layout)

        # Wrapper layout
        wrapper_layout = QVBoxLayout()
        wrapper_layout.addWidget(container)
        self.setLayout(wrapper_layout)

    def _create_standings_row(self, owner, team, record, is_first=False, is_last=False):
        """
        Create a single row for the standings table.

        Args:
            owner: Owner name
            team: Team name
            record: Win-loss record
            is_first: True if this is the first row (header)
            is_last: True if this is the last row

        Returns:
            QWidget containing the row
        """
        row_widget = QWidget()

        # Style with thin bottom border between rows, no rounding
        if is_last:
            border_style = "border: none;"
        else:
            border_style = "border: none; border-bottom: 1px solid #013369;"

        row_widget.setStyleSheet(f"""
            background-color: white;
            {border_style}
            padding: 8px;
            border-radius: 0px;
        """)

        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)
        row_layout.setContentsMargins(5, 0, 5, 0)
        row_widget.setLayout(row_layout)

        # Owner label
        owner_label = QLabel(str(owner))
        owner_label.setStyleSheet("""
            font: bold 14px;
            min-width: 5em;
            max-width: 5em;
            border: none;
            background: transparent;
        """)

        # Team label
        team_label = QLabel(str(team))
        team_label.setStyleSheet("""
            font: bold 14px;
            min-width: 8em;
            border: none;
            background: transparent;
        """)

        # Record label
        record_label = QLabel(str(record))
        record_label.setStyleSheet("""
            font: bold 14px;
            min-width: 5em;
            max-width: 5em;
            border: none;
            background: transparent;
        """)

        # Add to row layout
        row_layout.addWidget(owner_label)
        row_layout.addWidget(team_label)
        row_layout.addWidget(record_label)

        return row_widget
