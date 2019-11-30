import Game
import City
import Unit

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
                        [Unit.Unit([15, 15], 5, "b"),
                         Unit.Unit([18, 12], 5, "b"),
                         Unit.Unit([18, 13], 5, "r"),
                         Unit.Unit([4, 9], 5, "r")], 25, TERRAIN))
