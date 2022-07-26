#!/usr/bin/python3
#~*~ coding: utf-8 ~*~

import sys, pygame

class Engine:

    class VoidState:
        def update(self): pass
        def draw(self): pass

    def __init__(self, gameName='OPyGame', defaultState=VoidState, w=640, h=480, FPS_LIMIT=60, RESIZE=False):

        self.opg = pygame
        self.opg.init()

        self.game_name = gameName
        self.game_state = defaultState

        self.display_size = (w,h) if not RESIZE else [w,h]

        flags = self.opg.RESIZABLE if RESIZE else 0

        self.surface = self.opg.display.set_mode(self.display_size, flags)
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

            self.game_state.update(self)
            self.game_state.draw(self)

            self.opg.display.update()

        self.opg.quit()
        sys.exit()
