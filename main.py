import pygame
import random
import sys
import os
import requests
import json


###èñêóñâåíûé èíòèëåê
API_KEY = 'e18673a2a0374788b0c52b8d8af47588'
ENDPOINT = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/ocr'
DIR = 'imgs'

   

rashir=".jpg"
lang="ru"
def handler():
    text = ''
    for filename in sorted(os.listdir(DIR)):
        if filename.endswith(rashir): 
            pathToImage = '{0}/{1}'.format(DIR, filename)
            results = get_text(pathToImage)
            text += parse_text(results)
    return text

def parse_text(results):
    text = ''
    for region in results['regions']:
        for line in region['lines']:
            for word in line['words']:
                text += word['text'] + ' '
            text += '\n'
    return text  

def get_text(pathToImage):
    print('Processing: ' + pathToImage)
    headers  = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params   = {
        'language': lang,
        'detectOrientation ': 'true'
    }
    payload = open(pathToImage, 'rb').read()
    response = requests.post(ENDPOINT, headers=headers, params=params, data=payload)
    results = json.loads(response.content)
    return results
###èñêóñâåíûé èíòèëåê





def new_map(lon, lat, napr):

    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&z={}&size=450,450&l={}".format(lon, lat, 13, "map")
   

    response = requests.get(map_request)
    if not response:
        print("Îøèáêà âûïîëíåíèÿ çàïðîñà")
        print(map_request)
        print("Http ñòàòóñ:"), response.status_code, "(", response.reason, ")"
        sys.exit(1)
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Îøèáêà çàïèñè âðåìåííîãî ôàéëà")
        sys.exit(2)
    return map_file


def load_image(name, colorkey=None):
    fullname = os.path.join("pictures/", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

def whyevent(x, y, new):
    if x > 370 and x < 438 and y > 450 + 15 and y < 450 + 90:
        return 'bin'
    elif x > 370 and x < 438 and y >  550 and y < 616:
        return 'create'  
    elif x > 370 and x < 438 and y > 650 and y < 713:
        return 'find'  
    elif x < 450 and y < 450 and new == 1:
        return 'pole'  
    elif x < 450 and y < 450 and new == 2:
        return 'bin'     
    
    
pygame.init()

screen = pygame.display.set_mode((450, 725))
pygame.display.set_caption("Leisure map")
pygame.display.set_icon(pygame.image.load("pictures/logogo.png"))



all_sprites = pygame.sprite.Group()
song_sprites = pygame.sprite.Group()
games_sprites = pygame.sprite.Group()
films_sprites = pygame.sprite.Group()
art_sprites = pygame.sprite.Group()


image = "map.png"

def new(x, y):
    poster = 1
    for i in all_sprites:
        if i.rect.x <= x and i.rect.x + 60 >= x and i.rect.y <= y and i.rect.y + 60 >= y:
            poster *= 0
        else:
            poster *= 1
    if poster == 0:
        return False
    else:
        return True

metka = load_image("geometka.png")
metka = pygame.transform.scale(metka, (60, 60))

sprite = pygame.sprite.Sprite()
sprite.image = metka
sprite.rect = sprite.image.get_rect() 
sprite.rect.x = -100000
sprite.rect.y = -100000

all_sprites.add(sprite)
song_sprites.add(sprite)
games_sprites.add(sprite)
films_sprites.add(sprite)
art_sprites.add(sprite)

m = 0

spisok = []
spi = []
met = 0
typ = 0
rect = 0
enter = 0

gamer = False

lon, lat = 37.616546, 55.740334

xx, yy = 0, 0

while gamer == False:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print(met)
            xx, yy = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            eve = whyevent(xx, yy, 0)
            print(eve)
            #screen.blit(metka, pygame.mouse.get_pos())
            print(pygame.mouse.get_pos())
            
            if xx > 18 and xx < 81 and yy > 482 and yy < 533:
                typ = 1
            if xx > 130 and xx < 220 and yy > 480 and yy < 526:
                typ = 2
            if xx > 27 and xx < 107 and yy > 590 and yy < 660:
                typ = 3
            if xx > 147 and xx < 221 and yy > 590 and yy < 660:
                typ = 4

            
            
            
            if whyevent(xx, yy, met) == 'pole': 
                if typ == 1:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = metka
                    sprite.rect = sprite.image.get_rect()            
                    films_sprites.add(sprite)
                    sprite.rect.x, sprite.rect.y = xx - 30, yy - 60  
                if typ == 2:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = metka
                    sprite.rect = sprite.image.get_rect()            
                    art_sprites.add(sprite)
                    sprite.rect.x, sprite.rect.y = xx - 30, yy - 60  
                if typ == 3:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = metka
                    sprite.rect = sprite.image.get_rect()            
                    song_sprites.add(sprite)
                    sprite.rect.x, sprite.rect.y = xx - 30, yy - 60  
                if typ == 4:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = metka
                    sprite.rect = sprite.image.get_rect()            
                    games_sprites.add(sprite)
                    sprite.rect.x, sprite.rect.y = xx - 30, yy - 60  
                met = 0
                typ = 0
            
            if whyevent(xx, yy, met) == 'bin':
                for i in all_sprites:                
                    if i.rect.x < xx and i.rect.x + 60 > xx and i.rect.y < yy and i.rect.y + 60 > yy:
                        i.kill()   
                        met = 0
                        
                        
                        
            if xx > 252 and xx < 333 and yy > 461 and yy < 544:
                #handler()
                if rect == 0:
                    rect = 1
                    enter = 1
                elif rect == 1:
                    rect = 0
                
                
                
                
            if eve == 'create':
                met = 1
            if eve == 'bin':
                met = 2                        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            lat += 0.01
            image = new_map(lon, lat, "up")
            for i in song_sprites: 
                i.rect.y += 103     
            for i in films_sprites: 
                i.rect.y += 103 
            for i in games_sprites: 
                i.rect.y += 103 
            for i in art_sprites: 
                i.rect.y += 103 
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            lat -= 0.01
            image = new_map(lon, lat, "down")
            for i in song_sprites: 
                i.rect.y -= 103     
            for i in films_sprites: 
                i.rect.y -= 103 
            for i in games_sprites: 
                i.rect.y -= 103 
            for i in art_sprites: 
                i.rect.y -= 103 
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            lon -= 0.01
            image = new_map(lon, lat, "left")
            for i in song_sprites: 
                i.rect.x += 58    
            for i in films_sprites: 
                i.rect.x += 58 
            for i in games_sprites: 
                i.rect.x += 58 
            for i in art_sprites:    
                i.rect.x += 58
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            lon += 0.01
            image = new_map(lon, lat, "right")
            for i in song_sprites: 
                i.rect.x -= 58    
            for i in films_sprites: 
                i.rect.x -= 58 
            for i in games_sprites: 
                i.rect.x -= 58 
            for i in art_sprites:    
                i.rect.x -= 58            
            
        if event.type == pygame.QUIT:
            break

        

    if pygame.mouse.get_focused():
        '''pos = pygame.mouse.get_pos()
        kursor.rect.x = pos[0] - 42
        kursor.rect.y = pos[1] - 40
        '''
        pass
    
    screen.blit(pygame.image.load("map.png"), (0, 0))
    if xx > 18 and xx < 81 and yy > 482 and yy < 533 and eve == None:
        films_sprites.draw(screen)
    if xx > 130 and xx < 220 and yy > 480 and yy < 526 and eve == None:
        art_sprites.draw(screen)
    if xx > 27 and xx < 107 and yy > 590 and yy < 660 and eve == None:
        song_sprites.draw(screen)
    if xx > 147 and xx < 221 and yy > 590 and yy < 660 and eve == None:
        games_sprites.draw(screen)
    
    if rect == 1:
        pygame.draw.rect(screen, (255, 139, 62), (0, 0, 450, 450))
        
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render("ÌÓÇÅÉ ÈÇÎÁÐÀÇÈÒÅÏÜÍÜÆ", False, (0, 0, 0))
        screen.blit(textsurface,(0,0))   
        
        myfont1 = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface1 = myfont1.render("ÊÎËËÅÊÒÈÂÍÀß ÂÛÑÒÀÂÊÀ", False, (0, 0, 0))
        screen.blit(textsurface1,(0,70)) 
        
        myfont2 = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface2 = myfont2.render("22 ÀÂÃÓÑÒÀ - 27 ÑÅÍÒßÁÐß", False, (0, 0, 0))
        
        screen.blit(textsurface2,(0,140)) 
           
        if enter == 1:
            print(handler())
            handled_str = handler()
            c = len(handled_str)
            i = 0
            str_y, str_x = 10, 10
            while i < c:
                myfont = pygame.font.SysFont('Comic Sans MS', 30)
                textsurface = myfont.render(handled_str[i], False, (0, 0, 0))
                screen.blit(textsurface,(str_x,str_y))
                str_x += 5
                if i % 10 == 0:
                    str_y += 20
                i += 1
            
        enter = 0
    pygame.draw.rect(screen, (255, 204, 0), (0, 450, 450, 450))
    screen.blit(pygame.image.load("pictures/buttons.png"), (0, 450))
    
    
    
    pygame.display.flip()

pygame.quit()

