import pygame
import constants


class Button:
    def __init__(self, size, color, pos, text=None):
        self.pos = pos

        self.size = size
        self.color = color

        self.button_surface = None
        self.clear_surface()

        self.selected = False

        self.text = text

    def clear_surface(self):
        self.button_surface = pygame.Surface(self.size, pygame.SRCALPHA, 32)

    def draw(self, screen):
        # Blits rect
        pygame.draw.rect(self.button_surface, self.color, (0, 0, self.size[0], self.size[1]))
        # Selected circle
        if self.selected and (self.text is not None):
            pygame.draw.circle(self.button_surface, (255, 255, 255), (int(self.size[0] / 2), int(self.size[1] / 2)), 8)
        # Draws text
        if self.text is not None:
            rendered_text = constants.UNIT_NUM_FONT.render("DONE", False, (255, 255, 255))
            self.button_surface.blit(rendered_text, (5, 5))
        # Blits final
        screen.blit(self.button_surface, self.pos)

    def clicked(self, pos):
        return pygame.Rect(self.pos, self.size).collidepoint(pos)
