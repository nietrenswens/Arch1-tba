class Item:
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
    info(additional=""):
        Prints the person's name and age.
    """
    def __init__(self, name, equippable):
        self.name = name
        self.equippable = equippable
