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
    "used_zuurstoftank": False,
    "used_parachute": False,
    "passed_berenval": False,
    "used_bacardi": False
}


# Hier worden componenten zoals locatie's geregistreerd
def register_locations():
    """Dit registreert de locaties van de game"""
    register_location("start", "")
    register_location("klif", "Het pad lijkt hier abrupt te stoppen, een klif. Je kijkt naar beneden. Het is te hoog om de grond te zien.")
    register_location("bostop", "Je loopt een bos in. Het is donker maar iets verderop hoor je een vreemd gehuil....\nJe loopt verder... Het gehuil wordt steeds luider.\nAchter een gigantische steen ligt een gestrande walvis. \
Walvis: '..... h .. eeel p..... \n...\n..  please ...... make it stop....'\nNaast de walvis ligt een grote scherpe tak...")
    register_location("klifhuis", "Iets verderop zie je een kleine chalet staan. 'Dit zou het echt goed doen op AirBnB', denk je bij jezelf. Je opent de deur...\n\
Er staan geen meubels in de chalet.")
    register_location("bostopzuid", "Je loopt verder naar beneden door het bos. Je wordt omringd door de groene natuur en voelt de rust zich over je lichaam wassen...\
\nIneens voel je iets scherps om je been klemmen... 'AUAAAA' schreeuw je uit. Wanneer je naar beneden kijkt zie je dat je volop in een berenval bent gestapt.\
\n...Gelukkig heb je dit ooit in een Bear Grills show gezien... Je drukt met beide handen de veren aan de zijkant van de berenval omlaag.\
\nDe berenval opent en je haalt voorzichtig je been er uit... Je bloedt echter flink. Je voelt je lichtjes in je hoofd.")
    register_location("dehethek", "")
    register_location("appiebos", "")
    register_location("klifsprong", "")
    register_location("henk", "")
    register_location("rekenmachinebos", "")
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
    eventsmanager.register_event(location='all', condition='location.getName() != "bostopzuid" and gamechangers["passed_berenval"] == True and gamechangers["used_parachute"] == False', function=lambda: eventsmanager.end_game_bad("Je verloor te veel bloed en stierf een pijnlijke dood."))
    eventsmanager.register_event(location='all', condition='location.getName() != "bostopzuid" and gamechangers["passed_berenval"] == True and gamechangers["used_bacardi"] == False', function=lambda: eventsmanager.end_game_bad("Je wonden waren geïnfecteerd, je bent gestorven aan bloedvergiftiging"))

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
        elif item.getName() == "jonko":
            if location.getName() == "chalet":
                print("Je lit de jonko en voelt de stress je lichaam verlaten... met rode ogen en een zwaar hoofd druk je hem uit")
            else:
                print("Jonko doen kan alleen in de chalet")
        elif item.getName() == "parachute":
            if location.getName() == "klif":
                eventsmanager.end_game_bad("Je springt met de parachute de klif af en ziet pas in de lucht een enorm gat in de parachute.\
In plaats van te zweven donder je als een steen van de berg af en sterf je een pijnlijke dood.")
            elif location.getName() == "bostopzuid":
                gamechangers["used_parachute"] = True
                print("Dit kan je voor je wond gebruiken. Je wikkelt de parachute strak om je been heen om het bloeden te stoppen. Het is misschien niet steriel maar het zal maar moeten werken voor nu.")
            else:
                print("Je kan dit item niet gebruiken.")
        elif item.getName() == "bacardi":
            print("yp")
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
    prepare_klifhuis()
    prepare_bostopzuid()
    prepare_dehethek()
    prepare_appiebos()
    prepare_henk()
    prepare_rekenmachinebos()
    prepare_tovenaar()

#prepare locations
def prepare_start():
    """Dit voert alle voorbereidende opdrachten uit voor de start locatie"""
    start = get_location("start")
    start.setEast(get_location("bostop"))
    start.setNorth(get_location("klif"))
    start.addItem(Item(name="parachute", description="Een parachute. Hij ziet er hevig beschadigd uit. Zal hij nog werken?", usable=True))
    start.addItem(Item(name="zuurstoftank", description="Een zuurstoftank met ongeveer 50% capaciteit. De tank is duidelijk al over de datum, maar ziet er nog steeds goed uit, en is nog steeds bruikbaar.", usable=True))
    for item in start.items:
        itemname = item.getName()
        register_command(start, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName()])

def prepare_klif():
    """Dit voert alle voorbereidende opdrachten uit voor de klif locatie"""
    klif = get_location("klif")
    klif.setSouth(get_location("start"))
    klif.addItem(Item(name="steen", description="Een glimmende steen. Hij doet je denken aan je kindertijd.", usable=True))
    klif.addItem(Item(name="vis", description="Een grote vis. De vis laat je hongerig voelen, maar hij flopt al de klif af voordat je hem kan pakken."))
    register_command(klif, 'pak ' + "steen", "pak('" + "steen" + "')", ["p " + "steen", "pick up " + "steen"])

def prepare_bostop():
    """Dit voert alle voorbereidende opdrachten uit voor de bostop locatie"""
    bostop = get_location("bostop")
    bostop.setWest(get_location("start"))
    bostop.setEast(get_location("klifhuis"))
    bostop.setSouth(get_location("bostopzuid"))
    #register_command(bostop, 'trap de walvis') dit moet nog gefixt worden
    #register_command(bostop, 'dood de walvis')
    # bostop.addItem(Item(name="sleutel", description="Een sleutel. Hij ziet er oud uit, maar hij lijkt nog steeds te werken.", usable=True))
    # for item in bostop.items:
    #     itemname = item.getName()
    #     register_command(bostop, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName()])

def prepare_klifhuis():
    """Dit voert alle voorbereidende opdrachten uit voor de klifhuis locatie"""
    klifhuis = get_location("klifhuis")
    klifhuis.setWest(get_location("bostop"))
    klifhuis.addItem(Item(name="jonko", description="Naast het raampje zie je een dikke jonko liggen naast een verroestte Zippo aansteker."))
    for item in klifhuis.items:
        itemname = item.getName()
        register_command(klifhuis, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName()])

def prepare_bostopzuid():
    """Dit voert alle voorbereidende opdrachten uit voor de bostop zuid locatie"""
    bostopzuid = get_location("bostopzuid")
    bostopzuid.setNorth(get_location("bostop"))
    bostopzuid.setSouth(get_location("dehethek"))
    bostopzuid.addItem(Item(name="bacardi", description="Uit de grond steekt een fles met een rode dop. Het is een fles Bacardi Lemon."))
    for item in bostopzuid.items:
        itemname = item.getName()
        register_command(bostopzuid, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName()])

def prepare_dehethek():
    """Dit voert alle voorbereidende opdrachten uit voor de dehet hek locatie"""

def prepare_appiebos():
    """Dit voert alle voorbereidende opdrachten uit voor de appiebos locatie"""

def prepare_klifsprong():
    """Dit voert alle voorbereidende opdrachten uit voor de klifsprong locatie"""

def prepare_henk():
    """Dit voert alle voorbereidende opdrachten uit voor de henk locatie"""

def prepare_rekenmachinebos():
    """Dit voert alle voorbereidende opdrachten uit voor de rekenmachinebos locatie"""

def prepare_tovenaar():
    """Dit voert alle voorbereidende opdrachten uit voor de tovenaar locatie"""

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
            if location.getName() == "bostopzuid":
                gamechangers["passed_berenval"] = True
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
