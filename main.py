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
import wilma

#wilma.auth()
#wilma.get_schedule()

pygame.init()
pygame.font.init()

pygame.display.set_caption('KIDUTUS KELLO!!!')
with open("config.json", "r") as file:
    filecontent = file.read()
    config = json.loads(filecontent)
with open("homework.json", "r") as file:
    laksyt = json.loads(file.read())

    

screen = pygame.display.set_mode((1500, 1080), pygame.RESIZABLE)
clock = pygame.time.Clock()


beep = pygame.mixer.Sound("Sounds/boom.mp3")


clocktick = 5
songplaying = False

button_off =  pygame.transform.scale(pygame.image.load("images/textures/button_off.png"), (100,100))
button_on = pygame.transform.scale(pygame.image.load("images/textures/button_on.png"), (100,100))

kidutuskello = True
lukemiskello = False
normikello = False

with open("aikataulu.json", "r") as file:
    aikataulu = json.loads(file.read())

# different screens

def renderTextCenteredAt(text, font, colour, x, y, screen, allowed_width):
    # first, split the text into words
    words = text.split()

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    # now we've split our text into lines that fit into the width, actually
    # render them

    # we'll render each line below the last, so we need to keep track of
    # the culmative height of the lines we've rendered so far
    y_offset = 0
    y_margin = 5
    for line in lines:
        fw, fh = font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = x - fw / 2
        ty = y + y_offset

        font_surface = font.render(line, True, colour)
        font_surface_rect = font_surface.get_rect(topleft=(tx, ty))
        screen.blit(font_surface, font_surface_rect)
        #pygame.display.update(objects_to_update)

        y_offset += fh + y_margin

def kidutusKello():
    global timedingdong2, timedingdong, backround, frames, config, aikataulu
    fontsize = ((screen.get_width()) // 100) * ((screen.get_height() // 100)) - 25
    fontsize1 = (((screen.get_width()) // 100) * ((screen.get_height() // 100)) * 10) // 25
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
    

    



    kidutus = "Koulu"
    x = aikataulu["schedule"]
    aikataulupaivan = x[day]
    print(aikataulupaivan)

    for count, aikat in enumerate(aikataulupaivan):
        kidutus = aikataulupaivan[count-1]["tunti"]
        timestime = aikat["tunninalku"]
        
        time_1 = datetime.strptime(timestime, "%H:%M:%S")
        time_2 = datetime.strptime(currtime, "%H:%M:%S")
        
        currtime22 = int(currtime.replace(":", ""))
        i2 = int(timestime.replace(":", ""))
        
        if i2 - currtime22 > 0:
            print(i2 - currtime22)
            break
            
        else:
            
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
            
            sec = sec % (24 * 3600)
            hours = sec // 3600
            sec %= 3600
            minutes = sec // 60

            sec %= 60
            seconds = sec
            return hours, minutes, seconds
        
        hours, minutes, seconds = convert(int(tdelta))
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
        
        if int(i2) - int(currtime22) > 0:
            tuntiloppuusurface = myfont.render(
                str(hours) + str(hourtext) + str(minutes) + str(minutetext) + str(seconds) + "S!", False,
                tuple(map(int, config["textColor"].split(', '))))

        if seconds <= 1:
            pass

    except BaseException as e:
        print(e)
        pass
    currtimesurface_rect = currtimesurface.get_rect(center=(
        (screen.get_width() / 2) / 1.25, screen.get_height() / 2 - 80 * (fontsize / 50)))
    currdatesurface_rect = currdatesurface.get_rect(
        center=((screen.get_width() / 2) / 1.25, screen.get_height() / 2 - 50))
    try:
        tuntiloppuusurface_rect = tuntiloppuusurface.get_rect(
            center=((screen.get_width() / 2) / 1.25, screen.get_height() / 1.2))

        if minutes:
            if seconds > -1:
                if kidutus.lower() == "valkka" or kidutus.lower() == "ruokailu":
                    kidutussurface = myfont1.render(str(kidutus) + " Nauttimus loppuu:",
                                                    False, tuple(map(int, config["textColor"].split(', '))))
                elif kidutus.lower() == "historian":
                    kidutussurface = myfont1.render(
                        "Pasin jumaluus loppuu:", False, tuple(map(int, config["textColor"].split(', '))))

                else:
                    renderTextCenteredAt(str(kidutus) + " Opintokokemus loppuu:", myfont1, tuple(map(int, config["textColor"].split(', '))), (screen.get_width() / 2) / 1.25, screen.get_height()/1.7, screen, screen.get_width()-10)

    except BaseException:
        pass
    try:
        kidutussurface_rect = kidutussurface.get_rect(
            center=((screen.get_width() / 2) / 1.25, screen.get_height() / 2 + 75))
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
                            blinkingsurface = myfont.render("Opintokokemus loppui :(", False, tuple(map(
                                int, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))))
                            blinkingsurface_rect = blinkingsurface.get_rect(
                                center=(screen.get_width() / 2, screen.get_height() / 1.7 + 220))

                            screen.blit(blinkingsurface, blinkingsurface_rect)
            else:
                if seconds:
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
    
    tz = pytz.timezone('Europe/Helsinki')
    global backroundpic, config, timestarted, beep, breaktime, laksyt
    backroundpic = config["bgImage"]
    fontsize = ((screen.get_width()) // 100) * ((screen.get_height() // 100))
    fontsize1 = ((screen.get_width()) // 100) + ((screen.get_height() // 100)) * 5
    fontsize2 = ((screen.get_width()) // 100) + ((screen.get_height() // 100)) * 2
    
    try:
        myfont = pygame.font.Font('fonts/' + config["font"], fontsize)
        myfont1 = pygame.font.Font('fonts/' + config["font"], fontsize1)
        myfont2 = pygame.font.Font('fonts/' + config["font"], fontsize2)
    except BaseException:
        myfont = pygame.font.SysFont("Roboto", fontsize)
        myfont1 = pygame.font.SysFont('Roboto', fontsize1)
        myfont2 = pygame.font.SysFont('Roboto', fontsize2)
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
    currdate = datetime.now().astimezone(tz).strftime('%d.%m.%Y')
    
    print(currdate)
    print(studytime)
    if round(timestarted + studytime * 60) == round(datetime.today().timestamp()):
        breaktime = not breaktime
        if breaktime: beep.play()
        else: beep.play()
        print(breaktime)
        timestarted = datetime.today().timestamp()
    
    

    timertime = convert(hehehahaa) 
    
    timer = myfont.render(
        str(timertime), False, tuple(map(int, config["textColor"].split(', '))))
    screen.blit(timer, ((screen.get_width()/2 - 80 * (fontsize / 50)) / 1.25, (screen.get_height() - 100) - 80 * (fontsize / 50)))
    
    pygame.draw.rect(screen, (14, 49, 56), pygame.Rect(10, 10, screen.get_width()/2, screen.get_height()/2), 0, 10)
    #pygame.draw.rect(screen, (14, 49, 56), pygame.Rect(screen.get_width()/3, 10, screen.get_width()/4, screen.get_height()/2), 0, 10)
    renderTextCenteredAt("Kotitehtävät", myfont2, tuple(map(int, config["textColor"].split(', '))), round(screen.get_width()//2.2 - screen.get_width()//4.5), 20, screen, round(screen.get_width()//3 - screen.get_width()//4))
    ok = 0
    for homework in laksyt["laksyt"]:
        
        if homework["aine"] in laksyt["huomisen_tunnit"]:
            if (datetime.strptime(homework["paivamaara"], "%d.%m.%Y") - datetime.strptime(currdate, "%d.%m.%Y")).days == 0 and (datetime.strptime(homework["paivamaara"], "%d.%m.%Y") - datetime.strptime(currdate, "%d.%m.%Y")).days < 7:
                ok += 1
                aine = homework["aine"]
                paivamaara = homework["paivamaara"]
                tehtavat = homework["tehtavat"]
                massiivisenkokoinenonisabellaporrerinjuomapullo = f"{aine}: {tehtavat} / {paivamaara}"
                renderTextCenteredAt(massiivisenkokoinenonisabellaporrerinjuomapullo, myfont2, tuple(map(int, config["textColor"].split(', '))), round(screen.get_width()//2.2 - screen.get_width()//4.7), ok * (screen.get_height()//20 + screen.get_width()//20), screen, 600)
                

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
