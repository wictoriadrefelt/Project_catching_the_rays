# Music contribution by Matthew Pablo


import pygame
import pygame.freetype
import colors_scheme
import random
import os
from os import path


WIDTH = 900
HEIGHT = 900
FPS = 50
MOVE = 7
JUMP = - 20
display = pygame.display.set_mode((640, 480))
IMAGE = pygame.image.load(os.path.join('images', 'stylized-basic-cloud.png')).convert_alpha()
SUN_IMAGE = pygame.image.load(os.path.join("images", "sun_shiny.png")).convert_alpha()
SUN_IMAGE = pygame.transform.scale(SUN_IMAGE, (150, 150))
C_IMAGE = pygame.image.load(os.path.join("images", "pumpkin.png")).convert_alpha()
C_IMAGE = pygame.transform.scale(C_IMAGE, (70, 70))
sound = path.join(path.dirname(__file__), "sound")

font_name = pygame.font.match_font("arial")
# TODO Startscreen

def happiness_score(screen, text, size, x, y):
    font_name = pygame.font.match_font("arial")
    font = pygame.font.Font(font_name, size)
    text_box = font.render(text, True, colors_scheme.WHITE)
    text_rect = text_box.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_box, text_rect)


class Cloud(pygame.sprite.Sprite):
    def __init__(self):    #MORE HERE?
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGE
        pygame.transform.scale(display, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = random.randrange(-200, -0)
        self.speed_y = random.randrange(4, 7)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = 0


class Sun(Cloud):
    def __init__(self):
        super().__init__()
        self.image = SUN_IMAGE

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = 0


class Collector(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, color, x_s, y_s, display):
        pygame.sprite.Sprite.__init__(self)
        self.image = C_IMAGE
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - 20
        self.happiness = 100

    def update(self):
        self.x_step = 0
        movement = pygame.key.get_pressed()
        if movement[pygame.K_LEFT or "a"]:
            self.x_step = -5
        if movement[pygame.K_RIGHT or "d"]:
            self.x_step = 5
        self.rect.x += self.x_step
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


    def collision(self, collector, clouds):
        all_sprites = pygame.sprite.Group()
        hits = pygame.sprite.spritecollide(collector, clouds, True)
        for hit in hits:
            c = Cloud()
            all_sprites.add(c)
            clouds.add(c)

       # if hits:
            #self.happiness <= 0:



    #def draw_happiness_bar(self):  #TODO, set this up

def start_screen():

    startup = True

    while startup:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill(colors_scheme.YELLOW)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((WIDTH / 2), (HEIGHT / 2))
        display.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)


def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init() #TODO, add sound and music
    pygame.mixer.music.load(path.join(sound, 'Caketown1.mp3'))
    pygame.mixer.music.set_volume(0.4)
    display = pygame.display.set_mode((HEIGHT, WIDTH))
    pygame.display.set_caption("Catch the rays")
    collector = Collector(HEIGHT//2, WIDTH//2, 40, 40, colors_scheme.YELLOW, 0, 0, display)
    clock = pygame.time.Clock()
    cloud = Cloud()
    cloud_list = []
    sun = Sun()
    collision_list = pygame.sprite.spritecollide(collector, cloud_list, False)


    all_sprites = pygame.sprite.Group()
    all_sprites.add(collector)
    clouds = pygame.sprite.Group()
    suns = pygame.sprite.Group()
    for i in range(7):
        c = Cloud()
        all_sprites.add(c)
        clouds.add(c)

    for i in range(3):
        s = Sun()
        all_sprites.add(s)
        suns.add(s)
    happiness = 50

    pygame.mixer.music.play(loops=-1)
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        all_sprites.update()
        #collector.collision(collector, clouds)

        collision = pygame.sprite.spritecollide(collector, clouds, True)
        for hit in collision:
            happiness -= 5
            c = Cloud()
            all_sprites.add(c)
            clouds.add(c)

        good_hit = pygame.sprite.spritecollide(collector, suns, True)
        if good_hit:
            print("hit sun")
        for hit in good_hit:
            happiness += 5
            s = Sun()
            all_sprites.add(s)
            suns.add(s)



        display.fill(colors_scheme.LIGHT_BLUE)
        all_sprites.draw(display)
        #draw_happiness_bar()
        happiness_score(display, str(happiness), 10, WIDTH // 2, 10)
        pygame.display.flip()
        clock.tick(100)


if __name__ == "__main__":
    main()
