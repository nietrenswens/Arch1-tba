"""
Arch 1 Game-project
Noah en Rens Mulder
"""
from objects.location import Location

locations = []
location = locations[0]

def register_locations():
    """Dit registreert de locaties van de game"""
    register_location("top", "")

def register_location(name, description):
    """Dit registreert een locatie"""
    locations.append({
        "name": name, 
        "location": Location(name, description)
        })

def main():
    """Dit is de main functie van de game"""
    register_locations()

    gameloop()
    

if __name__ == "__main__":
    main()

def gameloop():
    """Dit is de gameloop van de game"""
    while True:
        location.printDescription()
        command = input("Wat wil je doen? ")