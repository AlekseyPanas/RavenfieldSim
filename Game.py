import Global as Globe
import constants
import pygame
import Layer
import Unit
import UnitSidebar


class Game(Layer.Layer):
    def __init__(self, cities, units, grid, terrain, territory=None):
        # Game Layer prevents every layer below it
        super().__init__(True, True, True)

        # The cities are the primary development points for units They define territory
        self.cities = cities

        # Units are groups of soldiers in one squad and can move around the map or guard cities. Units can be split into
        # 2 seperate squads
        self.units = units

        # The size of the grid (And integer value, grid is always a square)
        self.grid_size = grid

        # Tiles is an array which gives tile info: [terrain, owner]
        # terrains: "w" = ocean, "d" = desert, "p" = plains, "m" = mountains, "h" = hills
        # owners: "r" = Ravens, "b" = Eagles, "n" = no one
        self.terrain = terrain

        # If territory not specifies, sets every tile to "owned by no one"
        self.territory = territory if territory is not None else [["n" for x in range(self.grid_size)] for y in range(self.grid_size)]

        # The primary surface on which everything is drawn
        self.grid_surface = pygame.Surface((702, 702), pygame.SRCALPHA, 32)

        # The length of an edge of a tile based on given info
        self.edge_length = constants.GRID_SURF_SIZE[0] / self.grid_size

        # Sends terrain info to cities to let them calculate hammer rate
        for city in self.cities:
            city.calculate_hammer_rate(self.terrain)

        # The gamestate is what controls the entire game
        # 0 = start of turn
        self.gamestate = 0

        # Used to store unit instance of the selected unit
        self.selected_unit = None

        # sidebar for unit splitting and details
        self.unit_sidebar = UnitSidebar.UnitSidebar()

    def clear_grid_surface(self):
        self.grid_surface.fill((255, 255, 255, 0))
        self.grid_surface = self.grid_surface.convert()

    def run_layer(self, screen):
        if not self.visual_lock:
            self.draw(screen)

        if not self.update_lock:
            self.update()

        self.unit_sidebar.run_sidebar(screen, 1,
                                      self.selected_unit.quantity_not_moved if self.selected_unit is not None else 0,
                                      self.visual_lock,
                                      self.event_lock, self.update_lock)

    def update(self):
        if self.gamestate == 0:
            self.start_turn()
            self.gamestate += 1

        # Unit movements
        elif self.gamestate == 1:
            # Deselects all units
            for unit in self.units:
                unit.selected = False
            # Selects first unit in list that hasn't moved
            self.selected_unit = list(filter(lambda x: not x.quantity_not_moved == 0, self.units))[0]
            self.selected_unit.selected = True
            # Calls event which will control unit movement. Unit movement manages unit battle prompt
            if not self.event_lock:
                self.move_units_event()
            # Runs only if the above did not end the update
            if not self.update_lock:
                # Combines units in same tile
                self.units = Unit.Unit.stack(self.units)
                # Checks city capture
                self.check_city_capture()

                self.check_end_unit_movement()

    def check_city_capture(self):
        for unit in self.units:
            for city in self.cities:
                if tuple(unit.pos) == city.pos:
                    if unit.owner != city.owner:
                        city.owner = unit.owner

    def check_end_unit_movement(self):
        # Checks if all units moved to change gamestate
        if not len(list(filter(lambda x: not x.quantity_not_moved == 0, self.units))):
            self.selected_unit = None
            self.gamestate -= 1

    def move_units_event(self):
        for event in Globe.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.selected_unit.move(self.unit_sidebar.unit_slider.value, [-1, 0], self.units)
                elif event.key == pygame.K_RIGHT:
                    self.selected_unit.move(self.unit_sidebar.unit_slider.value, [1, 0], self.units)
                elif event.key == pygame.K_DOWN:
                    self.selected_unit.move(self.unit_sidebar.unit_slider.value, [0, 1], self.units)
                elif event.key == pygame.K_UP:
                    self.selected_unit.move(self.unit_sidebar.unit_slider.value, [0, -1], self.units)
                elif event.key == pygame.K_SPACE:
                    self.selected_unit.move(self.selected_unit.quantity, [0, 0], self.units)

    def start_turn(self):
        # Resets all units
        for unit in self.units:
            unit.quantity_not_moved = unit.quantity
            unit.quantity_moved = 0

        # Runs cities
        for city in self.cities:
            city.run_turn()
            # Checks if a unit was built and spawns it
            if city.soldiers >= 10:
                self.units.append(Unit.Unit(list(city.pos), int(city.soldiers / 10), city.owner))
                city.soldiers %= 10

    def draw(self, screen):
        self.clear_grid_surface()

        # Draws terrain
        self.draw_terrain()

        # Draws grid
        self.draw_grid()

        # Draws units
        self.draw_units()

        # Draws cities
        self.draw_cities()

        # Blits grid surface to screen
        screen.blit(self.grid_surface, (0, 0))

    def draw_units(self):
        for unit in self.units:
            # Draws glow circle if the unit is selected
            if unit.selected:
                self.grid_surface.blit(constants.RED_HIGHLIGHT if unit.owner == "r" else constants.BLUE_HIGHLIGHT,
                                       ((unit.pos[0] * self.edge_length) + (self.edge_length / 2) - (constants.GLOW_SIZE / 2),
                                        (unit.pos[1] * self.edge_length) + (self.edge_length / 2) - (constants.GLOW_SIZE / 2)))

            # Draws square outline for unit
            pygame.draw.polygon(self.grid_surface, constants.RED_COLOR if unit.owner == "r" else constants.BLUE_COLOR,
                                (((unit.pos[0] + 0.1) * self.edge_length, (unit.pos[1] + 0.1) * self.edge_length),
                                 ((unit.pos[0] + 0.9) * self.edge_length, (unit.pos[1] + 0.1) * self.edge_length),
                                 ((unit.pos[0] + 0.9) * self.edge_length, (unit.pos[1] + 0.9) * self.edge_length),
                                 ((unit.pos[0] + 0.1) * self.edge_length, (unit.pos[1] + 0.9) * self.edge_length)), 4)

            # Draws number on unit
            rendered_name = constants.UNIT_NUM_FONT.render(str(unit.quantity), False, (0, 0, 0))
            self.grid_surface.blit(rendered_name,
                                   ((unit.pos[0] * self.edge_length) + (self.edge_length / 2) - (rendered_name.get_width() / 2),
                                     unit.pos[1] * self.edge_length + 1.6))

            # Draws small debug values above units
            rendered_name = constants.TINY_FONT.render(str(unit.quantity_moved) + ", " + str(unit.quantity_not_moved), False, (0, 255, 0))
            self.grid_surface.blit(rendered_name,
                                   ((unit.pos[0] * self.edge_length), (unit.pos[1] * self.edge_length) - 10))

    def draw_grid(self):
        for col in range(self.grid_size):
            # As the grid is drawn during the loop, it shifts to the right according to grid size
            pygame.draw.line(self.grid_surface, (70, 70, 70), (self.edge_length * col, 0),
                             (self.edge_length * col, constants.GRID_SURF_SIZE[0]), 1)

            # As the grid is drawn during the loop, it shifts down according to grid size
            pygame.draw.line(self.grid_surface, (70, 70, 70), (0, self.edge_length * col),
                             (constants.GRID_SURF_SIZE[1], self.edge_length * col), 1)

    def draw_cities(self):
        for city in self.cities:
            # Draws dot only if there's no units in city
            if not len(list(filter(lambda x: city.pos == tuple(x.pos), self.units))):
                pygame.draw.circle(self.grid_surface, constants.BLUE_COLOR if city.owner == "b" else constants.RED_COLOR,
                                   ((int((city.pos[0] + .5) * self.edge_length)),
                                    (int((city.pos[1] + .5) * self.edge_length))), 6)

            # Draws name
            rendered_name = constants.CITY_NAME_FONT.render(city.name, False, (10, 10, 155) if city.owner == "b" else (155, 10, 10))
            self.grid_surface.blit(rendered_name,
                                   (((city.pos[0] + .5) * self.edge_length) - (rendered_name.get_width() / 2),
                                    ((city.pos[1] + .5) * self.edge_length) - 25))

    def draw_terrain(self):
        # Draws a colored square according to the terrain
        for idx1, row in enumerate(self.terrain):
            for idx2, col in enumerate(row):
                pygame.draw.polygon(self.grid_surface, constants.TERRAIN_DICT[col],
                                    ((self.edge_length * idx2, self.edge_length * idx1),
                                     (self.edge_length * (idx2 + 1), self.edge_length * idx1),
                                     (self.edge_length * (idx2 + 1), self.edge_length * (idx1 + 1)),
                                     (self.edge_length * idx2, self.edge_length * (idx1 + 1))))
