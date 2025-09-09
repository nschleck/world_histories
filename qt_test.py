import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QPushButton, QLabel, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Complex GUI Layout Example")
        self.setGeometry(100, 100, 900, 600)

        # === Main Container Widget ===
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # === Top Selection Bar ===
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout()
        top_bar.setLayout(top_bar_layout)

        # Add two text fields
        self.text1 = QLineEdit()
        self.text1.setPlaceholderText("Enter text 1")
        self.text2 = QLineEdit()
        self.text2.setPlaceholderText("Enter text 2")

        top_bar_layout.addWidget(self.text1)
        top_bar_layout.addWidget(self.text2)

        # Add four dropdowns
        self.dropdowns = []
        for i in range(4):
            combo = QComboBox()
            combo.addItems([f"Option {i+1}.{j+1}" for j in range(5)])
            self.dropdowns.append(combo)
            top_bar_layout.addWidget(combo)

        central_layout.addWidget(top_bar)

        # === Toggle Button ===
        self.toggle_button = QPushButton("Hide Content Below")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_content_visibility)
        central_layout.addWidget(self.toggle_button)

        # === Scrollable Content Area ===
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Only horizontal for now

        scroll_content = QWidget()
        scroll_layout = QHBoxLayout()  # Horizontal scroll

        # Simulate large content
        for i in range(20):
            lbl = QLabel(f"Element {i+1}")
            lbl.setStyleSheet("border: 1px solid gray; padding: 10px;")
            lbl.setMinimumWidth(120)
            lbl.setAlignment(Qt.AlignCenter)
            scroll_layout.addWidget(lbl)

        scroll_content.setLayout(scroll_layout)
        scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.scroll_area.setWidget(scroll_content)
        self.scroll_content = scroll_content  # Save for hiding/showing

        central_layout.addWidget(self.scroll_area)

    def toggle_content_visibility(self):
        is_hidden = self.scroll_content.isHidden()
        self.scroll_content.setVisible(is_hidden)
        if is_hidden:
            self.toggle_button.setText("Hide Content Below")
        else:
            self.toggle_button.setText("Show Content Below")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
