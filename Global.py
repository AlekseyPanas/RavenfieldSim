import Game
import City
import Unit
import os
import json
import Popup

running = True
events = []


def calculate_layer_locks(layers):
    visual_lock = False
    update_lock = False
    event_lock = False

    # Iterates through a reversed list (to start from the top)
    for layer in layers[::-1]:
        # If a previous layer had a prevent enabled, locks this layers' abilities accordingly
        if event_lock:
            layer.event_lock = True
        if update_lock:
            layer.update_lock = True
        if visual_lock:
            layer.visual_lock = True

        # Checks for prevents and saves them
        if layer.event_prevent:
            event_lock = True
        if layer.update_prevent:
            update_lock = True
            event_lock = True
        if layer.visual_prevent:
            visual_lock = True
            update_lock = True
            event_lock = True


layers = []

# Gets folder path
path = os.path.realpath("Global.py")
path = path.split('\\')
path.pop(-1)
path = "\\".join(path)

# Gets all json save files in the folder
directory = os.fsencode(path)

files = []

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".json"):
        files.append(filename)

# Since popup cant be pulled up right away, saves the data
conf_indices = -1

if len(files) > 0:
    [print() for x in range(10)]
    # Prints save files
    print("SAVE FILES:")
    for idx, file in enumerate(files):
        print(str(idx + 1), file)

    print()
    working = False
    while not working:
        try:
            # Gets chosen save file
            chosen_save = int(input("Please enter the number next to the save you want to load: "))
            # Checks if in range
            if 0 < chosen_save <= len(files):
                working = True
            else:
                # CRASH IT NOW
                x = int("ABC")
        except ValueError:
            print("ENTER A VALID NUMBER")

    with open(files[chosen_save - 1]) as file:
        loaded_json = json.load(file)

        UNITS = []
        for unit in loaded_json["units"]:
            UNITS.append(Unit.Unit(unit["pos"], unit["q"], unit["owner"]))
            UNITS[-1].quantity_not_moved = unit["q_nmov"]
            UNITS[-1].quantity_moved = unit["q_mov"]

        CITIES = []
        for city in loaded_json["cities"]:
            CITIES.append(City.City(city["name"], tuple(city["pos"]), city["owner"]))
            CITIES[-1].b_quantity = city["quantities"]
            CITIES[-1].done = city["done"]
            CITIES[-1].soldier_rate = city["soldier_rate"]
            CITIES[-1].soldiers = city["soldiers"]
            CITIES[-1].hammers = city["hammers"]
            # Selects buttons if maxed
            for idx, q in enumerate(CITIES[-1].b_quantity):
                if q >= CITIES[-1].b_max[idx]:
                    CITIES[-1].b_buttons[idx].selected = True

        GRID = loaded_json["grid"]
        TERRAIN = loaded_json["terrain"]

        layers.append(Game.Game(CITIES, UNITS, GRID, TERRAIN))
        layers[0].gamestate = loaded_json["gamestate"]

        if loaded_json["sel_unit"] != -1:
            layers[0].selected_unit = layers[0].units[loaded_json["sel_unit"]]

        if loaded_json["sel_city"] != -1:
            layers[0].selected_city = layers[0].cities[loaded_json["sel_city"]]

        conf_indices = loaded_json["conflicting_indices"]

else:
        TERRAIN = [["w" for x in range(25)],
                   ["w", "w", "w", "w", "w", "p", "p", "w", "w", "w", "w", "w", "t", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", ],
                   ["w", "w", "w", "w", "p", "m", "m", "d", "w", "w", "w", "t", "t", "t", "t", "w", "t", "t", "t", "w", "w", "w", "w", "w", "w", ],
                   ["w", "w", "w", "w", "d", "h", "m", "d", "w", "w", "t", "t", "t", "t", "t", "t", "t", "t", "t", "t", "w", "w", "w", "w", "w", ],
                   ["w", "w", "w", "w", "d", "p", "d", "d", "w", "w", "w", "t", "m", "t", "m", "t", "t", "t", "t", "t", "t", "w", "w", "w", "w", ],
                   ["w", "w", "w", "w", "w", "p", "p", "p", "w", "w", "w", "t", "m", "m", "t", "t", "m", "t", "t", "t", "w", "w", "w", "w", "w", ],
                   ["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "t", "t", "t", "t", "t", "t", "t", "m", "t", "p", "w", "w", "w", "w", "w", ],
                   ["w", "w", "w", "w", "w", "w", "w", "w", "w", "t", "t", "t", "t", "t", "t", "t", "t", "t", "t", "p", "w", "w", "w", "w", "w", ],
                   ["w", "w", "w", "w", "w", "w", "w", "w", "w", "t", "t", "t", "t", "p", "t", "p", "t", "t", "p", "t", "p", "w", "w", "w", "w", ],
                   ["w", "w", "w", "w", "w", "w", "w", "w", "p", "t", "p", "t", "p", "t", "h", "t", "h", "p", "t", "t", "h", "w", "w", "w", "w", ],
                   ["w", "w", "w", "w", "w", "w", "w", "w", "p", "p", "t", "p", "t", "h", "h", "p", "t", "p", "h", "p", "h", "w", "w", "w", "w", ],
                   ["w", "h", "w", "w", "w", "w", "w", "w", "t", "p", "m", "t", "t", "t", "p", "p", "p", "d", "d", "p", "p", "p", "w", "w", "w", ],
                   ["w", "p", "w", "h", "w", "w", "w", "w", "p", "p", "t", "m", "p", "p", "d", "d", "h", "d", "d", "d", "h", "p", "w", "w", "w", ],
                   ["w", "w", "w", "w", "w", "w", "w", "w", "p", "h", "h", "m", "m", "p", "d", "d", "d", "d", "d", "d", "d", "p", "w", "w", "w", ],
                   ["w", "w", "m", "w", "w", "w", "w", "p", "h", "p", "d", "m", "m", "d", "d", "d", "d", "d", "d", "d", "d", "d", "w", "w", "w", ],
                   ["w", "p", "m", "w", "w", "w", "h", "p", "p", "p", "h", "p", "m", "m", "d", "d", "d", "d", "d", "d", "d", "d", "w", "w", "w", ],
                   ["w", "w", "w", "w", "w", "w", "w", "w", "d", "p", "h", "p", "m", "d", "d", "d", "d", "d", "d", "d", "d", "p", "w", "w", "w", ],
                   ["w", "w", "w", "p", "w", "w", "w", "w", "d", "h", "p", "d", "d", "m", "m", "d", "d", "d", "d", "d", "h", "w", "w", "p", "p", ],
                   ["w", "w", "p", "p", "w", "w", "w", "w", "p", "d", "d", "m", "m", "m", "d", "d", "m", "d", "d", "d", "w", "w", "h", "m", "h", ],
                   ["w", "w", "w", "w", "w", "w", "w", "w", "p", "d", "d", "d", "p", "m", "m", "m", "m", "d", "m", "d", "w", "w", "w", "m", "p", ],
                   ["w", "d", "p", "w", "w", "w", "w", "w", "w", "d", "d", "d", "d", "d", "d", "m", "d", "d", "d", "d", "w", "w", "w", "p", "w", ],
                   ["w", "m", "w", "w", "w", "w", "w", "w", "w", "w", "d", "d", "d", "d", "m", "m", "m", "d", "p", "d", "w", "w", "w", "w", "w", ],
                   ["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "d", "d", "d", "d", "d", "d", "d", "d", "p", "w", "w", "d", "d", "w", ],
                   ["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "h", "d", "d", "d", "d", "d", "d", "d", "w", "w", "w", "h", "d", "h", ],
                   ["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "p", "d", "d", "d", "d", "w", "w", "w", "w", "w", "w", "p", "w", ]]

        layers.append(Game.Game([City.City("Canyon", (10, 14), "b"),
                                 City.City("Desert Hills", (11, 19), "b"),
                                 City.City("Tunnel", (16, 20), "b"),
                                 City.City("Dust Bowl", (18, 14), "b"),
                                 City.City("Twin Islands", (23, 20), "b"),
                                 City.City("Archipelago", (3, 18), "b"),
                                 City.City("Temple", (13, 9), "r"),
                                 City.City("Mountain Range", (13, 4), "r"),
                                 City.City("Glacier", (17, 5), "r"),
                                 City.City("Coastline", (20, 8), "r"),
                                 City.City("Island", (6, 4), "r")],
                                [Unit.Unit([18, 14], 1, "b"),
                                 Unit.Unit([16, 20], 1, "b"),
                                 Unit.Unit([13, 9], 1, "r"),
                                 Unit.Unit([13, 4], 1, "r")], 25, TERRAIN))

def load_pop():
    if conf_indices != -1:
        # Locks the layer
        layers[0].update_lock = True
        # Creates a popup
        layers.append(Popup.Popup(False, False, False,[layers[0].units[conf_indices[0]],
                                                           layers[0].units[conf_indices[1]]]))
