from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

import sys

# ✅ Step 1: Create a custom widget
class MyCustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        label = QLabel("Hello from MyCustomWidget")
        layout.addWidget(label)

# ✅ Step 2: Set up the application and apply QSS
app = QApplication(sys.argv)

# You can apply QSS using class name
style_sheet = """
MyCustomWidget {
    background-color: #f0f0ff;
    border: 2px solid #6666ff;
    border-radius: 10px;
    padding: 10px;
}

MyCustomWidget#specialOne {
    background-color: #fff0f0;
    border: 2px dashed #ff6666;
}
"""

app.setStyleSheet(style_sheet)

# ✅ Step 3: Instantiate and show the widgets
normal_widget = MyCustomWidget()
normal_widget.setWindowTitle("Normal MyCustomWidget")
normal_widget.resize(300, 100)
normal_widget.show()

special_widget = MyCustomWidget()
special_widget.setObjectName("specialOne")  # For targeted QSS
special_widget.setWindowTitle("Styled with Object Name")
special_widget.resize(300, 100)
special_widget.show()

sys.exit(app.exec_())