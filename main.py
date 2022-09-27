import pygame
from datetime import datetime
import pytz
import sys
import time
import random
import os
import requests
import shutil
import json

pygame.init()
pygame.font.init()

pygame.display.set_caption('KIDUTUS KELLO!!!')
with open("config.json", "r") as file:
    filecontent = file.read()

    config = json.loads(filecontent)

screen = pygame.display.set_mode((1500, 1080), pygame.RESIZABLE)
clock = pygame.time.Clock()


song = pygame.mixer.Sound("Sounds/TheFinalCountdown.wav")
breaktime_sound = pygame.mixer.Sound("Sounds/breaktime.wav")
breaktime_end = pygame.mixer.Sound("Sounds/studytime.wav")


clocktick = 5
songplaying = False

button_off =  pygame.transform.scale(pygame.image.load("images/textures/button_off.png"), (100,100))
button_on = pygame.transform.scale(pygame.image.load("images/textures/button_on.png"), (100,100))

kidutuskello = True
lukemiskello = False
normikello = False

# different screens
def kidutusKello():
    global timedingdong2, timedingdong, backround, frames, config
    fontsize = ((screen.get_width()) // 100) + \
        ((screen.get_height() // 100)) * 15
    fontsize1 = ((screen.get_width()) // 100) + \
        ((screen.get_height() // 100)) * 5
    timedingdong2 += 1

    if timedingdong2 >= timedingdong:
        if timedingdong != 0:
            timedingdong2 = 0
            change()
    backroundpic = config["bgImage"]

    
    try:
        myfont = pygame.font.Font('fonts/' + config["font"], fontsize)
        myfont1 = pygame.font.Font('fonts/' + config["font"], fontsize1)
    except BaseException:
        myfont = pygame.font.SysFont("Roboto", fontsize)
        myfont1 = pygame.font.SysFont('Roboto', fontsize1)
    try:
        backround = pygame.image.load(backroundpic)
        backround = pygame.transform.scale(
            backround, (screen.get_width(), screen.get_height()))
    except BaseException:
        pass
    try:
        screen.blit(backround, (0, 0))
    except BaseException:
        pass

    tz = pytz.timezone('Europe/Helsinki')
    currtime = datetime.now().astimezone(tz).strftime('%H:%M:%S')
    currdate = datetime.now().astimezone(tz).strftime('%Y-%m-%d')

    day = datetime.today().weekday()

    currtimesurface = myfont.render(
        str(currtime), False, tuple(map(int, config["textColor"].split(', '))))
    currdatesurface = myfont.render(
        str(currdate), False, tuple(map(int, config["textColor"].split(', '))))
    

    
    with open("aikataulu.txt", "r") as file:
        filecontent1 = file.read()

        filecontent1 = filecontent1.split("\n")

    times = []
    kidutus = "Koulu"
    x = filecontent1[day]
    x = x.split("|")
    daything = x[0]
    for i in x:
        if i != "":
            i = i.split("$")
            i1 = i
            i = i[0]

            i2 = i.replace(":", "")
            currtime22 = currtime.replace(":", "")
            if int(i2) - int(currtime22) > 0:
                times.append(str(i2) + "$" + kidutus)
                break
            try:
                kidutus = i1[1]
            except BaseException:
                pass

    times.sort()
    try:
        i = times[0]
        i = i.split("$")
        kidutus = i[1]
        timestime = i[0]

        timeshour = timestime[:2]
        timesminute = timestime[2:4]
        timessecond = timestime[4:6]

        timestime = timeshour + ":" + timesminute + ":" + timessecond
    except BaseException:
        pass
    try:
        time_1 = datetime.strptime(timestime, "%H:%M:%S")
        time_2 = datetime.strptime(currtime, "%H:%M:%S")

        tdelta = time_1 - time_2
        tdelta = tdelta.seconds
    except BaseException:
        pass
    try:
        def convert(sec):
            global hours, minutes, seconds
            sec = sec % (24 * 3600)
            hours = sec // 3600
            sec %= 3600
            minutes = sec // 60

            sec %= 60
            seconds = sec

        if int(i2) - int(currtime22) > 0:
            convert(int(tdelta))
    except Exception as e:
        print(e)
        pass
    try:

        if hours:
            hourtext = "H "

        else:
            hourtext = ""
            hours = ""
        if minutes:
            minutetext = "M "
        else:
            minutes = ""
            minutetext = ""
        if seconds:
            if int(i2) - int(currtime22) > 0:
                tuntiloppuusurface = myfont.render(
                    str(hours) + str(hourtext) + str(minutes) + str(minutetext) + str(seconds) + "S!", False,
                    tuple(map(int, config["textColor"].split(', '))))

        try:
            if seconds == 46:
                if not minutes:
                    if not songplaying:
                        if song:
                            songplaying = True
                            song.play()
                            print("Playing!")
            else:
                songplaying = False
        except BaseException:
            pass

        if seconds <= 1:
            pass

    except BaseException:
        pass
    currtimesurface_rect = currtimesurface.get_rect(center=(
        (screen.get_width() / 2) / 1.25, screen.get_height() / 2 - 80 * (fontsize / 50)))
    currdatesurface_rect = currdatesurface.get_rect(
        center=((screen.get_width() / 2) / 1.25, screen.get_height() / 2 - 50))
    try:
        tuntiloppuusurface_rect = tuntiloppuusurface.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2 + 220))

        if minutes:
            if seconds > 10:
                if kidutus.lower() == "valkka" or kidutus.lower() == "ruokailu":
                    kidutussurface = myfont1.render(str(kidutus) + " Nauttimus loppuu:",
                                                    False, tuple(map(int, config["textColor"].split(', '))))
                elif kidutus.lower() == "historian":
                    kidutussurface = myfont1.render(
                        "Pasin jumaluus loppuu:", False, tuple(map(int, config["textColor"].split(', '))))

                else:
                    kidutussurface = myfont1.render(str(kidutus) + " Kidutus loppuu:",
                                                    False, tuple(map(int, config["textColor"].split(', '))))

    except BaseException:
        pass
    try:
        kidutussurface_rect = kidutussurface.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2 + 75))
    except BaseException:
        pass

    screen.blit(currtimesurface, currtimesurface_rect)
    screen.blit(currdatesurface, currdatesurface_rect)
    try:
        if not hours:
            if not minutes:
                if seconds > 5:
                    screen.blit(tuntiloppuusurface, tuntiloppuusurface_rect)

                    screen.blit(kidutussurface, kidutussurface_rect)
                else:
                    if seconds > 2:
                        if (frames // 2) % 2 == 0:
                            blinkingsurface = myfont.render("TUNTI LOPPUI!", False, tuple(map(
                                int, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))))
                            blinkingsurface_rect = blinkingsurface.get_rect(
                                center=(screen.get_width() / 2, screen.get_height() / 2 + 220))

                            screen.blit(blinkingsurface, blinkingsurface_rect)
                    else:
                        song.stop()
            else:
                if seconds:
                    song.stop()
                    screen.blit(tuntiloppuusurface, tuntiloppuusurface_rect)

                    screen.blit(kidutussurface, kidutussurface_rect)

        else:
            screen.blit(tuntiloppuusurface, tuntiloppuusurface_rect)

            screen.blit(kidutussurface, kidutussurface_rect)

    except BaseException:
        pass

def lukemisKello():
    def convert(sec):
            sec = sec % (24 * 3600)
            hours = round(sec // 3600)
            sec %= 3600
            minutes = round(sec // 60)

            sec %= 60
            seconds = round(sec)
            
            return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    
    global backroundpic, config, timestarted, breaktime
    backroundpic = config["bgImage"]
    fontsize = ((screen.get_width()) // 100) + \
        ((screen.get_height() // 100)) * 15
    fontsize1 = ((screen.get_width()) // 100) + \
        ((screen.get_height() // 100)) * 5
    
    try:
        myfont = pygame.font.Font('fonts/' + config["font"], fontsize)
        myfont1 = pygame.font.Font('fonts/' + config["font"], fontsize1)
    except BaseException:
        myfont = pygame.font.SysFont("Roboto", fontsize)
        myfont1 = pygame.font.SysFont('Roboto', fontsize1)
    try:
        backround = pygame.image.load(backroundpic)
        backround = pygame.transform.scale(
            backround, (screen.get_width(), screen.get_height()))
    except BaseException:
        pass
    try:
        screen.blit(backround, (0, 0))
    except BaseException:
        pass
    
    
    if breaktime: studytime = 5
    else: studytime =  15
    print(studytime)
    
    hehehahaa = timestarted + studytime * 60 - datetime.today().timestamp()
    print(studytime)
    if round(timestarted + studytime * 60) == round(datetime.today().timestamp()):
        breaktime = not breaktime
        if breaktime: breaktime_sound.play()
        else: breaktime_end.play()
        print(breaktime)
        timestarted = datetime.today().timestamp()
    
    
        
    timertime = convert(hehehahaa) 
    
    timer = myfont.render(
        str(timertime), False, tuple(map(int, config["textColor"].split(', '))))
    screen.blit(timer, ((screen.get_width()/2 - 80 * (fontsize / 50)) / 1.25, (screen.get_height()/2.5) - 80 * (fontsize / 50)))

def change():
    global config, backround
    filename = ""
    if config["getImgFromInternet"]:
        r1 = requests.get(config["imgUrl"]).json()
        image_url = f"{r1[0]['url']}"
        prev_file = filename
        filename = image_url.split("/")[-1]

        r = requests.get(image_url, stream=True)

        if r.status_code == 200:
            r.raw.decode_content = True

            with open("images/wallpaper" + filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        images = os.listdir("images/wallpaper")
        try:
            if prev_file != "":
                os.remove("images/wallpaper/" + prev_file)
        except BaseException:
            pass

        config = config["bgImage"] = backround
    else:
        images = os.listdir("images/wallpaper")

        config = config["bgImage"] = backround



timedingdong = int(config["idk"]) * clocktick
timedingdong2 = 0

frames = 0

running = True
while running:
    clock.tick(clocktick)
    frames += 1
    screen.fill(tuple(map(int, config["bgColor"].split(', '))))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
            exit()
            pygame.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                change()
                timedingdong2 = 0
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if screen.get_width() / 1.10 <= mouse[0] <= screen.get_width() / 1.10 + 150 and 50 <= mouse[1] <= 150:
                kidutuskello = True
                lukemiskello = False
                normikello = False
            elif screen.get_width() / 1.10 <= mouse[0] <= screen.get_width() / 1.10 + 150 and 200 <= mouse[1] <= 300:
                kidutuskello = False
                lukemiskello = True
                normikello = False
            elif screen.get_width() / 1.10 <= mouse[0] <= screen.get_width() / 1.10 + 150 and 350 <= mouse[1] <= 450:
                kidutuskello = False
                lukemiskello = False
                normikello = True
    if kidutuskello: screen.blit(button_on, (screen.get_width() / 1.10, 50))
    else: screen.blit(button_off, (screen.get_width() / 1.10, 50))
    if lukemiskello:
        if not timestarted:
            timestarted = datetime.today().timestamp()
            breaktime = False
        print(timestarted)
        screen.blit(button_on, (screen.get_width() / 1.10, 200))
        
    else:
        timestarted = False
        breaktime = False
        screen.blit(button_off, (screen.get_width() / 1.10, 200))
    if normikello: screen.blit(button_on, (screen.get_width() / 1.10, 350))
    else: screen.blit(button_off, (screen.get_width() / 1.10, 350))

    if kidutuskello:
        kidutusKello()
    elif lukemiskello:
        lukemisKello()
    elif normikello:
        pass

    pygame.display.flip()
