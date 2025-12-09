import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self) 
        self.screen = screen
        self.image = pygame.draw.rect()
        pass

    def moving_left(self):
        pass

    def moving_right(self):
        pass

class Ball(pygame.sprite.Sprite): 
  '''This class defines the sprite for the Ball.''' 
  
  def __init__(self, screen): 
    '''This initializer takes a screen surface as a parameter, initializes  the image and rect attributes, and x,y direction of the ball.''' 
    # Call the parent __init__() method 
    pygame.sprite.Sprite.__init__(self) 
    # Create a small transparent surface for the ball and draw a yellow circle
    radius = 10
    diameter = radius * 2
    self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA).convert_alpha()
    pygame.draw.circle(self.image, (255, 255, 0), (radius, radius), radius)
    self.rect = self.image.get_rect() 
    self.rect.center = (screen.get_width()/2,screen.get_height()/2) 
    # Instance variables to keep track of the screen surface 
    # and set the initial x and y vector for the ball. 
    self.__screen = screen 
    self.__dx = 5 
    self.__dy = -3 
    
  def change_direction(self): 
    '''This method causes the x direction of the ball to reverse.''' 
    self.__dx = -self.__dx 
    self.__dy = -self.__dy


  

  def update(self): 
    '''This method will be called automatically to reposition the 
    ball sprite on the screen.''' 
    # Check if we have reached the left or right end of the screen. 
    # If not, keep moving the ball in the same x direction. 
    if ((self.rect.left > 0) and (self.__dx < 0)) or ((self.rect.right < self.__screen.get_width()) 
    and (self.__dx > 0)):  
      self.rect.left += self.__dx 
    # If yes, then reverse the x direction.  
    else: 
      self.__dx = -self.__dx 
    
    # Check if we have reached the top or bottom of the court.
    # If not, keep moving the ball in the same y direction. 
    if ((self.rect.top-40 > 0) and (self.__dy > 0)) or  ((self.rect.bottom+40 < self.__screen.get_height()) 
    and (self.__dy < 0)):  
      self.rect.top -= self.__dy 
      # If yes, then reverse the y direction.  
    else: 
      self.__dy = -self.__dy 


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()

        # brick size
        width = 35
        height = 20

        #create a surface for the brick
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        #generate the rect based on the image
        self.rect = self.image.get_rect()

        #position the rect
        self.rect.topleft = (x, y)
