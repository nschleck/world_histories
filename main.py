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


#TODOs
#TODO bundle date scale panel into a class
#TODO refresh/update to get rid of old elements
#TODO handle timespan objects in draw class
#TODO filter active events by selected date range
#TODO adjust scale endposts to be inclusive

#Testing -- Create UI Scale
Scale_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((20,100),(150,50)),
                                           text="create scale",
                                           tool_tip_text="try me!",
                                           manager=manager)

def date_range():
    #return date range
    try:
        start = dateStrToInt(topbar.date_start_entry.get_text())
        end = dateStrToInt(topbar.date_end_entry.get_text())
        return end - start
    except:
        return 0

def create_date_scale():
    start = dateStrToInt(topbar.date_start_entry.get_text())
    end = dateStrToInt(topbar.date_end_entry.get_text())
    int_range = date_range()
    ticks = []

    ideal_spacing = int_range / 15
    available_spacing = [5,10,50,100,200,500,1000,5000,10000,50000,100000,500000,1000000,5000000,1000000,5000000,10000000,50000000,100000000,500000000,1000000000]
    available_spacing.append(ideal_spacing)
    available_spacing.sort()
    index = available_spacing.index(ideal_spacing)

    tick_spacing = int(available_spacing[index+1])

    if start < 0:        
        start_tick = ((start % -tick_spacing) - start) * -1 #TODO adjust scale endposts to be inclusive
    else:
        start_tick = start - (start % tick_spacing) + tick_spacing #TODO adjust scale endposts to be inclusive
    
    tick = start_tick
    while tick < end:
        ticks.append(tick)        
        tick += tick_spacing

    return ticks

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
                ticks = create_date_scale()
                print(ticks)

                remap_factor = calculate_remap_scale(ticks)
                ticks_px = create_scale_px_list(ticks,remap_factor)
                print(ticks_px)

                scroll_area.create_ticks(ticks,ticks_px)
            if event.ui_element == Objects_Button:
                active_events = topbar.getEventsByTag()
                #TODO filter active events by selected date range
                draw_events(active_events,ticks,remap_factor,buffer)

        manager.process_events(event)

    manager.update(dt)
    screen.fill(light_purple)
    manager.draw_ui(screen)

    pyg.display.update()