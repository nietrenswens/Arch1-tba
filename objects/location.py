import utils
import time

class Location:
    """
    Een class die een locatie representeert

    ...

    Attributes
    ----------
    name : str
        naam van de locatie
    description : str
        beschrijving van de locatie
    north : location
        locatie object van de locatie naar het noorden
    east : location
        locatie object van de locatie naar het oosten
    south : location
        locatie object van de locatie naar het zuiden
    west : location 
        locatie object van de locatie naar het westen

    Methods
    -------
    printDescription()
        print de beschrijving van de locatie
    setNorth(north)
        zet de locatie naar het noorden
    setEast(east)
        zet de locatie naar het oosten
    setSouth(south)
        zet de locatie naar het zuiden
    setWest(west)
        zet de locatie naar het westen
    getNorth()
        geeft de locatie naar het noorden
    getEast()
        geeft de locatie naar het oosten
    getSouth()
        geeft de locatie naar het zuiden
    getWest()
        geeft de locatie naar het westen
    getCommands()
        geeft de commands van de locatie
    setCommands(commands)
        zet de commands van de locatie
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.north = ''
        self.east = ''
        self.south = ''
        self.west = ''
        self.commands = []
        self.items = []
        if name == 'start':
            starttext = """Je ontwaakt uit een diepe slaap. Je hoort een scherpe piep in je oren en alles doet in principe pijn.
Waarom lig je daar? Je herinnert je het parachute springen uit het vliegtuig, de scherpe duw die je in je rug
kreeg en je parachute die niet open wilde gaan. Het is een wonder dat je nog leeft. Je voelt je wazig en je kan
maar moeilijk ademen. (tip: weet je niet hoe je verder moet? Typ dan 'help' in). Je kan items oppakken door 'pak item' te doen. Je gebruikt het item
dan nog niet! Daarvoor moet je 'gebruik item' doen."""
            utils.slow_type(starttext)
            print('\n')
            time.sleep(2)
            
    def printDescription(self):
        items = ""
        for item in self.items:
            items += item.getDescription()
            if item != self.items[-1]:
                items += " Ook zie je "
        if items != "":
            utils.slow_type(self.description + " Naast je liggen ook nog een aantal items: " + items)
        else:
            utils.slow_type(self.description)
        print('\n')

    def getItem(self, itemName):
        for item in self.items:
            if item.getName() == itemName:
                return item
        return None

    def setDescription(self, description):
        self.description = description

    def setNorth(self, north):
        self.north = north

    def setEast(self, east):
        self.east = east

    def setSouth(self, south):
        self.south = south
    
    def setWest(self, west):
        self.west = west

    def getNorth(self):
        return self.north

    def getEast(self):
        return self.east

    def getSouth(self):
        return self.south

    def getWest(self):
        return self.west

    def getCommands(self):
        return self.commands

    def setCommands(self, commands):
        self.commands = commands

    def getName(self):
        return self.name

    def addCommand(self, name, aliases, function):
        self.commands.append({"name": name, "aliases": aliases, "function": function})

    def addItem(self, item):
        self.items.append(item)
    
    def removeItem(self, item):
        self.items.remove(item)

    def removeCommand(self, commandName):
        for command in self.commands:
            if command["name"] == commandName:
                self.commands.remove(command)
