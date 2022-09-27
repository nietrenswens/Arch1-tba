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

def gameloop():
    """Dit is de gameloop van de game"""
    while True:
        location.printDescription()
        command = input("Wat wil je doen? ")

def main():
    """Dit is de main functie van de game"""
    register_locations()


    prepgame()
    # print(locations[0].getName())
    gameloop()

if __name__ == "__main__":
    main()
