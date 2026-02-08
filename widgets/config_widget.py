"""
Configuration widget for managing application settings.
"""

import json
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog, QMessageBox, QSpinBox, QScrollArea, QGroupBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from config.config_manager import config
from config.styles import CONFIG_SAVE_BUTTON


class ConfigWidget(QWidget):
    """Widget for configuring application settings."""

    config_saved = pyqtSignal()  # Signal emitted when configuration is saved

    def __init__(self):
        super().__init__()
        self.config_path = "./config/league_config.json"
        self._setup_ui()
        self._load_config()

    def _setup_ui(self):
        """Initialize and configure all UI components."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Title
        title = QLabel("Configuration Settings")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        scroll_layout.addWidget(title)

        # General Settings Group
        general_group = QGroupBox("General Settings")
        general_layout = QVBoxLayout()

        # League Name
        league_name_layout = QHBoxLayout()
        league_name_label = QLabel("League Name:")
        league_name_label.setMinimumWidth(150)
        self.league_name_input = QLineEdit()
        self.league_name_input.setPlaceholderText("Enter league name")
        league_name_layout.addWidget(league_name_label)
        league_name_layout.addWidget(self.league_name_input)
        general_layout.addLayout(league_name_layout)

        # Number of Teams
        num_teams_layout = QHBoxLayout()
        num_teams_label = QLabel("Number of Teams:")
        num_teams_label.setMinimumWidth(150)
        self.num_teams_input = QSpinBox()
        self.num_teams_input.setMinimum(2)
        self.num_teams_input.setMaximum(20)
        self.num_teams_input.setValue(12)
        num_teams_layout.addWidget(num_teams_label)
        num_teams_layout.addWidget(self.num_teams_input)
        num_teams_layout.addStretch()
        general_layout.addLayout(num_teams_layout)

        # League Logo
        logo_layout = QHBoxLayout()
        logo_label = QLabel("League Logo:")
        logo_label.setMinimumWidth(150)
        self.logo_path_input = QLineEdit()
        self.logo_path_input.setPlaceholderText("Path to league logo")
        self.logo_browse_btn = QPushButton("Browse...")
        self.logo_browse_btn.clicked.connect(self._browse_logo)
        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(self.logo_path_input)
        logo_layout.addWidget(self.logo_browse_btn)
        general_layout.addLayout(logo_layout)

        general_group.setLayout(general_layout)
        scroll_layout.addWidget(general_group)

        # Owners/Teams Group
        owners_group = QGroupBox("Owners & Teams")
        owners_layout = QVBoxLayout()

        owners_label = QLabel("Edit owner information:")
        owners_layout.addWidget(owners_label)

        # Owner table
        self.owners_table = QTableWidget()
        self.owners_table.setColumnCount(4)
        self.owners_table.setHorizontalHeaderLabels(["Owner", "Team Name", "Record", "Owner Image Path"])
        self.owners_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.owners_table.setMinimumHeight(300)
        owners_layout.addWidget(self.owners_table)

        # Add/Remove row buttons
        table_buttons_layout = QHBoxLayout()
        self.add_row_btn = QPushButton("Add Owner")
        self.add_row_btn.clicked.connect(self._add_owner_row)
        self.remove_row_btn = QPushButton("Remove Selected")
        self.remove_row_btn.clicked.connect(self._remove_owner_row)
        table_buttons_layout.addWidget(self.add_row_btn)
        table_buttons_layout.addWidget(self.remove_row_btn)
        table_buttons_layout.addStretch()
        owners_layout.addLayout(table_buttons_layout)

        owners_group.setLayout(owners_layout)
        scroll_layout.addWidget(owners_group)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Action Buttons
        button_layout = QHBoxLayout()

        self.import_btn = QPushButton("Import Config")
        self.import_btn.clicked.connect(self._import_config)

        self.export_btn = QPushButton("Export Config")
        self.export_btn.clicked.connect(self._export_config)

        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(CONFIG_SAVE_BUTTON)
        self.save_btn.clicked.connect(self._save_config)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.close)

        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Configuration")
        self.resize(900, 700)

    def _load_config(self):
        """Load configuration from JSON file."""
        try:
            # Reload config from file
            config.reload_config()

            # Load general settings
            self.league_name_input.setText(config.league_name)
            self.num_teams_input.setValue(config.number_of_teams)
            self.logo_path_input.setText(config.logo_path)

            # Load owners
            owners = config.owners
            self.owners_table.setRowCount(len(owners))

            for i, owner_data in enumerate(owners):
                self.owners_table.setItem(i, 0, QTableWidgetItem(owner_data.get('owner', '')))
                self.owners_table.setItem(i, 1, QTableWidgetItem(owner_data.get('team_name', '')))
                self.owners_table.setItem(i, 2, QTableWidgetItem(owner_data.get('record', '')))
                self.owners_table.setItem(i, 3, QTableWidgetItem(owner_data.get('image_path', '')))

        except Exception as e:
            QMessageBox.warning(self, "Load Error", f"Error loading configuration: {str(e)}")

    def _add_owner_row(self):
        """Add a new row to the owners table."""
        row_count = self.owners_table.rowCount()
        self.owners_table.insertRow(row_count)
        self.owners_table.setItem(row_count, 0, QTableWidgetItem(""))
        self.owners_table.setItem(row_count, 1, QTableWidgetItem(""))
        self.owners_table.setItem(row_count, 2, QTableWidgetItem("0-0"))
        self.owners_table.setItem(row_count, 3, QTableWidgetItem("./data/wktownffbllogo.png"))

    def _remove_owner_row(self):
        """Remove selected row from the owners table."""
        current_row = self.owners_table.currentRow()
        if current_row >= 0:
            self.owners_table.removeRow(current_row)

    def _browse_logo(self):
        """Browse for league logo file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select League Logo",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if file_path:
            # Convert to relative path if possible
            try:
                rel_path = os.path.relpath(file_path)
                self.logo_path_input.setText(rel_path.replace('\\', '/'))
            except:
                self.logo_path_input.setText(file_path.replace('\\', '/'))

    def _save_config(self):
        """Save configuration to JSON file."""
        try:
            # Collect data from table
            owners_data = []

            for row in range(self.owners_table.rowCount()):
                owner_item = self.owners_table.item(row, 0)
                team_item = self.owners_table.item(row, 1)
                record_item = self.owners_table.item(row, 2)
                image_item = self.owners_table.item(row, 3)

                if owner_item and team_item:
                    owner = owner_item.text().strip()
                    team = team_item.text().strip()
                    record = record_item.text().strip() if record_item else "0-0"
                    image = image_item.text().strip() if image_item else "./data/wktownffbllogo.png"

                    if owner and team:  # Only add if owner and team are not empty
                        owners_data.append({
                            'owner': owner,
                            'team_name': team,
                            'record': record,
                            'image_path': image
                        })

            # Update NUMBER_OF_TEAMS to match actual number of owners
            num_teams = len(owners_data)

            # Create config data
            config_data = {
                'league_name': self.league_name_input.text(),
                'number_of_teams': num_teams,
                'logo_path': self.logo_path_input.text(),
                'owners': owners_data
            }

            # Write to JSON file
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(config_data, f, indent=2)

            # Reload the global config
            config.reload_config()

            QMessageBox.information(self, "Success", "Configuration saved successfully!\n\nPlease restart the application for changes to take effect.")
            self.config_saved.emit()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Error saving configuration: {str(e)}")

    def _export_config(self):
        """Export configuration to a JSON file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Configuration",
            "config_export.json",
            "JSON Files (*.json)"
        )

        if file_path:
            try:
                config_data = {
                    'league_name': self.league_name_input.text(),
                    'number_of_teams': self.num_teams_input.value(),
                    'logo_path': self.logo_path_input.text(),
                    'owners': []
                }

                for row in range(self.owners_table.rowCount()):
                    owner_item = self.owners_table.item(row, 0)
                    team_item = self.owners_table.item(row, 1)
                    record_item = self.owners_table.item(row, 2)
                    image_item = self.owners_table.item(row, 3)

                    if owner_item and team_item:
                        config_data['owners'].append({
                            'owner': owner_item.text(),
                            'team_name': team_item.text(),
                            'record': record_item.text() if record_item else "",
                            'image_path': image_item.text() if image_item else ""
                        })

                with open(file_path, 'w') as f:
                    json.dump(config_data, f, indent=2)

                QMessageBox.information(self, "Success", "Configuration exported successfully!")

            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Error exporting configuration: {str(e)}")

    def _import_config(self):
        """Import configuration from a JSON file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Configuration",
            "",
            "JSON Files (*.json)"
        )

        if file_path:
            try:
                with open(file_path, 'r') as f:
                    config_data = json.load(f)

                # Load general settings
                self.league_name_input.setText(config_data.get('league_name', ''))
                self.num_teams_input.setValue(config_data.get('number_of_teams', 12))
                self.logo_path_input.setText(config_data.get('logo_path', ''))

                # Load owners
                owners = config_data.get('owners', [])
                self.owners_table.setRowCount(len(owners))

                for i, owner_data in enumerate(owners):
                    self.owners_table.setItem(i, 0, QTableWidgetItem(owner_data.get('owner', '')))
                    self.owners_table.setItem(i, 1, QTableWidgetItem(owner_data.get('team_name', '')))
                    self.owners_table.setItem(i, 2, QTableWidgetItem(owner_data.get('record', '')))
                    self.owners_table.setItem(i, 3, QTableWidgetItem(owner_data.get('image_path', '')))

                QMessageBox.information(self, "Success", "Configuration imported successfully!")

            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Error importing configuration: {str(e)}")
