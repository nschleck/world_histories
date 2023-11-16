#IMPORTS
import pygame as pyg
import sys, pygame_gui
#from pygame.math import Vector2
from settings import *
from utilities import *
from gui import *


#INITIALIZE Pygame, Pygame GUI Manager
pyg.init()
screen = pyg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pyg.display.set_caption('World Histories')
programIcon = pyg.image.load('graphics/window_icon.png')
pyg.display.set_icon(programIcon)
manager = pygame_gui.UIManager((SCREEN_WIDTH,SCREEN_HEIGHT), 'theme.json')
clock = pyg.time.Clock()

#Create UI Elements
UI_topbar = UI_TopBar(manager)

scroll_area_height = SCREEN_HEIGHT-UI_topbar.height
scroll_area = pygame_gui.elements.UIScrollingContainer(relative_rect=pyg.Rect((0,UI_topbar.height),(SCREEN_WIDTH,scroll_area_height)),
                                                       manager=manager)

scroll_area.set_scrollable_area_dimensions((SCREEN_WIDTH*2,scroll_area_height))


#Testing objects
Test_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((0,0),(150,50)),
                                           text="print dates",
                                           tool_tip_text="try me!",
                                           manager=manager,
                                           anchors={'center': 'center'},
                                           container=scroll_area)
def test_button(events):
    for event in events:
        print(event)


#MAIN APP LOOP
while True:
    dt = clock.tick(60)/1000.0   
    
    display_events = UI_topbar.getEventsByTag()

    #EVENT LOOP
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()
        if event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE:
            pyg.quit()
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == Test_Button:
                test_button(display_events)

        
        manager.process_events(event)

    manager.update(dt)
    
    screen.fill(light_purple)
    manager.draw_ui(screen)

    pyg.display.update()