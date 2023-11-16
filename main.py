#IMPORTS
import pygame as pyg
import sys, pygame_gui
#from pygame.math import Vector2
from settings import *
from utilities import *


#INITIALIZE Pygame, Pygame GUI Manager
pyg.init()
screen = pyg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pyg.display.set_caption('World Histories')
programIcon = pyg.image.load('graphics/window_icon.png')
pyg.display.set_icon(programIcon)
manager = pygame_gui.UIManager((SCREEN_WIDTH,SCREEN_HEIGHT), 'theme.json')
clock = pyg.time.Clock()

#Create World Events List
testEvents()

#CONSTRUCT UI TOPBAR
class UI_TopBar:
    def __init__(self) -> None:
        self.panel = pygame_gui.elements.UIPanel(relative_rect=pyg.Rect((0,0),(SCREEN_WIDTH,100)),
                                         manager=manager)
        
        self.row = [5,40]
        self.col = [20,200,400,590,780,970]

        self.date_start_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pyg.Rect((self.col[0],self.row[1]),(150,30)),
                                                initial_text="0",
                                                manager=manager,
                                                container=self.panel)
        self.date_end_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pyg.Rect((self.col[1],self.row[1]),(150,30)),
                                              initial_text="2000 CE",
                                              manager=manager,
                                              container=self.panel)
        self.label_date_start = pygame_gui.elements.UILabel(relative_rect=pyg.Rect((self.col[0],self.row[0]),(150,50)),
                                               text='Start Date',
                                               manager=manager,
                                               container=self.panel)
        self.label_date_end = pygame_gui.elements.UILabel(relative_rect=pyg.Rect((self.col[1],self.row[0]),(150,50)),
                                               text='End Date',
                                               manager=manager,
                                               container=self.panel)

        self.type_selector = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((self.col[2],self.row[0]),(180,70)),
                                                item_list=['All'] + tagDict["type"],
                                                allow_multi_select=True,
                                                manager=manager,
                                                container=self.panel)
        self.era_selector = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((self.col[3],self.row[0]),(180,70)),
                                                item_list=['All'] + tagDict["era"],
                                                allow_multi_select=True,
                                                manager=manager,
                                                container=self.panel)
        self.culture_selector = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((self.col[4],self.row[0]),(180,70)),
                                                item_list=['All'] + tagDict["culture"],
                                                allow_multi_select=True,
                                                manager=manager,
                                                container=self.panel)
        self.region_selector = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((self.col[5],self.row[0]),(180,70)),
                                                item_list=['All'] + tagDict["region"],
                                                allow_multi_select=True,
                                                manager=manager,
                                                container=self.panel)

test_button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((0,0),(150,50)),
                                           text="print dates",
                                           tool_tip_text="try me!",
                                           manager=manager,
                                           anchors={'center': 'center'})

def getEventsByTag(ui_topbar):
    selected_events = []
    for worldEvent in worldEvents:
        common_tags = list(set(worldEvent.typeTag).intersection(ui_topbar.type_selector.get_multi_selection()))
        if len(common_tags) > 0 or "All" in ui_topbar.type_selector.get_multi_selection():
            selected_events.append(worldEvent)
    return selected_events

#Create UI Elements
UI_topbar = UI_TopBar()


#MAIN APP LOOP
while True:
    dt = clock.tick(60)/1000.0   
    
    display_events = getEventsByTag(UI_topbar)

    #EVENT LOOP
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()
        if event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE:
            pyg.quit()
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == test_button:
                #print(str(date_start) + " to " + str(date_end))
                for display_event in display_events:
                    print(display_event)

        
        manager.process_events(event)

    manager.update(dt)
    
    screen.fill(light_purple)
    manager.draw_ui(screen)

    pyg.display.update()