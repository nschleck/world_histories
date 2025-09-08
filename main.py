'''
This code creates a GUI window for examining world historical events as they relate to one another.
The user can control the time window and types of events they are viewing.
Implementation is handled mostly through use of the Pygame GUI module.
'''

#TODOs
#TODO: #if event_graphic.pressed_event == True: #check button pressed without going through pygame.Event system
#TODO: allow resizing of scrollable width
#TODO: allow resizing of window
#TODO: display event tooltips by default, click to turn off?
#TODO: left click to display alternate tooltip? (taglist, description, wiki link)
#TODO: sort drawn events into multiple y-levels, i.e. no overlapping. Sort by start date first? 
#TODO: implement color themeing, allow input to set themeing parameters?
#TODO: add emoticons / visual themeing to help distinguish icons
#TODO: don't allow dates before 13.5 BYA, or after 2100
#TODO: cleanup terminology / data handling: event(pygame), Event(WorldEvent), GUI_Event class

#IMPORTS
import sys
import pygame as pyg
import pygame_gui
#from pygame.math import Vector2
from settings import *
from utilities import *
from gui import *

def initialize_GUI():    
    pyg.init()
    screen = pyg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pyg.RESIZABLE)
    pyg.display.set_caption('World Histories')
    programIcon = pyg.image.load('graphics/window_icon.png')
    pyg.display.set_icon(programIcon)
    manager = pygame_gui.UIManager((SCREEN_WIDTH,SCREEN_HEIGHT), 'theme.json')
    clock = pyg.time.Clock()
    
    return screen, manager, clock

def doEventLoop(manager: pygame_gui.UIManager, 
                topbar: GUI_TopBar, 
                scroll_area: GUI_ScrollArea, 
                scale_bar: GUI_ScaleBar, 
                build_btn: pygame_gui.elements.UIButton, 
                reset_btn:pygame_gui.elements.UIButton,
                old_events_list: list) -> list:
    
    active_gui_events = old_events_list #default return, unless modified by build_button press

    for event in pyg.event.get():
        if event.type == pyg.QUIT or (event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE):
            pyg.quit()
            sys.exit()
        elif event.type == pyg.VIDEORESIZE:
                # Update screen dimensions
                new_scr_width, new_scr_height = event.size
                # Recreate the display surface with the new dimensions
                # screen = pyg.display.set_mode((new_scr_width, new_scr_height), pyg.RESIZABLE)
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == build_btn:
                scale_bar.reset()
                scale_bar.create_date_scale()
                scale_bar.calculate_remap_factor(scale_bar.scale_ticks_list)
                scale_bar.create_scale_px_list(scale_bar.scale_ticks_list)
                scale_bar.draw_ticks(scale_bar.scale_ticks_list)

                try:
                    reset_gui_events(old_events_list)
                except:
                    pass

                active_events = topbar.getEventsByTag()
                active_events = filterEventsByDate(active_events, scale_bar.scale_ticks_list)

                active_gui_events = draw_gui_events(active_events, manager, scale_bar, scroll_area.area)

            elif event.ui_element == reset_btn:
                scale_bar.reset()
                reset_gui_events(old_events_list)
                active_gui_events = []

        manager.process_events(event)

    return active_gui_events

#MAIN APP LOOP
def main():
    #INITIALIZE Pygame, Pygame GUI Manager
    screen, manager, clock = initialize_GUI()
    gui_event_objs = []

    #Create GUI Elements
    Topbar = GUI_TopBar(manager)
    Scroll_area = GUI_ScrollArea(Topbar, manager)
    Scale_bar = GUI_ScaleBar(Topbar,Scroll_area,manager)
    Build_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((20,100),(150,50)),
                                            text="Build Objects",
                                            tool_tip_text="try me!",
                                            manager=manager)
    Reset_Button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((20,150),(150,50)),
                                            text="Reset",
                                            tool_tip_text="try me!",
                                            manager=manager)    

    while True:
        dt = clock.tick(60)/1000.0   

        gui_event_objs = doEventLoop(manager, Topbar, Scroll_area, Scale_bar, Build_Button, Reset_Button, gui_event_objs)
        manager.update(dt)
        
        screen.fill(light_purple)
        manager.draw_ui(screen)

        pyg.display.update()

if __name__ == "__main__":
    main()