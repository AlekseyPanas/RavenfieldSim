import constants
import pygame
import Button
import Global as Globe


class City:
    def __init__(self, name, pos, owner):
        self.done = False

        self.pos = pos
        self.name = name
        self.owner = owner

        self.hammer_rate = 0
        self.hammers = 0

        self.buildings = 0

        self.soldier_rate = 1
        self.soldiers = 0

        # SIDEBAR
        self.sidebar_surface = pygame.Surface((200, 702), pygame.SRCALPHA, 32)

        # where the sidebar surface will be blit on the main screen
        self.x_blit_pos = 700
        self.y_blit_pos = 0

        # Buildings list
        # costs = Hammer cost, names = building name, effect = [(1 for add, 2 for mult), value], quantity = how manyUgot
        self.b_names = ["Training Center", "Gun Factory", "Advanced Training Facility", "Selection Bureau"]
        self.b_costs = [50, 100, 250, 500]
        self.b_effects = [[1, 1], [2, 1.5], [1, 5], [2, 2]]
        self.b_quantity = [0, 0, 0, 0]
        self.b_max = [9, 2, 2, 2]
        self.b_buttons = [Button.Button((150, 50), (80, 80, 80), (20, 200 + idx * 60),
                                        self.b_names[idx]) for idx in range(len(self.b_names))]

    def calculate_hammer_rate(self, terrain):
        rate = 0
        for col in range(3):
            for row in range(3):
                if len(terrain) - 1 >= (self.pos[1] - 1) + row:
                    if len(terrain[(self.pos[1] - 1) + row]) - 1 >= (self.pos[0] - 1) + col:
                        rate += constants.HAMMRT_dict[terrain[(self.pos[1] - 1) + row][(self.pos[0] - 1) + col]]

        self.hammer_rate = rate

    def run_turn(self):
        self.hammers += self.hammer_rate
        self.soldiers += self.soldier_rate

    def draw_sidebar(self, screen, visual_lock):
        if not visual_lock:
            # # Draws basic city info##
            # Draws Name
            rendered_text = constants.CITY_NAME_FONT_LARGE.render(self.name, False, (0, 0, 0))
            self.sidebar_surface.blit(rendered_text, (20, 10))

            # Draws Hammer and Rates
            rendered_text = constants.STATS_FONT.render("Hammers: " + str(self.hammers), False, (50, 50, 150))
            self.sidebar_surface.blit(rendered_text, (20, 50))

            rendered_text = constants.STATS_FONT.render("Hammer Rate: " + str(self.hammer_rate), False, (50, 50, 200))
            self.sidebar_surface.blit(rendered_text, (20, 75))

            # Draws Soldier and Rates
            rendered_text = constants.STATS_FONT.render("Soldiers: " + str(self.soldiers), False, (150, 50, 50))
            self.sidebar_surface.blit(rendered_text, (20, 100))

            rendered_text = constants.STATS_FONT.render("Soldier Rate: " + str(self.soldier_rate), False, (200, 50, 50))
            self.sidebar_surface.blit(rendered_text, (20, 125))

            # Draws buttons
            for butt in self.b_buttons:
                butt.draw(self.sidebar_surface)

            # Draws button Numbers (building quantities
            for idx in range(len(self.b_quantity)):
                rendered_text = constants.UNIT_NUM_FONT.render(str(self.b_quantity[idx]), False, (0, 255, 0))
                self.sidebar_surface.blit(rendered_text, (20, 225 + idx * 60))

            # Draws button Numbers (building costs
            for idx in range(len(self.b_costs)):
                rendered_text = constants.UNIT_NUM_FONT.render("Cost: " + str(self.b_costs[idx]), False, (0, 255, 0) if self.hammers >= self.b_costs[idx] else (255, 0, 0))
                self.sidebar_surface.blit(rendered_text, (70, 225 + idx * 60))

            # Blits final surface
            screen.blit(self.sidebar_surface, (self.x_blit_pos, self.y_blit_pos))

            # Clears surface
            self.sidebar_surface = pygame.Surface((200, 702), pygame.SRCALPHA, 32)

    def event_sidebar(self, event_lock):
        if not event_lock:
            for event in Globe.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    actual_pos = (event.pos[0] - self.x_blit_pos, event.pos[1] - self.y_blit_pos)
                    for butt in range(len(self.b_buttons)):
                        if self.b_buttons[butt].clicked(actual_pos) and not self.b_buttons[butt].selected:
                            # If a building button was clicked, checks the hammers
                            if self.hammers >= self.b_costs[butt]:
                                # Removes hammers
                                self.hammers -= self.b_costs[butt]
                                # Adds quantity
                                self.b_quantity[butt] += 1
                                # Applies building's effects
                                if self.b_effects[butt][0] == 1:
                                    self.soldier_rate += self.b_effects[butt][1]
                                elif self.b_effects[butt][0] == 2:
                                    self.soldier_rate = int(self.soldier_rate * self.b_effects[butt][1])
                                # Checks if button needs selecting
                                if self.b_quantity[butt] == self.b_max[butt]:
                                    self.b_buttons[butt].selected = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.done = True
