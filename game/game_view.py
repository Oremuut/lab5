from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer
from game_model import GameModel
from statistics import Statistics


class GameView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("5 в ряд")

        self.model = GameModel()

        self.time_limit = 5
        self.time_left = {"X": self.time_limit, "O": self.time_limit}
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.timer_label = QLabel(self.get_timer_text())
        self.timer_label.setStyleSheet("font-size: 16px;")

        self.grid_layout = QGridLayout()
        self.info_layout = QVBoxLayout()
        self.info_layout.addWidget(self.timer_label)
        self.info_layout.addLayout(self.grid_layout)

        self.setLayout(self.info_layout)

        self.buttons = []
        self.init_board()
        self.start_timer()

    def init_board(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.buttons = []
        size = self.model.board_size
        for y in range(size):
            row = []
            for x in range(size):
                button = QPushButton("")
                button.setFixedSize(40, 40)
                button.clicked.connect(self.create_click_handler(x, y))
                self.grid_layout.addWidget(button, y, x)
                row.append(button)
            self.buttons.append(row)

    def create_click_handler(self, x, y):
        def handler():
            self.make_move(x, y)
        return handler

    def make_move(self, x, y):
        if self.model.make_move(x, y):
            self.update_button(x, y)
            if self.model.check_winner():
                winner = "O" if self.model.current_player == "X" else "X"
                QMessageBox.information(self, "Победа!", f"Победил {winner}!")
                Statistics.add_to_statistics(winner)
                self.reset_game()
            elif self.time_left[self.model.current_player] == 0:
                self.end_game_due_to_timeout()
            else:
                self.update_timer_label()

    def update_button(self, x, y):
        self.buttons[y][x].setText(self.model.board[y][x])

    def reset_game(self):
        self.model.reset_board()
        self.init_board()
        self.time_left = {"X": self.time_limit, "O": self.time_limit}
        self.start_timer()

    def set_board_size(self, size):
        self.model.set_board_size(size)
        self.init_board()

    def start_timer(self):
        self.timer.start(1000)

    def update_timer(self):
        current_player = self.model.current_player
        self.time_left[current_player] -= 1
        self.update_timer_label()

        if self.time_left[current_player] == 0:
            self.end_game_due_to_timeout()

    def update_timer_label(self):
        self.timer_label.setText(self.get_timer_text())

    def get_timer_text(self):
        return f"Время игрока X: {self.time_left['X']} секунд | Время игрока O: {self.time_left['O']} секунд"

    def end_game_due_to_timeout(self):
        self.timer.stop()
        loser = self.model.current_player
        winner = "O" if loser == "X" else "X"
        QMessageBox.information(self, "Время истекло!", f"Игрок {loser} проиграл. Победил {winner}!")
        Statistics.add_to_statistics(winner)
        self.reset_game()
