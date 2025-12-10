import Sprites
import pygame

class Game: 
    def __init__(self):
        pygame.init()
        # ensure mixer is initialized (some systems need explicit init)
        """try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception:
            # continue even if mixer fails; sound will be disabled
            pass"""

        #screen is 630 wide because 630 is divisible by 18, to put 18 bricks in a row
        self.screen = pygame.display.set_mode((630, 700)) 
        pygame.display.set_caption("Super Break Out!!!!") 

        self.entities()
        self.alter()

        #hide mouse
        pygame.mouse.set_visible(False) 

        #close game
        pygame.quit()



    def entities(self):
        #background
        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.screen.blit(self.background, (0, 0))

        #self.sound = pygame.mixer.Sound("hit.wav")


        #colour for each row
        colors = [
            (75,0,130), #darker purple
            (148, 0, 211),  #violet
            (255, 0, 0),      #red
            (255, 165, 0),   #orange
            (0, 128, 0),   #green
            (0, 0, 255),  #blue
        ]

        brick_width = 35
        brick_height = 20


        #create a bricks group
        self.bricks = []

        for row in range(6):
            for col in range(18):
                x = col * brick_width
                y = row * brick_height
                color = colors[row]
                brick = Sprites.Brick(x, y, color)
                self.bricks.append(brick)

        #create paddle and ball 
        self.paddle = Sprites.Paddle(self.screen)
        self.ball = Sprites.Ball(self.screen)

        #all sprites group
        self.allSprites = pygame.sprite.Group()
        self.allSprites.add(self.paddle, self.ball, self.bricks)
        self.allSprites.add(self.bricks)  # add all bricks


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
                        self.paddle.moving_left()
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.paddle.moving_right()
            self.check_coll()
            self.refresh()
        pass

    def check_coll(self):

        #collision between ball and paddle
        if self.paddle.rect.colliderect(self.ball.rect):
            self.ball.change_direction()
        
        

        #collision between ball and wall
        if self.ball.rect.centerx < 0 or self.ball.rect.centerx > self.screen.get_width():
            self.ball.change_direction()
        
        if self.ball.rect.centery < 0 or self.ball.rect.centery > self.screen.get_height():
            self.ball.change_direction()

        #collision between ball and brick
        for brick in self.bricks:
            if self.ball.rect.colliderect(brick.rect):
                brick.kill()
                self.bricks.remove(brick)
                self.ball.change_direction()
                #Sprites.Brick.move_down()
                #self.sound.play()
                

            

        # REFRESH SCREEN 
        self.refresh()


    def refresh(self):
        self.allSprites.clear(self.screen, self.background) 
        self.allSprites.update() 
        self.allSprites.draw(self.screen) 
          
        pygame.display.flip()


Game()