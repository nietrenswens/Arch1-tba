import main
events = []

def register_event(location, function, condition):
    events.append({"location": location, "function": function, "condition": condition})

def check_events(location):
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