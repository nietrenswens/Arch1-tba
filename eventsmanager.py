"""Verzorgt het aanmaken en handelen van events"""
import main
events = []
inventory = []

def register_event(location, function, condition):
    """Registreert een event"""
    global events
    events.append({"location": location, "function": function, "condition": condition})

def check_events(location, inv):
    """Controleert of er een event moet worden afgevuurd"""
    global events
    global inventory
    inventory = inv
    for event in events:
        if event["location"] == location:
            if eval(event["condition"]):
                event["function"]()
        if event["location"] == "all":
            if eval(event["condition"]):
                event["function"]()

def end_game_bad(reason:str):
    """Eindigt het spel"""
    print("Je bent dood. " + reason)
    exit()

def has(itemname:str):
    """Kijkt of de speler een item heeft"""
    global inventory
    for item in inventory:
        if item.getName() == itemname:
            return True
    return False

if __name__ == "__main__":
    main.main()