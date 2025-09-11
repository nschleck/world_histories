from PySide6.QtWidgets import (
    QApplication, QWidget, QScrollArea, QLabel, QPushButton, QVBoxLayout
)
import sys


class ScrollableArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manual Placement in Scroll Area")

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Create a content widget for scroll area
        content_widget = QWidget()
        content_widget.setMinimumSize(1000, 800)  # Make it big enough to scroll

        # No layout — use absolute positioning
        label1 = QLabel("Label at (100, 100)", content_widget)
        label1.move(100, 100)

        button1 = QPushButton("Button at (300, 200)", content_widget)
        button1.setToolTip("I am placed manually.")
        button1.move(300, 200)

        scroll_area.setWidget(content_widget)

        # Place scroll_area in the main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrollableArea()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())