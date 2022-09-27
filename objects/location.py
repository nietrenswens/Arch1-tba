class Location:
    """
    Een class die een item representeert

    ...

    Attributes
    ----------
    name : str
        naam van het item
    equippable : bool
        kan de speler het item vasthouden

    Methods
    -------
    printDescription(additional=""):
        Prints the person's name and age.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.north = ''
        self.east = ''
        self.south = ''
        self.west = ''
        self.commands = []
        if name == 'start':
            print("Je bent in de startkamer. Je ziet een deur naar het noorden en een deur naar het oosten.")

    def printDescription(self):
        print(self.description)

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

