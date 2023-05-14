import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque

# 基础设置
Screen_Height = 480
Screen_Width = 600
Size = 20  # 小方格大小
Line_Width = 1

# 游戏区域的坐标范围
Area_x = (0, Screen_Width // Size - 1)  # 0是左边界，1是右边界
Area_y = (2, Screen_Height // Size - 1)

# 食物的初步设置
# 食物的分值+颜色
Food_Style_List = [(10, (255, 100, 100)), (20, (100, 255, 100)), (30, (100, 100, 255))]

# 整体颜色设置
Light = (100, 100, 100)
Dark = (200, 200, 200)
Black = (0, 0, 0)
Red = (200, 30, 30)
Back_Ground = (40, 40, 60)

# 文本输出格式设置
def Print_Txt(screen, font, x, y, text, fcolor=(255, 255, 255)):
    Text = font.render(text, True, fcolor)
    screen.blit(Text, (x, y))

# 初始化蛇
def init_snake():
    snake = deque()
    snake.append((2, Area_y[0]))
    snake.append((1, Area_y[0]))
    snake.append((0, Area_y[0]))
    return snake

# 食物设置
# 注意需要根据蛇的位置生成新的食物
def set_food(snake):
    while True:
        food_x = random.randint(Area_x[0], Area_x[1])
        food_y = random.randint(Area_y[0], Area_y[1])
        if (food_x, food_y) not in snake:
            break
    return food_x, food_y

# 游戏结束
def game_over(screen):
    screen.fill(Back_Ground)
    font = pygame.font.Font(None, 60)
    Print_Txt(screen, font, 200, 200, 'Game Over', Red)
    pygame.display.update()
    time.sleep(3)
    sys.exit()

# 主函数
def main():
    pygame.init()
    screen = pygame.display.set_mode((Screen_Width, Screen_Height))
    pygame.display.set_caption('贪吃蛇')
    clock = pygame.time.Clock()

    snake = init_snake()  # 初始化蛇
    food_x, food_y = set_food(snake)  # 设置食物

    direction = K_RIGHT  # 蛇的初始移动方向向右

    score = 0  # 初始分数
    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    paused = not paused
                elif event.key in (K_UP, K_w) and direction != K_DOWN:
                    direction = K_UP
                elif event.key in (K_DOWN, K_s) and direction != K_UP:
                    direction = K_DOWN
                elif event.key in (K_LEFT, K_a) and direction != K_RIGHT:
                    direction = K_LEFT
                elif event.key in (K_RIGHT, K_d) and direction != K_LEFT:
                    direction = K_RIGHT

        if not paused:
            next_x, next_y = snake[0]
            if direction == K_UP:
                next_y -= 1
            elif direction == K_DOWN:
                next_y += 1
            elif direction == K_LEFT:
                next_x -= 1
            elif direction == K_RIGHT:
                next_x += 1

            if (
                next_x < Area_x[0]
                or next_x > Area_x[1]
                or next_y < Area_y[0]
                or next_y > Area_y[1]
                or (next_x, next_y) in snake
            ):
                game_over(screen)

            snake.appendleft((next_x, next_y))
            if next_x == food_x and next_y == food_y:
                score += 1
                food_x, food_y = set_food(snake)
            else:
                snake.pop()

        screen.fill(Back_Ground)

        for x, y in snake:
            pygame.draw.rect(
                screen, Light, (x * Size, y * Size, Size - Line_Width, Size - Line_Width)
            )

        pygame.draw.rect(
            screen,
            Food_Style_List[score % len(Food_Style_List)][1],
            (food_x * Size, food_y * Size, Size, Size),
        )

        font = pygame.font.Font(None, 40)
        Print_Txt(screen, font, 30, 10, f"Score: {score}")

        pygame.display.update()
        clock.tick(10)

if __name__ == '__main__':
    main()
