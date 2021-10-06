import pygame as pg
import sys
from camera import *
from settings import *
from sprites import *
from os import path

pg.init()

# HUD function

# size of the game is : 29.27 kb


def draw_player_health(surf,x,y,pct):

    if pct < 0:
#thank you for watching
        pct = 0
    bar_length = 70
    bar_height = 10
    fill = pct * bar_length
    rect = pg.Rect(x,y,bar_length,bar_height)
    fill_rect = pg.Rect(x,y,fill,bar_height)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf,col,fill_rect)
    pg.draw.rect(surf,WHITE,rect,2)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()


    def music_data(self):
        self.shoot_sound = pg.mixer.Sound('gun.wav')

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.p = False
        self.map_g = 'map4.txt'
        map_folder = path.join(game_folder,'maps')
        self.map = Map(path.join(game_folder, 'map.txt'))
        self.mouse_img = pg.image.load('mpouse.png').convert_alpha()
        self.mouse_img.set_colorkey(BLACK)
        self.mx,self.my = pg.mouse.get_pos()
        self.splat = pg.image.load('splat green.png').convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.player_img = pg.image.load(PLAYER_IMG).convert_alpha()
        self.bullet_img = pg.image.load(BULLET_IMG).convert_alpha()
        self.bullet_img.set_colorkey((255,255,255))
        self.mob_img = pg.image.load(ZOMBIE_IMG).convert_alpha()
        self.tile_img = pg.image.load('tile_138.png').convert_alpha()
        self.tile_img = pg.transform.scale(self.tile_img,(TILESIZE,TILESIZE))
        self.tile_img2 = pg.image.load('tile_o.png').convert_alpha()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,50))
        self.tile_img2 = pg.transform.scale(self.tile_img2, (TILESIZE, TILESIZE))
        self.tile_img3 = pg.image.load('tile_137.png').convert_alpha()
        self.tile_img3 = pg.transform.scale(self.tile_img3, (TILESIZE, TILESIZE))
        self.tile_img4 = pg.image.load('tile_1390.png').convert_alpha()
        self.tile_img4 = pg.transform.scale(self.tile_img4, (TILESIZE, TILESIZE))
        self.fog = pg.Surface((WIDTH,HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.wave = 1
        self.night = False
        self.effects = pg.BLEND_MULT
        self.light_mask = pg.image.load(LIGHT_MASK).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask,LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        self.gun_flashes = []
        self.item_image = pg.image.load('health_pack.png').convert()
        self.shotgun_image = pg.image.load('obj_shotgun.png').convert_alpha()
        self.item_image.set_colorkey(BLACK)
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(img).convert_alpha())



    def new(self):
        n  =0
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.splats = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.items2 = pg.sprite.Group()
        self.muzzle = pg.sprite.Group()

        for row,tiles in enumerate(self.map.data):
            for col,tile in enumerate(tiles):
                if tile == '1':
                    Wall(self,col,row)
                if tile == 'M':
                    self.mob = Mob(self,col,row)
                if tile == '2':
                    Wall2(self,col,row)

                if tile == '4':
                    Wall4(self,col,row)
                if tile == 'P':
                    self.player = Player(self,col,row)

                if tile == 'H':
                    Items(self,col,row)

                if tile == "S":
                    ShotGun(self,col,row)




        self.camera = Camera(self.map.width,self.map.height)
        self.paused = False
        self.win = False



    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 900
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        global  PLAYER_ENERY,PLAYERSPEED2
        game_folder = path.dirname(__file__)
        # Game over ?
        if len(self.mobs) < 24:
            self.wave = 2
        if len(self.mobs) < 11:
            self.wave = "Final wave 3"
        if len(self.mobs) < 1:
            self.screen.fill(BLACK)
            self.effects = pg.BLEND_MULT
            self.draw_text('You Win', 'ZOMBIE.TTF', 100, RED, WIDTH / 2, HEIGHT / 2, align="center")
            self.draw_text('press any key to go to menu', 'ZOMBIE.TTF', 105, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
            pg.display.flip()
            pg.event.wait()
            waiting = True
            while waiting:
                self.clock.tick(FPS)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        waiting = False
                        self.quit()
                    if event.type == pg.KEYUP:
                        waiting = False





        # update portion of the game loop
        self.all_sprites.update()
        self.splats.update()
        self.camera.update(self.player)
        # mob collide player
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if self.player.health < 99:
                hit.kill()
                self.player.add_health(100)
        hits = pg.sprite.spritecollide(self.player,self.mobs,False,collide_hit_rect)

        for hit in hits:
            self.player.health -= 10
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
            self.player.hit()

        # bullet collide mob
        hits = pg.sprite.groupcollide(self.mobs,self.bullets,False, True)
        for hit in hits:
            hit.healths -= WEOPENS[self.player.weopen]['damage'] * len(hits[hit])
            hit.vel = vec(0,0)

        hits = pg.sprite.spritecollide(self.player,self.items2,False)
        for hit in hits:
            hit.kill()
            self.player.weopen = 'shotgun'
            self.player.go = True

    def draw_grid(self):
        pass

    def render_fog(self):
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask,self.light_rect)
        self.screen.blit(self.fog,(0,0),special_flags=self.effects)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()

        for sprite in self.splats:

            self.screen.blit(sprite.image,self.camera.apply(sprite))

        for sprite in self.all_sprites:
            if isinstance(sprite,Mob):
                sprite.draw_health()

            self.screen.blit(sprite.image,self.camera.apply(sprite))

        draw_player_health(self.screen,self.camera.apply(self.player).centerx - 50,self.camera.apply(self.player).centery - 40,self.player.health / PLAYER_HEALTH)


        if self.night:
            self.render_fog()
        self.draw_text('Zombies: {}'.format(len(self.mobs)), 'Impacted2.0.ttf', 30, WHITE,
                       WIDTH - 100, 100, align="ne")
        self.draw_text('Wave: {}'.format(self.wave), 'Impacted2.0.ttf', 30, WHITE,
                       WIDTH - 1211, 100, align="ne")
        if self.paused:
            self.screen.blit(self.dim_screen,(0,0))
            self.draw_text('Paused','ZOMBIE.TTF',105,RED,WIDTH / 2,HEIGHT / 2,align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused






    def help_screen(self):
        self.screen.fill(BLACK)
        print('joke')
        self.draw_text('Help','ZOMBIE.TTF',109,RED,WIDTH/2,140*1,align='center')
        self.draw_text('Arrow keys to move', 'ZOMBIE.TTF', 50, RED, WIDTH / 2, 140 * 2, align='center')
        self.draw_text('Space or Mouse click to Shoot', 'ZOMBIE.TTF', 50, RED, WIDTH / 2, 140 * 2.45, align='center')
        self.draw_text('Kill all Zombies to Win', 'ZOMBIE.TTF', 50, RED, WIDTH / 2, 140 * 2.85, align='center')
        self.draw_text('Programmer Divyansh Singh Kshatriya', 'ZOMBIE.TTF', 50, RED, WIDTH / 2, 140 * 3.45, align='center')
        self.draw_text('Art by Yuvraj Singh Kshatriya', 'ZOMBIE.TTF', 50, RED, WIDTH / 2, 140 * 3.85,
                       align='center')
        self.outline_rect = pg.draw.rect(self.screen,WHITE,[60,HEIGHT-100,130,100])
        self.back_button = pg.draw.rect(self.screen,RED,[60,HEIGHT-100,130,100])
        pg.display.flip()
        pg.event.wait()





    def show_start_screen(self):
        global PLAYER_IMG
        game_folder = path.dirname(__file__)
        self.screen.fill(BLACK)
        self.draw_text('ZOMBIE SHOOTER GAME', 'ZOMBIE.TTF', 105, WHITE, WIDTH / 2, 140, align="center")
        self.outline_rect = pg.draw.rect(self.screen,WHITE,[WIDTH/3,140*3-22,450,105-20],2)
        self.start_button = pg.draw.rect(self.screen,BLACK,[466,140*3,433,105- 45])
        self.help_outline_rect = pg.draw.rect(self.screen, WHITE, [WIDTH / 6+220, 140 * 4 - 22, 450, 105 - 20], 2)
        self.help_button = pg.draw.rect(self.screen, BLACK, [WIDTH/6+220, 140 * 4, 433, 105 - 45])
        self.draw_text('HELP', 'ZOMBIE.TTF', 105, WHITE, WIDTH / 3+100, 140 * 4 - 22, align="nw")
        self.draw_text('Settings', 'ZOMBIE.TTF', 79, WHITE, 90 , 140 * 2 - 22, align="nw")
        self.draw_text('Map 1','ZOMBIE.TTF',int(60),WHITE,1100, 145 * 3,align='center')
        self.map_choose_1 = pg.draw.rect(self.screen,WHITE ,[960, 135 * 3, 300, 125 - 45],2)
        self.draw_text('Map 2', 'ZOMBIE.TTF', int(60), WHITE, 1100, 145 * 4, align='center')
        self.map_choose_2 = pg.draw.rect(self.screen, WHITE, [960, 135 * 4, 300, 125 - 45], 2)
        self.draw_text('more levels coming soon', 'ZOMBIE.TTF', int(60), WHITE, 700, 145 * 5, align='center')
        #self.map_choose_3 = pg.draw.rect(self.screen, WHITE, [960, 135 * 5, 300, 125 - 45], 2)
        self.settings_outline_rect4 = pg.draw.rect(self.screen, WHITE, [91 - 20, 140 * 3 - 22, 333, 105 - 20], 2)
        self.settings_button4 = pg.draw.rect(self.screen, BLACK, [91, 140 * 3, 222, 105 - 45])
        self.settings_outline_rect5 = pg.draw.rect(self.screen, WHITE, [91 - 20, 140 * 4 - 22, 333, 105 - 20], 2)
        self.settings_button5 = pg.draw.rect(self.screen, BLACK, [91, 140 * 4, 222, 105 - 45])
        self.draw_text('night mode', 'ZOMBIE.TTF', 49, WHITE,91, 140 * 3 - 22, align="nw")
        self.draw_text('Zombie vision', 'ZOMBIE.TTF', 49, WHITE, 91-15, 140 * 4 - 22, align="nw")
        self.draw_text('START', 'ZOMBIE.TTF', 105, WHITE, WIDTH/3+80,140*3-22, align="nw")

        pg.display.flip()
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if self.start_button.collidepoint(pos):
                        waiting = False
                        self.doom = pg.mixer.music.load('Doom_classic.mp3')
                        pg.mixer.music.play(-1)

                    if self.help_button.collidepoint(pos):
                        self.help_screen()
                    if self.settings_button4.collidepoint(pos):
                       self.night = not self.night
                    if self.settings_button5.collidepoint(pos):

                       self.effects = pg.BLEND_MIN
                    if self.map_choose_1.collidepoint(pos):
                        self.map = Map(path.join(game_folder, 'map.txt'))
                    if self.map_choose_2.collidepoint(pos):
                        self.map = Map(path.join(game_folder, 'map2.txt'))




                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        waiting = False
                        self.doom = pg.mixer.music.load('Doom_classic.mp3')
                        pg.mixer.music.play(-1)
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                        self.quit()
                    if event.key == pg.K_o:
                        waiting = False
                        self.doom = pg.mixer.music.load('Doom_classic.mp3')
                        pg.mixer.music.play(-1)


    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.effects = pg.BLEND_MULT
        self.draw_text('GAME Over', 'ZOMBIE.TTF', 100, RED, WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text('press a key to start', 'ZOMBIE.TTF', 105, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        self.wave = 1
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False


if __name__ == '__main__':
    # create the game object
    game = Game()
    while True:
        game.show_start_screen()
        game.new()
        game.run()
        game.show_go_screen()