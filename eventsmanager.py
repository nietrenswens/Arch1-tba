"""Verzorgt het aanmaken en handelen van events"""
import main
import utils
events = []
inventory = []
gamechangers = {}

def register_event(location, function, condition):
    """Registreert een event"""
    global events
    events.append({"location": location, "function": function, "condition": condition})

def check_events(location, inv, gc):
    """Controleert of er een event moet worden afgevuurd"""
    global events
    global inventory
    global gamechangers
    gamechangers = gc
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
    utils.clear()
    utils.slow_type(reason + " Game over...")
    print(r"""
  ________                        ________                                                          
 /  _____/_____    _____   ____   \_____  \___  __ ___________                                      
/   \  ___\__  \  /     \_/ __ \   /   |   \  \/ // __ \_  __ \                                     
\    \_\  \/ __ \|  Y Y  \  ___/  /    |    \   /\  ___/|  | \/                                     
 \______  (____  /__|_|  /\___  > \_______  /\_/  \___  >__|                                        
        \/     \/      \/     \/          \/          \/                                            
__________           .___              __      __                               .__            __   
\______   \ ____   __| _/____    ____ |  | ___/  |_  ___  ______   ___________  |  |__   _____/  |_ 
 |    |  _// __ \ / __ |\__  \  /    \|  |/ /\   __\ \  \/ /  _ \ /  _ \_  __ \ |  |  \_/ __ \   __\
 |    |   \  ___// /_/ | / __ \|   |  \    <  |  |    \   (  <_> |  <_> )  | \/ |   Y  \  ___/|  |  
 |______  /\___  >____ |(____  /___|  /__|_ \ |__|     \_/ \____/ \____/|__|    |___|  /\___  >__|  
        \/     \/     \/     \/     \/     \/                                        \/     \/      
                      .__                                                                           
  ____________   ____ |  |   ____   ____                                                            
 /  ___/\____ \_/ __ \|  | _/ __ \ /    \                                                           
 \___ \ |  |_> >  ___/|  |_\  ___/|   |  \                                                          
/____  >|   __/ \___  >____/\___  >___|  /                                                          
     \/ |__|        \/          \/     \/                                                           

    """)
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