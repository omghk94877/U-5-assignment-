import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self) 
        self.screen = screen
        self.lives = 3
        pass

    def moving_left(self):
        pass

    def moving_right(self):
        pass

class Ball(pygame.sprite.Sprite):
    def __init__(self,screen):
        pass

    def moving(self):
        pass

class Bricks(pygame.sprite.Sprite):
    def __init__(self,screen):
        pass

    def voilet(self):
        pass

    def red(self):
        pass

    def orange(self):
        pass

    def green(self):
        pass

    def blue(self):
        pass