import Layer
import Global as Globe
import pygame
import constants
import Button
import UnitSidebar


class Popup(Layer.Layer):
    def __init__(self, visual_prevent, update_prevent, event_prevent, conflicting_units):
        super().__init__(visual_prevent, update_prevent, event_prevent)

        self.popup_surface = None
        self.clear_surface()

        self.blue_button = Button.Button((80, 50), constants.BLUE_COLOR, (35, 70))
        self.red_button = Button.Button((80, 50), constants.RED_COLOR, (150, 70))
        self.done_button = Button.Button((53, 35), (90, 90, 90), (210, 250), "DONE")

        self.slider = UnitSidebar.Slider(1, 1, (90, 250), 90, (150, 150, 150))

        self.screen_pos = (250, 200)

        self.shadow = constants.create_shadow((400, 300), (0, 0, 0))

        self.red_conflicting = [x for x in conflicting_units if x.owner == "r"][0]
        self.blue_conflicting = [x for x in conflicting_units if x.owner == "b"][0]

    def clear_surface(self):
        self.popup_surface = pygame.Surface((440, 340), pygame.SRCALPHA, 32)

    def run_layer(self, screen):
        if not self.visual_lock:
            self.draw(screen)

        self.slider.run_slider(self.popup_surface, self.visual_lock, self.event_lock, self.update_lock, self.screen_pos)

        if not self.event_lock:
            self.event_handler()

        if not self.update_lock:
            self.update()

        if not self.visual_lock:
            # Blits final
            screen.blit(self.popup_surface, self.screen_pos)
            # Clears surface
            self.clear_surface()

    def draw(self, screen):
        # Draws shadows
        self.popup_surface.blit(self.shadow, (0, 0))

        # Draws box
        pygame.draw.rect(self.popup_surface, (0, 0, 0), (20, 20, 400, 300))
        pygame.draw.rect(self.popup_surface, (255, 255, 255), (30, 30, 380, 280))

        # Draws text
        rendered_text = constants.UNIT_NUM_FONT.render("Who is the winner?", False, (0, 0, 0))
        self.popup_surface.blit(rendered_text, (40, 35))
        rendered_text = constants.UNIT_NUM_FONT.render("How many left?", False, (0, 0, 0))
        self.popup_surface.blit(rendered_text, (40, 180))

        # Draws buttons
        self.blue_button.draw(self.popup_surface)
        self.red_button.draw(self.popup_surface)
        self.done_button.draw(self.popup_surface)

    def update(self):
        if self.blue_button.selected:
            self.slider.maximum = self.blue_conflicting.quantity
        elif self.red_button.selected:
            self.slider.maximum = self.red_conflicting.quantity

    def event_handler(self):
        for event in Globe.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                actual_pos = (event.pos[0] - self.screen_pos[0], event.pos[1] - self.screen_pos[1])
                if self.blue_button.clicked(actual_pos):
                    self.blue_button.selected = True
                    self.red_button.selected = False
                elif self.red_button.clicked(actual_pos):
                    self.blue_button.selected = False
                    self.red_button.selected = True
                elif self.done_button.clicked(actual_pos):
                    if self.blue_button.selected or self.red_button.selected:
                        pass
