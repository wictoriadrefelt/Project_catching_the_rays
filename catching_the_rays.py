import pygame
import pygame.freetype
import colors_scheme
import random
import os



WIDTH = 900
HEIGHT = 900
FPS = 50
MOVE = 7
JUMP = - 20
display = pygame.display.set_mode((640, 480))
IMAGE = pygame.image.load(os.path.join('images', 'stylized-basic-cloud.png')).convert_alpha()
#IMAGE = pygame.transform.scale(IMAGE, (130,130))
SUN_IMAGE = pygame.image.load(os.path.join("images", "sun_shiny.png")).convert_alpha()
SUN_IMAGE = pygame.transform.scale(SUN_IMAGE, (150, 150))
C_IMAGE = pygame.image.load(os.path.join("images", "pumpkin.png")).convert_alpha()
C_IMAGE = pygame.transform.scale(C_IMAGE, (70, 70))

# TODO Startcreen

pygame.init()
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
            return c
       # if hits:
            #self.happiness <= 0:



    def draw_happiness_bar(self):
        if self.happiness > 70:
            col = colors_scheme.GREEN
        elif self.happiness > 40:
            col = colors_scheme.YELLOW
        else:
            col = colors_scheme.RED
        width = int(self.rect.width * self.happiness / 100)
        self.happiness_bar = pygame.Rect(0, 0, width, 7)
        if self.happiness < 100:
            pygame.draw.rect(self.image, col, self.happiness_bar)

def text_display(display, text, size, x, y):
    def draw_text(surf, text, size, x, y):
        pygame.font.init()
        font_name = pygame.font.match_font("arial")
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, colors_scheme.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.centre = (x, y)
        surf.blit(text_surface, text_rect)


def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
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
    #collector = pygame.sprite.Group()
    suns = pygame.sprite.Group()
    for i in range(7):
        c = Cloud()
        all_sprites.add(c)
        clouds.add(c)

    for i in range(3):
        s = Sun()
        all_sprites.add(s)
        suns.add(s)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        all_sprites.update()
        collector.collision(collector, clouds)
        #for hit in hits:
        #    c = Cloud()
         #   all_sprites.add(c)
          #  clouds.add(c)

        good_hits = pygame.sprite.spritecollide(collector, suns, True)
        if good_hits:
            print("hit sun")
        for hit in good_hits:
            s = Sun()
            all_sprites.add(s)
            suns.add(s)

        collector.draw_happiness_bar()

        display.fill(colors_scheme.LIGHT_BLUE)
        text_display(display, str("HELLO"), WIDTH//2, 20, 20)
        all_sprites.draw(display)
        pygame.display.flip()
        clock.tick(100)


if __name__ == "__main__":
    main()
