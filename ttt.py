import pygame
import sys
import os
import requests
import math


LAT_STEP = 0.008
LON_STEP = 0.02
coord_to_geo_x = 0.0000428
coord_to_geo_y = 0.0000428


class MapParams(object):
    def __init__(self):
        self.lat = 55.729738
        self.lon = 37.664777
        self.zoom = 15
        self.type = "map"
        self.pos = None
        self.use_postal_code = False
        self.pt = None
        self.text_to_print = ''
        self.geocode = None

    def ll(self):
        return ll(self.len, self.lat)

    def update(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
            if self.zoom < 17:
                self.zoom += 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
            if self.zoom > 0:
                self.zoom -= 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if self.lat + self.screen_to_geo()[1] < 85:
                self.lat += self.screen_to_geo()[1]
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if self.lat - self.screen_to_geo()[1] > -85:
                self.lat -= self.screen_to_geo()[1]
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if self.lon - self.screen_to_geo()[0] > -180:
                self.lon -= self.screen_to_geo()[0]
            else:
                self.lon -= self.screen_to_geo()[0]
                self.lon += 360
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if self.lon + self.screen_to_geo()[0] < 180:
                self.lon += self.screen_to_geo()[0]
            else:
                self.lon += self.screen_to_geo()[0]
                self.lon -= 360
        if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            if self.type == "sat,skl":
                self.type = "sat"
            elif self.type == "sat":
                self.type = "map"
            elif self.type == "map":
                self.type = "sat,skl"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.geocode = None
            self.pos = event.pos
            lon, lat = self.pos_to_geo(self.pos)
            self.pt = "&pt=" + ','.join([str(lon), str(lat), "pm2rdl"])
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
            self.pt = None
            self.text_to_print = ''
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.use_postal_code:
                self.use_postal_code = False
            else:
                self.use_postal_code = True
            self.pos_to_geo(self.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            search_api_server = "https://search-maps.yandex.ru/v1/"
            api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
            self.pos = event.pos
            lon1, lat1 = self.pos_to_geo(self.pos)
            address_ll = "{},{}".format(lon1,lat1)
            geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&format=json".format(address_ll)
            response = requests.get(geocoder_request)
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]            
            search_params = {
                "apikey": api_key,
                "text": toponym_address,
                "lang": "ru_RU",
                "ll": address_ll,
                "type": "biz",
                "rspn": 1
            }
            response = requests.get(search_api_server, params=search_params)
    
            json_response = response.json()
            organization = json_response["features"][0]
            org_name = organization["properties"]["CompanyMetaData"]["name"]
            point = organization["geometry"]["coordinates"]
            x1, x2, y1, y2 = lon1 * 111, point[0] * 111, lat1 * 111, point[1] * 111
            if ((x2 - x1)**2 + (y2 - y1)**2)**(1 / 2) < 50:
                self.text_to_print = org_name
            else:
                self.text_to_print = ''

    def screen_to_geo(self):
        dx = 600 * coord_to_geo_x * math.pow(2, 15 - self.zoom)
        dy = 450 * coord_to_geo_y * math.cos(math.radians(self.lat)) * math.pow(2, 15 - self.zoom)
        return dx, dy

    def pos_to_geo(self, pos):
        dy = 225 - pos[1]
        dx = pos[0] - 300
        lx = self.lon + dx * coord_to_geo_x * math.pow(2, 15 - self.zoom)
        ly = self.lat + dy * coord_to_geo_y * math.cos(math.radians(self.lat)) * math.pow(2, 15 - self.zoom)
        if self.geocode is None:
            self.geocode = ('{},{}').format(lx, ly)
        geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&format=json".format(self.geocode)
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            try:
                toponym_index = ', ' + toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
            except Exception as e:
                toponym_index = ''
            self.text_to_print = toponym_address
            if self.use_postal_code:
                self.text_to_print += toponym_index
        return lx, ly


def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&z={}&l={}".format(mp.lon, mp.lat, mp.zoom, mp.type)
    if mp.pt:
        map_request += mp.pt
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса")
        print(map_request)
        print("Http статус:"), response.status_code, "(", response.reason, ")"
        sys.exit(1)
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла")
        sys.exit(2)
    return map_file


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = MapParams()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        mp.update(event)
        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        myfont = pygame.font.SysFont('Arial', 16)
        textsurface = myfont.render(mp.text_to_print, True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 600, 20))        
        screen.blit(textsurface,(0,0))
        pygame.display.flip()

    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()