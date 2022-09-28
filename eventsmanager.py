import main
events = []
inventory = []

def register_event(location, function, condition):
    events.append({"location": location, "function": function, "condition": condition})

def check_events(location, inv):
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

def end_game_bad(reason):
    print("Je bent dood. " + reason)
    exit()

def has(itemname):
    global inventory
    for item in inventory:
        if item.getName() == itemname:
            return True
    return False

if __name__ == "__main__":
    main.main()