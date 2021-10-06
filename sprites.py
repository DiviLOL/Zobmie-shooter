import pygame as pg
from settings import *
from camera import collide_hit_rect
import random
from itertools import chain
import pytweening as tween
vec = pg.math.Vector2


def collide_with_tilemaps(sprite,group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2.0
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2.0
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.0
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2.0
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect2 = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.energy = PLAYER_ENERY
        self.damage = False
        self.weopen = 'pistol'
        self.go = False


    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYERSPEED,0).rotate(-self.rot)

        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYERSPEED / 2, 0).rotate(-self.rot)

        if keys[pg.K_SPACE]:
            self.shoot()


    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEOPENS[self.weopen]['rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BULLET_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEOPENS[self.weopen]['kickback'], 0).rotate(-self.rot)
            for i in range(WEOPENS[self.weopen]['bullet_count']):
                spread = random.uniform(-WEOPENS[self.weopen]['spread'],WEOPENS[self.weopen]['spread'])
                Bullet(self.game, pos, dir.rotate(spread))

            Muzzel_Flashes(self.game, pos)

    def add_health(self,amount):
        self.health += amount
        if self.health > 100:
            self.health = 100

    def hit(self):
        self.damage = True
        self.damage_alpha = chain(ALPHA_DAMAGE * 2)


    def update(self):
        self.get_keys()



        if self.go:
            if self.weopen == 'pistol':
                self.game.player_img = pg.image.load(PLAYER_IMG).convert_alpha()
                keys = pg.key.get_pressed()
                if keys[pg.K_z]:
                    self.weopen = 'shotgun'

            if self.weopen == 'shotgun':
                self.game.player_img = pg.image.load('survivor1_machine.png').convert_alpha()
                keys = pg.key.get_pressed()
                if keys[pg.K_t]:
                    self.weopen = 'pistol'

        self.rot = (self.rot - self.rot_speed * self.game.dt) % 360
        self.pos += self.vel * self.game.dt
        self.image = pg.transform.rotate(self.game.player_img,self.rot)
        if self.damage:
            try:
                self.image.fill((0,255,0,next(self.damage_alpha)),special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damage = False


        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_tilemaps(self,self.game.walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_tilemaps(self,self.game.walls,'y')
        self.rect.center = self.hit_rect.center


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image = game.bullet_img
        self.game = game
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        #spread = random.uniform(-5, 5)
        self.vel = dir * WEOPENS[game.player.weopen]['bullet_speed']
        self.spawntime = pg.time.get_ticks()


    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawntime > WEOPENS[self.game.player.weopen]['bullet_lifetime']:
            self.kill()

class Splat(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.splats
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.splat
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.mob_img
        self.game = game
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x,y) * TILESIZE
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.center = self.pos
        self.rot = 0
        self.score = 0
        self.healths = 100
        self.speed = random.choice(ZOMBIE_SPEED)

    def avoid_zombies(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):

        self.mpos = vec(pg.mouse.get_pos())
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.mob_img,self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1,0).rotate(-self.rot)
        self.avoid_zombies()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5  * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_tilemaps(self,self.game.walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_tilemaps(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        if self.healths <= 0:
            self.kill()
            Splat(self.game,self.pos)




    def draw_health(self):
        if self.healths >= 60:
            col = GREEN
        elif self.healths >= 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.healths / 100)
        self.health_bar = pg.Rect(0,0,width,7)
        if self.healths < 100:
            pg.draw.rect(self.image,col,self.health_bar)



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.tile_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Wall2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.tile_img2
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Wall3(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.tile_img3
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Wall4(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.tile_img4
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Muzzel_Flashes(pg.sprite.Sprite):
    def __init__(self,game,pos):
        self.groups = game.all_sprites, game.muzzle
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        size = random.randint(20,50)
        self.image = pg.transform.scale(random.choice(game.gun_flashes),(size,size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > 100:
            self.kill()

class Items(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.pos = vec(x * TILESIZE, y * TILESIZE)
        self.rect.center = self.pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

class ShotGun(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.shotgun_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.pos = vec(x * TILESIZE, y * TILESIZE)
        self.rect.center = self.pos
        self.tween = tween.easeInOutQuint
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

class Wall7(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites,game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.tile_img
        self.rect = self.image.get_rect()
        self.rect.center = pos
