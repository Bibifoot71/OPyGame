#!/usr/bin/python3
#~*~ coding: utf-8 ~*~

import sys, pygame

class Engine:

    def __init__(self, gameName='OPyGame', w=400, h=350, FPS_LIMIT=60, RESIZE=False):
        
        self.opg = pygame
        self.opg.init()
    
        self.game_name = gameName
        self.display_size = (w,h) if not RESIZE else [w,h]
        resize_flag = self.opg.RESIZABLE if RESIZE else None
        self.surface = self.opg.display.set_mode(self.display_size, resize_flag)
        self.FPS_LIMIT, self.clock, self.dt = FPS_LIMIT, self.opg.time.Clock(), 0
        self.events = None

        self.opg.display.set_caption(self.game_name)
        self.opg.key.set_repeat(40, 30)

        self.quit = False
        
    def _getDisplaySize(self,w,h):
        self.display_size[0] = w
        self.display_size[1] = h

    def run(self):
        while (not self.quit):

            self.dt = self.clock.tick(self.FPS_LIMIT)
            self.events = self.opg.event.get()

            for event in self.events:
                if event.type == self.opg.QUIT:
                    self.quit=True
                elif event.type == self.opg.VIDEORESIZE:
                    self._getDisplaySize(event.w,event.h)

            self.main_scene.update(self)
            self.main_scene.draw(self)

            self.opg.display.update()

        self.opg.quit()
        sys.exit()
