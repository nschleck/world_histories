#SETUP
FPS = 60
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# ======= THEME =======
# THEME COLORS
redwood      = "#AF5D63"
wisteria     = "#BDADEA"
periwinkle   = "#b5beff"
blue         = "#7891d6"
dark_blue    = "#454b66"
van_dyke     = "#322a26"
smoky_black  = "#191308"

# THEME COLORS
theme_main_style_sheet = f"""
    QWidget {{
        font-size: 16px;
    }} 
    
    QPushButton {{
        font-size: 22px;
    }}
    QLabel {{
        
    }}
    QComboBox {{
        background-color: {dark_blue};
    }}
    QLineEdit {{
        background-color: {dark_blue};
    }}

    QScrollArea {{
        background-color: {wisteria};
        color: white;
        border: 2px solid {van_dyke};
        border-radius: 6px;
        padding: 5px;
    }}
    QScrollBar:horizontal {{
        background: {van_dyke};
        min-height: 30px;  /* Lower min height for responsive drag */
        border-radius: 15px;
    }}
    QScrollBar::handle:horizontal {{
        background: {dark_blue};
        border: 4px solid {van_dyke};
        width: 20px;
        max-height: 20px;
        border-radius: 15px;
    }}
    QScrollBar::add-line:horizontal, 
    QScrollBar::sub-line:horizontal {{
        background: transparent;  /* MUST BE SET */
    }}
    QScrollBar::add-page:horizontal,
    QScrollBar::sub-page:horizontal {{  
        background: transparent;  /* MUST BE SET */
    }}
    QScrollBar::handle:hover {{
        border: 4px solid {dark_blue};
        background: {blue};
    }}
    QScrollBar::handle:pressed {{
        background: {periwinkle};
    }}
"""