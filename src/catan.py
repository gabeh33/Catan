# The classic Catan board game by Gabe Holmes, will make it multiplayer eventually
# Right now focusing on playing against one bot
import pygame
import os

pygame.init()

WIDTH, HEIGHT = 800, 690
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Catan')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (36, 0, 200)
GRAY = (130, 130, 130)

FPS = 60

TILE_WIDTH, TILE_HEIGHT = 99.2, 111.32

# The images for the tiles of the games
resource_tiles = []
resources = ['desert', 'brick', 'forest', 'ore', 'sheep', 'wheat']
for resource in resources:
    tile = pygame.image.load(os.path.join('Assets', 'Tiles', resource + '_tile.png'))
    resource_tiles.append(pygame.transform.scale(tile, (TILE_WIDTH, TILE_HEIGHT)))

DESERT = resource_tiles[0]
BRICK = resource_tiles[1]
WOOD = resource_tiles[2]
ORE = resource_tiles[3]
SHEEP = resource_tiles[4]
WHEAT = resource_tiles[5]


def draw_tiles():
    starting_x = 270
    starting_y = 33
    buffer = 3

    rectangle_starting_y = HEIGHT * 0.73
    # First row
    WIN.blit(WOOD, (starting_x, starting_y))
    WIN.blit(SHEEP, (starting_x + TILE_WIDTH - buffer, starting_y))
    WIN.blit(WHEAT, (starting_x + 2 * TILE_WIDTH - buffer, starting_y))

    # Second Row
    WIN.blit(BRICK, (starting_x - TILE_WIDTH / 2, starting_y + TILE_HEIGHT * 21 / 28))
    WIN.blit(ORE, (starting_x + TILE_WIDTH / 2 - 2, starting_y + TILE_HEIGHT * 21 / 28))
    WIN.blit(BRICK, (starting_x + TILE_WIDTH * 1.5 - 3, starting_y + TILE_HEIGHT * 21 / 28))
    WIN.blit(SHEEP, (starting_x + TILE_WIDTH * 2.5 - 4, starting_y + TILE_HEIGHT * 21 / 28))

    # Third row
    WIN.blit(DESERT, (starting_x - TILE_WIDTH, starting_y + 2 * TILE_HEIGHT * 21 / 28))
    WIN.blit(WOOD, (starting_x - 1, starting_y + 2 * TILE_HEIGHT * 21 / 28))
    WIN.blit(WHEAT, (starting_x + TILE_WIDTH - 3, starting_y + 2 * TILE_HEIGHT * 21 / 28))
    WIN.blit(WOOD, (starting_x + TILE_WIDTH * 2 - 4, starting_y + 2 * TILE_HEIGHT * 21 / 28))
    WIN.blit(WHEAT, (starting_x + TILE_WIDTH * 3 - 5, starting_y + 2 * TILE_HEIGHT * 21 / 28))

    # Fourth row
    WIN.blit(BRICK, (starting_x - TILE_WIDTH / 2, starting_y + 3 * TILE_HEIGHT * 21 / 28))
    WIN.blit(SHEEP, (starting_x + TILE_WIDTH / 2 - 2, starting_y + 3 * TILE_HEIGHT * 21 / 28))
    WIN.blit(SHEEP, (starting_x + TILE_WIDTH * 1.5 - 3, starting_y + 3 * TILE_HEIGHT * 21 / 28 - 1))
    WIN.blit(ORE, (starting_x + TILE_WIDTH * 2.5 - 4, starting_y + 3 * TILE_HEIGHT * 21 / 28 - 1))

    # Fifth row
    WIN.blit(ORE, (starting_x - 2, 4.4 * TILE_HEIGHT * 21/28 - 1))
    WIN.blit(WHEAT, (starting_x + TILE_WIDTH - buffer, 4.4 * TILE_HEIGHT * 21/28 - 1))
    WIN.blit(WHEAT, (starting_x + 2 * TILE_WIDTH - buffer - 1, 4.4 * TILE_HEIGHT * 21/28 - 2))

    pygame.draw.rect(WIN, GRAY, pygame.Rect(0, rectangle_starting_y, WIDTH, HEIGHT))



def draw_board():
    WIN.fill(BLUE)
    draw_tiles()
    Player().draw_hand()
    pygame.display.update()


class Player:
    def __init__(self):
        self.brick = 0
        self.wheat = 0
        self.wood = 0
        self.ore = 0
        self.sheep = 0
        self.vp = 0
        self.resource_cards = []
        self.card_width = 60
        self.card_height = 80
        self.init_resource_cards()


    def init_resource_cards(self):
        card_names = ['brick', 'wood', 'ore', 'sheep', 'wheat']
        for name in card_names:
            card = pygame.image.load(os.path.join('Assets', 'Resources', name + '_card.png'))
            self.resource_cards.append(pygame.transform.scale(card, (self.card_width, self.card_height)))

    def can_build_settlement(self):
        return self.wood and self.wheat and self.sheep and self.brick

    def draw_hand(self):
        starting_x = 20
        starting_y = 510
        vertical_buffer = 5
        horizantal_buffer = 10
        WIN.blit(self.resource_cards[0], (starting_x, starting_y))
        WIN.blit(self.resource_cards[1], (starting_x, starting_y + self.card_height + vertical_buffer))

def main():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_board()
        Player().draw_hand()

    pygame.quit()


if __name__ == '__main__':
    main()
