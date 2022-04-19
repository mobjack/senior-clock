
import os
import requests
import shutil
import pygame
import pendulum

from calendar import monthcalendar, setfirstweekday
from tracemalloc import start
from turtle import back
from copy import deepcopy


pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 192, 203)
GREEN = (0, 156, 76)
GREY = (169, 169, 169)
CORAL = (240, 128, 128)

FPS = 1
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

ZONE1_FONT = pygame.font.SysFont('rockwell', 80)

CAL_LEVEL = 300
CAL_POS_SPACE = 54
CAL_LEVEL_SPACE = 35
CALBOX_W = int(WIDTH * .45)
CALBOX_H = int(WIDTH * .35)
CALBOARDER = pygame.Rect(10, CAL_LEVEL, CALBOX_W, CALBOX_H)
CAL_MONTH_FONT = pygame.font.SysFont('rockwell', 30)
CAL_DAY_FONT = pygame.font.SysFont('rockwell', 17)
CAL_X_DAY_FONT = pygame.font.SysFont('rockwell', 15)

BACKGROUNDS = 'backgrounds'
BACKGROUND_URL = 'https://senior-clock.leewardbracket.com'


def get_grid(dt, col, level):
    setfirstweekday(6)  # usa first day is sun
    start_col = deepcopy(col)
    year = int(dt.format('YYYY'))
    month = int(dt.format('M'))
    weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    month_layout = monthcalendar(year, month)

    grid = []

    for weekday in weekdays:
        grid.append([weekday, (col, level)])
        col = col + CAL_POS_SPACE

    for month_week in month_layout:
        col = start_col  # new line in cal
        level = level + CAL_LEVEL_SPACE  # next row for date
        for date in month_week:

            if date != 0:
                grid.append([str(date), (col, level)])
            col = col + CAL_POS_SPACE

    return(grid)


def get_weather():
    return({'temp': 80})


def pull_background(image_file):
    print(f'pulling file {image_file}')
    download_file = os.path.join(BACKGROUNDS, image_file)
    pull_url = f'{BACKGROUND_URL}/{image_file}'
    print(pull_url)
    res = requests.get(pull_url, stream=True)
    if res.status_code == 200:
        with open(download_file, 'wb') as df:
            shutil.copyfileobj(res.raw, df)
        return(True)
    else:
        return(False)


def display_calendar(now, textcolor):
    month = now.format('MMMM')
    year = now.format('YYYY')
    today_date = int(now.format('D'))
    pygame.draw.rect(WINDOW, WHITE, CALBOARDER)

    cal_moyr = CAL_MONTH_FONT.render(f'{month}/{year}', 1, textcolor)
    month_level = CAL_LEVEL + 5
    WINDOW.blit(cal_moyr, (100, month_level))

    cal_pos = 13
    cal_level = month_level + CAL_LEVEL_SPACE
    cal_grid = get_grid(now, cal_pos, cal_level)

    for gridcord in cal_grid:

        if len(gridcord[0]) < 3:
            if int(gridcord[0]) < today_date:
                if len(gridcord[0]) == 2:
                    xdate = CAL_X_DAY_FONT.render('xx', 1, CORAL)
                else:
                    xdate = CAL_X_DAY_FONT.render('x', 1, CORAL)
                WINDOW.blit(xdate, gridcord[1])
                calinfo = CAL_DAY_FONT.render(gridcord[0], True, textcolor)
                WINDOW.blit(calinfo, gridcord[1])
            else:
                today_info = CAL_DAY_FONT.render(gridcord[0], True, GREEN)
                WINDOW.blit(today_info, gridcord[1])
        else:
            dayinfo = CAL_DAY_FONT.render(gridcord[0], True, textcolor)
            WINDOW.blit(dayinfo, gridcord[1])

    pygame.display.update()


def display_time(now, textcolor):

    dayofweek = now.format('dddd')
    date = now.format('LL')
    time = now.format('LT')
    hour = int(now.format('H'))
    minute = int(now.format('m'))

    background_file = ""
    if hour in range(7, 10):
        background_file = 'morning.jpg'
    elif hour in range(10, 19):
        background_file = 'day.jpg'
    elif hour in range(19, 20):
        background_file = 'evening.jpg'
    elif hour in range(20, 24):
        background_file = 'night.jpg'
    elif hour in range(0, 7):
        background_file = 'night.jpg'
    else:
        background_file = 'ocean.jpg'

    background_path = os.path.join(BACKGROUNDS, background_file)
    if not os.path.exists(background_path):
        pull_bg = pull_background(background_file)
        if pull_bg == False:
            background_file = 'ocean.jpg'

    background = pygame.transform.scale(pygame.image.load(
        os.path.join('backgrounds', background_file)), (WIDTH, HEIGHT))

    WINDOW.blit(background, (0, 0))

    zone1_text = ZONE1_FONT.render(dayofweek, 1, textcolor)
    zone2_text = ZONE1_FONT.render(date, 1, textcolor)
    zone3_text = ZONE1_FONT.render(time, 1, textcolor)

    WINDOW.blit(zone1_text, (10, 10))
    WINDOW.blit(zone2_text, (10, 100))
    WINDOW.blit(zone3_text, (10, 200))

    pygame.display.update()


def main():
    gameclock = pygame.time.Clock()
    pygame.display.set_caption('Clock')

    clockrun = True
    while clockrun:
        delay_seconds = 10
        gameclock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                clockrun = False
                pygame.quit()

        now = pendulum.now()
        display_time(now, WHITE)
        display_calendar(now, GREY)
        # waitdelay = int(delay_seconds * 1000)
        # pygame.time.wait(waitdelay)
        pygame.time.wait(delay_seconds)


if __name__ == main():
    main()
