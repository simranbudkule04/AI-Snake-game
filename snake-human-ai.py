
import pygame
import random
from pygame.math import Vector2
import heapq

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SNAKE_SPEED = 5
APPLE_COUNT = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Directions
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)

class Node:
    def __init__(self, position):
        self.position = position
        self.g_cost = 0
        self.h_cost = 0
        self.parent = None

    def f_cost(self):
        return self.g_cost + self.h_cost

# A* algorithm
def astar(start, end, obstacles):
    open_set = []
    closed_set = set()

    start_node = Node(start)
    end_node = Node(end)

    heapq.heappush(open_set, (start_node.f_cost(), id(start_node), start_node))

    while open_set:
        current_node = heapq.heappop(open_set)[2]

        if current_node.position == end_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(tuple(current_node.position))  # Convert Vector2 to tuple

        for neighbor_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = current_node.position + Vector2(neighbor_pos)
            if neighbor.x < 0 or neighbor.x >= GRID_WIDTH or neighbor.y < 0 or neighbor.y >= GRID_HEIGHT:
                continue
            if neighbor in obstacles:
                continue

            neighbor_node = Node(neighbor)
            neighbor_node.g_cost = current_node.g_cost + 1
            neighbor_node.h_cost = neighbor_node.position.distance_to(end_node.position)
            neighbor_node.parent = current_node

            if tuple(neighbor_node.position) in closed_set:  # Convert Vector2 to tuple
                continue

            if any(neighbor_node.position == node.position for _, _, node in open_set):
                continue

            heapq.heappush(open_set, (neighbor_node.f_cost(), id(neighbor_node), neighbor_node))

    return None


class Snake:
    def __init__(self, color, start_pos):
        self.color = color
        self.body = [start_pos]
        self.direction = RIGHT

    def move(self, grow=False):
        new_head = self.body[0] + self.direction
        if grow:
            self.body.insert(0, new_head)
        else:
            self.body.insert(0, new_head)
            self.body.pop()

    def draw(self, screen):
        for block in self.body:
            rect = pygame.Rect(
                block.x * GRID_SIZE, block.y * GRID_SIZE, GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(screen, self.color, rect)

    def collide_with_self(self):
        positions = [tuple(segment) for segment in self.body]
        unique_positions = set(positions)
        return len(positions) != len(unique_positions)

    def collide_with_apple(self, apple_pos):
        return self.body[0] == apple_pos


class Apple:
    def __init__(self):
        self.position = self.randomize_position()

    def randomize_position(self):
        return Vector2(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, screen):
        rect = pygame.Rect(
            self.position.x * GRID_SIZE, self.position.y * GRID_SIZE, GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(screen, RED, rect)



class AI:
    def __init__(self, color, start_pos):
        self.color = color
        self.body = [start_pos]
        self.direction = Vector2(1, 0)

    def move(self, apple_pos, obstacles, grow=False):
        path = astar(self.body[0], apple_pos, obstacles)
        if path:
            next_position = path[1]  # Next position after the head
            dx = next_position.x - self.body[0].x
            dy = next_position.y - self.body[0].y
            self.direction = Vector2(dx, dy)

        new_head = self.body[0] + self.direction
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()

    def draw(self, screen):
        for block in self.body:
            rect = pygame.Rect(block.x * GRID_SIZE, block.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.color, rect)

    def collide_with_self(self):
        for i in range(1, len(self.body)):
            if self.body[i] == self.body[0]:
                return True
        return False

    def collide_with_apple(self, apple_pos):
        return self.body[0] == apple_pos

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game_over = False

    human_snake = Snake(WHITE, Vector2(5, GRID_HEIGHT // 2))
    ai_snake = AI(BLUE, Vector2(GRID_WIDTH - 5, GRID_HEIGHT // 2))
    apples = [Apple() for _ in range(APPLE_COUNT)]

    while not game_over:
        clock.tick(SNAKE_SPEED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and human_snake.direction != DOWN:
            human_snake.direction = UP
        elif keys[pygame.K_DOWN] and human_snake.direction != UP:
            human_snake.direction = DOWN
        elif keys[pygame.K_LEFT] and human_snake.direction != RIGHT:
            human_snake.direction = LEFT
        elif keys[pygame.K_RIGHT] and human_snake.direction != LEFT:
            human_snake.direction = RIGHT

        human_snake.move()
        ai_snake.move(apples[0].position, human_snake.body + ai_snake.body)

        for apple in apples[:]:
            if human_snake.collide_with_apple(apple.position):
                apples.remove(apple)
                apples.append(Apple())
                human_snake.move(grow=True)
                break

            if ai_snake.collide_with_apple(apple.position):
                apples.remove(apple)
                apples.append(Apple())
                ai_snake.move(apples[0].position, human_snake.body + ai_snake.body, grow=True)
                break

        if human_snake.collide_with_self() or ai_snake.collide_with_self():
            game_over = True

        screen.fill(GREEN)

        for apple in apples:
            apple.draw(screen)



        human_snake.draw(screen)
        ai_snake.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
