import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


class Statistics(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Статистика")
        self.resize(270, 70)
        self.stats_file = "statistics.json"

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.stats_label = QLabel()
        layout.addWidget(self.stats_label)

        clear_button = QPushButton("Очистить статистику", self)
        clear_button.clicked.connect(self.clear_statistics)
        layout.addWidget(clear_button)

        self.load_statistics()

    def load_statistics(self):
        try:
            with open(self.stats_file, "r") as file:
                stats = json.load(file)
                if not stats:
                    stats = {"X": 0, "O": 0}
        except FileNotFoundError:
            stats = {"X": 0, "O": 0}

            with open(self.stats_file, "w") as file:
                json.dump(stats, file)

        self.stats_label.setText(self.format_statistics(stats))

    def format_statistics(self, stats):
        result = "Статистика побед:\n"
        for player, wins in stats.items():
            result += f"{player}: {wins} побед\n"
        return result

    def clear_statistics(self):
        stats = {"X": 0, "O": 0}
        with open(self.stats_file, "w") as file:
            json.dump(stats, file)
        self.stats_label.setText(self.format_statistics(stats))


    def add_to_statistics(winner):
        stats_file = "statistics.json"
        try:
            with open(stats_file, "r") as file:
                stats = json.load(file)
        except FileNotFoundError:
            stats = {}

        stats[winner] = stats.get(winner, 0) + 1

        with open(stats_file, "w") as file:
            json.dump(stats, file)
