import pygame
from pygame.version import PygameVersion
import os
from random import randint

class Settings():
    window_width = 500
    window_height = 750
    window_border = 10
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    fps = 60
    caption = "DTD"
    nof_darts = 5
    nof_leben = 3
    tp_uses = 3
    punktestand = 0
    ptnd = 10
    hit = False

class Background(object):
    def __init__(self, filename) -> None:
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

class Bloon(pygame.sprite.Sprite):
    def __init__(self, picturefile) -> None:
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, picturefile)).convert_alpha()
        self.image = self.image_orig
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.window_width / 2
        self.rect.centery = 650
        self.directionx = 0
        self.directiony = 0
        self.speed = 3
        self.stop()

    def update(self):
        newrect = self.rect.move(self.directionx * self.speed, self.directiony * self.speed)
        if newrect.right >= Settings.window_width:
            self.stop()
        if newrect.left <= Settings.window_border:
            self.stop()
        if newrect.bottom >= Settings.window_height:
            self.stop()
        if newrect.top <= Settings.window_border:
            self.stop()
        self.rect.move_ip((self.directionx * self.speed, self.directiony * self.speed))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def stop(self):
        self.directionx = 0
        self.directiony = 0

    def down(self):
        self.directiony = 1

    def up(self):
        self.directiony = -1

    def left(self):
        self.directionx = -1

    def right(self):
        self.directionx = 1

    def space(self):
        if Settings.tp_uses >= 1:
            self.rect.centerx = randint(10, 490)
            self.rect.centery = randint(10, 740)
            Settings.tp_uses = Settings.tp_uses - 1

class Dart(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.dg = randint(35, 50)
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, "dart.png")).convert_alpha()
        self.image = self.image_orig
        self.image = pygame.transform.scale(self.image, (self.dg, self.dg))
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(10, 490)
        self.rect.centery = randint(-100, -10)
        self.speed = randint(1, 3)

    def update(self):
        if self.rect.top >= Settings.window_height:
            self.rect.centerx = randint(10, 490)
            self.rect.centery = randint(-100, -10)
            Settings.punktestand = Settings.punktestand + 1
            Settings.ptnd = Settings.ptnd - 1
            if self.speed >= 10:
                self.speed = 10
            else:
                self.speed = self.speed + 0.3
        self.rect.move_ip(0, self.speed)
        if Settings.nof_leben <= 0:
            self.speed = 0
        if Settings.hit == True:
            self.rect.centery = self.rect.centery - Settings.window_height

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Leben(pygame.sprite.Sprite):
    def __init__(self, filename1, filename2, filename3) -> None:
        super().__init__()
        self.image_3Leben = pygame.image.load(os.path.join(Settings.path_image, filename1)).convert_alpha()
        self.image_2Leben = pygame.image.load(os.path.join(Settings.path_image, filename2)).convert_alpha()
        self.image_1Leben = pygame.image.load(os.path.join(Settings.path_image, filename3)).convert_alpha()
        self.image = self.image_3Leben
        self.rect = self.image.get_rect()
        self.rect.centerx = 90
        self.rect.centery = 80
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Losescreen(object):
    def __init__(self, filename) -> None:
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.lose = 500

    def draw(self, screen):
        screen.blit(self.image, (self.lose, 0))

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "50,30"
        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.screen = pygame.display.set_mode((Settings.window_width,Settings.window_height))
        self.clock = pygame.time.Clock()
        self.running = False
        self.background = Background("Hintergrund.png")
        self.losescreen = Losescreen("Hintergrund2.png")
        self.bloon = Bloon("bloon.png")
        self.leben = Leben("3Leben.png", "2Leben.png", "1Leben.png")
        self.all_darts = pygame.sprite.Group()
        for a in range(Settings.nof_darts):
            self.all_darts.add(Dart())


    def run(self):
        self.running = True 
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()

        pygame.quit()

    def draw(self):
        self.background.draw(self.screen)
        self.bloon.draw(self.screen)
        self.all_darts.draw(self.screen)
        self.leben.draw(self.screen)
        self.losescreen.draw(self.screen)
        text_surface_punktestand = self.font.render("Punktestand: {0}".format(Settings.punktestand), True, (0, 0, 0))
        self.screen.blit(text_surface_punktestand, dest=(10, 10))

        pygame.display.flip()

    def increase_darts(self):
        if Settings.ptnd <= 0:
                Settings.ptnd = 10
                if Settings.nof_darts <= 10:
                    for a in range(1):
                        self.all_darts.add(Dart())

    def check_for_collision(self):
        Settings.hit = False
        for s in self.all_darts:
            if pygame.sprite.collide_mask(s, self.bloon):
                Settings.hit = True
                break
        if Settings.hit:
            self.bloon.rect.centerx = Settings.window_width / 2
            self.bloon.rect.centery = 650
            Settings.nof_leben = Settings.nof_leben -1
            if Settings.nof_leben == 2:
                self.leben.image = self.leben.image_2Leben
            if Settings.nof_leben == 1:
                self.leben.image = self.leben.image_1Leben
            if Settings.nof_leben <= 0:
                self.losescreen.lose = 0

    def update(self):
        self.check_for_collision()
        self.bloon.update()
        self.increase_darts()
        self.all_darts.update()

    def watch_for_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_DOWN:
                        self.bloon.down()
                    elif event.key == pygame.K_UP:
                        self.bloon.up()
                    elif event.key == pygame.K_LEFT:
                        self.bloon.left()
                    elif event.key == pygame.K_RIGHT:
                        self.bloon.right()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.bloon.stop()
                    elif event.key == pygame.K_UP:
                        self.bloon.stop()
                    elif event.key == pygame.K_LEFT:
                        self.bloon.stop()
                    elif event.key == pygame.K_RIGHT:
                        self.bloon.stop()
                    elif event.key == pygame.K_SPACE:
                        self.bloon.space()

if __name__ == "__main__":

    game = Game()
    game.run()