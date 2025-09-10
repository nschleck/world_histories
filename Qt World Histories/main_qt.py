import sys

from settings import *
from core import *
from worldHistoryEvents import * #add all events to worldHistoryEvents list

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QSpacerItem,
    QLineEdit, QComboBox, QPushButton, QLabel, QScrollArea, QSizePolicy
)
from PySide6.QtGui import (
    QIcon, QPainter, QPen, QFont)
from PySide6.QtCore import Qt, QRect

class HistoryScale(QWidget):
    def __init__(self):
        super().__init__()
        self.minor_tick = 100     # Pixels per small tick
        self.major_tick = 500     # Pixels per major tick
        self.setFixedHeight(30)     # Scale height // really the height of the major tick
        self.setFixedWidth(3000)    # Scale width
        self.color = ash_grey
        self.setAutoFillBackground(False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(bone)
        pen.setWidth(2)
        painter.setPen(pen)
        font = QFont()
        font.setPointSize(12)
        painter.setFont(font)

        width = self.width()
        height = self.height()

        # Draw ticks across the scale
        for x in range(0, width, self.minor_tick):
            if x % self.major_tick == 0:
                # Major tick
                painter.drawLine(x, height, x, 0)
                painter.drawText(x + 2, height - 2, f"{x}")
            else:
                # Minor tick
                painter.drawLine(x, height, x, height * 0.6)

        painter.end()
    
    def mousePressEvent(self, event):
        self.color = blue
        self.update()  # Triggers paintEvent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("World Histories  |  Qt")
        self.setWindowIcon(QIcon('graphics/window_icon.png'))
        self.setGeometry(100, 100, SCREEN_WIDTH, SCREEN_HEIGHT)

        # === Main Container Widget ===
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # === Top UI Selection Bar ===
        central_layout.addWidget(self._init_build_topbar())

        # === Toggle Button ===
        central_layout.addWidget(self._init_build_buttons(), alignment= Qt.AlignmentFlag.AlignLeft)

        # === Scrollable Content Area ===
        central_layout.addWidget(self._init_build_scroll_area())

    def toggle_content_visibility(self):
        is_hidden = self.scroll_content.isHidden()
        self.scroll_content.setVisible(is_hidden)
        if is_hidden:
            self.toggle_button.setText("Hide Content Below")
        else:
            self.toggle_button.setText("Show Content Below")

    def _init_build_topbar(self):
        top_bar = QWidget()
        top_bar_layout = QGridLayout()
        top_bar.setLayout(top_bar_layout)

        # Add two text fields
        self.startDateEntry = QLineEdit()
        self.startDateEntry.setPlaceholderText("Date Range Start")
        self.endDateEntry = QLineEdit()
        self.endDateEntry.setPlaceholderText("Date Range End")
        dateLabel1 = QLabel("Start Date")
        dateLabel2 = QLabel("End Date")

        top_bar_layout.addWidget(self.startDateEntry, 1, 0)
        top_bar_layout.addWidget(self.endDateEntry, 1, 1)
        top_bar_layout.addWidget(dateLabel1, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        top_bar_layout.addWidget(dateLabel2, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add four dropdowns
        self.dropdowns = []
        for i in range(4):
            combo = QComboBox()
            combo.addItems([f"Option {i+1}.{j+1}" for j in range(5)])
            self.dropdowns.append(combo)
            top_bar_layout.addWidget(combo, 1, i+2)
            tagLabel = QLabel(f"Tags {i+1}")
            top_bar_layout.addWidget(tagLabel, 0, i+2, alignment=Qt.AlignmentFlag.AlignCenter)
    
        return top_bar

    def _init_build_buttons(self):
        self.toggle_button = QPushButton("Hide Content Below")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setMinimumWidth(400)
        # self.toggle_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #3498db;
        #         color: white;
        #         border: 2px solid #2980b9;
        #         border-radius: 12px;
        #         padding: 10px;
        #         font-size: 16px;
        #     }
        #     QPushButton:hover {
        #         background-color: #2980b9;
        #     }
        #     QPushButton:pressed {
        #         background-color: #1c5980;
        #     }
        #     """)
        self.toggle_button.clicked.connect(self.toggle_content_visibility)

        return self.toggle_button

    def _init_build_scroll_area(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Only horizontal for now

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()

        # Simulate large content
        # for i in range(20):
        #     lbl = QLabel(f"Element \N{GRINNING FACE} {i+1}")
        #     lbl.setStyleSheet("border: 1px solid gray; padding: 10px;")
        #     lbl.setMinimumWidth(200)
        #     lbl.setAlignment(Qt.AlignCenter)
        #     scroll_layout.addWidget(lbl)

        # Build history scale bar
        scale_bar = HistoryScale()
        scroll_layout.addWidget(scale_bar)
        scroll_layout.setAlignment(scale_bar, Qt.AlignmentFlag.AlignBottom)


        scroll_content.setLayout(scroll_layout)
        scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.scroll_area.setWidget(scroll_content)
        self.scroll_content = scroll_content  # Save for hiding/showing

        return self.scroll_area

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(theme_main_style_sheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())