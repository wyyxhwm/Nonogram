import numpy
import pygame
import json

class Interface:
    def __init__(self, window, json_name):
        self.window = window
        self.width, self.height = window.get_size()
        self.interface = "初始界面"
        with open(json_name, 'r', encoding='utf-8') as f:
            self.json = json.load(f)


    def draw(self):
        self.window.fill((227, 227, 227))
        for i in self.json['interface']:
            if i['Interface_name'] == self.interface:
                start_x = self.width // i['layout']['col_sum']
                start_y = i['layout']['start_y']
                for j in range(i['layout']['row_sum']):
                    x = len(i['buttons']['text']) * i['font_size']
                    y = i['font_size'] + j * i['font_size']
                    pygame.draw.rect(self.window,'black',(start_x, start_y, x, y), 1)



class Game:
    def __init__(self):
        pass


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    interface = Interface(window)
    interface.draw()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
