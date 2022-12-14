from argparse import HelpFormatter


class Item:
    """
    Een class die een item representeert

    ...

    Attributes
    ----------
    name : str
        naam van het item
    description : str
        beschrijving van het item

    Methods
    -------
    info(additional=""):
        print de beschrijving van het item
    getName()
        geeft de naam van het item
    """
    def __init__(self, name: str, description: str, held_description = "", usable: bool = False):
        self.name = name
        self.description = description
        self.usable = usable
        self.used = False
        self.held_description = held_description
        if held_description == "":
            self.held_description = description

    def info(self):
        print(self.held_description)
    
    def setHeldDescription(self, description):
        self.held_description = description

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description
    
    def isUsable(self):
        return self.usable