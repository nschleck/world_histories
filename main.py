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
topbar = GUI_TopBar(manager)
scroll_area = GUI_ScrollArea(topbar, manager)
scale_bar = GUI_ScaleBar(topbar,scroll_area,manager)


#TODOs
#TODO bundle date scale panel into a class
#TODO refresh/update to get rid of old elements
#TODO handle timespan objects in draw class
#TODO filter active events by selected date range

#Testing -- Create UI Scale
Scale_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((20,100),(150,50)),
                                           text="create scale",
                                           tool_tip_text="try me!",
                                           manager=manager)

buffer = 20

def calculate_remap_scale(date_list):
    date_range = date_list[-1] - date_list[0]

    px_range = scroll_area.width - (buffer * 2)
    scale_factor = px_range / date_range

    return scale_factor

def remap_date_to_px(date,offset,factor,buffer_width):
    #want: px_postion = (date +/- offset) * factor + buffer_width
    return int((date - offset) * factor) + buffer_width

def create_scale_px_list(date_list,factor):
    mapped_ticks = []
    for tick in date_list:
        tick_pos = remap_date_to_px(tick,date_list[0],factor,buffer)
        mapped_ticks.append(tick_pos)

    return mapped_ticks

#Testing -- create UI event objects
Objects_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((20,150),(150,50)),
                                           text="create objects",
                                           tool_tip_text="try me!",
                                           manager=manager)

drawn_events = []
def draw_events(event_list,ticks,factor,buffer_px):
    event_width = 30
    center_offset = int(event_width / 2)

    for event in event_list:
        x_pos = remap_date_to_px(int(event.date),ticks[0],factor,buffer_px)
        text = dateIntToStr(event.date) + ": " + event.name
        event_graphic = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((x_pos - center_offset,-100),(event_width,event_width)),
                                                    text = "",
                                                    manager=manager,
                                                    tool_tip_text=text,
                                                    anchors={'bottom': 'bottom'},
                                                    object_id=pygame_gui.core.ObjectID(class_id='@event_panel'),
                                                    container=scroll_area.area)
        drawn_events.append(event_graphic)
def reset_drawn_events():
    for event in drawn_events:
        event.kill()

Reset_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((20,200),(150,50)),
                                           text="reset",
                                           tool_tip_text="try me!",
                                           manager=manager)


#Initialize some variables
remap_factor = 1
ticks = []

#MAIN APP LOOP
while True:
    dt = clock.tick(60)/1000.0   
    
    display_events = topbar.getEventsByTag()

    #EVENT LOOP
    for event in pyg.event.get():
        if event.type == pyg.QUIT or (event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE):
            pyg.quit()
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == Scale_Button:
                ticks = scale_bar.create_date_scale()
                print(ticks)

                remap_factor = calculate_remap_scale(ticks)
                ticks_px = create_scale_px_list(ticks,remap_factor)
                print(ticks_px)

                scale_bar.draw_ticks(ticks,ticks_px)
            if event.ui_element == Objects_Button:
                active_events = topbar.getEventsByTag()
                #TODO filter active events by selected date range
                draw_events(active_events,ticks,remap_factor,buffer)
            if event.ui_element == Reset_Button:
                #TODO : reset, delete existing scale and objects
                scale_bar.reset()
                reset_drawn_events()

        manager.process_events(event)

    manager.update(dt)
    screen.fill(light_purple)
    manager.draw_ui(screen)

    pyg.display.update()