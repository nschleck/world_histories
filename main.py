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

#Create GUI Elements
Topbar = GUI_TopBar(manager)
Scroll_area = GUI_ScrollArea(Topbar, manager)
Scale_bar = GUI_ScaleBar(Topbar,Scroll_area,manager)


#TODOs
#TODO handle timespan objects in draw class
#TODO filter active events by selected date range
#TODO: #if event_graphic.pressed_event == True: #check button pressed without going through pygame.Event system

#Testing -- Create UI Scale
Scale_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((20,100),(150,50)),
                                           text="create scale",
                                           tool_tip_text="try me!",
                                           manager=manager)

buffer = 20

#Testing -- create UI event objects
Objects_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((20,150),(150,50)),
                                           text="create objects",
                                           tool_tip_text="try me!",
                                           manager=manager)

drawn_events = []

Reset_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((20,200),(150,50)),
                                           text="reset",
                                           tool_tip_text="try me!",
                                           manager=manager)

#MAIN APP LOOP
while True:
    dt = clock.tick(60)/1000.0   
    
    display_events = Topbar.getEventsByTag()

    #EVENT LOOP
    for event in pyg.event.get():
        if event.type == pyg.QUIT or (event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE):
            pyg.quit()
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == Scale_Button:
                Scale_bar.create_date_scale()
                Scale_bar.calculate_remap_factor(Scale_bar.scale_ticks_list)
                Scale_bar.create_scale_px_list(Scale_bar.scale_ticks_list)
                Scale_bar.draw_ticks(Scale_bar.scale_ticks_list)

            if event.ui_element == Objects_Button:
                active_events = Topbar.getEventsByTag()

                #TODO filter active events by selected date range
                Events_Objs = GUI_Events(Scroll_area.area,manager,active_events)
                Events_Objs.draw_gui_events(Scale_bar.scale_ticks_list,Scale_bar.remap_factor,buffer) #TODO make this part of __init__

            if event.ui_element == Reset_Button:
                Scale_bar.reset()
                Events_Objs.reset()

        manager.process_events(event)

    manager.update(dt)
    
    screen.fill(light_purple)
    manager.draw_ui(screen)

    pyg.display.update()