import pygame
import math

class Paddle(pygame.sprite.Sprite):
    def __init__(self,screen):
        self.screen = screen
        pygame.sprite.Sprite.__init__(self) 
        self.screen = screen

        #Paddle size and appearance
        width, height = 100, 20
        self.image = pygame.Surface((width, height))
        self.image.fill((200, 200, 200))
        
        #create rect and place near bottom center of the screen
        self.rect = self.image.get_rect()
        self.rect.midbottom = (screen.get_width() // 2, screen.get_height() - 30)
        self.dx = 0

    def moving_left(self):
        self.dx = -5
        if self.rect.left < 0:
            self.rect.left = 0

    def moving_right(self):
          self.dx = 5
          if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()

    def update(self):
      #self.rect.x, self.rect.y = pygame.mouse.get_pos()
      #self.rect.x = self.rect.x
      self.rect.x += self.dx

      if self.rect.left < 0:
          self.rect.left = 0
      elif self.rect.right > self.screen.get_width():
         self.rect.right = self.screen.get_width()

          

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
        self.color = color
        self.outline_color = (255, 255, 255)  # white outline
        self.angle = 0
        self.size = 15
        self.create_star_image()
        
        #Position the rect
        #17.5 bc half of 35, which is the width. Same as 10
        self.rect.center = (x + 17.5, y + 10)  #Center of brick
        self.pos_x = x + 17.5
        self.pos_y = y + 10

    def create_star_image(self):
        """Create a rotating star shape"""
        #Create surface large enough for rotated star
        surface_size = 50
        self.image = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        
        #Draw 5-point star
        center_x, center_y = surface_size // 2, surface_size // 2
        points = []
        
        for i in range(10):
            # Alternate between outer and inner radius
            if i % 2 == 0:
                radius = self.size
            else:
                radius = self.size * 0.4
            
            angle_rad = math.radians(self.angle + (i * 36))
            px = center_x + radius * math.cos(angle_rad)
            py = center_y - radius * math.sin(angle_rad)
            points.append((px, py))
        
        # Draw filled star
        if len(points) > 2:
            pygame.draw.polygon(self.image, self.color, points)
            pygame.draw.polygon(self.image, self.outline_color, points, 2)
        
        self.rect = self.image.get_rect()
        #self.rect.center = (self.pos_x, self.pos_y)

    def update(self):
        """Spin the star continuously"""
        self.angle = (self.angle + 5) % 360
        self.create_star_image()
        self.rect.center = (self.pos_x, self.pos_y)

    def move_down(self):
        self.pos_y += 2



