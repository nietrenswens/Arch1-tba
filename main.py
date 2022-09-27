"""
Arch 1 Game-project
Noah en Rens Mulder
"""
from objects.location import Location

locations = []
location = Location("NO0", "Er is iets fout gegaan tijdens het opzetten van de game.")

def register_locations():
    """Dit registreert de locaties van de game"""
    register_location("start", "Hey ho")

def register_command(location, name, function, aliases=[]):
    """Dit registreert een commando voor een locatie"""
    location.addCommand(name=name, function=function, aliases=aliases)
    
def prepare_all_locations():
    """Dit voert alle voorbereidende opdrachten uit voor alle locaties"""
    start = get_location("start")
    register_command(start, "noord", lambda: move("noord"), ["n"])
    print(start.getCommands())

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
            asked_command = ask_for_command()
            for command in location.getCommands():
                if command["name"] == asked_command:
                    command["function"]()
                    break
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

    prepgame()
    # print(locations[0].getName())
    gameloop()

if __name__ == "__main__":
    main()
