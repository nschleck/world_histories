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
        
        self.area.set_scrollable_area_dimensions((self.width,self.height))

        self.scale_height = 50
        self.scale_panel = pygame_gui.elements.UIPanel(relative_rect=pyg.Rect((0,(self.scale_height*-1)+5),(self.width,self.scale_height)),
                                                             manager=self.manager,
                                                             anchors={'bottom': 'bottom'},
                                                             object_id=pygame_gui.core.ObjectID(class_id='@scale_panel'),
                                                             container = self.area)
        
    def create_ticks(self,date_list,px_list):
        for i in range(len(date_list)):
            pos_x = px_list[i]
            if date_list[i] == 0:
                tick_height = 40
            else:
                tick_height = 20

            tick_mark = pygame_gui.elements.UIPanel(relative_rect=pyg.Rect((pos_x,(tick_height+10)*-1),(5,tick_height)),
                                            manager=self.manager,
                                            anchors={'bottom': 'bottom'},
                                            container=self.area,
                                            object_id=pygame_gui.core.ObjectID(class_id='@tick_panel'))
            label = dateIntToStr(date_list[i])
            if not i == len(date_list) - 1:
                tick_label = pygame_gui.elements.UILabel(relative_rect=pyg.Rect((pos_x+10,-32),(200,25)),
                                                        text=label,
                                                        manager=self.manager,
                                                        anchors={'bottom': 'bottom'},
                                                        container=self.area,
                                                        object_id=pygame_gui.core.ObjectID(class_id='@tick_label'))
