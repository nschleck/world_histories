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



#TODO bundle date scale panel into a class
#TODO refresh/update to get rid of old elements

#Testing objects
Test_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((0,0),(150,50)),
                                           text="print dates",
                                           tool_tip_text="try me!",
                                           manager=manager,
                                           anchors={'center': 'center'},
                                           container=scroll_area.area)
def test_button1(events):
    for event in events:
        print(event)

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
    rng = date_range()
    ticks = []
    #temporary spacing layout
    '''if rng < 100:
        tick_spacing = 10
    elif rng < 500:
        tick_spacing = 50
    elif rng < 1000:
        tick_spacing = 100
    elif rng < 5000:
        tick_spacing = 500
    else:
        tick_spacing = 1000'''
   
    tick_spacing = 300

    if start < 0:        
        start_tick = ((start % -tick_spacing) - start) * -1
    else:
        start_tick = start - (start % tick_spacing) + tick_spacing
    
    tick = start_tick
    while tick < end:
        ticks.append(tick)        
        tick += tick_spacing

    return ticks
    
def map_scale_to_area(map_from_list):
    map_from_range = map_from_list[-1]-map_from_list[0]
    
    buffer = 20
    map_to_range = scroll_area.width - (buffer * 2)
    map_scale = map_to_range / map_from_range

    mapped_ticks = []
    for tick in map_from_list:
        tick -= map_from_list[0]
        tick = int(tick * map_scale) + buffer
        mapped_ticks.append(tick)

    return mapped_ticks


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
            if event.ui_element == Test_Button:
                ticks = create_date_scale()
                print(ticks)
                ticks_px = map_scale_to_area(ticks)
                print(ticks_px)
                scroll_area.create_ticks(ticks,ticks_px)

        manager.process_events(event)

    manager.update(dt)
    screen.fill(light_purple)
    manager.draw_ui(screen)

    pyg.display.update()