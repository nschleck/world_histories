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
#top_bar = pyg.Surface((SCREEN_WIDTH,100))
top_bar_UI = pygame_gui.elements.UIPanel(relative_rect=pyg.Rect((0,0),(SCREEN_WIDTH,100)),
                                         manager=manager)
row = [5,40]
col = [20,200,400,590,780,970]

UIdate_start = pygame_gui.elements.UITextEntryLine(relative_rect=pyg.Rect((col[0],row[1]),(150,30)),
                                                initial_text="0",
                                                manager=manager,
                                                container=top_bar_UI)
UIdate_end = pygame_gui.elements.UITextEntryLine(relative_rect=pyg.Rect((col[1],row[1]),(150,30)),
                                              initial_text="2000 CE",
                                              manager=manager,
                                              container=top_bar_UI)
UIdate_start_label = pygame_gui.elements.UILabel(relative_rect=pyg.Rect((col[0],row[0]),(150,50)),
                                               text='Start Date',
                                               manager=manager,
                                               container=top_bar_UI)
UIdate_start_label = pygame_gui.elements.UILabel(relative_rect=pyg.Rect((col[1],row[0]),(150,50)),
                                               text='End Date',
                                               manager=manager,
                                               container=top_bar_UI)
'''date_header = pygame_gui.elements.UILabel(relative_rect=pyg.Rect(((col2+col1)/2,-12),(150,50)),
                                               text='Date Range',
                                               manager=manager,
                                               container=top_bar_UI)'''

tag_list_type = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((col[2],row[0]),(180,70)),
                                                item_list=['All'] + tagDict["type"],
                                                allow_multi_select=True,
                                                manager=manager,
                                                container=top_bar_UI)
tag_list_era = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((col[3],row[0]),(180,70)),
                                                item_list=['All'] + tagDict["era"],
                                                allow_multi_select=True,
                                                manager=manager,
                                                container=top_bar_UI)
tag_list_culture = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((col[4],row[0]),(180,70)),
                                                item_list=['All'] + tagDict["culture"],
                                                allow_multi_select=True,
                                                manager=manager,
                                                container=top_bar_UI)
tag_list_region = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((col[5],row[0]),(180,70)),
                                                item_list=['All'] + tagDict["region"],
                                                allow_multi_select=True,
                                                manager=manager,
                                                container=top_bar_UI)



test_button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((0,0),(150,50)),
                                           text="print dates",
                                           tool_tip_text="try me!",
                                           manager=manager,
                                           anchors={'center': 'center'})

for worldEvent in worldEvents:
    print(worldEvent.typeTag) 

def getSelectedEvents():
    selected_events = []
    for worldEvent in worldEvents:
        common_tags = list(set(worldEvent.typeTag).intersection(tag_list_type.get_multi_selection()))
        if len(common_tags) > 0 or "All" in tag_list_type.get_multi_selection():
            selected_events.append(worldEvent)
    return selected_events


#MAIN APP LOOP
while True:
    dt = clock.tick(60)/1000.0   
    
    display_events = getSelectedEvents()

    '''try:
        date_start = dateFormatToInt(UIdate_start.get_text())
        date_end = dateFormatToInt(UIdate_end.get_text())
    except:
        date_start = "N/A"
        date_end = "N/A"'''
    
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