import pygame
import sys
import random
from pygame.math import Vector2


class Fruit:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos = Vector2(self.x, self.y)
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.x * cell_size, self.y * cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_num - 1)
        self.y = random.randint(0, cell_num - 1)
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.head = pygame.image.load("assets/head_right.png").convert_alpha()
        self.tail = pygame.image.load("assets/tail_left.png").convert_alpha()

        self.head_up = pygame.image.load("assets/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("assets/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("assets/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("assets/head_left.png").convert_alpha()

        self.tail_up = pygame.image.load("assets/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("assets/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("assets/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("assets/tail_left.png").convert_alpha()

        self.body_vertical = pygame.image.load("assets/body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("assets/body_horizontal.png").convert_alpha()

        self.body_tr = pygame.image.load("assets/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("assets/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("assets/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("assets/body_bl.png").convert_alpha()
        self.crunch_sound = pygame.mixer.Sound("assets/crunch.wav")

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body)-1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index+1] - block
                next_block = self.body[index -1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def move_snake(self):
        if self.new_block:
            self.add_block()
        else:
            body_copy = self.body[:-1]  # only the first and second
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        body_copy = self.body[:]  # only the first and second
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]
        self.new_block = False

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        if head_relation == Vector2(-1, 0):
            self.head = self.head_right
        if head_relation == Vector2(0, 1):
            self.head = self.head_up
        if head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        if tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        if tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        if tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(4, 10)]


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.new_block = True
            self.snake.play_crunch_sound()

    def game_over(self):
        self.snake.reset()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_num or not 0 <= self.snake.body[0].y < cell_num:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_num):
            if row % 2 == 0:
                for col in range(cell_num):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size , cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_num):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size , cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        welcome_str = "maya's snake game"
        score_text = str((len(self.snake.body)-3) * 10)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        welcome_surface = game_font.render(welcome_str, True, (56, 74, 12))
        welcome_x = int(cell_num * cell_size - 130)  # bit to the let
        welcome_y = int(cell_num * cell_size - 60)  # a bit up
        score_x = int(cell_num * cell_size - 80)  # bit to the let
        score_y = int(cell_num * cell_size - 30)  # a bit up
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        welcome_rect = welcome_surface.get_rect(center=(welcome_x, welcome_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        screen.blit(score_surface, score_rect)
        screen.blit(welcome_surface, welcome_rect)
        screen.blit(apple, apple_rect)


pygame.init()
cell_num = 20
cell_size = 40
screen = pygame.display.set_mode((cell_num * cell_size, cell_num * cell_size))
pygame.display.set_caption('snake')
logo_surface = pygame.image.load("assets/head_up.png")
pygame.display.set_icon(logo_surface)

clock = pygame.time.Clock()
apple = pygame.image.load("assets/apple.png").convert_alpha()
game_font = pygame.font.Font("assets/PoetsenOne-Regular.ttf", 25)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_grass()
    main_game.draw_elements()
    main_game.check_collision()
    main_game.check_fail()
    pygame.display.update()
    clock.tick(60)
