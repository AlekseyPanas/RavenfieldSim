import pygame
import Global
import copy
import constants


class Slider:
    def __init__(self, minimum, maximum, center, length, color):
        # Constants
        self.SLIDER_PIECE_WIDTH = 8

        # Maximum and minimum value of slider
        self.minimum = minimum
        self.maximum = maximum

        # Calculates the value based on the position of the slider and the maximums
        self.value = 0

        # Center position of entire slider
        self.center = center
        # Visual length of slider bar
        self.length = length

        # Position of slider on bar
        self.slider_pos = 0
        # When dragging begins, saves initial positions to control the slider relative to mouse movement
        self.saved_mouse_pos = 0
        self.saved_slider_pos = 0

        # Is the slider being moved
        self.dragging = False

        self.slider_surface = None
        self.clear_surface()

        # Slider color shade
        self.color = color

    # Shift determines what positions need to be shifted so that events positions are relative to the whole screen
    def run_slider(self, screen, visual_lock, event_lock, update_lock, shift):
        if not visual_lock:
            self.draw(screen)
            if self.minimum == -1:
                print("DRAWING")
        if not event_lock:
            self.events(shift)
        if not update_lock:
            self.update()

    def clear_surface(self):
        self.slider_surface = pygame.Surface((self.length, 50), pygame.SRCALPHA, 32)

    def draw(self, screen):
        # Clears surfaces
        self.clear_surface()

        # Draws decorative circles
        pygame.draw.circle(self.slider_surface, self.color, (3, 10), 5)
        pygame.draw.circle(self.slider_surface, self.color, (self.length - 3, 10), 5)

        # Draws slider
        pygame.draw.rect(self.slider_surface, self.color, ((0, 7), (self.length, 6)))
        pygame.draw.rect(self.slider_surface, tuple([self.color[x] - 50 for x in range(3)]), ((self.slider_pos, 0),
                                                                                       (self.SLIDER_PIECE_WIDTH, 20)))

        # Draws value
        rendered_text = constants.UNIT_NUM_FONT.render(str(self.value), False, (0, 0, 0))
        self.slider_surface.blit(rendered_text, (self.slider_surface.get_width() / 2 - rendered_text.get_width() / 2, 25))

        screen.blit(self.slider_surface, (self.center[0] - (self.length / 2), self.center[1] - 10))

    def events(self, shift):
        for event in Global.events:
            # Checks if mouse was pressed on slider to start dragging
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.center[0] - self.length / 2 < event.pos[0] - shift[0] < self.center[0] + self.length / 2:
                        if self.center[1] - 5 < event.pos[1] - shift[1] < self.center[1] + 5:
                            self.dragging = True
                            self.saved_mouse_pos = copy.copy(event.pos[0])
                            self.saved_slider_pos = copy.copy(self.slider_pos)
            # Checks if mouse was unclicked to stop dragging
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False

    def update(self):
        if self.dragging:
            # Calculates the offset of the slider based on saved positions
            self.slider_pos = self.saved_slider_pos + (pygame.mouse.get_pos()[0] - self.saved_mouse_pos)

        # Ensures slider doesn't go outside of screen
        if self.slider_pos >= self.length - self.SLIDER_PIECE_WIDTH:
            self.slider_pos = self.length - self.SLIDER_PIECE_WIDTH
        elif self.slider_pos <= 0:
            self.slider_pos = 0

        # Updates slider value
        self.value = self.minimum + ((self.slider_pos / (self.length - self.SLIDER_PIECE_WIDTH)) * (self.maximum - self.minimum))
        self.value = int(self.value)


class UnitSidebar:
    def __init__(self):
        self.sidebar_surface = pygame.Surface((200, 702), pygame.SRCALPHA, 32)

        self.unit_slider = Slider(0, 10, (100, 200), 170, (255, 255, 255))

        # where the surface will be blit on the main screen
        self.x_blit_pos = 700
        self.y_blit_pos = 0

    def run_sidebar(self, screen, minimum, maximum, visual_lock, event_lock, update_lock):
        self.unit_slider.minimum = minimum
        self.unit_slider.maximum = maximum
        self.unit_slider.run_slider(self.sidebar_surface, visual_lock, event_lock, update_lock, (self.x_blit_pos,
                                                                                                 self.y_blit_pos))

        if not visual_lock:
            self.draw(screen)

    def draw(self, screen):
        screen.blit(self.sidebar_surface, (self.x_blit_pos, self.y_blit_pos))

        # Clears surface
        self.sidebar_surface = pygame.Surface((200, 702), pygame.SRCALPHA, 32)
