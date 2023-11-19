#IMPORTS
import pygame as pyg
import pygame_gui
from settings import *
from utilities import *

#UI TOPBAR Object
class GUI_TopBar:
    def __init__(self, manager) -> None:
        self.manager = manager
        
        self.height = 100
        self.panel = pygame_gui.elements.UIPanel(relative_rect=pyg.Rect((0,0),(SCREEN_WIDTH,self.height)),
                                         manager=manager)
        
        self.row = [5,40]
        self.col = [20,200,400,590,780,970]

        self.date_start_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pyg.Rect((self.col[0],self.row[1]),(150,30)),
                                                initial_text="1000 BCE",
                                                manager=self.manager,
                                                container=self.panel)
        self.date_end_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pyg.Rect((self.col[1],self.row[1]),(150,30)),
                                              initial_text="2000 CE",
                                              manager=self.manager,
                                              container=self.panel)
        self.label_date_start = pygame_gui.elements.UILabel(relative_rect=pyg.Rect((self.col[0],self.row[0]),(150,50)),
                                               text='Start Date',
                                               manager=self.manager,
                                               container=self.panel)
        self.label_date_end = pygame_gui.elements.UILabel(relative_rect=pyg.Rect((self.col[1],self.row[0]),(150,50)),
                                               text='End Date',
                                               manager=self.manager,
                                               container=self.panel)

        self.type_selector = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((self.col[2],self.row[0]),(180,70)),
                                                item_list=['All'] + tagDict["type"],
                                                allow_multi_select=True,
                                                manager=self.manager,
                                                container=self.panel,
                                                default_selection='All')
        self.era_selector = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((self.col[3],self.row[0]),(180,70)),
                                                item_list=['All'] + tagDict["era"],
                                                allow_multi_select=True,
                                                manager=self.manager,
                                                container=self.panel,
                                                default_selection='All')
        self.culture_selector = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((self.col[4],self.row[0]),(180,70)),
                                                item_list=['All'] + tagDict["culture"],
                                                allow_multi_select=True,
                                                manager=self.manager,
                                                container=self.panel,
                                                default_selection='All')
        self.region_selector = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((self.col[5],self.row[0]),(180,70)),
                                                item_list=['All'] + tagDict["region"],
                                                allow_multi_select=True,
                                                manager=self.manager,
                                                container=self.panel,
                                                default_selection='All')

    def getEventsByTag(self):
        selected_events = []
        for worldEvent in worldEvents:
            common_type_tags = list(set(worldEvent.typeTag).intersection(self.type_selector.get_multi_selection()))
            if len(common_type_tags) == 0 and "All" not in self.type_selector.get_multi_selection():
                continue
            common_era_tags = list(set(worldEvent.eraTag).intersection(self.era_selector.get_multi_selection()))
            if len(common_era_tags) == 0 and "All" not in self.era_selector.get_multi_selection():
                continue
            common_culture_tags = list(set(worldEvent.cultureTag).intersection(self.culture_selector.get_multi_selection()))
            if len(common_culture_tags) == 0 and "All" not in self.culture_selector.get_multi_selection():
                continue
            common_region_tags = list(set(worldEvent.regionTag).intersection(self.region_selector.get_multi_selection()))
            if len(common_region_tags) == 0 and "All" not in self.region_selector.get_multi_selection():
                continue
            selected_events.append(worldEvent)

        return selected_events

class GUI_ScrollArea:
    def __init__(self, topbar, manager) -> None:
        self.manager = manager        
        self.topbar = topbar

        self.width = SCREEN_WIDTH*2
        self.height = SCREEN_HEIGHT-self.topbar.height
        self.ypos = self.topbar.height

        self.area = pygame_gui.elements.UIScrollingContainer(relative_rect=pyg.Rect((0,self.ypos),(SCREEN_WIDTH,self.height)),
                                                             manager=self.manager)
        
        self.area.set_scrollable_area_dimensions((self.width,self.height-20))

class GUI_ScaleBar:
    def __init__(self,topbar,scroll_area,manager) -> None:
        self.manager = manager
        self.topbar = topbar
        self.scroll_area = scroll_area
        
        self.width = self.scroll_area.width
        self.height = 50
        self.scale_panel = pygame_gui.elements.UIPanel(relative_rect=pyg.Rect((0,(self.height*-1)+5),(self.width,self.height)),
                                                             manager=self.manager,
                                                             anchors={'bottom': 'bottom'},
                                                             object_id=pygame_gui.core.ObjectID(class_id='@scale_panel'),
                                                             container = self.scroll_area.area)
        
        self.UIticks = []
        self.UItick_labels = []

    def create_date_scale(self):
        start = dateStrToInt(self.topbar.date_start_entry.get_text())
        end = dateStrToInt(self.topbar.date_end_entry.get_text())
        int_range = end - start
        ticks = []

        ideal_spacing = int_range / 15
        available_spacing = [5,10,50,100,200,500,1000,2000,5000,10000,20000,50000,100000,200000,500000,1000000,5000000,1000000,5000000,10000000,50000000,100000000,500000000,1000000000]
        available_spacing.append(ideal_spacing)
        available_spacing.sort()
        index = available_spacing.index(ideal_spacing)
        tick_spacing = int(available_spacing[index+1])     
        
        start_tick = start - (start % tick_spacing)
        tick = start_tick-tick_spacing
        while tick < end:
            tick += tick_spacing
            ticks.append(tick)  

        return ticks

    def draw_ticks(self,date_list,px_list):
        for i in range(len(date_list)):
            pos_x = px_list[i]
            if date_list[i] == 0:
                tick_height = 40
            else:
                tick_height = 20

            tick_mark = pygame_gui.elements.UIPanel(relative_rect=pyg.Rect((pos_x,(tick_height+10)*-1),(5,tick_height)),
                                            manager=self.manager,
                                            anchors={'bottom': 'bottom'},
                                            container=self.scroll_area.area,
                                            object_id=pygame_gui.core.ObjectID(class_id='@tick_panel'))
            self.UIticks.append(tick_mark)
            label = dateIntToStr(date_list[i])
            if not i == len(date_list) - 1:
                tick_label = pygame_gui.elements.UILabel(relative_rect=pyg.Rect((pos_x+10,-32),(200,25)),
                                                        text=label,
                                                        manager=self.manager,
                                                        anchors={'bottom': 'bottom'},
                                                        container=self.scroll_area.area,
                                                        object_id=pygame_gui.core.ObjectID(class_id='@tick_label'))
                self.UItick_labels.append(tick_label)

    def reset(self):
        for tick_mark in self.UIticks:
            tick_mark.kill()
        for tick_label in self.UItick_labels:
            tick_label.kill()

class GUI_Event:
    def __init__(self, Event, graphics_area, manager, x_pos) -> None:
        self.manager = manager
        self.graphics_area = graphics_area
        self.Event = Event
        self.x_pos = x_pos
        
        #temp color
        self.color = pyg.Color(0,0,0,255)
        self.width = 30
        self.center_offset = int(self.width / 2)

        self.text = dateIntToStr(self.Event.date) + ": " + self.Event.name

        self.button = pygame_gui.elements.UIButton(relative_rect=pyg.Rect((self.x_pos - self.center_offset,-100),(self.width,self.width)),
                                                    text = "",
                                                    manager=manager,
                                                    tool_tip_text=self.text,
                                                    anchors={'bottom': 'bottom'},
                                                    object_id=pygame_gui.core.ObjectID(class_id='@event_panel'),
                                                    container=self.graphics_area)

class GUI_Events:
    def __init__(self, graphics_area, manager, events_list) -> None:
        self.manager = manager
        self.graphics_area = graphics_area
        self.events_list = events_list

        self.GUI_Events_list = []

        #self.draw_gui_events()

    
    def draw_gui_events(self,ticks,factor,buffer_px):
        #TODO: move factor, buffer, ticks to GUI scale object?
        #TODO cleanup function, move to init
        for Event in self.events_list:
            x_pos = remap_date_to_px(int(Event.date),ticks[0],factor,buffer_px)
            gui_Event = GUI_Event(Event,self.graphics_area,self.manager,x_pos)
            self.GUI_Events_list.append(gui_Event)

    def reset(self):
        for Event in self.GUI_Events_list:
            Event.button.kill()
