"""
author : Student Name
date : 
description : Main application file for Super Break Out game.
"""

import pygame
import Sprites

# button class
class Button:
    """
    This class defines a clickable button with hover effect.
    """

    def __init__(self, rect, text, onclick, font, bg=(80,80,80), hover_bg=(110,110,110), text_color=(255,255,255)):
        #initialize everything in the introduction screen
        self.rect = pygame.Rect(rect)
        self.text = text
        self.onclick = onclick
        self.font = font
        self.bg = bg
        self.hover_bg = hover_bg
        self.text_color = text_color

    def update_text(self, new_text):
        self.text = new_text

    def draw(self, surface):
        #play hover efffect if mouse on button
        mouse = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse)
        color = self.hover_bg if is_hover else self.bg
        pygame.draw.rect(surface, color, self.rect, border_radius=6)

        #setting texts and set text's collision box for clicking
        txt = self.font.render(self.text, True, self.text_color)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if callable(self.onclick):
                    self.onclick()

class Screen:
    def __init__(self, app):
        self.app = app

    
    def handle_event(self, event):
        pass
    def update(self):
        pass
    def draw(self, surface):
        pass
    def on_enter(self):
        pass
    def on_exit(self):
        pass


class MainMenu(Screen):
    """
    """
    def __init__(self, app):

        #adjust menu entities
        super().__init__(app)
        w, h = app.size
        btn_w, btn_h = 240, 50
        cx = w // 2 - btn_w // 2
        top = h // 2 - 40
        self.title_font = pygame.font.SysFont(None, 56)
        self.font = pygame.font.SysFont(None, 28)

        #Adjustable paddle width
        self.paddle_options = ["small", "medium", "large", "extra_large"]
        self.current_paddle_idx = 1 #Start at medium

        self.paddle_btn = Button((cx, top + 0*(btn_h+14), btn_w, btn_h), 
                                 f"Paddle: {self.paddle_options[self.current_paddle_idx]}", 
                                 self.cycle_paddle, self.font)
        
        #3 buttons, play, intro or quit
        self.buttons = [
            self.paddle_btn,
            Button((cx, top + 1*(btn_h+14), btn_w, btn_h), "Play", self.start_game, self.font),
            Button((cx, top + 2*(btn_h+14), btn_w, btn_h), "Introduction", self.show_intro, self.font),
            Button((cx, top + 3*(btn_h+14), btn_w, btn_h), "Quit", self.quit_game, self.font),
        ]

    def cycle_paddle(self):

        #choosing paddle size
        self.current_paddle_idx = (self.current_paddle_idx + 1) % len(self.paddle_options)
        choice = self.paddle_options[self.current_paddle_idx]

        #showing different size of the paddle
        self.paddle_btn.update_text(f"Paddle: {choice}")

        #use the selected paddle as the choice
        self.app.selected_paddle = choice

    def start_game(self):
        #to change to the gameplay screen
        self.app.change_screen(GamePlay(self.app))

    def show_intro(self):
        #to change to intro screen
        self.app.change_screen(Introduction(self.app))

    def quit_game(self):
        #to leave the game and eng the loop
        self.app.running = False

    def handle_event(self, event):

        #exccute the function if one of the button is clicked
        for b in self.buttons:
            b.handle_event(event)

    def draw(self, surface):

        #fill colour for the 
        surface.fill((18, 20, 28))
        title = self.title_font.render("Super Break Out", True, (255, 220, 60))
        surface.blit(title, title.get_rect(center=(self.app.size[0]//2, 100)))

        for b in self.buttons:
            b.draw(surface)

#Introduction screen
class Introduction(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.font = pygame.font.SysFont(None, 24)

        #intro content
        self.lines = [
            "Welcome to Super Break Out!",
            "",
            "Instructions:",
            "- Use Left/Right arrows to move.",
            "- Break bricks to earn points.",
            "- Colors have different points (Blue=1, Violet=6).",
            "- Max Score: 378.",
            "",
            "- You have 3 Lives.",
            "- Difficulty increases when 50% bricks are gone!",
            "",
            "Press ESC to return to menu."
        ]

    def handle_event(self, event):
        #if user click ESC
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.change_screen(MainMenu(self.app))

    def draw(self, surface):
        surface.fill((12, 12, 40))
        for i, line in enumerate(self.lines):
            txt = self.font.render(line, True, (230,230,230))
            surface.blit(txt, (40, 40 + i*28))


class GamePlay(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.screen = app.screen
        self.size = app.size
        
        #game state
        self.lives = 3
        self.score = 0
        self.bricks_destroyed = 0
        self.difficulty_triggered = False

        #Fonts
        self.score_font = pygame.font.SysFont(None, 30)

        #Background
        try:
            self.background = pygame.image.load("src\\image\\background.png")
            self.background = pygame.transform.scale(self.background, self.screen.get_size())
        except:
            self.background = pygame.Surface(self.screen.get_size())
            self.background.fill((0,0,0))

        #Row 0  Violet 6pts
        #Row 5  Blue 1pt
        #Order Top to Bottom: Violet, Red, Yellow, Orange, Green, Blue
        color_map = [
            (148, 0, 211, 6),  #Violet
            (255, 0, 0, 5),   #Red
            (255, 255, 0, 4),   #Yellow
            (255, 165, 0, 3),   #Orange
            (0, 128, 0, 2),    #Green
            (0, 0, 255, 1)  #Blue
        ]
        
        #setting the size of the brick
        brick_w, brick_h = 35, 20

        #a group to put all bricks
        self.bricks = pygame.sprite.Group()

        #initialize the total brick numer
        self.total_bricks = 0
        
        #6 Rows, 18 Columns
        for row in range(6):
            for col in range(18):
                #use a class from another module to create a brick each loop with given entities
                x = col * brick_w
                y = 60 + row * brick_h # Start a bit lower to leave room for score
                color_data = color_map[row]
                b = Sprites.Brick(x, y, color_data)

                #add the brick into the whole brick list
                self.bricks.add(b)

                #add 1 brick to the counting
                self.total_bricks += 1

        #assign paddle and Ball
        self.paddle = Sprites.Paddle(self.screen, app.selected_paddle)
        self.ball = Sprites.Ball(self.screen)

        #set srpite group to put all sprite
        self.allSprites = pygame.sprite.Group()
        self.allSprites.add(self.paddle, self.ball)
        self.allSprites.add(*self.bricks.sprites())

        #setting hitting sound
        self.hit_sound = self.app.hit_sound

    def on_enter(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except: pass

    def handle_event(self, event):
        #Allow ESC to quit to menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_screen(MainMenu(self.app))

    def update(self):
        self.allSprites.update()

        #Paddle hit ball
        if self.paddle.rect.colliderect(self.ball.rect):
            #Simple reflection based on hitting the top
            if self.ball.rect.bottom >= self.paddle.rect.top:
                 self.ball.bounce_y()
                 #Prevent ball getting stuck inside paddle
                 self.ball.rect.bottom = self.paddle.rect.top
                 if self.hit_sound: self.hit_sound.play()

        #Ball falling below paddle
        if self.ball.rect.top > self.screen.get_height():
            self.lives -= 1
            if self.lives > 0:
                self.ball.reset_position(self.screen)
            else:
                #return to menu (or could show Game Over screen) after game over
                print("Game Over")
                self.app.change_screen(MainMenu(self.app))
                return

        #Ball hit brick
        hit_brick = pygame.sprite.spritecollideany(self.ball, self.bricks)
        if hit_brick:
            self.ball.bounce_y() # Bounce vertical usually
            if self.hit_sound: self.hit_sound.play()
            
            #Add Score when hit 
            self.score += hit_brick.score_value
            self.bricks_destroyed += 1
            
            #remove the brick after hit
            hit_brick.kill()
            
            #Moving bricks
            #After a shape is destroyed, move rows down slightly
            for b in self.bricks:
                b.move_down()

            #Increasing difficulty
            #When half bricks destroyed, reduce paddle width
            if not self.difficulty_triggered and self.bricks_destroyed >= (self.total_bricks / 2):
                self.paddle.shrink()
                self.difficulty_triggered = True

        #Victory condition
        if len(self.bricks) == 0:
            print("You Win!")
            self.app.change_screen(MainMenu(self.app))

    def draw(self, surface):
        surface.blit(self.background, (0,0))
        self.allSprites.draw(surface)
        
        #Draw UI, score and lives
        score_text = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = self.score_font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        
        #put lives and scores onto screen
        surface.blit(score_text, (20, 10))
        surface.blit(lives_text, (self.size[0] - 120, 10))


class App:
    def __init__(self, size=(630,700)):
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Super Break Out")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Global Settings
        self.selected_paddle = "medium" 

        # Sound initialization
        try:
            pygame.mixer.init()
            # pygame.mixer.music.load("src/sound/hit.wav") 
            # pygame.mixer.music.set_volume(0.5)
            # pygame.mixer.music.play(-1)
            self.hit_sound = pygame.mixer.Sound("src/sound/hit.wav")
            self.hit_sound.set_volume(0.6)
        #If the initialization has failed this message will be printed
        except Exception as e:
            print("Audio init failed (files missing?):", e)
            #after the initialization failed, it will set the sound effect to none to keep the program running
            self.hit_sound = None

        #Check which screen the game in on 
        self.current_screen = MainMenu(self)
        #If the screen name is on_enter, it will call the fnction to change the screen
        if hasattr(self.current_screen, "on_enter"):
            self.current_screen.on_enter()

    def change_screen(self, new_screen):
        """
        this method take self and the new_screen (str name) as it parameter
        it will check which name it is and call the funtion
        """
        #if the name is on_exit it will call method on_exit
        if hasattr(self.current_screen, "on_exit"):
            self.current_screen.on_exit()

        #If the name is on_enter, it will call metod on_enter
        self.current_screen = new_screen
        if hasattr(self.current_screen, "on_enter"):
            self.current_screen.on_enter()

    def run(self):
        """
        """

        #running loop
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_screen.handle_event(event)

            self.current_screen.update()
            self.current_screen.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    App().run()