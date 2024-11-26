from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMainWindow

from game.game_view import GameView
from game.settings import Settings
from game.statistics import Statistics


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("5 в ряд")
        self.resize(270, 100)
        self.game_view = GameView()
        self.settings_dialog = Settings()
        self.statistics_dialog = Statistics()
        self.init_ui()

    def init_ui(self):
        play_button = QPushButton("Играть")
        settings_button = QPushButton("Настройки")
        stats_button = QPushButton("Статистика")

        play_button.clicked.connect(self.start_game)
        settings_button.clicked.connect(self.open_settings)
        stats_button.clicked.connect(self.show_statistics)

        layout = QVBoxLayout()
        for button in [play_button, settings_button, stats_button]:
            layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def start_game(self):
        board_size = self.settings_dialog.get_board_size()
        self.game_view.set_board_size(board_size)
        self.game_view.show()

    def open_settings(self):
        self.settings_dialog.show()

    def show_statistics(self):
        self.statistics_dialog.load_statistics()
        self.statistics_dialog.show()
