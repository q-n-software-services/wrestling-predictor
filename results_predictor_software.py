# Importing built-in functions from libraries
import math
from PyQt5.QtWidgets import QApplication, QDialog,QComboBox, QLineEdit, QFontComboBox, QVBoxLayout, QHBoxLayout,QDial, QTextEdit, QLCDNumber, QMessageBox, QListWidget, QListWidgetItem, QListView, QPushButton, QCalendarWidget, QLabel, QWidget, QTableWidget, QTableWidgetItem
import sys, calendar, datetime
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtCore import QSize, QTime, QTimer, QLocale
import time
from random import randint
import sqlite3, sys, os

# Database setup and related stuff of SQLite3
conn = sqlite3.connect("results_predictor.sqlite")
cur = conn.cursor()

# cur.execute('''DROP TABLE IF EXISTS Player_Data''')

# cur.execute('''CREATE TABLE Player_Data (id INTEGER, name TEXT, rating REAL)''')

# cur.execute('INSERT INTO Player_Data (id, name, rating) VALUES (?, ?, ?)', (3, "vacant_id", 12.12))
# cur.execute('INSERT INTO Player_Data (id, name, rating) VALUES (?, ?, ?)', (player1_id, player1_name, player1_rating))
# cur.execute('INSERT INTO Player_Data (id, name, rating) VALUES (?, ?, ?)', (player2_id, player2_name, player2_rating))
conn.commit()

# Data initialization with Dummy Data
player1_name = "PLAYER 1"
player1_id = 1
player1_rating = 7.12
# validate match points to be under 16
player1_match_points = 2

player2_name = "PLAYER 2"
player2_id = 2
player2_rating = 8.12
# validate match points to be under 16
player2_match_points = 2


# Prediction statement with placeholders for player's name and predicted points to win by
prediction = "{} is predicted to win by {} points"

# Predicted winning points calculation
rating_difference = math.fabs(player2_rating - player1_rating).__round__(2)
predicted_win_points = int(rating_difference / 0.19)
if predicted_win_points > 16:
    predicted_win_points = 16

if player1_rating > player2_rating:
    prediction_show = prediction.format(player1_name, predicted_win_points)
elif player2_rating > player1_rating:
    prediction_show = prediction.format(player2_name, predicted_win_points)


# Rating Handler Algorithm
points_difference = math.fabs(player2_match_points - player1_match_points)
if player2_match_points > player1_match_points:
    player2_rating = player2_rating + 0.2
    player2_rating = player2_rating + (int(points_difference/5) * 0.05)
    player1_rating = player1_rating - 0.2

elif player1_match_points > player2_match_points:
    player1_rating = player1_rating + 0.2
    player1_rating = player1_rating + (int(points_difference/5) * 0.05)
    player2_rating = player2_rating - 0.2


# Validating Rating calculations
if player1_rating > 15:
    player1_rating = 15.00

if player2_rating > 15:
    player2_rating = 15.00

# Database setup dfor dummy data. Was used before testing process
cur.execute('UPDATE Player_Data SET rating = ? WHERE name = ?', (player1_rating, player1_name))
cur.execute('UPDATE Player_Data SET rating = ? WHERE name = ?', (player2_rating, player2_name))
conn.commit()

# Below is the GUI code written using PyQt5 library of PYTHON
class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.showFullScreen()

        self.setWindowTitle("Drop_Down_List_PyQt5")
        self.setWindowIcon(QIcon("burger.ico"))

        self.create_combo_box()

    def create_combo_box(self):
        global player1_id
        global player1_name
        global player1_rating
        global player1_match_points
        global player2_id
        global player2_name
        global player2_rating
        global player2_match_points
        global prediction_show
        global cur
        global conn
        vbox = QVBoxLayout()

# labels are used to display text and data on screen

        self.label_title1 = QLabel("  NAME")
        self.label_title1.setFont(QFont("Sanserif", 12))
        self.label_title1.setStyleSheet("background-color:white")
        self.label_title1.setFixedWidth(60)


        self.label_title2 = QLabel("   ID")
        self.label_title2.setFont(QFont("Sanserif", 12))
        self.label_title2.setStyleSheet("background-color:white")
        self.label_title2.setFixedWidth(60)


        self.label_title3 = QLabel(" RATING")
        self.label_title3.setFont(QFont("Sanserif", 11))
        self.label_title3.setStyleSheet("background-color:white")
        self.label_title3.setFixedWidth(60)


        self.label = QLabel("\t\t       Results Predictor")
        self.label.setFont(QFont("Sanserif", 36))
        self.label.setFixedHeight(120)

        self.label.setStyleSheet("background-color:yellow")
        vbox.addWidget(self.label)
# Combo Box is the dropdown-list used to show players name present in database
        self.cbox = QComboBox()
        names = ['Mohib', 'Hassaan', 'Ahmad', 'Maaz', 'Ayesha']
        cur.execute("SELECT id FROM Player_Data WHERE name=?", ("vacant_id",))
        next_id = cur.fetchall()
        next_id = list(next_id[0])
        next_id = int(next_id[0])
        for i in range(next_id):
            cur.execute("SELECT name FROM Player_Data WHERE id =?", (i + 1,))
            name = cur.fetchall()
            if name != []:
                name = list(name[0])
                name = str(name[0])

                if name != "vacant_id":
                    self.cbox.addItem(name)

        try:
            self.cbox.currentIndexChanged.connect(self.hovered1)

        except:
            self.warning_message()


        self.cbox2 = QComboBox()
        names = ['Mohib', 'Hassaan', 'Ahmad', 'Maaz', 'Ayesha']
        for i in range(next_id):
            cur.execute("SELECT name FROM Player_Data WHERE id =?", (i + 1,))
            name = cur.fetchall()
            if name != []:
                name = list(name[0])
                name = str(name[0])

                if name != "vacant_id":
                    self.cbox2.addItem(name)

        try:
            self.cbox2.currentIndexChanged.connect(self.hovered2)

        except:
            self.warning_message()

        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()

        self.label11 = QLabel("\t" + player1_name)
        self.label11.setFont(QFont("Sanserif", 24))
        self.label11.setStyleSheet("background-color:white")
        hbox_name = QHBoxLayout()
        hbox_name.addWidget(self.label_title1)
        hbox_name.addWidget(self.label11)

        vbox1.addLayout(hbox_name)

        vbox1.addWidget(self.cbox)

        self.label12 = QLabel("\t" + str(player1_id))
        self.label12.setFont(QFont("Sanserif", 24))
        self.label12.setStyleSheet("background-color:white")
        hbox_id = QHBoxLayout()
        hbox_id.addWidget(self.label_title2)
        hbox_id.addWidget(self.label12)

        vbox1.addLayout(hbox_id)

        self.label13 = QLabel("\t" + str(math.fabs(player1_rating).__round__(2)))
        self.label13.setFont(QFont("Sanserif", 24))
        self.label13.setStyleSheet("background-color:white")
        hbox_rating = QHBoxLayout()
        hbox_rating.addWidget(self.label_title3)
        hbox_rating.addWidget(self.label13)

        vbox1.addLayout(hbox_rating)
# single line input box used to input points that the respective player scored
        self.input1 = QLineEdit()
        self.input1.setFont(QFont("Sanserif", 12))
        self.input1.setPlaceholderText("\tPoints scored by " + player1_name)
        vbox1.addWidget(self.input1)

        self.label21 = QLabel("\t" + player2_name)
        self.label21.setFont(QFont("Sanserif", 24))
        self.label21.setStyleSheet("background-color:white")
        vbox2.addWidget(self.label21)

        vbox2.addWidget(self.cbox2)

        self.label22 = QLabel("\t" + str(player2_id))
        self.label22.setFont(QFont("Sanserif", 24))
        self.label22.setStyleSheet("background-color:white")
        vbox2.addWidget(self.label22)

        self.label23 = QLabel("\t" + str(math.fabs(player2_rating).__round__(2)))
        self.label23.setFont(QFont("Sanserif", 24))
        self.label23.setStyleSheet("background-color:white")
        vbox2.addWidget(self.label23)

        self.input2 = QLineEdit()
        self.input2.setFont(QFont("Sanserif", 12))
        self.input2.setPlaceholderText("\tPoints scored by " + player2_name)
        vbox2.addWidget(self.input2)

        btn_close = QPushButton("CLOSE")
        btn_close.setStyleSheet("Background-color:red")
        btn_close.setFont(QFont("Sanserif", 12))
        btn_close.setFixedHeight(60)
        btn_close.clicked.connect(self.closew)

        btn_minimize = QPushButton("MINIMIZE")
        btn_minimize.setStyleSheet("Background-color:yellow")
        btn_minimize.setFont(QFont("Sanserif", 12))
        btn_minimize.setFixedHeight(60)
        btn_minimize.clicked.connect(self.minimizew)

        btn_removep = QPushButton("REMOVE PLAYER")
        btn_removep.setStyleSheet("Background-color:pink")
        btn_removep.setFont(QFont("Sanserif", 12))
        btn_removep.setFixedHeight(60)
        btn_removep.clicked.connect(self.remove_player)

        btn_addp = QPushButton("ADD PLAYER")
        btn_addp.setStyleSheet("Background-color:Green")
        btn_addp.setFont(QFont("Sanserif", 12))
        btn_addp.setFixedHeight(60)
        btn_addp.clicked.connect(self.add_player)

        hbox = QHBoxLayout()

        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        vbox.addLayout(hbox)

        btn_points = QPushButton("SUBMIT")
        btn_points.setFont(QFont("sanserif", 16))
        btn_points.setStyleSheet("background-color:violet")
        btn_points.clicked.connect(self.submit_points)
        vbox.addWidget(btn_points)

        self.label_prediction_heading = QLabel("\t\t\t\t       PREDICTION")
        self.label_prediction_heading.setFont(QFont("sanserif", 24))
        self.label_prediction_heading.setFixedHeight(60)

        self.label_prediction_text = QLabel("\t\t\t\t\t\t  " + prediction_show)
        self.label_prediction_text.setFont(QFont("Sanserif", 16))
        self.label_prediction_text.setFixedHeight(60)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.label_prediction_heading)
        vbox3.addWidget(self.label_prediction_text)
        vbox.addLayout(vbox3)


        hbox2 = QHBoxLayout()

        hbox2.addWidget(btn_addp)
        hbox2.addWidget(btn_removep)
        hbox2.addWidget(btn_minimize)
        hbox2.addWidget(btn_close)

        vbox.addLayout(hbox2)

        self.setLayout(vbox)
# function that is called when a new entry is chosen from the first dropdown list
    def hovered1(self):
        global cur
        global conn
        global player1_rating
        global player1_name
        global player1_id
        global player2_name
        global player2_rating
        global player2_id
        global rating_difference
        global predicted_win_points
        global prediction

        text = self.cbox.currentText()

        self.input1.setPlaceholderText("\tPoints scored by " + text)
        cur.execute("SELECT rating, id FROM Player_Data WHERE name =?", (text,))
        data = cur.fetchall()
        rating = list(data[0])
        rating = float(rating[0])
        rating = str(rating)

        id1 = list(data)
        id1 = id1[0][1]

        id1 = str(id1)
        self.label12.setText("\t" + id1)
        self.label13.setText("\t" + rating)

        player1_name = text
        player1_rating = float(rating)
        player1_id = int(id1)
        # Predicted winning points calculation
        rating_difference = math.fabs(player2_rating - player1_rating).__round__(2)
        predicted_win_points = int(rating_difference / 0.19)
        if predicted_win_points > 16:
            predicted_win_points = 16

        if player1_rating > player2_rating:
            prediction_show1 = prediction.format(player1_name, predicted_win_points)
        elif player2_rating > player1_rating:
            prediction_show1 = prediction.format(player2_name, predicted_win_points)
        else:
            prediction_show1 = "No Prediction. Their Ratings are equal. "

        self.label_prediction_text.setText("\t\t\t\t\t\t  " + prediction_show1)

        self.label11.setText("\t" + str(text))
        self.label11.setFont(QFont("Sanserif", 24))

    # function that is called when a new entry is chosen from the second dropdown list
    def hovered2(self):
        global cur
        global conn
        global player1_rating
        global player1_name
        global player1_id
        global player2_name
        global player2_rating
        global player2_id
        global rating_difference
        global predicted_win_points
        global prediction

        text = self.cbox2.currentText()
        self.input2.setPlaceholderText("\tPoints scored by " + text)
        cur.execute("SELECT rating, id FROM Player_Data WHERE name =?", (text,))
        data = cur.fetchall()
        rating = list(data[0])
        rating = float(rating[0])
        rating = str(rating)

        id1 = list(data)
        id1 = id1[0][1]

        id1 = str(id1)
        self.label22.setText("\t" + id1)
        self.label23.setText("\t" + rating)
        self.label21.setText("\t" + str(text))

        player2_name = text
        player2_rating = float(rating)
        player2_id = int(id1)

        # Predicted winning points calculation
        rating_difference = math.fabs(player2_rating - player1_rating).__round__(2)
        predicted_win_points = int(rating_difference / 0.19)
        if predicted_win_points > 16:
            predicted_win_points = 16

        if player1_rating > player2_rating:
            prediction_show1 = prediction.format(player1_name, predicted_win_points)
        elif player2_rating > player1_rating:
            prediction_show1 = prediction.format(player2_name, predicted_win_points)
        else:
            prediction_show1 = "No Prediction. Their Ratings are equal. "

        self.label_prediction_text.setText("\t\t\t\t\t\t  " + prediction_show1)

        self.label21.setFont(QFont("Sanserif", 24))

# fuction called to close the software
    def closew(self):
        self.close()

# fuction called to minimize the software window
    def minimizew(self):
        self.showMinimized()

# Function to add player to the software and database
    def add_player(self):

        CheckOut_dialog = QDialog()
        CheckOut_dialog.setModal(True)
        CheckOut_dialog.setWindowTitle("            ADD PLAYER")
        CheckOut_dialog.setWindowIcon(QIcon("burger.ico"))
        CheckOut_dialog.setGeometry(500, 200, 400, 300)
        vbox = QVBoxLayout()

        my_label = QLabel("  NAME ")
        my_label.setStyleSheet("background-color:white")
        my_label.setFont(QFont("Sanserif", 22))

        vbox.addWidget(my_label)

        self.line_edit = QLineEdit()
        self.line_edit.setStyleSheet("background-color:white")
        self.line_edit.setFont(QFont("sanserif", 16))
        self.line_edit.setPlaceholderText("Enter Name of the Player ")
        vbox.addWidget(self.line_edit)

        my_label2 = QLabel("  Rating ")
        my_label2.setStyleSheet("background-color:white")
        my_label2.setFont(QFont("Sanserif", 22))

        vbox.addWidget(my_label2)

        self.line_edit2 = QLineEdit()
        self.line_edit2.setStyleSheet("background-color:white")
        self.line_edit2.setFont(QFont("sanserif", 16))
        self.line_edit2.setPlaceholderText("Enter the Present Rating of the Player ")
        vbox.addWidget(self.line_edit2)

        self.label = QLabel(" ")
        self.label.setFont(QFont("sanserif", 12))
        vbox.addWidget(self.label)

        btn_submit = QPushButton("SUBMIT")
        btn_submit.setFont(QFont("sanserif", 16))
        btn_submit.setStyleSheet("background-color:green")
        btn_submit.clicked.connect(self.submit_addplayer)
        vbox.addWidget(btn_submit)



        CheckOut_dialog.setLayout(vbox)
        CheckOut_dialog.exec_()

# fuction to submit data to the software for new player added
    def submit_addplayer(self):
        global cur
        global conn
        self.label.setText("\tProcess Successful")
        name = self.line_edit.text().upper()
        rating = self.line_edit2.text()
        rating = float(rating)
        cur.execute("SELECT id FROM Player_Data WHERE name=?", ("vacant_id",))
        next_id = cur.fetchall()
        next_id = list(next_id[0])
        next_id = int(next_id[0])

        cur.execute('INSERT INTO Player_Data (id, name, rating) VALUES (?, ?, ?)',
                    (next_id, name, rating))
        cur.execute('UPDATE Player_Data SET id = ? WHERE name = ?', (next_id + 1, "vacant_id"))
        conn.commit()

        self.cbox.addItem(name)
        self.cbox2.addItem(name)

    # Function to remove/delete player from the software and database
    def remove_player(self):
        CheckOut_dialog = QDialog()
        CheckOut_dialog.setModal(True)
        CheckOut_dialog.setWindowTitle("            REMOVE PLAYER")
        CheckOut_dialog.setWindowIcon(QIcon("burger.ico"))
        CheckOut_dialog.setGeometry(500, 200, 400, 300)
        vbox = QVBoxLayout()

        my_label = QLabel("  NAME ")
        my_label.setStyleSheet("background-color:white")
        my_label.setFont(QFont("Sanserif", 22))

        vbox.addWidget(my_label)

        self.line_edit3 = QLineEdit()
        self.line_edit3.setStyleSheet("background-color:white")
        self.line_edit3.setFont(QFont("sanserif", 16))
        self.line_edit3.setPlaceholderText("Enter Name of the Player ")
        vbox.addWidget(self.line_edit3)



        self.labelnew = QLabel(" ")
        self.labelnew.setFont(QFont("sanserif", 12))
        vbox.addWidget(self.labelnew)

        btn_submit = QPushButton("SUBMIT")
        btn_submit.setFont(QFont("sanserif", 16))
        btn_submit.setStyleSheet("background-color:green")
        btn_submit.clicked.connect(self.submit_removeplayer)
        vbox.addWidget(btn_submit)

        CheckOut_dialog.setLayout(vbox)
        CheckOut_dialog.exec_()

# function to submit data to software for the player to be removed
    def submit_removeplayer(self):
        global cur
        global conn

        name = self.line_edit3.text().upper()

        cur.execute("DELETE from Player_Data where name = ?", (name,))
        conn.commit()
        a = self.cbox.findText(name)
        self.cbox.removeItem(a)
        self.cbox2.removeItem(a)
        self.labelnew.setText("\tProcess Successful")

# function to submit points entered to the software that were scored by a player
    def submit_points(self):
        global cur
        global conn
        # Rating Handler Algorithm
        player1_match_point = self.input1.text()
        player1_match_point = int(player1_match_point)
        player2_match_point = self.input2.text()
        player2_match_point = int(player2_match_point)
        point_difference = math.fabs(player2_match_point - player1_match_point)

        player1_ratings = self.label13.text().rstrip().lstrip()
        player1_ratings = float(player1_ratings)

        player2_ratings = self.label23.text().rstrip().lstrip()
        player2_ratings = float(player2_ratings)
        if player2_match_point > player1_match_point:
            player2_ratings = player2_ratings + 0.2
            player2_ratings = player2_ratings + (int(point_difference / 5) * 0.05)
            player1_ratings = player1_ratings - 0.2

        elif player1_match_point > player2_match_point:
            player1_ratings = player1_ratings + 0.2
            player1_ratings = player1_ratings + (int(point_difference / 5) * 0.05)
            player2_ratings = player2_ratings - 0.2

        # Validating Rating calculations
        if player1_ratings > 15:
            player1_ratings = 15.00

        if player2_ratings > 15:
            player2_ratings = 15.00

        player1_ratings = math.fabs(player1_ratings).__round__(2)
        player2_ratings = math.fabs(player2_ratings).__round__(2)

        player1_names = self.label11.text().rstrip().lstrip()
        player2_names = self.label21.text().rstrip().lstrip()

        pl_id1 = self.label12.text().rstrip().lstrip()
        pl_id1 = int(pl_id1)
        cur.execute('UPDATE Player_Data SET rating = ? WHERE id = ?', (player1_ratings, pl_id1))
        conn.commit()

        pl_id2 = self.label22.text().rstrip().lstrip()
        pl_id2 = int(pl_id2)
        cur.execute('UPDATE Player_Data SET rating = ? WHERE id = ?', (player2_ratings, pl_id2))
        conn.commit()

        self.label13.setText("\t" + str(player1_ratings))
        self.label23.setText("\t" + str(player2_ratings))


# GUI window setup clauses

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())








