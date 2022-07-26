#!/usr/bin/python3
#~*~ coding: utf-8 ~*~

import math, random # For Demos
from OPyGame import Engine

class Main(Engine):
    def __init__(self):
        super().__init__('OPyGame - Demo', DemoScene1, 480, 360, RESIZE=True)

        self.opg.font.init() # Initialisation de la gestion des polices

        self.font_x14 = self.opg.font.SysFont("Deja Vu Sans", 14)
        self.font_x22 = self.opg.font.SysFont("Deja Vu Sans", 22)

        self.font_info_state_DS1 = self.font_x14.render("Demo Scene 1", False, (255,255,255))
        self.font_info_state_DS2 = self.font_x14.render("Demo Scene 2", False, (255,255,255))
        self.font_info_state_DS3 = self.font_x14.render("Demo Scene 3", False, (255,255,255))

        self.font_instructions_DS2 = self.font_x22.render("Specify the number of vertices in the terminal.", False, (255,255,255))

    # Valeurs pour la DemoScene1 #

        self.line = { 'x': self.display_size[0]/3,
                      'y': self.display_size[1]/2,
                      'w': 1, 'h': 1, 'p': [ random.randint(10,20), random.random() ],
                      'p_reverse': False, 'p_orig': None }

        self.line['p_orig'] = self.line['p'][0]

    # Valeurs de la DemoScene2 #

        self.pix = [
            [ # Position
                self.display_size[0]/2,
                self.display_size[1]/10, # * (self.vertices*x), # TROUVER MOYEN PLUS EFFICACE DE CENTRER 'Y' selon la taille de la figure
            ],
            [ # Couleur RGB
                random.randint(63,191),
                random.randint(63,191),
                random.randint(63,191)
            ]
        ]

    # Valeurs "globales"

        self.pseudo_timer = 0
        self.actual_state = 1

    def change_state(self):

        self.pseudo_timer = 0
        self.actual_state += 1

        if self.actual_state > 3:
            self.actual_state = 1

        if self.actual_state == 1:
            self.line['x']      = self.display_size[0]/3
            self.line['y']      = self.display_size[1]/2
            self.line['p'][0]   = random.randint(10,20)
            self.line['p'][1]   = random.random()
            self.line['p_orig'] = self.line['p'][0]
            self.game_state = DemoScene1

        elif self.actual_state == 2:
            self.draw_black_bg()
            self.ask_number_of_vertices()
            self.pix[0][0] = self.display_size[0]/2
            self.pix[0][1] = self.display_size[1]/10
            self.pix[1][0] = random.randint(63,191)
            self.pix[1][1] = random.randint(63,191)
            self.pix[1][2] = random.randint(63,191)
            self.game_state = DemoScene2

        elif self.actual_state == 3:
            self.game_state = DemoScene3

        self.draw_black_bg()

    """ DOC: PIX_MOVE(..)
        fm = factor_movement : fm = fx || fy
        fv = factor_vertices : fv = sin(timer * vertices) - Si sin() est remplacer par cos(), le '4 sommets' sera perpeniculaire à l'affichage.
        const 10: Sert à avoir une figure plus grande, tout simplement. TROUVER MOYEN D'AVOIR TOUJOURS LA MEME ECHELLE DE FIGURE.
    """

    def pix_move(self, fm, fv): return ((fm * fv) * self.vertices) * 10 # For DemoScene1

    def ask_number_of_vertices(self): # For DemoScene1

        """ VERTICES: Sert a afficher le nombre sommets souhaités.
                Si l'entier est pair il s'affichera le double du nombre indiqué.
                Si il est impaire il s'affichera le nombre indiqué, simplement.
        """

        # TROUVER MOMYEN DE FAIRE 6 BRANCHES, car 6%2=0 donc 6/2=3 branches
        # Hypothese: le 6 et 10 branches ne sont pas faisables avec cet algo.

        self.surface.blit(self.font_instructions_DS2, (0,(self.display_size[1]-22)/2))
        self.surface.blit(self.font_info_state_DS2, (0,0)); self.opg.display.update()

        print("\nSpecify the desired number of vertices (default -> 4)\n")

        while(True):
            try:   self.vertices = float( input("USER > ") or 4 ); break
            except ValueError: print("ERROR: Please enter an integer or float number.")

        if self.vertices % 2 == 0:
            self.vertices /= 2

    def draw_black_bg(self):   # Draw black background
        self.opg.draw.rect(self.surface, (0,0,0), self.opg.Rect(0,0,self.display_size[0],self.display_size[1]))


class DemoScene1:

    def update(self):

        for event in self.events:
            if event.type == self.opg.MOUSEBUTTONUP:
                self.change_state()

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
        self.surface.set_at( # Affichage du pixel de la "spirale"
            (int(self.line['x']),int(self.line['y'])),
            (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        ); self.surface.blit(self.font_info_state_DS1, (0,0))


class DemoScene2:

    def update(self):

        for event in self.events:
            if event.type == self.opg.MOUSEBUTTONUP:
                self.change_state()

        fx, fy = math.sin(self.pseudo_timer), \
                 math.cos(self.pseudo_timer)  # factor_movement_positionXY

        fv = math.sin(self.pseudo_timer*self.vertices) # factor vertices

        self.pix[0][0] += self.pix_move(fx, fv)
        self.pix[0][1] += self.pix_move(fy, fv)

        for rgb in range(len(self.pix[1])): # THIS IS JUST AN EXPERIMENT
            color_inc = (fx*fy) * random.randint(-10,10)
            if  self.pix[1][rgb] + color_inc < 255 \
            and self.pix[1][rgb] + color_inc > 0:
                self.pix[1][rgb] += color_inc

        self.pseudo_timer += .1

    def draw(self):
        self.surface.set_at(
            (int(self.pix[0][0]),
             int(self.pix[0][1])),
            self.pix[1]
        )

        self.surface.blit(self.font_info_state_DS2, (0,0))


class DemoScene3:

    def update(self):

        for event in self.events:
            if event.type == self.opg.MOUSEBUTTONUP:
                self.change_state()

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

        self.surface.blit(self.font_info_state_DS3, (0,0))


if __name__ == '__main__':
    App = Main()
    App.run()
