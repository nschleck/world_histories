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
    QSpacerItem, QStyledItemDelegate, QListView, 
    QLineEdit, QComboBox, QPushButton, QLabel, QScrollArea, QSizePolicy
)
from PySide6.QtGui import (
    QIcon, QPainter, QPen, QFont, QColor, QBrush, QPolygon,
    QStandardItem, QStandardItemModel)
from PySide6.QtCore import Qt, QPoint, QRect, Signal, QModelIndex, QItemSelectionModel

# TODO: prevent tooltips from overflowing the scroll_area
# TODO: click scrollarea to kill all tooltips

# TODO: implement tag filtering
# TODO: select era tag => zoom into that time span
# TODO: add links to wiki "learn more"
# TODO: some indication of era in scroll area


class PersistentTooltip(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.adjustSize()

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
        super().paintEvent(event)
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

        #make sure scale starts at a valid tick multiple
        if self.start_date_int % self.minor_tick != 0:
            self.start_date_int = (self.start_date_int // self.minor_tick) * self.minor_tick

        self.update()

        return

class HistoryEventButton(QPushButton):
    def __init__(self, world_event: WorldEvent, parent, creation_index:int, scale_bar: HistoryScale):
        super().__init__(world_event.icon, parent)
        self.world_event = world_event
        self.creation_index = creation_index
        self.scale_bar = scale_bar
        self.scroll_content = parent

        if not isinstance(self.world_event, WorldSpan):
            self.setProperty("tag", "world_event_button")
            self.start_date = self.world_event.date
            self.end_date = None
        else:
            self.setProperty("tag", "world_span_button")
            self.start_date = self.world_event.spanStart
            self.end_date = self.world_event.spanEnd

        world_event.qButton = self # attach this button instance to WorldEvent object
        self.draw()

        self.tooltip = None
        self.clicked.connect(self.show_custom_tooltip)

    def draw(self):
        self.x_pos = mapDateToScaleBar(self.start_date, self.scale_bar.start_date_int, self.scale_bar.px_per_year)
        self.y_pos = random.randrange(50,150)

        # Set random button color TODO get this to work
        # tint = random.randrange(100, 130)
        # color = QColor(random.choice(theme_colors)).lighter(tint)
        # self.setObjectName(f"colorButton{self.creation_index}")
        # self.setStyleSheet(f"""HistoryEventButton#colorButton{self.creation_index} {{
        #                                     background-color: {color};}}""")

        if isinstance(self.world_event, WorldSpan):
            x_pos_right_edge = mapDateToScaleBar(self.world_event.spanEnd, self.scale_bar.start_date_int, self.scale_bar.px_per_year)
            self.setFixedWidth(x_pos_right_edge-self.x_pos)

        self.move(self.x_pos, self.y_pos)
        self.show()
    
    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw a custom pointer triangle
        w = 10
        h = 10
        point1 = QPoint(0, h)
        point2 = QPoint(0, -h)
        point3 = QPoint(w, 0)

        triangle = QPolygon([point1, point2, point3])
        painter.setBrush(QBrush(redwood))
        painter.setPen(Qt.NoPen)  # Optional: no border
        painter.drawPolygon(triangle)

        painter.end()

    def show_custom_tooltip(self):
        if self.tooltip and self.tooltip.isVisible():
            self.tooltip.hide()
            return

        self.tooltip = PersistentTooltip(str(self.world_event), parent=self.scroll_content)
        local_pos = self.mapTo(self.scroll_content, QPoint(0, self.height()))
        self.tooltip.move(local_pos)
        self.tooltip.show()

class CheckableComboBox(QComboBox):
    selectionChanged = Signal(list)

    def __init__(self, list_items, parent=None):
        super().__init__(parent)
        self.setView(QListView())  # To allow for checkable items
        self.setModel(QStandardItemModel(self))
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setPlaceholderText("Select...")

        self._items = list_items
        #self._items = ["All", "0", "1", "2", "3"]
        self._item_lookup = {}

        self._block_signal = False
        self.initItems()
        self.view().pressed.connect(self.handleItemPressed)
        self.setEditable(False)

    def initItems(self):
        for text in self._items:
            item = QStandardItem(text)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
            self.model().appendRow(item)
            self._item_lookup[text] = item

        # Connect signals
        self.model().itemChanged.connect(self.handleItemChanged)

    def handleItemChanged(self, changed_item):
        if self._block_signal:
            return

        self._block_signal = True
        text = changed_item.text()

        if text == "All":
            if changed_item.checkState() == Qt.Checked:
                # Deselect all others
                for t, item in self._item_lookup.items():
                    if t != "All":
                        item.setCheckState(Qt.Unchecked)
            # Else: Do nothing
        else:
            if changed_item.checkState() == Qt.Checked:
                # Deselect "All" if another item is selected
                all_item = self._item_lookup["All"]
                if all_item.checkState() == Qt.Checked:
                    all_item.setCheckState(Qt.Unchecked)

        #self.updateDisplayText()
        #self.selectionChanged.emit(self.getSelectedItems())
        self._block_signal = False

    def updateDisplayText(self):
        return
        #     #self.setEditable(True)
        #     selected = self.getSelectedItems()
        #     display_text = ", ".join(selected) if selected else "Select..."
        #     self.lineEdit().setText(display_text)
        #     #self.setEditable(False)

    def getSelectedItems(self):
        return [
            item.text()
            for item in self._item_lookup.values()
            if item.checkState() == Qt.Checked
        ]

    def handleItemPressed(self, index: QModelIndex):
        item = self.model().itemFromIndex(index)
        if not item:
            return

        # Toggle check state
        checked = item.checkState() == Qt.Checked
        item.setCheckState(Qt.Unchecked if checked else Qt.Checked)



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
        self._build_buttons()
        self.button_panel = QWidget()
        button_layout = QHBoxLayout()
        central_layout.addWidget(self.button_panel)
        self.button_panel.setLayout(button_layout)

        button_layout.addWidget(self.toggle_button)
        button_layout.addWidget(self.hideshow_button)

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

        if self.hidden_tooltips:
            self.hide_show_tooltips()

        for index, worldEvent in enumerate(worldHistoryEvents):
            
            # clean up any previous button/tooltip elements
            if worldEvent.qButton is not None:
                worldEvent.qButton.deleteLater()
                if worldEvent.qButton.tooltip is not None:
                    worldEvent.qButton.tooltip.deleteLater()

            if isinstance(worldEvent, WorldEvent) and not isinstance(worldEvent,WorldSpan):
                if (worldEvent.date < end_year) and (worldEvent.date > begin_year):
                    HistoryEventButton(worldEvent, self.scroll_content, index, self.scale_bar)
                    self.active_world_events.append(worldEvent)
            else:
                if (worldEvent.spanStart < end_year) and (worldEvent.spanEnd > begin_year):
                    #self.draw_worldEvent(worldEvent, index, worldEvent.spanStart)
                    HistoryEventButton(worldEvent, self.scroll_content, index, self.scale_bar)
                    self.active_world_events.append(worldEvent)

    def hide_show_tooltips(self):       
        self.hidden_tooltips = not self.hidden_tooltips #invert boolean
        if self.hidden_tooltips:
            self.hideshow_button.setText("Show ToolTips")
            for worldEvent in self.active_world_events:
                if worldEvent.qButton is not None:
                    if worldEvent.qButton.tooltip is not None:
                        worldEvent.qButton.tooltip.hide()
        else:
            self.hideshow_button.setText("Hide ToolTips")
            for worldEvent in self.active_world_events:
                if worldEvent.qButton is not None:
                    if worldEvent.qButton.tooltip is not None:
                        worldEvent.qButton.tooltip.show()

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
        tag_categories = ["Type","Era","Culture","Region"]
        self.comboboxes = {} #parent combobox list
        for i in range(4):
            tag_category = tag_categories[i]
            labelTagList = tagDict[tag_category]
            # add emojis
            if tag_category == "Type":
                for j in range(len(tagDict[tag_category])):
                    labelTagList[j] = emojiDict[tagDict[tag_category][j]] + labelTagList[j]

            labelTagList.insert(0, "All")

            combo = CheckableComboBox(labelTagList)
            top_bar_layout.addWidget(combo, 1, i+2)
            self.comboboxes[tag_category] = combo #add combobox to self.comboboxes dictionary

            tagLabel = QLabel(tag_category)
            top_bar_layout.addWidget(tagLabel, 0, i+2, alignment=Qt.AlignmentFlag.AlignCenter)
    
        return top_bar

    def _build_buttons(self):
        btn_width = 400
        self.toggle_button = QPushButton("Rebuild")
        #self.toggle_button.setCheckable(True)
        self.toggle_button.setMinimumWidth(btn_width)
        self.toggle_button.clicked.connect(self.update_scale)
        self.toggle_button.clicked.connect(self.update_worldEvents)

        self.hideshow_button = QPushButton("Hide ToolTips")
        self.hideshow_button.setMinimumWidth(btn_width)
        self.hideshow_button.clicked.connect(self.hide_show_tooltips)
        self.hidden_tooltips = False

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