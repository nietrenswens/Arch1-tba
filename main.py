"""
Arch 1 Game-project
Noah en Rens Mulder
"""
from objects.location import Location
from objects.item import Item

# Hier worden de belangrijke variabelen voor de game aangemaakt
locations = []
location = Location("NO0", "Er is iets fout gegaan tijdens het opzetten van de game.")
inventory = []
commands = []


# Hier worden componenten zoals locatie's geregistreerd
def register_locations():
    """Dit registreert de locaties van de game"""
    register_location("start", "Hey ho")

def register_command(location, name, function, aliases=[]):
    """Dit registreert een commando voor een locatie"""
    location.addCommand(name=name, function=function, aliases=aliases)

def register_global_command(name, function, aliases=[]):
    """Dit registreert een globaal commando"""
    commands.append({"name": name, "function": function, "aliases": aliases})

def register_global_commands():
    register_global_command("inventory", check_inventory, ["i", "inv", "inventaris"])
    
def check_inventory():
    """Dit checkt of de speler een item in zijn inventory heeft"""
    if(len(inventory) == 0):
        print("Je hebt niets in je inventory.")
    else:
        print("Je hebt de volgende items in je inventory:")
        for item in inventory:
            print(item)

def pak(item):
    """Dit pakt een item op"""
    if item in location.items:
        inventory.append(item)
        location.items.remove(item)
        register_command(location, "onderzoek " + item.getName(), lambda: examine(item), ["o " + item.getName(), "onderzoek " + item.getName(), "onderzoek " + item.getName()])
        location.removeCommand("pak " + item.getName()) # Zorgt ervoor dat de speler niet twee keer hetzelfde item kan oppakken
        print("Je hebt het item opgepakt.")
    else:
        print("Je kan dit item niet oppakken.")

# Hier komt grotendeels de game logica
def prepare_all_locations():
    """Dit voert alle voorbereidende opdrachten uit voor alle locaties"""

    start = get_location("start")
    start.addItem(Item("zuurstoftank", "Een zuurstoftank met ongeveer 50% capaciteit."))
    register_command(start, "noord", lambda: move("noord"), ["n", "north"])
    for item in start.items:
        register_command(start, "pak " + item.getName(), lambda: pak(item), ["p " + item.getName(), "pak " + item.getName(), "pick up " + item.getName()])
    # register_command(start, "pak zuurstoftank", lambda: )

def examine(item):
    """Dit onderzoekt een item"""
    if item in inventory:
        print(item.info())
    else:
        print("Je kan dit item niet onderzoeken.")

def move(direction):
    """Dit verplaatst de speler naar een andere locatie"""
    global location
    if direction == "noord":
        location = get_location(location.getNorth())
        print("Je gaat naar het noorden...")
    elif direction == "oost":
        location = get_location(location.getEast())
        print("Je gaat naar het oosten...")
    elif direction == "zuid":
        location = get_location(location.getSouth())
        print("Je gaat naar het zuiden...")
    elif direction == "west":
        location = get_location(location.getWest())
        print("Je gaat naar het westen...")

def register_location(name, description):
    """Dit registreert een locatie"""
    locations.append(Location(name, description))

def get_location(name):
    """Dit zoekt een locatie op"""
    for location in locations:
        if location.getName() == name:
            return location

def prepgame():
    """Voert alle voorbereidende opdrachten uit"""
    global location
    location = get_location("start")


# This is where the magic happens

def ask_for_command():
    """Vraagt om een commando"""
    command = input("Wat wil je doen? ")
    return command

def gameloop():
    """Dit is de gameloop van de game"""
    while True:
        global location
        location.printDescription()
        valid = False
        while not valid:
            print("Je kan de volgende dingen doen: ")
            for command in location.getCommands():
                print(command["name"])
            for command in commands:
                print(command["name"])
            print('\n')
            asked_command = ask_for_command()
            for command in location.getCommands():
                if command["name"] == asked_command:
                    command["function"]()
                    valid = True
                else:
                    for alias in command["aliases"]:
                        if alias == asked_command:
                            valid = True
                            command["function"]()
            for command in commands:
                if command["name"] == asked_command:
                    command["function"]()
                    valid = True
                else:
                    for alias in command["aliases"]:
                        if alias == asked_command:
                            valid = True
                            command["function"]()
            if not valid:
                print("Dat is geen geldig commando.")



def main():
    """Dit is de main functie van de game"""
    register_locations()
    prepare_all_locations()
    register_global_commands()
    prepgame()
    # print(locations[0].getName())
    gameloop()

if __name__ == "__main__":
    main()
