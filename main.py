"""
Arch 1 Game-project
Noah El Menyari en Rens Mulder (1G Basecamp)
"""
from operator import getitem
import time, sys, random, utils
from objects.location import Location
from objects.item import Item
import eventsmanager
import gamedata



# Hier worden de belangrijke variabelen voor de game aangemaakt
# Dit zijn de locaties
locations = []
# Dit is 'de' locatie waar de speler zich nu bevindt. Standaard is het een error locatie.
location = Location("NO0", "Er is iets fout gegaan tijdens het opzetten van de game.")
# Dit zijn alle items die een speler bezit.
inventory = []
# Dit zijn alle globale commando's
commands = []
# Dit is data die tijdens de game veranderd die het spel kunnen veranderen (daarom ook 'gamechangers').
gamechangers = {
    "used_zuurstoftank": False,
    "used_parachute": False,
    "passed_berenval": False,
    "used_bacardi": False,
    "opened_hek": False,
    "tried_tovenaar": False,
    "killed_walvis": False,
}



# Registraties van locaties en commando's en events en items en gewoon alles ================================================

# Hier worden componenten zoals locatie's geregistreerd
def register_locations():
    """Dit registreert de locaties van de game"""
    for name, desc in gamedata.locdesc_dict.items():
        register_location(name, desc)

def register_command(location, name, function, aliases=[]):
    """Dit registreert een commando voor een locatie"""
    location.addCommand(name=name, function=function, aliases=aliases)

def register_global_command(name, function, aliases=[]):
    """Dit registreert een globaal commando"""
    commands.append({"name": name, "function": function, "aliases": aliases})

def register_global_commands():
    """Dit registreert alle globale commando's"""
    register_global_command("help", lambda: print_help(), ["h", "help"])
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

def register_location(name: str, description: str):
    """Dit registreert een locatie"""
    locations.append(Location(name, description))  

def register_item(loc: location, itemname: str, usable=False):
    """Dit registreert een item met bijbehorende beschrijvingen"""
    loc.addItem(Item(name=itemname, description=gamedata.getItemDesc(itemname), held_description=gamedata.getHeldDesc(itemname), usable=usable))

def removeCommand(name: str):
    """Dit verwijdert een commando"""
    theCommand = None
    for command in commands:
        if command["name"] == name:
            theCommand = command
    if theCommand is not None:
        commands.remove(theCommand)
        
# Einde registraties ============================================================================================================


# Spelerfuncties beginnen hier =================================================================================================

def drink(itemname: str):
    """Hiermee drink je een item... eigenlijk maar 1 item (bacardiiiiiii - Rens)"""
    theitem = None
    for item in inventory:
        if item.getName() == itemname:
            theitem = item
            break
    if theitem.getName() == "bacardi":
        eventsmanager.end_game_bad("Je opent de fles en neemt een slok. En nog een slok... en nog een slok. \nDe alcohol verdunt je bloed waardoor je nog sneller uitbloedt... De pijn vaagt langzaam weg en je sterft een vredige dood." )

def gebruik(item: Item):
    """Dit gebruikt een item"""
    if item in inventory:
        if item.getName() == "zuurstoftank":
            utils.slow_type("Met je laatste kracht reik je naar het masker van de zuurstoftank. Je kan weer ademen. Je zicht is weer scherp en je voelt je langzaam beter.")
            gamechangers["used_zuurstoftank"] = True
            inventory.remove(item)
            removeCommand("gebruik " + item.getName())
            removeCommand("pak " + item.getName())
            removeCommand("onderzoek " + item.getName())
        elif item.getName() == "jonko":
            if location.getName() == "klifhuis":
                utils.slow_type("Je lit de jonko en neemt een paar hijsjes. Je voelt de stress je lichaam verlaten... met rode ogen en een zwaar hoofd druk je hem uit.")
                inventory.remove(item)
                removeCommand("gebruik " + item.getName())
                removeCommand("onderzoek " + item.getName())
            else:
                print("Jonko doen kan alleen in de chalet")
        elif item.getName() == "parachute":
            if location.getName() == "klif":
                eventsmanager.end_game_bad("Je springt met de parachute de klif af en ziet pas in de lucht een enorm gat in de parachute.\
 In plaats van te zweven donder je als een steen van de berg af en stierf je een pijnlijke dood.")
            elif location.getName() == "bostopzuid":
                gamechangers["used_parachute"] = True
                utils.slow_type("Dit kan je voor je wond gebruiken. Je wikkelt de parachute strak om je been heen. Het is misschien niet steriel maar het zal het bloeden stoppen voor nu.")
                inventory.remove(item)
                removeCommand("gebruik " + item.getName())
                removeCommand("onderzoek " + item.getName())
            else:
                print("Je kan dit item hier niet gebruiken.")
        elif item.getName() == "bacardi":
            if location.getName() == "bostopzuid":
                gamechangers["used_bacardi"] = True
                utils.slow_type("Je rolt je broek op en draait de dop van de fles open. Je neemt een flinke slok en gooit de rest over je wond. Je bijt bijna je kiezen kapot van de pijn... \nJe wond is schoon.")
                inventory.remove(item)
                removeCommand("gebruik " + item.getName())
                removeCommand("onderzoek " + item.getName())
                location.setDescription("Je bent in het bos. Je ziet de berenval nog liggen waar je in bent getrapt. Richting het zuiden zie je een pad dat dieper het bos in leidt. Richting het noorden zie je een pad wat naar een minderbegroeid deel van het bos lijkt te gaan.")
            else:
                print("Je kan dit item hier niet gebruiken.")
        elif item.getName() == "tak":
            if location.getName() == "bostop":
                utils.slow_type("Je grijpt naar de tak en valt bijna om van het gewicht. Met al je kracht zwaai je hem de lucht in en doorboor je het hart van de walvis.\
\nHet gehuil van de walvis sterft langzaam uit. ")
                gamechangers["killed_walvis"] = True
                location.setDescription("De walvis ligt er nog... Je voelt je er niet heel goed bij en kijkt weg. Richting het westen zie je een pad dat omhoog loopt. Richting het zuiden zie je een pad het bos in leidt. Richting het oosten zie je de bomen minderen en lijk je een huisje te zien.")
                inventory.remove(item)
                register_item(location, "sleutel", True)
                utils.slow_type(location.getItem("sleutel").getDescription())
                register_command(location, 'pak sleutel', "pak('sleutel')", ["p sleutel", "pick up sleutel", "pick up key"])
                removeCommand("gebruik " + item.getName())
                removeCommand("onderzoek " + item.getName())
            else:
                print("Je kan dit item hier niet gebruiken.")
        elif item.getName() == "sleutel":
            if location.getName() == "dehethek":
                gamechangers["opened_hek"] = True
                utils.slow_type("Je forceert de sleutel in het stroeve veroestte slot. *ching* Het slot opent.")
                location.setEast(get_location("appiebos"))
                location.setWest(get_location("klifsprong"))
                location.setDescription("Je ziet het open hek, achter het hek scheiden de wegen. Richting het oosten zie je het pad dichter het bos in lopen. Richting het westen lijk je een klif te zien. Richting het noorden zie je meer bos.")
                inventory.remove(item)
                removeCommand("gebruik " + item.getName())
                removeCommand("onderzoek " + item.getName())
            else:
                print("Je kan dit item hier niet gebruiken.")
        elif item.getName() == "mobiel":
            utils.slow_type("Je pakt het mobieltje. Geen bereik. Je opent de enige app die op de mobiel lijkt te staan, Subway Surfers.\n")
            print("'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'")
            print("'!!! You need an internet connection to play this game !!!!'")
            print("'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'")
            utils.slow_type("Teleurgesteld sluit je de app. Je wilt een foto maken maar het is een Android. Uit frustratie gooi je het mobieltje tegen een boom.")
            inventory.remove(item)
            removeCommand("gebruik " + item.getName())
            removeCommand("onderzoek " + item.getName())
        elif item.getName() == "tas":
            if location.getName() == "klifsprong":
                utils.slow_type("Je hebt vroeger bij de Albert Heijn gewerkt en weet dat deze tassen van het sterkste gerecycelde plastic worden gemaakt. Je pakt de handvaten stevig vast en springt met je armen in de lucht van de klif.\n")
                location.setWest(get_location("henk"))
                move("west")
                inventory.remove(item)
                removeCommand("gebruik " + item.getName())
                removeCommand("onderzoek " + item.getName())
            else:
                print("Je kan dit item hier niet gebruiken.")
        elif item.getName() == "steen":
            if location.getName() == "bostop" and not gamechangers["killed_walvis"]:
                print("Je gooit de steen tegen de walvis. Walvis: 'Auw! Waarom de #&$% doe je dat?!' Je voelt je schuldig en pakt maar snel weer de steen op.")
            elif location.getName() == "henk":
                utils.slow_type("Henk is best breed dus je gebruikt de steen als wapen. Je gooit de steen met chirurgische preciesie op zijn slaap. Henk valt neer.\
\nVoordat het leven Henks lichaam verlaat mompelt hij zijn laatste woorden...               \n'J..e...... moeder.......'\nYOU DEFEATED HENK.")
                inventory.remove(item)
                removeCommand("gebruik " + item.getName())
                removeCommand("onderzoek " + item.getName())
                location.setNorth(get_location("rekenmachinebos"))
                location.setSouth(get_location("tovenaar"))
                location.setDescription("Op de grond zie je Henk liggen. Hij lijkt best wel dood. Was geweld wel echt de oplossing? (Ja, ja dat was het) Richting het zuiden zie je een open grasvlakte waar je iemand lijkt te zien. Richting het noorden zie je meer bomen. Richting het oosten zie je de hoge klif waar je van af was gesprongen.")
            elif location.getName() == "bostopzuid" and not gamechangers["used_parachute"]:
                print("Je wrijft met de steen over je wond. Het doet pijn. Wat had je verwacht?")
            else:
                print("Je kan dit item hier niet gebruiken.")
        elif item.getName() == "rekenmachine":
            if location.getName() == "tovenaar":
                utils.slow_type("Je haalt je rekenmachine tevoorschijn. De tovenaar schrikt. Met beide handen pak je hem vast en tik je 2 + 2 in....\
\n'Neeee' schreeuwt de tovenaar nog uit maar het is te laat. Je hebt al op de = gedrukt. Op het scherm van de rekenmachine komt heel groot '4' te staan.\
\nJe kijkt omhoog en de tovenaar lijkt in het niets te zijn verdwenen... De bomen die eerst je zicht naar beneden blokkeerden zijn weg...\
\nOnderaan de berg zie je je moeders auto staan. Ineens heb je totaal geen herinnering van hoe je onderaan deze berg komt, maar het voelt alsof je erg lang bent weggeweest...")
                time.sleep(2)
                eventsmanager.end_game_win()
            else:
                print("Je tikt 58008 in op de rekenmachine.")
        elif item.getName() == "spons":
            if location.getName() == 'tovenaar':
                print("Tovenaar: Haha heel grappig. Een natte spons, wat een grap. Los nu maar eerst mijn raadsel op voordat je grappig komt doen.")
            else:
                print("Je wast met de natte spons je gezicht. Je voelt je fris en fruitig. Je hebt geen idee waarom je dit doet.") 
        else:
            print("Je kan dit item niet gebruiken.")
    else:
        print("Je kan dit item niet gebruiken.")

def trap_de_walvis():
    print("Je trapte de walvis, je bent een monster!")

def reken():
    """Dit beantwoordt de rekensom van de tovenaar"""
    if gamechangers["tried_tovenaar"] == False:
        gamechangers["tried_tovenaar"] = True
        print("Tovenaar: 'Kom op! Je kan toch wel mijn simpele rekensom oplossen? Ik geef je nog één kans. Gebruik desnoods een hulpmiddel ofzo!'")
    else:
        eventsmanager.end_game_bad("Tovenaar: 'Serieus? Ik had beter van je verwacht. Nu moet ik je ziel hier voor eeuwig vasthouden enzo en daar had ik eigenlijk helemaal geen zin in.'")

def klim():
    """Hiermee klim je op dehethek"""
    if gamechangers["opened_hek"] == False:
        utils.slow_type("Met beide armen pak je het hek stevig vast en zet je af met je been. Je voelt direct een scherpe pijn door je scheenbeen en valt neer. Dit gaat niet lukken zo.")
    else:
        print("Waarom typ je dit in? Het hek is al open...")

def die(reason: str):
    """Commandos die leiden tot spelerdood"""
    eventsmanager.end_game_bad(reason)

def check_inventory():
    """Dit checkt of de speler een item in zijn inventory heeft"""
    if(len(inventory) == 0):
        print("Je hebt niets in je inventory.")
    else:
        print("Je hebt de volgende items in je inventory:")
        for item in inventory:
            print(item.getName())

def pak(itemname: str):
    """Dit pakt een item op"""
    item = location.getItem(itemname)
    if item is not None:
        inventory.append(item)
        location.items.remove(item)
        register_global_command("onderzoek " + item.getName(), lambda: examine(item), ["o " + item.getName(), "onderzoek " + item.getName(), "onderzoek " + item.getName()])
        if item.getName() == "bacardi":
            register_command(get_location("bostopzuid"), 'drink ' + item.getName(), "drink('" + item.getName() + "')", ["d " + item.getName(), "at " + item.getName() ]) #beetje lelijk maja
        location.removeCommand("pak " + item.getName()) # Zorgt ervoor dat de speler niet twee keer hetzelfde item kan oppakken
        if item.isUsable():
            register_global_command("gebruik " + item.getName(), lambda: gebruik(item), ["g " + item.getName(), "gebruik " + item.getName(), "use " + item.getName()])

        print("Je hebt het item(" + item.getName() + ") opgepakt.")
    else:
        print("Je kan dit item niet oppakken.")

def move(direction: str):
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

def examine(asked_item):
    """Dit onderzoekt een item"""
    for item in inventory:
        if item.getName() == asked_item.getName():
            item.info()

# Spelerfuncties eindigen hier =================================================================================================

# Voorbereidingen van locaties beginnen hier ===================================================================================
def prepare_all_locations():
    """Dit voert alle voorbereidende opdrachten uit voor alle locaties"""

    prepare_start()
    prepare_bostop()
    prepare_klif()
    prepare_klifhuis()
    prepare_bostopzuid()
    prepare_dehethek()
    prepare_appiebos()
    prepare_klifsprong()
    prepare_henk()
    prepare_rekenmachinebos()
    prepare_tovenaar()

#prepare locations
def prepare_start():
    """Dit voert alle voorbereidende opdrachten uit voor de start locatie"""
    start = get_location("start")
    start.setEast(get_location("bostop"))
    start.setNorth(get_location("klif"))
    register_item(start, "parachute", True)
    register_item(start, "zuurstoftank", True)
    for item in start.items:
        itemname = item.getName()
        register_command(start, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName()])

def prepare_klif():
    """Dit voert alle voorbereidende opdrachten uit voor de klif locatie"""
    klif = get_location("klif")
    klif.setSouth(get_location("start"))
    register_item(klif, "steen", True)
    register_item(klif, "vis")
    register_command(klif, 'pak ' + "steen", "pak('" + "steen" + "')", ["p " + "steen", "pick up " + "steen"])

def prepare_bostop():
    """Dit voert alle voorbereidende opdrachten uit voor de bostop locatie"""
    bostop = get_location("bostop")
    bostop.setWest(get_location("start"))
    bostop.setEast(get_location("klifhuis"))
    bostop.setSouth(get_location("bostopzuid"))
    register_item(bostop, "tak", True)
    register_item(bostop, "spons", True)
    for item in bostop.items:
        itemname = item.getName()
        register_command(bostop, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName()])
    register_command(bostop, 'trap walvis', lambda: trap_de_walvis(), ["kick walvis"])

def prepare_klifhuis():
    """Dit voert alle voorbereidende opdrachten uit voor de klifhuis locatie"""
    klifhuis = get_location("klifhuis")
    klifhuis.setWest(get_location("bostop"))
    register_item(klifhuis, "jonko", True)
    for item in klifhuis.items:
        itemname = item.getName()
        register_command(klifhuis, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName()])

def prepare_bostopzuid():
    """Dit voert alle voorbereidende opdrachten uit voor de bostop zuid locatie"""
    bostopzuid = get_location("bostopzuid")
    bostopzuid.setNorth(get_location("bostop"))
    bostopzuid.setSouth(get_location("dehethek"))
    register_item(bostopzuid, "bacardi", True)
    for item in bostopzuid.items:
        itemname = item.getName()
        register_command(bostopzuid, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName()])

def prepare_dehethek():
    """Dit voert alle voorbereidende opdrachten uit voor de dehet hek locatie"""
    dehethek = get_location("dehethek")
    dehethek.setNorth(get_location("bostopzuid"))
    register_command(dehethek, "klim", lambda: klim(), ["climb"]) 

def prepare_appiebos():
    """Dit voert alle voorbereidende opdrachten uit voor de appiebos locatie"""
    appiebos = get_location("appiebos")
    appiebos.setWest(get_location("dehethek"))
    register_item(appiebos, "mobiel", True)
    register_item(appiebos, "tas", True)
    for item in appiebos.items:
        itemname = item.getName()
        if itemname == "tas":
            register_command(appiebos, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName(), "pak tasje", "p tasje", "pick up tasje"])
        else:
            register_command(appiebos, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName()])

def prepare_klifsprong():
    """Dit voert alle voorbereidende opdrachten uit voor de klifsprong locatie"""
    klifsprong = get_location("klifsprong")
    klifsprong.setEast(get_location("dehethek"))
    register_command(klifsprong, "spring", lambda: die("Je neemt een kleine aanloop en springt van de klif af. Je mikt op een boom maar mist volledig en valt op je nek. Je stierf een pijnloze dood (je was direct verlamd geraakt)."),\
         ["jump", "ren"])

def prepare_henk():
    """Dit voert alle voorbereidende opdrachten uit voor de henk locatie"""
    henk = get_location("henk")
    register_command(henk, 'stomp henk',  lambda: die("Je rent op Henk af en begint wild te slaan. Je was alleen vergeten dat Henk Basic gaat. Henk slaat je K.O. met één stomp.") , \
        ["gebruik vuisten", "use vuisten", "sla henk", "hit henk", "vecht"])

def prepare_rekenmachinebos():
    """Dit voert alle voorbereidende opdrachten uit voor de rekenmachinebos locatie"""
    rekenmachinebos = get_location("rekenmachinebos")
    register_item(rekenmachinebos, "rekenmachine", True)
    for item in rekenmachinebos.items:
        itemname = item.getName()
        if itemname == 'rekenmachine':
            register_command(rekenmachinebos, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName(), "pak gr", "p gr", "pick up gr"])
        register_command(rekenmachinebos, 'pak ' + itemname, "pak('" + itemname + "')", ["p " + item.getName(), "pick up " + item.getName()])
    rekenmachinebos.setSouth(get_location("henk"))
    

def prepare_tovenaar():
    """Dit voert alle voorbereidende opdrachten uit voor de tovenaar locatie"""
    tovenaar = get_location("tovenaar")
    tovenaar.setNorth(get_location("henk"))
    register_command(tovenaar, '8', "reken()", ["acht"])
    register_command(tovenaar, '3', "reken()", ["drie"])
    register_command(tovenaar, '21', "reken()", ["eenentwintig"])

# Voorbereidingen van locaties eindigen hier ==============================================================================

def print_help():
    """Geeft een lijst met commando's die de speler kan gebruiken"""
    print("Je kan de volgende dingen doen: ")
    for command in location.getCommands():
        print('-',command["name"])
    for command in commands:
        print('-',command["name"])
    print('\n')

def get_location(name: str):
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
    command = input("Wat wil je doen? ").strip().lower()
    return command

def gameloop():
    """Dit is de gameloop van de game"""
    global location
    global inventory
    location.printDescription()
    while True:
        valid = False
        while not valid:
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


def print_title():
    """Dit print de titel van de game"""
    print(r"""
___________.__                            .__           .___                                               .___      
\__    ___/|  |__   ____   __  _  __ ____ |__|______  __| _/   ____   ______ ____ _____  ___________     __| _/____  
  |    |   |  |  \_/ __ \  \ \/ \/ // __ \|  \_  __ \/ __ |  _/ __ \ /  ___// ___\\__  \ \____ \__  \   / __ |/ __ \ 
  |    |   |   Y  \  ___/   \     /\  ___/|  ||  | \/ /_/ |  \  ___/ \___ \\  \___ / __ \|  |_> > __ \_/ /_/ \  ___/ 
  |____|   |___|  /\___  >   \/\_/  \___  >__||__|  \____ |   \___  >____  >\___  >____  /   __(____  /\____ |\___  >
                \/     \/               \/               \/       \/     \/     \/     \/|__|       \/      \/    \/ 

    """)
    time.sleep(2)
    utils.slow_type("Gemaakt door Noah El Menyari en Rens Mulder voor Basecamp 2022 aan Hogeschool Rotterdam")
    time.sleep(2)
    utils.clear()


def main():
    """Dit is de main functie van de game"""
    print_title() #<-- uncomment deze regel om de titel te laten zien
    register_locations() # Registreert alle locaties
    prepare_all_locations() # Zet North, South, East en West, en items in de locaties
    register_global_commands() # Registreert alle globale commando's
    register_events() # Registreert alle events
    prepgame() # Voert alle voorbereidende opdrachten uit
    # print(locations[0].getName())
    gameloop() # Start de gameloop

if __name__ == "__main__":
    main()
