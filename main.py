"""
Arch 1 Game-project
Noah El Menyari en Rens Mulder (1G Basecamp)
"""
import time, sys, random
from objects.location import Location
from objects.item import Item
import eventsmanager

# Hier worden de belangrijke variabelen voor de game aangemaakt
locations = []
location = Location("NO0", "Er is iets fout gegaan tijdens het opzetten van de game.")
inventory = []
commands = []
gamechangers = {
    "used_zuurstoftank": False
}


# Hier worden componenten zoals locatie's geregistreerd
def register_locations():
    """Dit registreert de locaties van de game"""
    register_location("start", "Je wordt wakker op een onbekende plek. Je bent omringd door wolken en krijgt het gevoel dat je niet kan ademen... Je zicht voelt wazig.. \nHet lijkt erop dat je je in een bos bevindt bovenaan een berg...")
    register_location("klif", "")
    register_location("bostop", "")
    register_location("klifhuis", "")
    register_location("zuidelijke bostop", "")
    register_location("dehet hek - dicht", "")
    register_location("dehet hek - open", "")
    register_location("het appie bos", "")
    register_location("klifsprong", "")
    register_location("henk", "")
    register_location("dode henk", "")
    register_location("het rekenmachinebos", "")
    register_location("tovenaar", "")

def register_command(location, name, function, aliases=[]):
    """Dit registreert een commando voor een locatie"""
    location.addCommand(name=name, function=function, aliases=aliases)

def register_global_command(name, function, aliases=[]):
    """Dit registreert een globaal commando"""
    commands.append({"name": name, "function": function, "aliases": aliases})

def register_global_commands():
    """Dit registreert alle globale commando's"""
    register_global_command("inventory", check_inventory, ["i", "inv", "inventaris"])
    register_global_command("noord", lambda: move("noord"), ["n", "north"])
    register_global_command("oost", lambda: move("oost"), ["o", "east"])
    register_global_command("zuid", lambda: move("south"), ["z", "south"])
    register_global_command("west", lambda: move("west"), ["w", "west"])
    register_global_command("kijk", lambda: location.printDescription(), ["k", "kijk", "look"])

def register_events():
    """Registreert alle events"""
    eventsmanager.register_event(location='all', condition='location.getName() != "start" and gamechangers["used_zuurstoftank"] == False', function=lambda: eventsmanager.end_game_bad("Je kreeg geen zuurstof meer en stierf een pijnlijke dood."))

def check_inventory():
    """Dit checkt of de speler een item in zijn inventory heeft"""
    if(len(inventory) == 0):
        print("Je hebt niets in je inventory.")
    else:
        print("Je hebt de volgende items in je inventory:")
        for item in inventory:
            print(item.getName())

def pak(itemname):
    """Dit pakt een item op"""
    item = location.getItem(itemname)
    if item is not None:
        inventory.append(item)
        location.items.remove(item)
        register_global_command("onderzoek " + item.getName(), lambda: examine(item), ["o " + item.getName(), "onderzoek " + item.getName(), "onderzoek " + item.getName()])
        location.removeCommand("pak " + item.getName()) # Zorgt ervoor dat de speler niet twee keer hetzelfde item kan oppakken
        
        if item.isUsable():
            register_global_command("gebruik " + item.getName(), lambda: gebruik(item), ["g " + item.getName(), "gebruik " + item.getName(), "use " + item.getName()])

        print("Je hebt het item(" + item.getName() + ") opgepakt.")
    else:
        print("Je kan dit item niet oppakken.")

def removeCommand(name):
    """Dit verwijdert een commando"""
    for command in commands:
        if command["name"] == name:
            theCommand = command
    if theCommand is not None:
        commands.remove(theCommand)

def gebruik(item):
    """Dit gebruikt een item"""
    if item in inventory:
        if item.getName() == "zuurstoftank":
            print("Met je laatste kracht reik je naar het masker van de zuurstoftank. Je kan weer ademen. Je zicht is weer scherp en je voelt je langzaam beter.")
            gamechangers["used_zuurstoftank"] = True
            inventory.remove(item)
            removeCommand("gebruik " + item.getName())
            removeCommand("pak " + item.getName())
            removeCommand("onderzoek " + item.getName())
        elif item.getName() == "sleutel": # Dit is een voorbeeld van een item dat niet gebruikt kan worden op sommige locaties
            if location.getName() == "test":
                print("Je hebt de sleutel gebruikt.")
                location.setSouth(get_location("test2"))
            else:
                print("Je kan dit item hier niet gebruiken.")
        else:
            print("Je kan dit item niet gebruiken.")
    else:
        print("Je kan dit item niet gebruiken.")

# Hier komt grotendeels de game logica
def prepare_all_locations():
    """Dit voert alle voorbereidende opdrachten uit voor alle locaties"""

    prepare_start()
    prepare_bostop()
    prepare_klif()


#prepare locations
def prepare_start():
    """Dit voert alle voorbereidende opdrachten uit voor de start locatie"""
    start = get_location("start")
    start.setEast(get_location("bostop"))
    start.setNorth(get_location("klif"))
    start.addItem(Item(name="parachute", description="Een parachute. Hij ziet hevig beschadigd uit. Zal hij nog werken?", usable=True))
    start.addItem(Item(name="zuurstoftank", description="Een zuurstoftank met ongeveer 50% capaciteit. De tank is duidelijk al over de datum, maar ziet er nog steeds goed uit, en is nog steeds bruikbaar.", usable=True))
    for item in start.items:
        itemname = item.getName()
        register_command(start, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName()])

def prepare_klif():
    """Dit voert alle voorbereidende opdrachten uit voor de klif locatie"""
    klif = get_location("klif")
    klif.setSouth(get_location("start"))

def prepare_bostop():
    """Dit voert alle voorbereidende opdrachten uit voor de bostop locatie"""
    bostop = get_location("bostop")
    bostop.setWest(get_location("start"))
    # bostop.addItem(Item(name="sleutel", description="Een sleutel. Hij ziet er oud uit, maar hij lijkt nog steeds te werken.", usable=True))
    # for item in bostop.items:
    #     itemname = item.getName()
    #     register_command(bostop, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName()])

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
        loc = location.getNorth()
        if loc == '':
            print("Je kan niet naar het noorden.")
        else:
            location = loc 
            print("Je gaat naar het noorden...")
            eventsmanager.check_events(location, inventory, gamechangers)
            location.printDescription()
    elif direction == "oost":
        loc = location.getEast()
        if loc == '':
            print("Je kan niet naar het oosten.")
        else: 
            location = loc 
            print("Je gaat naar het oosten...")
            eventsmanager.check_events(location, inventory, gamechangers)
            location.printDescription()
    elif direction == "south":
        loc = location.getSouth()
        if loc == '':
            print("Je kan niet naar het zuiden.")
        else: 
            location = loc 
            print("Je gaat naar het zuiden...")
            eventsmanager.check_events(location, inventory, gamechangers)
            location.printDescription()
    elif direction == "west":
        loc = location.getWest()
        if loc == '':
            print("Je kan niet naar het westen.")
        else: 
            location = loc 
            print("Je gaat naar het westen...")
            eventsmanager.check_events(location, inventory, gamechangers)
            location.printDescription()

typing_speed = 100 #wpm
def slow_type(t):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)

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
    global location
    global inventory
    location.printDescription()
    while True:
        valid = False
        while not valid:
            # Geeft een lijst met commando's die de speler kan gebruiken
            print("Je kan de volgende dingen doen: ")
            for command in location.getCommands():
                print('-',command["name"])
            for command in commands:
                print('-',command["name"])
            print('\n')
            asked_command = ask_for_command()
            for command in location.getCommands():
                if command["name"] == asked_command:
                    if type(command["function"]) == str:
                        eval(command["function"])
                    else:
                        command["function"]()
                    valid = True
                    break
                else:
                    for alias in command["aliases"]:
                        if alias == asked_command:
                            if type(command["function"]) == str:
                                eval(command["function"])
                            else:
                                command["function"]()
                            valid = True
                            break
            for command in commands:
                if command["name"] == asked_command:
                    command["function"]()
                    valid = True
                    break
                else:
                    for alias in command["aliases"]:
                        if alias == asked_command:
                            valid = True
                            command["function"]()
                            break
            if not valid:
                print("Dat is geen geldig commando.")
            print('\n')



def main():
    """Dit is de main functie van de game"""
    register_locations() # Registreert alle locaties
    prepare_all_locations() # Zet North, South, East en West, en items in de locaties
    register_global_commands() # Registreert alle globale commando's
    register_events() # Registreert alle events
    prepgame() # Voert alle voorbereidende opdrachten uit
    # print(locations[0].getName())
    gameloop() # Start de gameloop

if __name__ == "__main__":
    main()
