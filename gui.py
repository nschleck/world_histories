#IMPORTS
import pygame as pyg
import pygame_gui
from settings import *
from utilities import *

#UI TOPBAR Object
class UI_TopBar:
    def __init__(self, manager) -> None:
        self.height = 100
        self.panel = pygame_gui.elements.UIPanel(relative_rect=pyg.Rect((0,0),(SCREEN_WIDTH,self.height)),
                                         manager=manager)
        
        self.row = [5,40]
        self.col = [20,200,400,590,780,970]

        self.date_start_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pyg.Rect((self.col[0],self.row[1]),(150,30)),
                                                initial_text="0",
                                                manager=manager,
                                                container=self.panel)
        self.date_end_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pyg.Rect((self.col[1],self.row[1]),(150,30)),
                                              initial_text="2000 CE",
                                              manager=manager,
                                              container=self.panel)
        self.label_date_start = pygame_gui.elements.UILabel(relative_rect=pyg.Rect((self.col[0],self.row[0]),(150,50)),
                                               text='Start Date',
                                               manager=manager,
                                               container=self.panel)
        self.label_date_end = pygame_gui.elements.UILabel(relative_rect=pyg.Rect((self.col[1],self.row[0]),(150,50)),
                                               text='End Date',
                                               manager=manager,
                                               container=self.panel)

        self.type_selector = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((self.col[2],self.row[0]),(180,70)),
                                                item_list=['All'] + tagDict["type"],
                                                allow_multi_select=True,
                                                manager=manager,
                                                container=self.panel)
        self.era_selector = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((self.col[3],self.row[0]),(180,70)),
                                                item_list=['All'] + tagDict["era"],
                                                allow_multi_select=True,
                                                manager=manager,
                                                container=self.panel)
        self.culture_selector = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((self.col[4],self.row[0]),(180,70)),
                                                item_list=['All'] + tagDict["culture"],
                                                allow_multi_select=True,
                                                manager=manager,
                                                container=self.panel)
        self.region_selector = pygame_gui.elements.UISelectionList(relative_rect=pyg.Rect((self.col[5],self.row[0]),(180,70)),
                                                item_list=['All'] + tagDict["region"],
                                                allow_multi_select=True,
                                                manager=manager,
                                                container=self.panel)

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

'''class UI_ScrollArea:
    def __init__(self,height) -> None:
        self.height = height,'''