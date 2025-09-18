#SETUP
FPS = 60
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCROLL_WIDTH = 3000

# ======= THEME =======
# THEME COLORS
redwood      = "#AF5D63"
wisteria     = "#BDADEA"

white        = "#FFFFFF"
bone         = "#D3CABB"
ash_grey     = "#B0AFA0"
periwinkle   = "#b5beff"
blue         = "#7891d6"
dark_blue    = "#454b66"
van_dyke     = "#322a26"
smoky_black  = "#191308"

# extra random element colors
orange      = "#F3A712"
red_sand    = "#E4BB97"
lime        = "#FCFF6C"
mint        = "#D7FFAB"
jade        = "#44AF69"
aqua        = '#44BBA4'
viridian    = "#4C8577"
sky_blue    = "#44CCFF"
bean        = "#2F0601"
dark_purple = "#32021F"



theme_colors = [redwood, wisteria, bone, ash_grey, periwinkle, blue, dark_blue, van_dyke, smoky_black]
scrollarea_colors = [redwood, wisteria, periwinkle, blue, orange, red_sand, lime, mint, jade, aqua, viridian, sky_blue, bean, dark_purple]

# THEME COLORS
theme_main_style_sheet = f"""
    /* Central Themeing */
    QWidget {{
        font-size: 16px;
        background-color: {dark_blue};
        /* border-radius: 15px; */
        /* background-color: rgba(255, 0, 0, 0.2);  red transparent */
    }} 
    QWidget[tag="scroll_content"] {{
        background-color: {ash_grey};
    }} 

    #history_scale_bar {{
        padding: 12px;
        border-radius: 15px;
    }} 

    QComboBox {{
        background-color: {blue};
        min-width: 150px;
    }}
    QComboBox QAbstractItemView::indicator {{
        width: 20px;
        height: 20px;
        border: 2px solid {ash_grey};
        border-radius: 5px;
        background-color: {van_dyke};
    }}
    QComboBox QAbstractItemView::indicator:checked {{
        background-color: {redwood};
    }}
    QComboBox QAbstractItemView::item {{
        padding: 4px;
    }}
    QComboBox QAbstractItemView::item:selected {{
        background-color: {ash_grey};
    }}
    QComboBox QAbstractItemView::item:hover {{
        background-color: {van_dyke};
        border: none;
    }}


    QLineEdit {{
        background-color: {blue};
        min-width: 100px;
    }}
    QPushButton {{
        background-color: {blue};
        border: 2px solid {ash_grey};
        border-radius: 6px;
        font-size: 22px;
    }}
    QPushButton:hover {{
        background-color: {blue};
        border: 2px solid {bone};
    }}
    QPushButton:pressed {{
        background-color: {periwinkle};
    }}

    
    /* World Event button objects */
    QPushButton[tag="world_event_button"] {{
        font-size: 24px;
        padding: 6px;
        border-radius: 15px;
        background-color: rgba(255, 0, 0, 0.2);
    }} 
    QPushButton[tag="world_span_button"] {{
        font-size: 24px;
        padding: 6px;
        border-radius: 15px;
        background-color: rgba(0, 0, 255, 0.2);
    }}  
    PersistentTooltip {{
        background-color: {dark_blue};
        border: 2px solid {blue};
        padding: 6px;
        font-size: 14px;
        border-radius: 12px;
    }}  

    
    /* Scroll Area objects */
    QScrollArea {{
        background-color: {bone};
        color: white;
        border: 2px solid {van_dyke};
        border-radius: 6px;
        padding: 6px;
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
"""