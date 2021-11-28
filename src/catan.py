# The classic Catan board game by Gabe Holmes, will make it multiplayer eventually
# Right now focusing on playing against one bot
from enum import Enum

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


class DevCard(Enum):
    Knight = 14
    VictoryPoint = 5
    RoadBuilding = 2
    YearOfPlenty = 2
    Monopoly = 2


# List of x,y coordinates representing all the vertices where settlements can be placed at the start of the game
# This list will be modified as settlements are placed
legal_settlement_pos = [(320, 36), (415, 35), (516, 35), (273, 61), (368, 62), (466, 62), (563, 62),
                        (272, 117), (364, 118), (466, 116), (564, 116), (224, 144), (317, 144),
                        (414, 147), (515, 146), (613, 146), (221, 200), (320, 200), (416, 202),
                        (515, 201), (613, 200), (171, 231), (270, 227), (368, 231), (465, 228),
                        (561, 229), (661, 228), (172, 282), (267, 282), (366, 283), (464, 283),
                        (562, 283), (661, 283), (221, 311), (318, 310), (415, 312), (512, 311),
                        (612, 312), (221, 365), (320, 365), (417, 366), (513, 366), (612, 367),
                        (269, 394), (367, 393), (467, 391), (562, 394), (270, 449), (369, 448),
                        (466, 449), (564, 449), (319, 477), (417, 477), (513, 477)]


def draw_circle(x_pos, y_pos):
    pygame.draw.circle(WIN, GRAY, (x_pos, y_pos), 10)


def place_starting_settlement():
    # TODO draw circles everywhere settlements can be placed
    for pos in legal_settlement_pos:
        draw_circle(pos[0], pos[1])


# Renders all of the info
def draw_board(board, player, place_settlements):
    WIN.fill(BLUE)
    board.draw_board()
    player.draw_hand()
    if place_settlements:
        place_starting_settlement()
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
        self.number_tile_mapping = {0: 11, 1: 12, 2: 9, 3: 4, 4: 6, 5: 5, 6: 10, 8: 3, 9: 11,
                                    10: 4, 11: 8, 12: 8, 13: 10, 14: 9, 15: 3, 16: 5, 17: 2, 18: 6}

        # List containing all of the development cards
        self.dev_cards = []
        self.init_dev_cards()

        self.number_tiles = []
        self.init_number_tile_pics()

    def init_number_tile_pics(self):
        for i in range(2, 13):
            if i != 7:
                num = pygame.image.load(os.path.join('Assets', 'NumberTiles', 'number_{}.png'.format(str(i))))
                num = pygame.transform.scale(num, (35, 35))
                self.number_tiles.append(num)
        self.number_tiles.insert(0, -1)
        self.number_tiles.insert(0, -1)
        self.number_tiles.insert(7, -1)

    def init_dev_cards(self):
        for i in range(25):
            if i < 2:
                self.dev_cards.append(DevCard.Monopoly)
            elif i < 4:
                self.dev_cards.append(DevCard.YearOfPlenty)
            elif i < 6:
                self.dev_cards.append(DevCard.RoadBuilding)
            elif i < 11:
                self.dev_cards.append(DevCard.VictoryPoint)
            elif i < 25:
                self.dev_cards.append(DevCard.Knight)

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
        WIN.blit(self.number_tiles[self.number_tile_mapping[0]], (starting_x + TILE_WIDTH / 3,
                                                                  starting_y + TILE_HEIGHT / 3))
        WIN.blit(self.resource_list[1], (starting_x + TILE_WIDTH - buffer, starting_y))
        WIN.blit(self.number_tiles[self.number_tile_mapping[1]], (starting_x + 4 * TILE_WIDTH / 3,
                                                                  starting_y + TILE_HEIGHT / 3))
        WIN.blit(self.resource_list[2], (starting_x + 2 * TILE_WIDTH - buffer, starting_y))
        WIN.blit(self.number_tiles[self.number_tile_mapping[2]], (starting_x + 7 * TILE_WIDTH / 3 - 10,
                                                                  starting_y + TILE_HEIGHT / 3))
        # Second Row
        WIN.blit(self.resource_list[3], (starting_x - TILE_WIDTH / 2, starting_y + TILE_HEIGHT * 21 / 28))
        WIN.blit(self.number_tiles[self.number_tile_mapping[3]], (starting_x - TILE_WIDTH / 3 + 15,
                                                                  starting_y + 3 * TILE_HEIGHT / 3 + 10))
        WIN.blit(self.resource_list[4], (starting_x + TILE_WIDTH / 2 - 2, starting_y + TILE_HEIGHT * 21 / 28))
        WIN.blit(self.number_tiles[self.number_tile_mapping[4]], (starting_x + TILE_WIDTH / 2 + 30,
                                                                  starting_y + 3 * TILE_HEIGHT / 3 + 10))
        WIN.blit(self.resource_list[5], (starting_x + TILE_WIDTH * 1.5 - 3, starting_y + TILE_HEIGHT * 21 / 28))
        WIN.blit(self.number_tiles[self.number_tile_mapping[5]], (starting_x + 1.5 * TILE_WIDTH + 30,
                                                                  starting_y + 3 * TILE_HEIGHT / 3 + 10))
        WIN.blit(self.resource_list[6], (starting_x + TILE_WIDTH * 2.5 - 4, starting_y + TILE_HEIGHT * 21 / 28))
        WIN.blit(self.number_tiles[self.number_tile_mapping[6]], (starting_x + 2.5 * TILE_WIDTH + 26,
                                                                  starting_y + 3 * TILE_HEIGHT / 3 + 10))

        # Third row
        WIN.blit(self.resource_list[7], (starting_x - TILE_WIDTH, starting_y + 2 * TILE_HEIGHT * 21 / 28))
        WIN.blit(self.resource_list[8], (starting_x - 1, starting_y + 2 * TILE_HEIGHT * 21 / 28))
        WIN.blit(self.number_tiles[self.number_tile_mapping[8]], (starting_x + TILE_WIDTH / 3,
                                                                  starting_y + 5 * TILE_HEIGHT / 3 + 16))
        WIN.blit(self.resource_list[9], (starting_x + TILE_WIDTH - 3, starting_y + 2 * TILE_HEIGHT * 21 / 28))
        WIN.blit(self.number_tiles[self.number_tile_mapping[9]], (starting_x + 1.3 * TILE_WIDTH,
                                                                  starting_y + 5 * TILE_HEIGHT / 3 + 16))
        WIN.blit(self.resource_list[10], (starting_x + TILE_WIDTH * 2 - 4, starting_y + 2 * TILE_HEIGHT * 21 / 28))
        WIN.blit(self.number_tiles[self.number_tile_mapping[10]], (starting_x + 2.3 * TILE_WIDTH,
                                                                   starting_y + 5 * TILE_HEIGHT / 3 + 16))
        WIN.blit(self.resource_list[11], (starting_x + TILE_WIDTH * 3 - 5, starting_y + 2 * TILE_HEIGHT * 21 / 28))
        WIN.blit(self.number_tiles[self.number_tile_mapping[11]], (starting_x + 3.25 * TILE_WIDTH,
                                                                   starting_y + 5 * TILE_HEIGHT / 3 + 16))

        # Fourth row
        WIN.blit(self.resource_list[12], (starting_x - TILE_WIDTH / 2 - 1, starting_y + 3 * TILE_HEIGHT * 21 / 28 - 1))
        WIN.blit(self.number_tiles[self.number_tile_mapping[12]], (starting_x - TILE_WIDTH / 3 + 15,
                                                                   starting_y + 7.5 * TILE_HEIGHT / 3 + 10))
        WIN.blit(self.resource_list[13], (starting_x + TILE_WIDTH / 2 - 2, starting_y + 3 * TILE_HEIGHT * 21 / 28 - 1))
        WIN.blit(self.number_tiles[self.number_tile_mapping[13]], (starting_x + TILE_WIDTH / 1.6 + 15,
                                                                   starting_y + 7.5 * TILE_HEIGHT / 3 + 10))
        WIN.blit(self.resource_list[14],
                 (starting_x + TILE_WIDTH * 1.5 - 3, starting_y + 3 * TILE_HEIGHT * 21 / 28 - 1))
        WIN.blit(self.number_tiles[self.number_tile_mapping[14]], (starting_x + 1.63 * TILE_WIDTH + 15,
                                                                   starting_y + 7.5 * TILE_HEIGHT / 3 + 10))
        WIN.blit(self.resource_list[15],
                 (starting_x + TILE_WIDTH * 2.5 - 5, starting_y + 3 * TILE_HEIGHT * 21 / 28 - 1))
        WIN.blit(self.number_tiles[self.number_tile_mapping[15]], (starting_x + 2.65 * TILE_WIDTH + 15,
                                                                   starting_y + 7.5 * TILE_HEIGHT / 3 + 10))

        # Fifth row
        WIN.blit(self.resource_list[16], (starting_x - 2, 4.4 * TILE_HEIGHT * 21 / 28 - 2))
        WIN.blit(self.number_tiles[self.number_tile_mapping[16]], (starting_x + TILE_WIDTH / 3,
                                                                   starting_y + 10 * TILE_HEIGHT / 3))
        WIN.blit(self.resource_list[17], (starting_x + TILE_WIDTH - buffer, 4.4 * TILE_HEIGHT * 21 / 28 - 1))
        WIN.blit(self.number_tiles[self.number_tile_mapping[17]], (starting_x + 4 * TILE_WIDTH / 3,
                                                                   starting_y + 10 * TILE_HEIGHT / 3))
        WIN.blit(self.resource_list[18], (starting_x + 2 * TILE_WIDTH - buffer - 1, 4.4 * TILE_HEIGHT * 21 / 28 - 2))
        WIN.blit(self.number_tiles[self.number_tile_mapping[18]], (starting_x + 7 * TILE_WIDTH / 3,
                                                                   starting_y + 10 * TILE_HEIGHT / 3))

        # Bottom gray rectangle
        pygame.draw.rect(WIN, GRAY, pygame.Rect(0, rectangle_starting_y, WIDTH, HEIGHT))


class Player:
    def __init__(self, is_bot=False):
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

        self.isBot = is_bot

        self.max_roads = 15
        self.max_cities = 4
        self.max_settlements = 5

    def init_resource_cards(self):
        card_names = ['brick', 'wood', 'ore', 'sheep', 'wheat']
        for name in card_names:
            # Create the cards and set them to the correct size
            card = pygame.image.load(os.path.join('Assets', 'Resources', name + '_card.png'))
            self.resource_cards.append(pygame.transform.scale(card, (self.card_width, self.card_height)))

    def can_build_settlement(self):
        return self.wood and self.wheat and self.sheep and self.brick

    def can_build_city(self):
        return self.ore >= 3 and self.wheat >= 2

    def can_build_road(self):
        return self.wood and self.brick

    def can_buy_dev_card(self):
        return self.sheep and self.wheat and self.ore

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
    board1 = Board()
    player1 = Player()
    need_place_starting_settle = True
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                if need_place_starting_settle:
                    need_place_starting_settle = False

        draw_board(board1, player1, True)

    pygame.quit()


if __name__ == '__main__':
    main()
