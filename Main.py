import Sprites
import pygame

class Game: 
    def __init__(self):
        pygame.__init__()

        #screen is 630 wide because 630 is divisible by 18, to put 18 bricks in a row
        self.screen = pygame.display.set_mode((630, 1000)) 
        pygame.display.set_caption("Super Break Out!!!!") 

        self.entities()
        self.alter()

        #hide mouse
        pygame.mouse.set_visible(True) 

        #close game
        pygame.quit()



    def entities(self):
        #background
        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        #background music
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play(False)




        #sound effects
        self.sound = pygame.mixer.Sound("sound.wav")

        #create bricks, put all bricks in list
        self.bricks = []
        for i in range(108): 
            self.bricks.append(Sprites.Bricks(self.screen)) 
        #assign paddle
        paddle = Sprites.Paddle(self.screen)
        self.moving_paddle = paddle
        
        #assign ball sprite
        self.ball = Sprites.Ball(self.screen)

        #put them all into one sprite
        self.allSprites = pygame.sprite.Group(self.bricks, paddle)

    def alter(self):

        #main loop
        clock = pygame.time.Clock()
        keepGoing = True

        # L - Loop
        while keepGoing:
            # Time 
            clock.tick(30) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keepGoing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.moving_paddle.moving_left
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.moving_paddle.moving_right
            self.check_coll()
            self.refresh()

        pass

    def check_coll(self):
        for i in self.bricks:
            pass
    
    def refresh(self):
        self.allSprites.clear(self.screen, self.background) 
        self.allSprites.update() 
        self.allSprites.draw(self.screen) 
          
        pygame.display.flip() 



        