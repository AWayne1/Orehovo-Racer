import pygame
import random
import sys
import time
from pygame.locals import *
import os

screen_width = 800
screen_height = 600
txt_c = (255, 255, 0)
bckg_c = (0, 0, 0)
FPS = 60
minimum_size_car = 10
maximum_size_car = 40
minimum_speed_car = 8
maximum_speed_car = 8
new_rate_car_added = 6
pl_movement_rate = 5
counting_seconds = 3


def Exit():
    pygame.quit()
    sys.exit()


def Press_Key_shortcut():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                Exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Exit()
                return


def player_crash(pl_crashRect, opponent):
    for ado in opponent:
        if pl_crashRect.colliderect(ado['rect']):
            return True
    return False


def txt_objects(t, f, s, x, y):
    txt_objects = f.render(t, 1, txt_c)
    txt_Rect = txt_objects.get_rect()
    txt_Rect.topleft = (x, y)
    s.blit(txt_objects, txt_Rect)


pygame.init()
time_clock = pygame.time.Clock()
screen_display_window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Orehovo Race')
pygame.mouse.set_visible(False)
fontsize = pygame.font.SysFont(None, 30)
player_car_photo = pygame.image.load('images/player_photo.png')
computer_car3 = pygame.image.load('images/car1.png')
computer_car4 = pygame.image.load('images/car2.png')
gamer_Rect = player_car_photo.get_rect()
computer_car_photo = pygame.image.load('images/car3.png')
another = [computer_car3, computer_car4, computer_car_photo]
w_left = pygame.image.load('images/left_side.png')
w_right = pygame.image.load('images/right_side.png')

txt_objects('Чтобы начать - нажмите любую кнопку', fontsize, screen_display_window,
            (screen_width / 3) - 30, (screen_height / 3))
txt_objects('Удачи!', fontsize, screen_display_window,
            (screen_width / 3), (screen_height / 3) + 30)
pygame.display.update()
Press_Key_shortcut()
zero = 0
if not os.path.exists("datafile/save.dat"):
    ado = open("datafile/save.dat", 'w')
    ado.write(str(zero))
    ado.close()
datafile = open("datafile/save.dat", 'r')
highest_scores = int(datafile.readline())
datafile.close()
while (counting_seconds > 0):
    opponent = []
    score = 0
    gamer_Rect.topleft = (screen_width / 2, screen_height - 50)
    moving_left = moving_right = moving_up = moving_down = False
    counter_reverse = slowing_reverse = False
    adding_counter_opponent = 0

    while True:
        score += 1

        for event in pygame.event.get():

            if event.type == QUIT:
                Exit()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    counter_reverse = True
                if event.key == ord('x'):
                    slowing_reverse = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moving_right = False
                    moving_left = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moving_left = False
                    moving_right = True
                if event.key == K_UP or event.key == ord('w'):
                    moving_down = False
                    moving_up = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moving_up = False
                    moving_down = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    counter_reverse = False
                    score = 0
                if event.key == ord('x'):
                    slowing_reverse = False
                    score = 0
                if event.key == K_ESCAPE:
                    Exit()

                if event.key == K_LEFT or event.key == ord('a'):
                    moving_left = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moving_right = False
                if event.key == K_UP or event.key == ord('w'):
                    moving_up = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moving_down = False

        if not counter_reverse and not slowing_reverse:
            adding_counter_opponent += 1
        if adding_counter_opponent == new_rate_car_added:
            adding_counter_opponent = 0
            computer_car_size = 30
            new_computer_car = {'rect': pygame.Rect(random.randint(140, 485), 0 - computer_car_size, 23, 47),
                                'speed': random.randint(minimum_speed_car, maximum_speed_car),
                                'surface': pygame.transform.scale(random.choice(another), (23, 47)),
                                }
            opponent.append(new_computer_car)
            left_side = {'rect': pygame.Rect(0, 0, 126, 600),
                         'speed': random.randint(minimum_speed_car, maximum_speed_car),
                         'surface': pygame.transform.scale(w_left, (126, 599)),
                         }
            opponent.append(left_side)
            right_side = {'rect': pygame.Rect(497, 0, 303, 600),
                          'speed': random.randint(minimum_speed_car, maximum_speed_car),
                          'surface': pygame.transform.scale(w_right, (303, 599)),
                          }
            opponent.append(right_side)

        if moving_left and gamer_Rect.left > 0:
            gamer_Rect.move_ip(-1 * pl_movement_rate, 0)
        if moving_right and gamer_Rect.right < screen_width:
            gamer_Rect.move_ip(pl_movement_rate, 0)
        if moving_up and gamer_Rect.top > 0:
            gamer_Rect.move_ip(0, -1 * pl_movement_rate)
        if moving_down and gamer_Rect.bottom < screen_height:
            gamer_Rect.move_ip(0, pl_movement_rate)

        for car in opponent:
            if not counter_reverse and not slowing_reverse:
                car['rect'].move_ip(0, car['speed'])
            elif counter_reverse:
                car['rect'].move_ip(0, -5)
            elif slowing_reverse:
                car['rect'].move_ip(0, 1)

        for car in opponent[:]:
            if car['rect'].top > screen_height:
                opponent.remove(car)

        screen_display_window.fill(bckg_c)

        txt_objects('Счет: %s' % (score), fontsize, screen_display_window, 128, 0)
        txt_objects('Лучший счет: %s' % (highest_scores), fontsize, screen_display_window, 128, 20)
        txt_objects('Ваши жизни: %s / 3' % (counting_seconds), fontsize, screen_display_window, 128, 40)

        screen_display_window.blit(player_car_photo, gamer_Rect)

        for car in opponent:
            screen_display_window.blit(car['surface'], car['rect'])

        pygame.display.update()

        if player_crash(gamer_Rect, opponent):  # Лучший рекорд
            if score > highest_scores:
                g = open("datafile/save.dat", 'w')
                g.write(str(score))
                g.close()
                highest_scores = score
            break

        time_clock.tick(FPS)

    counting_seconds = counting_seconds - 1
    if (counting_seconds == 0):
        txt_objects('Игра окончена', fontsize, screen_display_window, (screen_width / 3), (screen_height / 3))
        txt_objects('Нажмите любую клавишу для начала игры', fontsize, screen_display_window, (screen_width / 3) - 80,
                    (screen_height / 3) + 30)
        pygame.display.update()
        time.sleep(2)
        Press_Key_shortcut()
        counting_seconds = 3
