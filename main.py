import pygame
import constants
import json
import Global as Globe

screen = pygame.display.set_mode(constants.SCREEN_SIZE, pygame.DOUBLEBUF)
clock = pygame.time.Clock()

# Runs extra func to load files
Globe.load_pop()

# Calls function requiring .convert()
constants.define_highlights()

while Globe.running:
    # Clears screen by filling it gray
    screen.fill((110, 110, 110))

    # Gets events and writes them
    Globe.events = pygame.event.get()

    # Closes program if X is pressed
    for event in Globe.events:
        if event.type == pygame.QUIT:
            Globe.running = False

            file_name = input("Please enter a file name: ")

            sel_unit_index = -1
            if Globe.layers[0].selected_unit is not None:
                sel_unit_index = Globe.layers[0].units.index(Globe.layers[0].selected_unit)

            sel_city_index = -1
            if Globe.layers[0].selected_city is not None:
                sel_city_index = Globe.layers[0].cities.index(Globe.layers[0].selected_city)

            conf_indices = -1
            if len(Globe.layers) > 1:
                conf_indices = [Globe.layers[0].units.index(Globe.layers[1].red_conflicting),
                                Globe.layers[0].units.index(Globe.layers[1].blue_conflicting)]

            json_save = {"units": [],
                         "cities": [],
                         "grid": Globe.layers[0].grid_size,
                         "terrain": Globe.layers[0].terrain,
                         "gamestate": Globe.layers[0].gamestate,
                         "sel_city": sel_city_index,
                         "sel_unit": sel_unit_index,
                         "conflicting_indices": conf_indices}

            # Saves cities
            for city in Globe.layers[0].cities:
                json_save["cities"].append({"name": city.name,
                                            "pos": city.pos,
                                            "owner": city.owner,
                                            "quantities": city.b_quantity,
                                            "done": city.done,
                                            "hammers": city.hammers,
                                            "soldiers": city.soldiers,
                                            "soldier_rate": city.soldier_rate})
            # Saves units
            for unit in Globe.layers[0].units:
                json_save["units"].append({"pos": unit.pos,
                                           "owner": unit.owner,
                                           "q_mov": unit.quantity_moved,
                                           "q_nmov": unit.quantity_not_moved,
                                           "q": unit.quantity})

            # Saves game
            with open(file_name + ".json", "w") as outfile:
                json.dump(json_save, outfile)

    # Updates all the layers
    Globe.calculate_layer_locks(Globe.layers)
    # Runs all the layers
    for layer in Globe.layers:
        layer.run_layer(screen)

    # Updates display
    pygame.display.update()

    # Reads FPS and sets it to caption
    pygame.display.set_caption(str(clock.get_fps()))
    clock.tick(70)
