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


# Renders all of the info
def draw_board():
    WIN.fill(BLUE)
    Board().draw_board()
    Player().draw_hand()
    pygame.display.update()


# Class that deals with the board itself, including drawing the tiles and keeping track of what numbers
# correspond to what tiles
class Board:
    def __init__(self):
        # List of all of the resource tiles. The order they appear here is the order they appear on the board
        # The inited list is used as a default
        self.resource_list = [WOOD, SHEEP, WHEAT, BRICK, ORE, BRICK, SHEEP,
                              DESERT, WOOD, WHEAT, WOOD, WHEAT, BRICK, SHEEP, SHEEP, ORE, ORE, WHEAT, WOOD]

        # Map from int -> list of ints where the first int is a number tile value [2, 12] and the second
        # is the indices in resource_list that the number tile maps to
        # maps to a list of int because most numbers, such as 6 and 8, will appear multiple times on the board
        self.number_tile_mapping = {2: [17], 3: [8, 15], 4: [3, 10], 5: [5, 16], 6: [4, 18], 7: None,
                                    8: [11, 12], 9: [2, 14], 10: [6, 13], 11: [0, 9], 12: [1]}

    def gen_random_board(self):
        # TODO Make this board generate a random assortment of tiles, but only allowing 4 of any one resource
        return

    # Draws the hexagonal tiles, and then draws the number tiles on top
    def draw_board(self):
        starting_x = 270
        starting_y = 33
        buffer = 3

        rectangle_starting_y = HEIGHT * 0.73
        # First row
        WIN.blit(self.resource_list[0], (starting_x, starting_y))
        WIN.blit(self.resource_list[1], (starting_x + TILE_WIDTH - buffer, starting_y))
        WIN.blit(self.resource_list[2], (starting_x + 2 * TILE_WIDTH - buffer, starting_y))

        # Second Row
        WIN.blit(self.resource_list[3], (starting_x - TILE_WIDTH / 2, starting_y + TILE_HEIGHT * 21 / 28))
        WIN.blit(self.resource_list[4], (starting_x + TILE_WIDTH / 2 - 2, starting_y + TILE_HEIGHT * 21 / 28))
        WIN.blit(self.resource_list[5], (starting_x + TILE_WIDTH * 1.5 - 3, starting_y + TILE_HEIGHT * 21 / 28))
        WIN.blit(self.resource_list[6], (starting_x + TILE_WIDTH * 2.5 - 4, starting_y + TILE_HEIGHT * 21 / 28))

        # Third row
        WIN.blit(self.resource_list[7], (starting_x - TILE_WIDTH, starting_y + 2 * TILE_HEIGHT * 21 / 28))
        WIN.blit(self.resource_list[8], (starting_x - 1, starting_y + 2 * TILE_HEIGHT * 21 / 28))
        WIN.blit(self.resource_list[9], (starting_x + TILE_WIDTH - 3, starting_y + 2 * TILE_HEIGHT * 21 / 28))
        WIN.blit(self.resource_list[10], (starting_x + TILE_WIDTH * 2 - 4, starting_y + 2 * TILE_HEIGHT * 21 / 28))
        WIN.blit(self.resource_list[11], (starting_x + TILE_WIDTH * 3 - 5, starting_y + 2 * TILE_HEIGHT * 21 / 28))

        # Fourth row
        WIN.blit(self.resource_list[12], (starting_x - TILE_WIDTH / 2, starting_y + 3 * TILE_HEIGHT * 21 / 28))
        WIN.blit(self.resource_list[13], (starting_x + TILE_WIDTH / 2 - 2, starting_y + 3 * TILE_HEIGHT * 21 / 28))
        WIN.blit(self.resource_list[14],
                 (starting_x + TILE_WIDTH * 1.5 - 3, starting_y + 3 * TILE_HEIGHT * 21 / 28 - 1))
        WIN.blit(self.resource_list[15],
                 (starting_x + TILE_WIDTH * 2.5 - 4, starting_y + 3 * TILE_HEIGHT * 21 / 28 - 1))

        # Fifth row
        WIN.blit(self.resource_list[16], (starting_x - 2, 4.4 * TILE_HEIGHT * 21 / 28 - 1))
        WIN.blit(self.resource_list[17], (starting_x + TILE_WIDTH - buffer, 4.4 * TILE_HEIGHT * 21 / 28 - 1))
        WIN.blit(self.resource_list[18], (starting_x + 2 * TILE_WIDTH - buffer - 1, 4.4 * TILE_HEIGHT * 21 / 28 - 2))

        pygame.draw.rect(WIN, GRAY, pygame.Rect(0, rectangle_starting_y, WIDTH, HEIGHT))


class Player:
    def __init__(self):
        self.brick = 0
        self.wheat = 0
        self.wood = 0
        self.ore = 0
        self.sheep = 0

        self.vp = 0

        self.card_width = 60
        self.card_height = 80
        self.resource_cards = []
        self.init_resource_cards()

    def init_resource_cards(self):
        card_names = ['brick', 'wood', 'ore', 'sheep', 'wheat']
        for name in card_names:
            # Create the cards and set them to the correct size
            card = pygame.image.load(os.path.join('Assets', 'Resources', name + '_card.png'))
            self.resource_cards.append(pygame.transform.scale(card, (self.card_width, self.card_height)))

    def can_build_settlement(self):
        return self.wood and self.wheat and self.sheep and self.brick

    # Draws all the information about a players hand, including how many of each resource they have
    # how many and what development cards they have, their victory points,
    def draw_hand(self):
        # x and y coordinates of starting card in the players hand
        starting_x = 20
        starting_y = 510
        # Buffers between cards
        vertical_buffer = 5
        horizontal_buffer = 5

        # Draw all the resource cards
        WIN.blit(self.resource_cards[0], (starting_x, starting_y))
        WIN.blit(self.resource_cards[1], (starting_x, starting_y + self.card_height + vertical_buffer))
        WIN.blit(self.resource_cards[2], (starting_x + self.card_width + horizontal_buffer, starting_y))
        WIN.blit(self.resource_cards[3], (starting_x + self.card_width + horizontal_buffer,
                                          starting_y + self.card_height + vertical_buffer))
        WIN.blit(self.resource_cards[4], (starting_x + 2 * self.card_width + 2 * horizontal_buffer, starting_y))

        # Draw the amount of each resource that the player has
        font = pygame.font.Font('freesansbold.ttf', 18)

        # For the number of bricks
        num = font.render(str(self.brick), True, BLACK, WHITE)
        rect = num.get_rect()
        rect.center = (starting_x + self.card_width - 10, starting_y + self.card_height - 15)
        WIN.blit(num, rect)

        # Number of ore
        num = font.render(str(self.ore), True, BLACK, WHITE)
        rect = num.get_rect()
        rect.center = (starting_x + 2 * self.card_width + horizontal_buffer - 10,
                       starting_y + self.card_height - 15)
        WIN.blit(num, rect)

        # Number of wheat
        num = font.render(str(self.wheat), True, BLACK, WHITE)
        rect = num.get_rect()
        rect.center = (starting_x + 3 * self.card_width + 2 * horizontal_buffer - 10,
                       starting_y + self.card_height - 15)
        WIN.blit(num, rect)

        # Number of wood
        num = font.render(str(self.wood), True, BLACK, WHITE)
        rect = num.get_rect()
        rect.center = (starting_x + self.card_width - 10,
                       starting_y + 2 * self.card_height + vertical_buffer - 15)
        WIN.blit(num, rect)

        # Number of sheep
        num = font.render(str(self.sheep), True, BLACK, WHITE)
        rect = num.get_rect()
        rect.center = (starting_x + 2 * self.card_width + horizontal_buffer - 10,
                       starting_y + 2 * self.card_height + vertical_buffer - 15)
        WIN.blit(num, rect)


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
