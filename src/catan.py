# The classic Catan board game by Gabe Holmes, will make it multiplayer eventually
# Right now focusing on playing against one bot
import math
import random
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
RED = (255, 0, 0)
GREEN = (0, 180, 0)
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
settlement_circle_size = 10
settlements_placed = []
SETTLEMENT_WIDTH = 15
SETTLEMENT_HEIGHT = 15

red_settlement = pygame.image.load(os.path.join('Assets', 'Pieces', 'red_settlement.png'))
red_settlement = pygame.transform.scale(red_settlement, (SETTLEMENT_WIDTH, SETTLEMENT_HEIGHT))

# The coordinates of all of the number tiles
# In the board class we will map each number that the dice can roll to a coordinate here, and a resource
# We then check if any settlements are within a certain distance from these coordinates, and if they
# are we add the resource to their player.
number_tile_pos = [(321, 89), (419, 88), (509, 87), (270, 173), (367, 176), (467, 172), (564, 173),
                   (219, 256), (322, 253), (417, 251), (517, 254), (610, 252), (270, 340), (365, 339),
                   (465, 340), (566, 340), (320, 422), (422, 421), (519, 420)]


def place_starting_settlement():
    # Draws circles where any starting settlement can be placed, and then waits for a choice from the player
    for pos in legal_settlement_pos:
        pygame.draw.circle(WIN, GRAY, (pos[0], pos[1]), settlement_circle_size)


# Displays the total rolled from the dice
def draw_total_rolled(total):
    font = pygame.font.Font('freesansbold.ttf', 18)
    roll_dice = font.render(str(total), True, BLACK, GREEN)
    dice_small_rect = roll_dice.get_bounding_rect()
    dice_small_rect.center = (60, 30)
    WIN.blit(roll_dice, dice_small_rect)


def draw_dev_card_display(player):
    pass


# Renders all of the info
def draw_board(board, player, place_settlements, settlements_placed, total, dev_card_display):
    WIN.fill(BLUE)
    board.draw_board()
    player.draw_hand()

    if place_settlements:
        place_starting_settlement()
    for pos in settlements_placed:
        pygame.draw.circle(WIN, RED, (pos[0], pos[1]), settlement_circle_size)

    draw_total_rolled(total)

    if dev_card_display:
        player.draw_dev_display()

    pygame.display.update()


# Class that deals with the board itself, including drawing the tiles and keeping track of what numbers
# correspond to what tiles
class Board:
    def __init__(self):
        # List of all of the resource tiles. The order they appear here is the order they appear on the board
        # The inited list is used as a default
        self.resource_list = [WOOD, SHEEP, WHEAT, BRICK, ORE, BRICK, SHEEP,
                              DESERT, WOOD, WHEAT, WOOD, WHEAT, BRICK, SHEEP, SHEEP, ORE, ORE, WHEAT, WOOD]

        self.resource_strings = ["WOOD", "SHEEP", "WHEAT", "BRICK", "ORE", "BRICK", "SHEEP",
                                 "DESERT", "WOOD", "WHEAT", "WOOD", "WHEAT", "BRICK", "SHEEP", "SHEEP", "ORE", "ORE",
                                 "WHEAT", "WOOD"]

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

    # Maps the possible numbers the dice can roll to a coordinate representing the resource tile position
    # and a resource itself
    def get_number_to_pos_and_resource_mapping(self):
        mapping = {}
        for i in range(2, 13):
            if i != 7:
                index_list = self.get_key_by_value(i)
                mapping_list = []
                for index in index_list:
                    try:
                        mapping_list.append((number_tile_pos[index], self.resource_strings[index]))
                    except IndexError:
                        print(str(i) + " index_list:")
                        print(index_list)
                mapping[i] = mapping_list
        mapping[7] = ([], "DESERT")
        return mapping

    def get_key_by_value(self, value):
        key_list = []
        for key in self.number_tile_mapping:
            if self.number_tile_mapping[key] == value:
                key_list.append(key)
        return key_list

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

        self.knights = 0
        self.vp_cards = 0
        self.road_building = 0
        self.year_of_plenty = 0
        self.monopoly = 0
        self.dev_cards = []

    def init_resource_cards(self):
        card_names = ['brick', 'wood', 'ore', 'sheep', 'wheat']
        for name in card_names:
            # Create the cards and set them to the correct size
            card = pygame.image.load(os.path.join('Assets', 'Resources', name + '_card.png'))
            self.resource_cards.append(pygame.transform.scale(card, (self.card_width, self.card_height)))

    def update_resources(self, resource_string):
        print(F"Resource massed = {resource_string}")
        if resource_string == "WHEAT":
            self.wheat += 1
        elif resource_string == "BRICK":
            self.brick += 1
        elif resource_string == "SHEEP":
            self.sheep += 1
        elif resource_string == "WOOD":
            self.wood += 1
        elif resource_string == "ORE":
            self.ore += 1
        else:
            return

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

        # Draw the development card
        # If a user clicks on this card, they will be able to see how many of each development card they have
        dev_card_default = pygame.image.load(os.path.join('Assets', 'DevCards', 'dvc.png'))
        dev_card_default = pygame.transform.scale(dev_card_default, (self.card_width, self.card_height))
        WIN.blit(dev_card_default, (starting_x + 2 * self.card_width + 2 * horizontal_buffer,
                                    starting_y + self.card_height + vertical_buffer))
        # boundaries are 20 + 120 + 10 = 150
        #                 510 + 80 + 5 = 595
        # then 210, 675

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

        # Draw the roll dice rectangle
        font = pygame.font.Font('freesansbold.ttf', 18)
        roll_dice = font.render('Roll Dice!', True, BLACK, GREEN)
        dice_small_rect = roll_dice.get_bounding_rect()
        dice_small_rect.center = (WIDTH - 60, HEIGHT - 30)
        WIN.blit(roll_dice, dice_small_rect)
        # Boundaries are width - 100, height - 36
        # width - 17, height - 21

    def draw_dev_display(self):
        horizontal_buffer = 5
        vertical_buffer = 3
        starting_x = 9
        starting_y = 484
        # First draw a white rectangle coming from the dev card displayed
        pygame.draw.rect(WIN, WHITE, pygame.Rect(starting_x, starting_y + vertical_buffer - 155,
                                                 760,
                                                 230))
        pygame.draw.polygon(WIN, WHITE, [(166, 597), (188, 597), (245, 554), (105, 554)])

        # Create the cards
        card_names = ['chapel', 'knight', 'monopoly', 'road_building', 'year_of_plenty']
        for name in card_names:
            # Create the cards and set them to the correct size
            card = pygame.image.load(os.path.join('Assets', 'DevCards', name + '_dvc.png'))
            self.dev_cards.append(pygame.transform.scale(card, (card.get_width() / 2.2, card.get_height() / 2.2)))

        # Draw the cards
        for i, card in enumerate(self.dev_cards):
            # Only draw 5 cards
            if i == 5:
                break
            WIN.blit(card, ((i + 3) * horizontal_buffer + i * card.get_width(), starting_y + vertical_buffer - 150))


# Checks if the coordinates are a valid settlement position
# If it is draws a red circle and returns True, False otherwise
def check_starting_settlement_placed(x_cord, y_cord):
    for pos in legal_settlement_pos:
        if math.hypot(pos[0] - x_cord, pos[1] - y_cord) <= settlement_circle_size:
            settlements_placed.append(pos)
            legal_settlement_pos.remove(pos)
            # TODO remove the 2 or 3 adjacent settlements from legal_settlement_pos too
            WIN.blit(red_settlement, (pos[0], pos[1]))
            return True
    return False


def check_roll_dice_clicked_and_roll(x_cord, y_cord, board, player):
    if WIDTH - 100 <= x_cord <= WIDTH - 17 and HEIGHT - 36 <= y_cord <= HEIGHT - 21:
        return roll_dice_and_distribute(board, player)


def get_distance(x1, y1, x2, y2):
    asq = (x1 - x2) ** 2
    bsq = (y1 - y2) ** 2
    return math.sqrt(asq + bsq)


def roll_dice_and_distribute(board, player):
    num1 = random.randint(1, 6)
    num2 = random.randint(1, 6)
    total = num1 + num2
    if total == 7:
        return 7

    # List of tuples that contain ((x_cord, y_cord), resource_tile)
    mapping = board.get_number_to_pos_and_resource_mapping()
    lst = mapping[total]
    circle_radius = 76.02
    for entry in lst:
        if entry[1] != "DESERT":
            for settlement_pos in settlements_placed:
                if get_distance(settlement_pos[0], settlement_pos[1], entry[0][0], entry[0][1]) <= circle_radius:
                    player.update_resources(entry[1])
    return total


# Returns True of the coordinates passed are within the development card
# displayed at the bottom of the screen, False otherwise
def check_dev_card_clicked(x_cord, y_cord):
    # boundaries are 20 + 120 + 10 = 150
    #                 510 + 80 + 5 = 595
    # then 210, 675
    return 150 <= x_cord <= 210 and 595 <= y_cord <= 675


def main():
    board1 = Board()
    player1 = Player()
    drew_settlement = False
    draw_starting_settlements = True
    draw_dev_cards = False
    pos = []
    run = True
    total = -1
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                x_cord, y_cord = pygame.mouse.get_pos()
                print(str(x_cord) + " " + str(y_cord))
                # pos.append((x_cord, y_cord))

                # Check if a settlement was placed, and if it was don't draw the possible positions
                # that a settlement can be placed
                drew_settlement = check_starting_settlement_placed(x_cord, y_cord)

                # Check if the roll dice button was pressed, and if it was distribute the appropriate resources
                total = check_roll_dice_clicked_and_roll(x_cord, y_cord, board1, player1)

                # Check if the resource card was clicked, and if it was indicate that the dev card display
                # should be drawn
                draw_dev_cards = check_dev_card_clicked(x_cord, y_cord)
        if drew_settlement:
            draw_starting_settlements = False

        draw_board(board1, player1, draw_starting_settlements, settlements_placed, total, draw_dev_cards)
    # print(pos)
    pygame.quit()


if __name__ == '__main__':
    main()
