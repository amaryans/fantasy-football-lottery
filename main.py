import sys
import pandas as pd

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QPixmap

from layout_colorwidget import Color
from layout import Layout
from lottery import LotterySim

OWNER_IMAGES = {'Addi':'./data/addi.JPEG',
                'Owen':'./data/owen.jpeg',
                'Beans':"./data/wktownffbllogo.png",
                'Logan':"./data/wktownffbllogo.png",
                'TCoop':"./data/wktownffbllogo.png",
                'Batches':"./data/wktownffbllogo.png",
                'Austin':"./data/wktownffbllogo.png",
                'Gus':"./data/wktownffbllogo.png",
                'Carson':"./data/wktownffbllogo.png",
                'Dom':"./data/wktownffbllogo.png",
                'Sam':"./data/wktownffbllogo.png",
                'Jakeb':"./data/wktownffbllogo.png"
                } 


DRAFT_ORDER_BUTTON = """background-color: beige;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: #013369;
    font: bold 12px;
    min-width: 10em;
    min-height: 10em;
    max-height: 10em;
    padding: 6px;
"""

DRAFT_PICK_SELECTOR = """background-color: white;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: #013369;
    font: bold 12px;
    min-width: 10em;
    max-width: 20em;
    max-height: 10em;
    padding: 6px;
"""

DRAFT_PICK_SELECTOR_HIGHLIGHTED = """background-color: white;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: #D50A0A;
    font: bold 12px;
    min-width: 10em;
    max-width: 20em;
    max-height: 10em;
    padding: 6px;
"""

DRAFT_PICK_SELECTOR_DISABLED = """background-color: grey;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: #013369;
    font: bold 12px;
    min-width: 10em;
    max-width: 20em;
    max-height: 10em;
    padding: 6px;
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
    border-radius: 10px;
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

NEXT_PICK_BUTTON = """background-color: white;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: #013369;
    font: bold 12px;
    min-width: 10em;
    max-width: 20em;
    min-height: 5em;
    max-height: 5em;
"""

NUMBER_OF_TEAMS = 12

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.lotterySimulation = LotterySim()
        self.lotterySimulation.runSampleSim()
        self.pickOrder = self.lotterySimulation.runSim()

        self.pickNumber = 0
        self.draftBegun = False

        self.pickSelection = None
        self.pickSelectionButton = None
        self.setWindowTitle("West KTown Fantasy Football Lottery")
        self.setGeometry(100, 100, 1920, 1080)
        self.addDraftOrder()
        self.addDraftPickSelector()
        self.previousYearStandings()
        self.addLotteryWindow()
        print(self.lotteryWindow)
        # Creates the background for the whole application
        mainLayout = QVBoxLayout()
        mainWidget = Color("#013369")
        mainWidget.setLayout(mainLayout)

        selectionWindow = QHBoxLayout()
        selectionWindow.addLayout(self.previousYearStandingsLayout)
        selectionWindow.addLayout(self.lotteryWindow, 1)
        selectionWindow.addLayout(self.draftOrderSelector)
        
        # Adds the other sub layouts to main layout
        mainLayout.addLayout(self.addHeader())
        mainLayout.addLayout(self.draftOrder)
        mainLayout.addLayout(selectionWindow)
        
        self.setCentralWidget(mainWidget)
        # button = QPushButton("Press Me")
        # button.clicked.connect(self.buttonClicked)
        # self.setCentralWidget(button)

    def addHeader(self):
        palette = Color("#013369")
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        imageLabel = QLabel()
        textLabel = QLabel("West KTown Fantasy Football League")
        textLabel.setStyleSheet(HEADER)
        pixmap = QPixmap("./data/wktownffbllogo.png")
        pixmap = pixmap.scaledToHeight(150)
        imageLabel.setPixmap(pixmap)
        textLabel.setText("West KTown Fantasy Football League")
        layout.addWidget(imageLabel, alignment=Qt.AlignCenter)
        layout.addWidget(textLabel, alignment=Qt.AlignCenter)
        return layout

    def addDraftOrder(self):
        self.draftOrder = QHBoxLayout()

        self.picks = []
        for i in range(NUMBER_OF_TEAMS):
            label = QLabel()
            label.setStyleSheet(DRAFT_ORDER_BUTTON)
            self.picks.append(label)
        
        for pick in self.picks:
            self.draftOrder.addWidget(pick)

    def createOwnerCard(self):
        self.ownerCard = QVBoxLayout()
        self.ownerCardName = QLabel("Welcome to the 2025 West KTown Fantasty Football Draft", alignment=Qt.AlignCenter)
        self.ownerCardImage = QLabel("", alignment=Qt.AlignCenter)
        pixmap = QPixmap("./data/wktownffbllogo.png")
        pixmap = pixmap.scaledToHeight(250)
        self.ownerCardImage.setPixmap(pixmap)

        self.ownerCard.addWidget(self.ownerCardImage, alignment=Qt.AlignCenter)
        self.ownerCard.addWidget(self.ownerCardName, alignment=Qt.AlignCenter)

    def addLotteryWindow(self):
        self.lotteryWindow = QHBoxLayout()
        self.createOwnerCard()
        subWindow = QVBoxLayout()
        rowWidget = QWidget()
        rowWidget.setStyleSheet(LOTTERY_WINDOW_BACKGROUND)
        rowWidget.setLayout(subWindow)

        nextPickLabel = QLabel("The next pick goes to...", alignment=Qt.AlignCenter)
        self.currentOwnerLabel = QLabel()
        self.getNextPick = QPushButton("Begin Lottery")
        self.getNextPick.setStyleSheet(NEXT_PICK_BUTTON)
        self.getNextPick.clicked.connect(self._nextPickButton)
        subWindow.addWidget(nextPickLabel, alignment=Qt.AlignCenter)
        subWindow.addLayout(self.ownerCard)
        subWindow.addWidget(self.getNextPick, alignment=Qt.AlignCenter)
        self.lotteryWindow.addWidget(rowWidget)
        print(self.lotteryWindow)


    def _nextPickButton(self):
        self.draftBegun = True
        clickedButton = self.sender()
        clickedButton.setText("Next Pick")
        clickedButton.setEnabled(False)
        pixmap = QPixmap(OWNER_IMAGES[self.pickOrder[self.pickNumber]])
        pixmap = pixmap.scaledToHeight(250)
        self.ownerCardName.setText(self.pickOrder[self.pickNumber])
        self.ownerCardImage.setPixmap(pixmap)
        self.pickNumber += 1


    def addDraftPickSelector(self):
        self.draftOrderSelector = QHBoxLayout()
        
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        for i in range(NUMBER_OF_TEAMS):
            button = QPushButton(str(i+1))
            button.clicked.connect(self.makePickSelection)
            button.setStyleSheet(DRAFT_PICK_SELECTOR)
            if i < NUMBER_OF_TEAMS/2:
                leftLayout.addWidget(button)
            else:
                rightLayout.addWidget(button)
        
        self.cancelButton = QPushButton("Undo")
        self.confirmButton = QPushButton("Confirm")
        self.confirmButton.setStyleSheet(DRAFT_PICK_SELECTOR)
        self.cancelButton.setStyleSheet(DRAFT_PICK_SELECTOR)
        self.confirmButton.clicked.connect(self._confirmPick)
        self.cancelButton.clicked.connect(self._undoPick)
        self.confirmButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
        rightLayout.addWidget(self.confirmButton)
        leftLayout.addWidget(self.cancelButton)
        self.draftOrderSelector.addLayout(leftLayout)
        self.draftOrderSelector.addLayout(rightLayout)

    def _confirmPick(self):
        if self.draftBegun:
            self.draftOrder.itemAt(self.pickSelection).widget().setText(self.ownerCardName.text())
            self.pickSelectionButton.setEnabled(False)
            self.pickSelectionButton.setStyleSheet(DRAFT_PICK_SELECTOR_DISABLED)
            self.getNextPick.setEnabled(True)
            self.confirmButton.setEnabled(False)
            self.cancelButton.setEnabled(False)

    def _undoPick(self):
        if self.draftBegun:
            self.pickSelectionButton.setStyleSheet(DRAFT_PICK_SELECTOR)
            self.confirmButton.setEnabled(False)
            self.cancelButton.setEnabled(False)
    
    def makePickSelection(self):
        clickedButton = self.sender()
        if self.pickSelectionButton:
            self.pickSelectionButton.setStyleSheet(DRAFT_PICK_SELECTOR)
        if self.draftBegun:
            self.confirmButton.setEnabled(True)
            self.cancelButton.setEnabled(True)
            for iter in range(NUMBER_OF_TEAMS):
                children = self.draftOrderSelector.children()
                if iter < NUMBER_OF_TEAMS/2:
                    button = children[0].itemAt(iter).widget()
                else:
                    button = children[1].itemAt(iter-6).widget()
                if button is clickedButton:
                    self.pickSelection = iter
                    self.pickSelectionButton = button
                    button.setStyleSheet(DRAFT_PICK_SELECTOR_HIGHLIGHTED)
                    break
                iter+=1

    def previousYearStandings(self):
        self.previousYearStandingsLayout = QVBoxLayout()
        self._importFinalStandings()
        print(self.finalStandings)

        for i in range(NUMBER_OF_TEAMS + 1):
            rowLayout = QHBoxLayout()
            rowWidget = QWidget()
            rowWidget.setStyleSheet(STANDINGS_ROW)
            rowWidget.setLayout(rowLayout)

            ownerLabel = QLabel(self.finalStandings[i][0])
            ownerLabel.setStyleSheet(OWNER_LABEL)
            teamLabel = QLabel(self.finalStandings[i][1])
            teamLabel.setStyleSheet(TEAM_LABEL)
            recordLabel = QLabel(self.finalStandings[i][2])
            recordLabel.setStyleSheet(WIN_LOSS_LABEL)

            rowLayout.addWidget(ownerLabel)
            rowLayout.addWidget(teamLabel)
            rowLayout.addWidget(recordLabel)

            self.previousYearStandingsLayout.addWidget(rowWidget)

    def _importFinalStandings(self):
        df = pd.read_csv("./data/finalStandings.csv")
        self.finalStandings = df.to_numpy()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()