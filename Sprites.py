import pygame
import math

class Paddle(pygame.sprite.Sprite):

    #width type default is medium
    def __init__(self, screen, width_type="medium"):
        pygame.sprite.Sprite.__init__(self) 

        #get screen infomation
        self.screen = screen
        self.width_type = width_type
        
        #Adjustable paddle width
        # extra_large is half screen size
        screen_w = screen.get_width()

        #different size for the paddle
        self.sizes = {
            "small": 60,
            "medium": 100,
            "large": 150,
            "extra_large": screen_w // 2
        }
        
        #paddle info
        self.width = self.sizes.get(width_type, 100)
        self.height = 20
        self.color = (200, 200, 200)
        
        self.create_image()
        
        # Place near bottom center
        self.rect = self.image.get_rect()
        self.rect.midbottom = (screen.get_width() // 2, screen.get_height() - 30)
        self.dx = 0

    def create_image(self):
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        #Add a visual outline
        pygame.draw.rect(self.image, (100,100,100), (0,0,self.width,self.height), 2)

    def shrink(self):
        """Requirement: Reduce paddle width by 50%"""
        center = self.rect.center
        #multiply by half
        self.width = int(self.width * 0.5)

        #create image
        self.create_image()
        self.rect = self.image.get_rect()
        self.rect.center = center

    def moving_left(self):
        self.dx = -7 # Increased speed slightly for better feel
        if self.rect.left < 0:
            self.rect.left = 0

    def moving_right(self):
          self.dx = 7
          if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()

    def update(self):
        #Reset dx each frame to stop movement if key isn't held
        self.dx = 0 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dx = -7
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dx = 7


        self.rect.x += self.dx

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.screen.get_width():
             self.rect.right = self.screen.get_width()

          

class Ball(pygame.sprite.Sprite): 
  '''This class defines the sprite for the Ball.''' 
  
  def __init__(self, screen): 
    pygame.sprite.Sprite.__init__(self) 

    #setting ball's entities
    radius = 8
    diameter = radius * 2
    self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA).convert_alpha()
    pygame.draw.circle(self.image, (255, 255, 0), (radius, radius), radius)
    self.rect = self.image.get_rect() 
    
    #Place ball explicitly
    self.reset_position(screen)
    
    self.__screen = screen 
    self.__dx = 4 
    self.__dy = -4 
    
  def reset_position(self, screen):
      self.rect.center = (screen.get_width()/2, screen.get_height()/2 + 50)
      self.__dy = -4 # Reset to moving up
      self.__dx = 4

  def bounce_y(self):
      """Reverse vertical direction"""
      self.__dy = -self.__dy

  def bounce_x(self):
      """Reverse horizontal direction"""
      self.__dx = -self.__dx
      
  # Kept for compatibility, but splits logic
  def change_direction(self): 
      self.__dx = -self.__dx 
      self.__dy = -self.__dy

  def update(self): 

    #moving the ball
    self.rect.x += self.__dx
    self.rect.y += self.__dy
    
    #Wall collisions left/right
    if self.rect.left <= 0:
        self.rect.left = 0
        self.bounce_x()

    #wall collision
    elif self.rect.right >= self.__screen.get_width():
        self.rect.right = self.__screen.get_width()
        self.bounce_x()
    
    # Ceiling collision
    if self.rect.top <= 0:
        self.rect.top = 0
        self.bounce_y()


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color_data):
        super().__init__()
        # color_data is a tuple: (R, G, B, Score_Value)
        self.color = color_data[:3]
        self.score_value = color_data[3]
        
        self.outline_color = (255, 255, 255)
        self.angle = 0
        self.size = 15
        self.create_star_image()
        
        self.rect.center = (x + 17.5, y + 10)
        self.pos_x = x + 17.5
        self.pos_y = y + 10

    def create_star_image(self):
        """Create a rotating star shape"""
        surface_size = 40
        self.image = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        
        center_x, center_y = surface_size // 2, surface_size // 2
        points = []
        
        for i in range(10):
            if i % 2 == 0:
                radius = self.size
            else:
                radius = self.size * 0.4
            
            angle_rad = math.radians(self.angle + (i * 36))
            px = center_x + radius * math.cos(angle_rad)
            py = center_y - radius * math.sin(angle_rad)
            points.append((px, py))
        
        if len(points) > 2:
            pygame.draw.polygon(self.image, self.color, points)
            pygame.draw.polygon(self.image, self.outline_color, points, 2)
        
        self.rect = self.image.get_rect()

    def update(self):
        """Spin the star continuously"""

        #plus 3 degree each time
        self.angle = (self.angle + 3) % 360
        self.create_star_image()
        self.rect.center = (self.pos_x, self.pos_y)

    def move_down(self):
        #Move bricks down 1-2 pixels
        self.pos_y += 1
        self.rect.center = (self.pos_x, self.pos_y)