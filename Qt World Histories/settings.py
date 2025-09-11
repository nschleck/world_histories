#SETUP
FPS = 60
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# ======= THEME =======
# THEME COLORS
redwood      = "#AF5D63"
wisteria     = "#BDADEA"

bone         = "#D3CABB"
ash_grey     = "#B0AFA0"
periwinkle   = "#b5beff"
blue         = "#7891d6"
dark_blue    = "#454b66"
van_dyke     = "#322a26"
smoky_black  = "#191308"

# THEME COLORS
theme_main_style_sheet = f"""
    QWidget {{
        font-size: 16px;
        background-color: {dark_blue};
        /* border-radius: 15px; */
        /* background-color: rgba(255, 0, 0, 0.2);  red transparent */
    }} 
    
    QPushButton {{
        font-size: 22px;
    }}
    QPushButton:hover {{
        background-color: {blue};
    }}
    QPushButton:pressed {{
        background-color: {periwinkle};
    }}
    QLabel {{
        
    }}
    QComboBox {{
        background-color: {blue};
        min-width: 100px;
    }}
    QLineEdit {{
        background-color: {blue};
        min-width: 100px;
    }}

    QScrollArea {{
        background-color: {bone};
        color: white;
        border: 2px solid {van_dyke};
        border-radius: 6px;
        padding: 12px;
    }}
    QScrollBar:horizontal {{
        background: {ash_grey};
        min-height: 30px;  /* Lower min height for responsive drag */
        border-radius: 0px;
    }}
    QScrollBar::handle:horizontal {{
        background: {blue};
        border: 4px solid {dark_blue};
        width: 20px;
        max-height: 20px;
        border-radius: 15px;
    }}
    QScrollBar::add-line:horizontal, 
    QScrollBar::sub-line:horizontal {{
        border-radius: 0px;
        background: transparent;  /* MUST BE SET */
    }}
    QScrollBar::add-page:horizontal,
    QScrollBar::sub-page:horizontal {{  
        border-radius: 0px;
        background: transparent;  /* MUST BE SET */
    }}
    QScrollBar::handle:hover {{
        background: {periwinkle};
    }}
    QScrollBar::handle:pressed {{
        border: 4px solid {blue};
    }}

    HistoryScale {{
        background-color: {ash_grey};
        color: {ash_grey};
        background: {ash_grey};
        border-radius: 10px;
    }}
"""