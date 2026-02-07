"""
Stylesheet constants for the Fantasy Football Lottery application.
"""

DRAFT_ORDER_BUTTON = """
        background-color: white;
        border: 1px solid #013369;
        font: bold 12px;
        min-width: 10em;
        min-height: 10em;
        max-height: 10em;
        padding: 8px;
"""

DRAFT_PICK_SELECTOR = """
    QPushButton {
        background-color: white;
        border-style: outset;
        border-width: 2px;
        border-color: #013369;
        font: bold 12px;
        min-width: 10em;
        max-width: 20em;
        max-height: 10em;
        padding: 6px;
    }
    QPushButton:hover {
        background-color: #E8F4F8;
        border-color: #0066CC;
    }
"""

DRAFT_PICK_SELECTOR_HIGHLIGHTED = """
    QPushButton {
        background-color: white;
        border-style: outset;
        border-width: 2px;
        border-color: #D50A0A;
        font: bold 12px;
        min-width: 10em;
        max-width: 20em;
        max-height: 10em;
        padding: 6px;
    }
    QPushButton:hover {
        background-color: #FFE8E8;
        border-color: #FF0000;
    }
"""

DRAFT_PICK_SELECTOR_DISABLED = """
    QPushButton {
        background-color: grey;
        border-style: outset;
        border-width: 2px;
        border-color: #013369;
        font: bold 12px;
        min-width: 10em;
        max-width: 20em;
        max-height: 10em;
        padding: 6px;
    }
    QPushButton:disabled {
        background-color: #CCCCCC;
    }
"""

STANDINGS_ROW = """background-color: white;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: #013369;
    font: bold 14px;
    min-width: 8em;
    max-height: 10em;
    padding: 6px;
"""

OWNER_LABEL = """background-color: white;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: #013369;
    font: bold 14px;
    min-width: 5em;
    max-width: 5em;
    max-height: 10em;
    padding: 6px;
"""

TEAM_LABEL = """background-color: white;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: #013369;
    font: bold 14px;
    min-width: 5em;
    max-height: 10em;
    padding: 6px;
"""

WIN_LOSS_LABEL = """background-color: white;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: #013369;
    font: bold 14px;
    min-width: 5em;
    max-width: 5em;
    max-height: 10em;
    padding: 6px;
"""

HEADER = """font: bold 24px;
    color: white;
    max-height: 10em;
    padding: 6px;
    text-align: center;
"""

LOTTERY_WINDOW_BACKGROUND = """background-color: white;
    border-style: outset;
    font: bold 14px;
    min-width: 20em;
    padding: 6px;
"""

LOTTERY_WINDOW_HEADER = """background-color: white;
    border-style: outset;
    font: bold 14px;
    min-width: 20em;
    max-height: 10em;
"""

NEXT_PICK_BUTTON = """
    QPushButton {
        background-color: white;
        border-style: outset;
        border-width: 2px;
        border-color: #013369;
        font: bold 12px;
        min-width: 10em;
        max-width: 20em;
        min-height: 5em;
        max-height: 5em;
    }
    QPushButton:hover {
        background-color: #E8F4F8;
        border-color: #0066CC;
    }
    QPushButton:disabled {
        background-color: #F0F0F0;
        color: #999999;
    }
"""
