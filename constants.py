from PIL import Image, ImageFilter
import pygame
pygame.init()


# Creates a glow light to be drawn under the units when selected
def create_unit_glow(size, color):
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    surface = surface.convert_alpha()

    pygame.draw.circle(surface, RED_COLOR if color == "r" else BLUE_COLOR, (int(size/2), int(size/2)), int(size/4))

    # Blurs the circle surface
    surface = Image.frombytes('RGBA', surface.get_size(),
                                  pygame.image.tostring(surface, 'RGBA', False)).filter(
        ImageFilter.GaussianBlur(radius=7))
    surface = pygame.image.frombuffer(surface.tobytes(), surface.size,
                                                  surface.mode)

    # This is how you set the transparency of this surface if needed
    surface.fill((255, 255, 255, 150), None, pygame.BLEND_RGBA_MULT)

    return surface


SCREEN_SIZE = (900, 900)
GRID_SURF_SIZE = (700, 700)

# terrains: "w" = ocean, "d" = desert, "p" = plains, "m" = mountains, "h" = hills, "t" = tundra
# converts terrain to colors in rgb
TERRAIN_DICT = {"w": (70, 130, 180), "d": (238, 232, 170), "p": (50, 205, 50), "m": (128, 128, 128), "h": (34, 139, 34), "t": (255, 255, 255)}

# converts terrain to hammer values
HAMMRT_dict = {"w": 4, "d": 1, "p": 3, "m": 7, "h": 5, "t": 2}

CITY_NAME_FONT = pygame.font.SysFont("Arial Black", 15)
UNIT_NUM_FONT = pygame.font.SysFont("Impact", 20)
TINY_FONT = pygame.font.SysFont("Minion Web", 20)

# The glow highlight below a selected unit
GLOW_SIZE = 100

RED_HIGHLIGHT = None
BLUE_HIGHLIGHT = None

RED_COLOR = (255, 0, 0)
BLUE_COLOR = (0, 0, 255)


# Video must be set prior to converting, so this function is called right after screen is defined in main
def define_highlights():
    global RED_HIGHLIGHT, BLUE_HIGHLIGHT
    RED_HIGHLIGHT = create_unit_glow(GLOW_SIZE, "r")
    BLUE_HIGHLIGHT = create_unit_glow(GLOW_SIZE, "b")
