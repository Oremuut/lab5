from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox


class Settings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.resize(270, 70)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Размер поля (от 10 до 20):", self))

        self.size = 10

        self.size_input = QLineEdit(self)
        self.size_input.setPlaceholderText("Введите число")
        layout.addWidget(self.size_input)

        save_button = QPushButton("Сохранить", self)
        save_button.clicked.connect(self.validate)
        layout.addWidget(save_button)

    def validate(self):
        try:
            size = int(self.size_input.text())
            if 10 <= size <= 20:
                self.size = size
            else:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите число от 10 до 20!")

    def get_board_size(self):
        return self.size
