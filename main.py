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
#TODO: #if event_graphic.pressed_event == True: #check button pressed without going through pygame.Event system
#TODO: allow resizing of scrollable width
#TODO: display event tooltips by default, click to turn off
#TODO: left click to display alternate tooltip? (taglist, description, wiki link)
#TODO: sort drawn events into multiple y-levels, i.e. no overlapping. Sort by start date first? 
#TODO: implement color themeing, allow input to set themeing parameters
#TODO: add emoticons / visual themeing to help distinguish icons

#Testing objects
Scale_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((20,100),(150,50)),
                                           text="create scale",
                                           tool_tip_text="try me!",
                                           manager=manager)
Objects_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((20,150),(150,50)),
                                           text="create objects",
                                           tool_tip_text="try me!",
                                           manager=manager)
Reset_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((20,200),(150,50)),
                                           text="reset",
                                           tool_tip_text="try me!",
                                           manager=manager)

#MAIN APP LOOP
while True:
    dt = clock.tick(60)/1000.0   

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
                active_events = filterEventsByDate(active_events,Scale_bar.scale_ticks_list)

                try:
                    Events_Objs.reset()
                except:
                    pass

                Events_Objs = GUI_Events(Scroll_area.area, manager, active_events)
                Events_Objs.draw_gui_events(Scale_bar) #TODO make this part of __init__?

            if event.ui_element == Reset_Button:
                Scale_bar.reset()
                Events_Objs.reset()

        manager.process_events(event)

    manager.update(dt)
    
    screen.fill(light_purple)
    manager.draw_ui(screen)

    pyg.display.update()