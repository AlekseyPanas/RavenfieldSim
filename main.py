import pygame
import constants
import Global as Globe

screen = pygame.display.set_mode(constants.SCREEN_SIZE, pygame.DOUBLEBUF)
clock = pygame.time.Clock()

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
