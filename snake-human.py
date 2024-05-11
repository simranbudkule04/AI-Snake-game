import pygame
from pygame import *
import random
import itertools


# initializing pygame
pygame.init()

# declaring finals
BG_COLOR = (175,215,70)
SNAKE_COLOR = (100, 171, 70)
SNAKE_BORDER_COLOR = BG_COLOR
SNAKE_FOOD_COLOR = (224, 93, 79)
SNAKE_FOOD_BORDER_COLOR = SNAKE_BORDER_COLOR
A_STAR_COLOR = (63, 101, 204)
SNAKE_INITIAL_POS = [0, 0]
FONT = pygame.font.Font("freesansbold.ttf", 24)
GAME_OVER_FONT_COLOR = (255, 255, 255)
RED = (255, 0, 0)
FPS = 11

# cycle iter for a star the simulation
a_star_cycle = itertools.cycle('yn')

# initializing snake array
snake_body_array = [SNAKE_INITIAL_POS]

# initializing pygame display
display = pygame.display.set_mode((700, 600))
display.fill(BG_COLOR)
display_border = pygame.draw.rect(display, (255, 255, 255), [0, 0, 700, 600], 1)

# Title and Icon
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        pass

    def add_length(self, pos):
        snake_body_array.append(pos)

    def draw(self):
        for XnY in snake_body_array:
            pygame.draw.rect(display, SNAKE_COLOR, [XnY[0], XnY[1], 19, 19], 0)  # solid
            pygame.draw.rect(display, SNAKE_BORDER_COLOR, [XnY[0], XnY[1], 20, 20], 1)  # border


class Spot:
    def __init__(self, pos_x=0, pos_y=0, color=SNAKE_COLOR):
        # validating whether the coordinates of the spots will fit in the grid
        if pos_x <= 700 - 20:
            self.pos_x = pos_x
        else:
            self.pos_x = 0
        if pos_y <= 600 - 20:
            self.pos_y = pos_y
        else:
            self.pos_y = 0

        self.color = color
        # scores (g, h, f)
        self.g_score = 0
        self.h_score = 0
        self.f_score = 0
        # previous spot
        self.previous = None

    def draw(self):
        """this method will draw the spot on the grid"""
        pygame.draw.rect(display, self.color, [self.pos_x, self.pos_y, 19, 19])
        pygame.draw.rect(display, SNAKE_BORDER_COLOR, [self.pos_x, self.pos_y, 20, 20], 1)

    def get_coord(self):
        return self.pos_x, self.pos_y

    def __repr__(self):
        return '(' + str(self.pos_x) + ',' + str(self.pos_y) + ')'

    def __eq__(self, other):
        return isinstance(other, Spot) and (other.pos_x == self.pos_x and other.pos_y == self.pos_y)

    def __ne__(self, other):
        return not(isinstance(other, Spot)) or (other.pos_x != self.pos_x or other.pos_y != self.pos_y)


# getting a random food position and drawing it
def get_random_food_pos(snake_array):
    food_x_pos = random.randint(0, 680)
    food_y_pos = random.randint(0, 580)

    # validating the positions
    while ([food_x_pos, food_y_pos] in snake_array) or (food_x_pos % 19 != 0) or (food_y_pos % 19 != 0):
        food_x_pos = random.randint(0, 680)
        food_y_pos = random.randint(0, 580)

    return [food_x_pos, food_y_pos]


food_pos = get_random_food_pos(snake_body_array)


# game over window
def game_over():
    # game over text
    pygame.font.init()
    game_over_text = FONT.render("GAME OVER!", True, GAME_OVER_FONT_COLOR)
    restart_text = FONT.render("Press SPACE to Restart", True, GAME_OVER_FONT_COLOR)
    text_rect = game_over_text.get_rect()
    text_rect.center = (350, 300)
    display.blit(game_over_text, text_rect)
    text_rect = restart_text.get_rect()
    text_rect.center = (350, 340)
    display.blit(restart_text, text_rect)


def display_score():
    score_text = FONT.render("Score: " + str(score), True, GAME_OVER_FONT_COLOR)
    text_rect = score_text.get_rect()
    text_rect.center = (610, 40)
    display.blit(score_text, text_rect)


# A STAR
# head of snake position
head_of_snake_pos_x = snake_body_array[0][0]
head_of_snake_pos_y = snake_body_array[0][1]
# We need 2 spots in the beginning, one start spot and one end spot
start_spot = Spot(head_of_snake_pos_x, head_of_snake_pos_y, color=SNAKE_COLOR)
end_spot = Spot(food_pos[0], food_pos[1], color=SNAKE_FOOD_COLOR)
# explored spots (A*)
closed_list = []
# unexplored spots (A*)
open_list = [start_spot]  # placing the starting spot
# solution path (A*)
path = []
# A* goal reached boolean
goal_reached = False


def valid_places_to_go_a_star(current_spot_pos, obstacle_list):
    valid_places = []

    right_of_curr_coord = [current_spot_pos[0] + 19, current_spot_pos[1]]
    left_of_curr_coord = [current_spot_pos[0] - 19, current_spot_pos[1]]
    top_of_curr_coord = [current_spot_pos[0], current_spot_pos[1] - 19]
    bottom_of_curr_coord = [current_spot_pos[0], current_spot_pos[1] + 19]

    if (left_of_curr_coord not in obstacle_list) \
            and (left_of_curr_coord[0] >= 0) and (left_of_curr_coord[0] <= 680) and (left_of_curr_coord[1] >= 0) \
            and (left_of_curr_coord[1] <= 580):
        valid_places.append(Spot(left_of_curr_coord[0], left_of_curr_coord[1]))

    if (right_of_curr_coord not in obstacle_list) \
            and (right_of_curr_coord[0] >= 0) and (right_of_curr_coord[0] <= 680) and (right_of_curr_coord[1] >= 0) \
            and (right_of_curr_coord[1] <= 580):
        valid_places.append(Spot(right_of_curr_coord[0], right_of_curr_coord[1]))

    if (top_of_curr_coord not in obstacle_list) \
            and (top_of_curr_coord[0] >= 0) and (top_of_curr_coord[0] <= 680) and (top_of_curr_coord[1] >= 0) \
            and (top_of_curr_coord[1] <= 580):
        valid_places.append(Spot(top_of_curr_coord[0], top_of_curr_coord[1]))

    if (bottom_of_curr_coord not in obstacle_list) \
            and (bottom_of_curr_coord[0] >= 0) and (bottom_of_curr_coord[0] <= 680) and (bottom_of_curr_coord[1] >= 0) \
            and (bottom_of_curr_coord[1] <= 580):
        valid_places.append(Spot(bottom_of_curr_coord[0], bottom_of_curr_coord[1]))
    return valid_places


def find_a_star_path(explorable_list=open_list, start_spot_pos=start_spot, end_spot_pos=end_spot,
                     explored_list=closed_list, obstacle_spots=snake_body_array,
                     goal_reached_bool=goal_reached):
    while not goal_reached_bool:
        if len(explorable_list) != 0:
            # finding the spot with the lowest f score in the open list
            sorted_open_list_spots_f_scores = sorted(explorable_list, key=lambda n: n.f_score)
            q = sorted_open_list_spots_f_scores[0]  # spot with the lowest f score
            explorable_list.remove(q)
            # generating q's neighbors
            valid_places = valid_places_to_go_a_star((q.pos_x, q.pos_y), obstacle_spots)
            for neighbor in valid_places:
                if neighbor == end_spot_pos:
                    neighbor.previous = q
                    temp = neighbor
                    while temp.previous is not None:
                        path.append(temp.previous)
                        temp = temp.previous
                    goal_reached_bool = True

                else:
                    neighbor.g_score = q.g_score + 1
                    neighbor.h_score = (abs(neighbor.pos_x - end_spot.pos_x) +
                                        abs(neighbor.pos_y - end_spot.pos_y))
                    neighbor.f_score = neighbor.g_score + neighbor.h_score
                    neighbor.previous = q

                    if neighbor in explorable_list:
                        indx = explorable_list.index(neighbor)
                        if explorable_list[indx].f_score < neighbor.f_score:
                            continue

                    elif neighbor in explored_list:
                        indx = explored_list.index(neighbor)
                        if explored_list[indx].f_score < neighbor.f_score:
                            continue

                    else:
                        explorable_list.append(neighbor)

            if q not in closed_list:
                explored_list.append(q)

        else:
            raise IndexError
    for p in path:
        if p is not start_spot_pos:
            Spot(p.pos_x, p.pos_y, color=A_STAR_COLOR).draw()


def pick_random_valid_place(valid_places):
    try:
        random_idx = random.randint(1, len(valid_places))
        return valid_places[random_idx - 1]
    except (IndexError, ValueError):
        return None


# pygame run loop
running = True

# initializing the snake
snake = Snake()

# booleans to validate keyboard inputs
snake_block_left = False
snake_block_right = False
snake_block_bottom = False
snake_block_top = False

# change in head snake position
head_x_change = 0
head_y_change = 0

# initializing length of snake (not counting the head)
snake_len = 0

# initializing score
score = 0

# game over boolean
lost = False

# restart choice made boolean
choice_made = True

# choice to enable A* path finding help
a_star_enable = ""

while running:
    previous_head_pos_x = head_of_snake_pos_x
    previous_head_pos_y = head_of_snake_pos_y

    if score >= 100:
        lost = True
        #score_text = FONT.render("Score: " + str(score), True, GAME_OVER_FONT_COLOR)
        head_x_change = 0
        head_y_change = 0
        choice_made = False
        game_over()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not lost:
            # KEYDOWN means key pressed
            if event.type == pygame.KEYDOWN:
                if a_star_enable == '' or a_star_enable == 'n':
                    if event.key == pygame.K_DOWN:
                        if not snake_block_bottom:
                            head_y_change = 19
                            head_x_change = 0
                    elif event.key == pygame.K_UP:
                        if not snake_block_top:
                            head_y_change = -19
                            head_x_change = 0
                    elif event.key == pygame.K_RIGHT:
                        if not snake_block_right:
                            head_x_change = 19
                            head_y_change = 0
                    elif event.key == pygame.K_LEFT:
                        if not snake_block_left:
                            head_x_change = -19
                            head_y_change = 0
                if event.key == pygame.K_a:
                    a_star_enable = next(a_star_cycle)
                    head_x_change = 0
                    head_y_change = 0
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lost = False
                    choice_made = True
                    snake_body_array.clear()
                    snake_body_array.append(SNAKE_INITIAL_POS)
                    snake_len = 0
                    score = 0
                    head_of_snake_pos_x = 0
                    head_of_snake_pos_y = 0
                    head_x_change = 0
                    head_y_change = 0
                    previous_head_pos_x = 0
                    previous_head_pos_y = 0
                    snake_block_left = False
                    snake_block_right = False
                    snake_block_bottom = False
                    snake_block_top = False

    if choice_made:
        display.fill(BG_COLOR)

        if a_star_enable == "y":
            open_list = [Spot(head_of_snake_pos_x, head_of_snake_pos_y)]
            closed_list = []
            path = []
            start_spot = open_list[0]
            end_spot = Spot(food_pos[0], food_pos[1])

            try:
                find_a_star_path(explorable_list=open_list, explored_list=closed_list,
                                 start_spot_pos=start_spot, end_spot_pos=end_spot,
                                 obstacle_spots=snake_body_array)
                try:
                    head_of_snake_pos_x = path[-2].pos_x
                    head_of_snake_pos_y = path[-2].pos_y

                except IndexError:
                    head_of_snake_pos_x = food_pos[0]
                    head_of_snake_pos_y = food_pos[1]

            except IndexError:
                try:
                    valid_places = valid_places_to_go_a_star([head_of_snake_pos_x, head_of_snake_pos_y],
                                                             snake_body_array)
                    rand_place = pick_random_valid_place(valid_places)
                    try:
                        head_of_snake_pos_x = rand_place.pos_x
                        head_of_snake_pos_y = rand_place.pos_y
                    except AttributeError:
                        print("WHAT DO I DO!!!")
                        a_star_enable = 'n'
                        pass
                except IndexError:
                    print("WHAT DO I DO!!!")
                    a_star_enable = 'n'
                    pass
        else:
            # updating the head snake position
            head_of_snake_pos_x += head_x_change
            head_of_snake_pos_y += head_y_change

        snake_body_array[0][0] = head_of_snake_pos_x
        snake_body_array[0][1] = head_of_snake_pos_y

        # drawing the snake
        snake.draw()

        # displaying player score
        display_score()

        # drawing the food
        pygame.draw.rect(display, SNAKE_FOOD_COLOR, [food_pos[0], food_pos[1], 19, 19], 0)  # food solid
        pygame.draw.rect(display, SNAKE_FOOD_BORDER_COLOR, [food_pos[0], food_pos[1], 20, 20], 1)  # food border

        # checking if snake ate the food, if yes, then adding its length
        if food_pos == [head_of_snake_pos_x, head_of_snake_pos_y]:
            # adding length to snake
            snake_len += 1
            score += 10
            snake_body_array.append([previous_head_pos_x, previous_head_pos_y])
            # moving the food spot elsewhere
            food_pos = get_random_food_pos(snake_body_array)

        # propagating the non head positions
        for j in range(1, len(snake_body_array)):
            snake_body_array[j][0] = snake_body_array[j - snake_len][0]
            snake_body_array[j][1] = snake_body_array[j - snake_len][1]

        # restricting invalid moves
        if snake_len >= 1:
            if head_of_snake_pos_x > previous_head_pos_x and head_of_snake_pos_y == previous_head_pos_y:
                snake_block_left = True
                snake_block_right = False
                snake_block_top = False
                snake_block_bottom = False
            elif head_of_snake_pos_x < previous_head_pos_x and head_of_snake_pos_y == previous_head_pos_y:
                snake_block_left = False
                snake_block_right = True
                snake_block_top = False
                snake_block_bottom = False
            elif head_of_snake_pos_y > previous_head_pos_y and head_of_snake_pos_x == previous_head_pos_x:
                snake_block_left = False
                snake_block_right = False
                snake_block_top = True
                snake_block_bottom = False
            elif head_of_snake_pos_y < previous_head_pos_y and head_of_snake_pos_x == previous_head_pos_x:
                snake_block_left = False
                snake_block_right = False
                snake_block_top = False
                snake_block_bottom = True

            # detecting self-collision
            if [head_of_snake_pos_x, head_of_snake_pos_y] in snake_body_array[1:-1]:
                if not(head_x_change == 0 and head_y_change == 0):
                    print("Cause of Death: Self-Collision")
                    lost = True
                    head_x_change = 0
                    head_y_change = 0
                    choice_made = False
                    game_over()

        # detecting boundary collision
        if not ((0 <= head_of_snake_pos_x <= 679) and (0 <= head_of_snake_pos_y <= 579)):
            print("Cause of Death: Boundary Collision")
            lost = True
            head_x_change = 0
            head_y_change = 0
            choice_made = False
            game_over()

    # pygame update loop
    pygame.display.update()
    clock.tick(FPS)
