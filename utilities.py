# world events master list
worldEvents = []

tagDict = {
    "type": ["Astrological","Geological","Scientific","Life","People","Invention","War"],
    "era": ["Pre Earth", "Early Earth", "Early Life", "Prehistory","Antiquity","Middle Ages", "Modern"],
    "culture": ["Greek","Roman","temp"],
    "region": ["North America", "South America", "Central America", "Western Europe", "Mediterranean",
                "Eastern Europe","Africa","Middle East","Asia", "Oceania","Arctic","Antarctic"]
}

class WorldEvent:
    def __init__(self, name, date, tags, desc=None) -> None:
        self.name = name
        self.date = date
        self.tags = tags
        self.desc = desc
        
        self.typeTag = tagFilter(tags,"type")
        self.eraTag = tagFilter(tags,"era")
        self.cultureTag = tagFilter(tags,"culture")
        self.regionTag = tagFilter(tags,"region")

        worldEvents.append(self)

    def __str__(self) -> str:
        if self.desc:
            return(f"{self.name}: {dateFormatToDate(self.date)}\n"
                    f"\t{self.desc} \n"
                    f"\tType: {self.typeTag}\n"
                    f"\tEra: {self.eraTag}\n"
                    f"\tCulture: {self.cultureTag}\n"
                    f"\tRegion: {self.regionTag}\n"
            )
        else:
            return(f"{self.name}: {dateFormatToDate(self.date)}\n"
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
            return(f"{self.name}: {dateFormatToDate(self.spanStart)} to {dateFormatToDate(self.spanEnd)}\n"
                    f"\t{self.desc}\n"
                    f"\tType: {self.typeTag}\n"
                    f"\tEra: {self.eraTag}\n"
                    f"\tCulture: {self.cultureTag}\n"
                    f"\tRegion: {self.regionTag}\n"
            )
        else:
            return(f"{self.name}: {dateFormatToDate(self.spanStart)} to {dateFormatToDate(self.spanEnd)}\n"
                    f"\tType: {self.typeTag}\n"
                    f"\tEra: {self.eraTag}\n"
                    f"\tCulture: {self.cultureTag}\n"
                    f"\tRegion: {self.regionTag}\n"
            )
     
#### Utilities ####

def dateFormatToDate(date):

    #converts int date to readable date format
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

def dateFormatToInt(date):
    #converts readable date format to int date
    number, suffix = date.split(" ")
    if suffix == "CE":
        return int(number)
    elif suffix == "BCE":
        return int(number) * -1
    elif suffix == "MYA":
        return int(number) * -1000000
    elif suffix == "BYA":
        return int(number) * -1000000000

def tagFilter(rawTagList,tagType):
    #returns tags of a specific tag type, from an event's general tag list
    typedTags = []
    for tag in rawTagList:
        if tag in tagDict[tagType]:
            typedTags.append(tag)
    return typedTags

def tagChecker(list):
    #checks that all world event tags are contained somewhere in the tag dictionary
    for event in list:
        tags = event.tags
        for tag in tags:
            if any([tagFilter([tag],"type"),tagFilter([tag],"era"),tagFilter([tag],"culture"),tagFilter([tag],"region")]):
                continue
            else:
                print(f"{event.name}: unused tag - {tag}")

#### Events ####

#Astrological / Geological / Early Life
e1 = WorldEvent("The Big Bang",-13500000000,["Astrological", "Pre Earth"])
e2 = WorldEvent("Earth Formed", -4500000000,["Astrological","Early Earth"])
e3 = WorldSpan("Cambrian Explosion","-540000000,-515000000",["Geological","Life","Early Life"])
e4 = WorldSpan("Carboniferous Period", "-360000000,-300000000",["Geological","Life","Early Life"])
e5 = WorldSpan("Most Recent Ice Age (LGP)","-115000,-9700",["Geological","Prehistory"])
e6 = WorldEvent("The Holocene begins", -9700,["Geological", "Antiquity"], desc="This is the current geological epoch.")

#Early Humans

#Classical Antiquity

#Middle Ages
ey = WorldEvent("Western Roman Empire Falls", 476, ["People","War","Antiquity","Middle Ages","Roman","Mediterranean","Western Europe"],desc="This marks the beginning of the Middle Ages")

#Modern
