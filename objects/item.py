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
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def info(self):
        print(self.description)

    def getName(self):
        return self.name
        
    def getDescription(self):
        return self.description