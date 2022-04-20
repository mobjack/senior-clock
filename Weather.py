
import os
import json
from pendulum import local
from requests import request
from ImagePull import pullimage


class Weather():

    def __init__(self, config_file):
        self.wnow = {}
        with open(config_file) as ac:
            config = json.load(ac)

        self.url = config['weather']['url']
        self.lat = config['weather']['lat']
        self.lon = config['weather']['lon']
        self.key = config['weather']['key']
        self.exclude = config['weather']['exclude']
        self.units = config['weather']['units']
        self.icon_url = config['weather']['icon_url']
        self.images = config['weather']['image_location']

    def all_weather(self):
        '''Returns all weather details'''
        url = f'{self.url}?lat={self.lat}&lon={self.lon}&appid={self.key}&units={self.units}&exclude={self.exclude}'
        payload = {}
        headers = {}

        self.wnow = request("GET", url, headers=headers, data=payload)

        return(self.wnow.json())

    def get_temps(self):
        '''Returns current, high and low temps'''
        if not self.wnow:
            self.wnow = self.all_weather()

        current_temp = int(self.wnow['current']['temp'])
        high_temp = int(self.wnow['daily'][0]['temp']['max'])
        low_temp = int(self.wnow['daily'][0]['temp']['min'])

        return({'current_temp': current_temp, 'high': high_temp, 'low': low_temp})

    def get_sky(self):
        '''Return the current sky details'''
        if not self.wnow:
            self.wnow = self.all_weather()

        sky = self.wnow['current']['weather'][0]
        return({'sky': sky})

    def get_sky_icon(self):
        '''Open weather map icon'''
        if not self.wnow:
            self.wnow = self.all_weather()

        api_icon = self.wnow['current']['weather'][0]['icon']
        local_file = f'{api_icon}.png'
        local_file_path = os.path.join('backgrounds', local_file)

        if not os.path.exists(local_file_path):
            api_file = f'{api_icon}@2x.png'
            pullimage(self.icon_url, api_file, local_file, self.images)

        return({'filepath': os.path.join(self.images, local_file)})

    def get_calendar_weather(self):
        tt = self.get_temps()
        tt.update(self.get_sky())
        tt.update(self.get_sky_icon())
        return(tt)
