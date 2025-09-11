'''
This code creates a GUI window for examining world historical events as they relate to one another.
The user can control the time window and types of events they are viewing.
Implementation is handled mostly through use of the Qt PySide6 module
'''

import sys
import random

from settings import *
from core import *
from worldHistoryEvents import * #add all events to worldHistoryEvents list

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QSpacerItem,
    QLineEdit, QComboBox, QPushButton, QLabel, QScrollArea, QSizePolicy
)
from PySide6.QtGui import (
    QIcon, QPainter, QPen, QFont, QColor)
from PySide6.QtCore import Qt, QRect

# TODO: update HistoryScale to deal with odd start dates (e.g. 9011 BCE)


class HistoryScale(QWidget):
    def __init__(self, start_entryline: QLineEdit, end_entryline: QLineEdit, parent=None, 
                 start_date_int=-2000, end_date_int=2000, minor_tick = 100):
        super().__init__(parent)
        self.minor_tick = minor_tick            # Years per small tick
        self.major_tick = 5 * self.minor_tick   # Years per major tick
        self.setFixedHeight(50)     # Scale height // really the height of the major tick
        self.setFixedWidth(SCROLL_WIDTH)    # Scale width
        self.color = dark_blue
        self.setObjectName("history_scale_bar")
        self.setAutoFillBackground(False)

        self.start_entryline = start_entryline
        self.end_entryline = end_entryline

        self.start_date_int = start_date_int
        self.end_date_int = end_date_int
        self.px_per_year = self.width() / (self.end_date_int - self.start_date_int)

    def paintEvent(self, event): #paintEvent(self, event):       
        # print(f"painting {self.minor_tick} minor ticks")
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), self.color)

        pen = QPen(bone)
        pen.setWidth(2)
        painter.setPen(pen)
        font = QFont()
        font.setPointSize(12)
        painter.setFont(font)

        height = self.height()

        # Draw ticks across the scale
        for x in range(self.start_date_int, self.end_date_int, self.minor_tick):
            #x_px_coord = int((x - self.start_date_int)*self.px_per_year) # map x(date) to x pixel coordinates
            x_px_coord = mapDateToScaleBar(x, self.start_date_int, self.px_per_year)
            if x % self.major_tick == 0:
                # Major tick
                painter.drawLine(x_px_coord, height, x_px_coord, 0)
                painter.drawText(x_px_coord + 2, height - 2, dateIntToStr(x))
            else:
                # Minor tick
                painter.drawLine(x_px_coord, height, x_px_coord, height * 0.6)

        painter.end()
    
    def set_tick_spacing(self):
        # recalculate date range, px per year
        try:
            self.start_date_int = dateStrToInt(self.start_entryline.text())
            self.end_date_int = dateStrToInt(self.end_entryline.text())
            self.px_per_year = self.width() / (self.end_date_int - self.start_date_int)
        except:
            print("Incompatible Date Format(s) - try again.")
            return

        # Determine minor/major tick sizes
        scale_factor = 60   # larger factor => more spaced out ticks
        valid_minor_ticks = [5,10,50,100,200,500,1000,2000,5000,10000,20000,50000,100000,200000,500000,1000000,5000000,1000000,5000000,10000000,50000000,100000000,500000000,1000000000]
        
        self.minor_tick = scale_factor / self.px_per_year
        valid_minor_ticks.append(self.minor_tick)
        valid_minor_ticks.sort()
        self.minor_tick = int(valid_minor_ticks[valid_minor_ticks.index(self.minor_tick)+1])    
        self.major_tick = 5 * self.minor_tick
        self.update()

        return

class HistoryEventButton(QPushButton):
    def __init__(self, world_event: WorldEvent, parent, creation_index:int, scale_bar: HistoryScale):
        super().__init__(world_event.icon, parent)
        self.world_event = world_event
        self.creation_index = creation_index
        self.scale_bar = scale_bar

        if not isinstance(self.world_event, WorldSpan):
            self.start_date = self.world_event.date
            self.end_date = None
        else:
            self.start_date = self.world_event.spanStart
            self.end_date = self.world_event.spanEnd

        self.setProperty("tag", "world_event_button")
        self.setToolTip(str(world_event))

        world_event.qButton = self # attach this button instance to WorldEvent object
        self.draw()

    def draw(self):
        x_pos = mapDateToScaleBar(self.start_date, self.scale_bar.start_date_int, self.scale_bar.px_per_year)
        y_pos = random.randrange(50,150)

        # Set random button color
        #tint = random.randrange(100, 130)
        #color = QColor(random.choice(theme_colors)).lighter(tint)
        # world_event_button.setObjectName(f"colorButton{i}")
        # world_event_button.setStyleSheet(f"""QPushButton#colorButton{i} {{
        #                                     background-color: {color};}}""")

        if isinstance(self.world_event, WorldSpan):
            x_pos_right_edge = mapDateToScaleBar(self.world_event.spanEnd, self.scale_bar.start_date_int, self.scale_bar.px_per_year)
            self.setFixedWidth(x_pos_right_edge-x_pos)

        self.move(x_pos, y_pos)
        self.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("World Histories  |  Qt")
        self.setWindowIcon(QIcon('graphics/window_icon.png'))
        self.setGeometry(100, 100, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.active_world_events = [] # world events currently drawable on scroll area (in-scope)

        # === Main Container Widget ===
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # === Top UI Selection Bar ===
        self.UI_topbar = self._build_topbar()
        central_layout.addWidget(self.UI_topbar)

        # === Toggle Button ===
        central_layout.addWidget(self._build_buttons(), alignment= Qt.AlignmentFlag.AlignLeft)

        # === Scrollable Content Area ===
        central_layout.addWidget(self._build_scroll_area())

    def update_scale(self):
        try:
            self.scale_bar.set_tick_spacing()
        except ValueError:
            print("Invalid input: Please enter numeric values")

    def update_worldEvents(self):
        self.active_world_events = [] #reset drawable world_events list
        begin_year, end_year = self.scale_bar.start_date_int, self.scale_bar.end_date_int

        for index, worldEvent in enumerate(worldHistoryEvents):
            # clean up any previous button elements
            if worldEvent.qButton is not None:
                worldEvent.qButton.deleteLater()

            if isinstance(worldEvent, WorldEvent) and not isinstance(worldEvent,WorldSpan):
                if (worldEvent.date < end_year) and (worldEvent.date > begin_year):
                    HistoryEventButton(worldEvent, self.scroll_content, index, self.scale_bar)
                    self.active_world_events.append(worldEvent)
            else:
                if (worldEvent.spanStart < end_year) and (worldEvent.spanEnd > begin_year):
                    #self.draw_worldEvent(worldEvent, index, worldEvent.spanStart)
                    HistoryEventButton(worldEvent, self.scroll_content, index, self.scale_bar)
                    self.active_world_events.append(worldEvent)

    def _build_topbar(self):
        top_bar = QWidget()
        top_bar_layout = QGridLayout()
        top_bar.setLayout(top_bar_layout)

        # Add two date-input text fields
        self.startDateEntry = QLineEdit()
        self.startDateEntry.setText("2000 BCE")
        self.endDateEntry = QLineEdit()
        self.endDateEntry.setText("2000 CE")
        dateLabel1 = QLabel("Start Date")
        dateLabel2 = QLabel("End Date")

        top_bar_layout.addWidget(self.startDateEntry, 1, 0)
        top_bar_layout.addWidget(self.endDateEntry, 1, 1)
        top_bar_layout.addWidget(dateLabel1, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        top_bar_layout.addWidget(dateLabel2, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add four dropdown tag menus
        self.dropdowns = []
        labels = ["Type","Era","Culture","Region"]
        for i in range(4):
            #labelTagList = tagDict[labels[i]]
            combo = QComboBox()
            combo.addItem("All")
            
            for j in range(len(tagDict[labels[i]])):
                #print(tagDict[labels[i]][j])
                if not tagDict[labels[i]][j] in emojiDict:
                    combo.addItem(f"{tagDict[labels[i]][j]}")
                else:
                     combo.addItem(f"{emojiDict[tagDict[labels[i]][j]]} {tagDict[labels[i]][j]}")
            self.dropdowns.append(combo)
            top_bar_layout.addWidget(combo, 1, i+2)
            tagLabel = QLabel(labels[i])
            top_bar_layout.addWidget(tagLabel, 0, i+2, alignment=Qt.AlignmentFlag.AlignCenter)
    
        return top_bar

    def _build_buttons(self):
        self.toggle_button = QPushButton("Rebuild")
        #self.toggle_button.setCheckable(True)
        self.toggle_button.setMinimumWidth(400)
        self.toggle_button.clicked.connect(self.update_scale)
        self.toggle_button.clicked.connect(self.update_worldEvents)

        return self.toggle_button

    def _build_scroll_area(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Only horizontal for now

        scroll_content = QWidget()
        scroll_content.setProperty("tag", "scroll_content")
        scroll_content.setFixedWidth(SCROLL_WIDTH)
        scroll_content.setMinimumHeight(400)

        # Build history scale bar
        self.scale_bar = HistoryScale(start_entryline = self.startDateEntry, end_entryline = self.endDateEntry, parent=scroll_content)
        self.scale_bar.move(0,0)

        scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.scroll_area.setWidget(scroll_content)
        self.scroll_content = scroll_content

        return self.scroll_area

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(theme_main_style_sheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())