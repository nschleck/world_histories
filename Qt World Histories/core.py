worldHistoryEvents = []

tagDict = {
    "Type": ["Astrological", "Geological", "Scientific", "Life", "People", "Art", "Invention", "War", "Construction"],
    "Era": ["Pre Earth", "Early Earth", "Early Life", "Prehistory","Antiquity","Middle Ages", "Modern"],
    "Culture": ["Greek","Roman","Polynesian","Chinese"],
    "Region": ["North America", "South America", "Central America", "Western Europe", "Mediterranean",
                "Eastern Europe","Africa","Middle East","Asia", "Oceania","Arctic","Antarctic"]
}
# lookup table for tag emojis
emojiDict = {
    "Astrological": "🔭",
    "Geological": "🌋",
    "Scientific": "🔬",
    "Life": "🧬",
    "People": "👥",
    "Art": "🎨",
    "Invention": "💡",
    "War": "⚔️",
    "Construction": "🏛️"
}

class WorldEvent:
    def __init__(self, name, date, tags, desc=None) -> None:
        self.name = name
        self.date = date
        self.tags = tags
        self.desc = desc
        
        self.typeTag = tagFilter(tags,"Type")
        self.eraTag = tagFilter(tags,"Era")
        self.cultureTag = tagFilter(tags,"Culture")
        self.regionTag = tagFilter(tags,"Region")

        worldHistoryEvents.append(self)

    def __str__(self) -> str:
        if self.desc:
            return(f"{self.name}: {dateIntToStr(self.date)}\n"
                    f"\t{self.desc} \n"
                    f"\tType: {self.typeTag}\n"
                    f"\tEra: {self.eraTag}\n"
                    f"\tCulture: {self.cultureTag}\n"
                    f"\tRegion: {self.regionTag}\n"
            )
        else:
            return(f"{self.name}: {dateIntToStr(self.date)}\n"
                    f"\tType: {self.typeTag}\n"
                    f"\tEra: {self.eraTag}\n"
                    f"\tCulture: {self.cultureTag}\n"
                    f"\tRegion: {self.regionTag}\n"
            )

class WorldSpan(WorldEvent):
    def __init__(self, name, date, tags, desc=None) -> None:
        super().__init__(name, date, tags, desc)
        self.spanStart = int(self.date.split(",")[0])
        self.spanEnd = int(self.date.split(",")[1])

    def __str__(self) -> str:
        if self.desc:
            return(f"{self.name}: {dateIntToStr(self.spanStart)} to {dateIntToStr(self.spanEnd)}\n"
                    f"\t{self.desc}\n"
                    f"\tType: {self.typeTag}\n"
                    f"\tEra: {self.eraTag}\n"
                    f"\tCulture: {self.cultureTag}\n"
                    f"\tRegion: {self.regionTag}\n"
            )
        else:
            return(f"{self.name}: {dateIntToStr(self.spanStart)} to {dateIntToStr(self.spanEnd)}\n"
                    f"\tType: {self.typeTag}\n"
                    f"\tEra: {self.eraTag}\n"
                    f"\tCulture: {self.cultureTag}\n"
                    f"\tRegion: {self.regionTag}\n"
            )
        
#### Data Input Utilities ####
def tagChecker(list):
    #checks that all world event tags are contained somewhere in the tag dictionary
    for event in list:
        tags = event.tags
        for tag in tags:
            if any([tagFilter([tag],"type"),tagFilter([tag],"era"),tagFilter([tag],"culture"),tagFilter([tag],"region")]):
                continue
            else:
                print(f"{event.name}: unused tag - {tag}")

#### Utilities ####
def dateIntToStr(date):
    #converts int date to readable date format
    # e.g. -20000 -> 20,000 BCE
    if date >= 0:
        return f"{date} CE"
    elif date > -10000:
        return f"{date*-1} BCE"
    elif date > -1000000:
        date = "{:,}".format(date*-1)
        return f"{date} BCE"
    elif date > -10000000:
        date = '{:.1f}'.format(date / -1000000)
        return f"{date} MYA"
    elif date > -1000000000:
        date = int(date / -1000000)
        return f"{date} MYA"
    else:
        date = '{:.1f}'.format(date / -1000000000)
        return f"{date} BYA"

def dateStrToInt(date):
    #converts readable date format to int date
    #e.g. 20,000 BCE -> -20000
    #TODO fix lazy code here, handle input
    number, suffix = date.split(" ")
    number = float(number)
    if suffix == "CE":
        return int(number)
    elif suffix == "BCE":
        return int(number * -1)
    elif suffix == "MYA":
        return int(number * -1000000)
    elif suffix == "BYA":
        return int(number * -1000000000)

def tagFilter(rawTagList,tagType):
    #returns tags of a specific tag type, from an event's general tag list
    typedTags = []
    for tag in rawTagList:
        if tag in tagDict[tagType]:
            typedTags.append(tag)
    return typedTags

def filterEventsByDate(events,scale_ticks_list):
    #remove events from events list that are outside of GUI scale scope (i.e. offscreen)
    filtered_events = []
    lower_bound = scale_ticks_list[0]
    upper_bound = scale_ticks_list[-1]

    for event in events:
        if isinstance(event,WorldEvent) and not isinstance(event,WorldSpan):
            if event.date > lower_bound and event.date < upper_bound:
                filtered_events.append(event)
        elif isinstance(event,WorldSpan):
            if event.spanEnd > lower_bound and event.spanStart < upper_bound:
                filtered_events.append(event)
    
    return filtered_events
