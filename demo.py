#!/usr/bin/python3
#~*~ coding: utf-8 ~*~

import math, random # for demo

from OPyGame import Engine

class Main(Engine):
    def __init__(self):
        super().__init__('Demo OPG', 900,600, RESIZE=True)
        self.main_scene = DemoScene1 # Scene au demarage
        
    # Valeurs pour la démo uniquement #

        self.line = { 'x': self.display_size[0]/3,
                      'y': self.display_size[1]/2,
                      'w': 1, 'h': 1, 'p': [ random.randint(10,20), random.random() ],
                      'p_reverse': False, 'p_orig': None }

        self.line['p_orig'] = self.line['p'][0]
        
        self.pseudo_timer = 0
    
    def draw_black_bg(self):   # Black background
        self.opg.draw.rect(self.surface, (0,0,0), self.opg.Rect(0,0,self.display_size[0],self.display_size[1]))


class DemoScene1:
    
    def update(self):

        for event in self.events:
            if event.type == self.opg.MOUSEBUTTONUP:
                self.main_scene = DemoScene2

        self.line['x'] += math.sin(self.pseudo_timer)*self.line['p'][0]
        self.line['y'] += math.cos(self.pseudo_timer)*self.line['p'][0]

        if not self.line['p_reverse'] and self.line['p'][0] > 0:
            self.line['p'][0] -= self.line['p'][1]

        elif self.line['p_reverse'] and self.line['p'][0] < self.line['p_orig']:
            self.line['p'][0] += self.line['p'][1]

        else:
            self.line['p_reverse'] = not self.line['p_reverse']

        self.pseudo_timer += .1

    def draw(self):

        # Spirale
        self.opg.draw.rect(self.surface,
            (random.randint(0,255),random.randint(0,255),random.randint(0,255)), 
            self.opg.Rect(self.line['x'], self.line['y'], self.line['w'], self.line['h'])
        )


class DemoScene2:

    def update(self):

        for event in self.events:
            if event.type == self.opg.MOUSEBUTTONUP:

                self.line['x'] = self.display_size[0]/3
                self.line['y'] = self.display_size[1]/2
                self.line['p'][0] = random.randint(10,20)
                self.line['p'][1] = random.random()
                self.line['p_orig'] = self.line['p'][0]

                self.main_scene = DemoScene1
                self.draw_black_bg()
                

    def draw(self):

        self.draw_black_bg() # Background

        # Adaptative rectangle to display size
        self.opg.draw.rect(self.surface, (255,255,255), 
            self.opg.Rect(
                (self.display_size[0]*.5) - (self.display_size[0]*.1)*.5,
                (self.display_size[1]*.5) - (self.display_size[1]*.1)*.5,
                self.display_size[0]*.1, self.display_size[1]*.1
            )
        )


if __name__ == '__main__':
    App = Main()
    App.run()
