from settings import *


class SpriteSheet(object):
    def __init__(self,filename):
        image = pg.image.load(filename).convert_alpha()
        self.image = pg.Surface([64,64],pg.SRCALPHA)
