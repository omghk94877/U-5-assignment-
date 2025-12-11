"""
author : 
date :
description : Main application file for Super Break Out game.
"""

import pygame
import Sprites  

# button class
class Button:
    def __init__(self, rect, text, onclick, font, bg=(80,80,80), hover_bg=(110,110,110), text_color=(255,255,255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.onclick = onclick
        self.font = font
        self.bg = bg
        self.hover_bg = hover_bg
        self.text_color = text_color

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse)
        color = self.hover_bg if is_hover else self.bg
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        txt = self.font.render(self.text, True, self.text_color)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if callable(self.onclick):
                    self.onclick()

# Screen base class
class Screen:
    def __init__(self, app):
        self.app = app

    def handle_event(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass
    def on_enter(self):
        pass
    def on_exit(self):
        pass


# Main Menu Screen
class MainMenu(Screen):
    def __init__(self, app):
        super().__init__(app)
        w, h = app.size
        btn_w, btn_h = 200, 50
        cx = w // 2 - btn_w // 2
        top = h // 2 - 80
        self.title_font = pygame.font.SysFont(None, 56)
        self.font = pygame.font.SysFont(None, 28)

        self.buttons = [
            Button((cx, top + 0*(btn_h+14), btn_w, btn_h), "Play", self.start_game, self.font),
            Button((cx, top + 1*(btn_h+14), btn_w, btn_h), "Introduction", self.show_intro, self.font),
            Button((cx, top + 2*(btn_h+14), btn_w, btn_h), "Quit", self.quit_game, self.font),
        ]

    def start_game(self):
        self.app.change_screen(GamePlay(self.app))

    def show_intro(self):
        self.app.change_screen(Introduction(self.app))

    def quit_game(self):
        self.app.running = False

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    def draw(self, surface):
        surface.fill((18, 20, 28))
        title = self.title_font.render("Super Break Out", True, (255, 220, 60))
        surface.blit(title, title.get_rect(center=(self.app.size[0]//2, 120)))

        for b in self.buttons:
            b.draw(surface)

# Introduction Screen
class Introduction(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.font = pygame.font.SysFont(None, 26)
        self.lines = [
            "Welcome to Super Break Out!",
            "",
            "Instructions:",
            "- Use the left and right arrow keys (or A and D) to move the paddle.",
            "- Bounce the ball to break all the bricks.",
            "- If the ball falls below the paddle, you lose a life.",
            "- Clear all bricks to win the game!",
            "",
            "Press ESC to return to the main menu."
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.change_screen(MainMenu(self.app))

    def draw(self, surface):
        surface.fill((12, 12, 40))
        for i, line in enumerate(self.lines):
            txt = self.font.render(line, True, (230,230,230))
            surface.blit(txt, (40, 40 + i*30))

# -----------------------------
# GamePlay Screen (改寫你的 Game)
# -----------------------------
class GamePlay(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.screen = app.screen
        self.size = app.size
        self.clock = app.clock

        # background
        self.background = pygame.image.load("src\\image\\background.png")
        self.background = pygame.transform.scale(self.background, self.screen.get_size())

        # 
        colors = [
            (75,0,130), (148, 0, 211), (255, 0, 0),
            (255, 165, 0), (0, 128, 0), (0, 0, 255)
        ]
        brick_w, brick_h = 35, 20
        self.bricks = pygame.sprite.Group()
        for row in range(6):
            for col in range(18):
                x = col * brick_w
                y = row * brick_h
                color = colors[row]
                b = Sprites.Brick(x, y, color)
                self.bricks.add(b)

        # paddle and ball
        self.paddle = Sprites.Paddle(self.screen)
        self.ball = Sprites.Ball(self.screen)

        # all sprites group
        self.allSprites = pygame.sprite.Group()
        self.allSprites.add(self.paddle, self.ball)
        # add bricks to all sprites group
        self.allSprites.add(*self.bricks.sprites())

        # sound effect
        self.hit_sound = self.app.hit_sound

    def on_enter(self):
        # initlize the mixer if not already initialized
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception:
            pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                self.paddle.moving_left()
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                self.paddle.moving_right()


    def update(self):
        self.allSprites.update()

        # detect collisions
        # paddle hit ball
        if self.paddle.rect.colliderect(self.ball.rect):
            self.ball.change_direction()
            if self.hit_sound: self.hit_sound.play()

        # ball hit wall
        if self.ball.rect.centerx < 0 or self.ball.rect.centerx > self.screen.get_width():
            self.ball.change_direction()
        if self.ball.rect.centery < 0:
            self.ball.change_direction()

        # ball fall below paddle
        if self.ball.rect.top > self.screen.get_height():
            # 
            self.app.change_screen(MainMenu(self.app))
            return

        
        for brick in list(self.bricks):
            if self.ball.rect.colliderect(brick.rect):
                brick.kill()     
                # Remove from groups
                try:
                    self.bricks.remove(brick)
                except Exception:
                    pass
                # Remove from allSprites
                try:
                    self.allSprites.remove(brick)
                except Exception:
                    pass

                self.ball.change_direction()
                if self.hit_sound: self.hit_sound.play()

               
                for remaining in self.bricks:
                    if hasattr(remaining, "move_down"):
                        remaining.move_down()
                break  # only handle one brick collision per update

    def draw(self, surface):
        # preload background
        surface.blit(self.background, (0,0))
        self.allSprites.draw(surface)


# app which manages screens
class App:
    def __init__(self, size=(630,700)):
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Super Break Out")
        self.clock = pygame.time.Clock()
        self.running = True

        # Fonts
        self.font = pygame.font.SysFont(None, 24)

        # Sound initialization
        try:
            pygame.mixer.init()
            # background music
            pygame.mixer.music.load("src\\sound\\dvofak-9.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            # sound effect
            self.hit_sound = pygame.mixer.Sound("src\\sound\\hit.wav")
            self.hit_sound.set_volume(0.6)
        except Exception as e:
            print("Audio init failed:", e)
            self.hit_sound = None

        # initialize first screen
        self.current_screen = MainMenu(self)
        if hasattr(self.current_screen, "on_enter"):
            self.current_screen.on_enter()

    def change_screen(self, new_screen):
        # change screen with proper enter/exit calls
        if hasattr(self.current_screen, "on_exit"):
            self.current_screen.on_exit()
        self.current_screen = new_screen
        if hasattr(self.current_screen, "on_enter"):
            self.current_screen.on_enter()

    def run(self):
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


# Run the app
App().run()
