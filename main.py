import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.mute = False
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.kills = 0
        self.deaths = 0
        self.spawn_time = 150
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        pg.mixer.music.load(path.join(self.snd_folder, "bg_music.ogg"))
        if not self.mute:
            pg.mixer.music.play(-1)
        pg.display.set_icon(self.mob_img)

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, "img")
        self.snd_folder = path.join(self.game_folder, "snd")
        self.map_folder = path.join(self.game_folder, "maps")
        self.player_img = pg.image.load(path.join(self.img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(self.img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(self.img_folder, MOB_IMG)).convert_alpha()
        self.mob_splat = pg.image.load(path.join(self.img_folder, MOB_SPLAT)).convert_alpha()
        self.mob_splat = pg.transform.scale(self.mob_splat, (TILESIZE, TILESIZE))
        self.wall_img = pg.image.load(path.join(self.img_folder, WALL_IMG)).convert_alpha()
        self.effects_sounds = {}
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.weapon_sounds = {}
        self.grass_tile = pg.image.load(path.join(self.img_folderGRASS_IMG)).convert_alpha()
        self.grass_tile = pg.transform.scale(self.grass_tile, (64, 64))
        self.bg = pg.Surface([WIDTH, HEIGHT])
        for x in range(WIDTH):
            for y in range(HEIGHT):
                self.bg.blit(self.grass_tile, (x * 64, y * 64))
        with open("save.txt", "r") as f:
            try:
                self.map_no = int(f.read())
            except:
                self.map_no = 1
        self.map = Map(path.join(self.map_folder,'map' + str(self.map_no) + '.txt'))
        self.gun_flashes = []
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(self.img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(img).convert_alpha())
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(LIGHT_MASK).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, (500,500))
        self.light_rect = self.light_mask.get_rect()
        self.zombie_moan_sounds = []
        s = pg.mixer.Sound(path.join(self.snd_folder, "zombie-roar1.wav"))
        s.set_volume(0.4)
        self.zombie_moan_sounds.append(s)
        self.zombie_atack_sound = pg.mixer.Sound(path.join(self.snd_folder, ZOMBIE_HIT_SOUND))
        self.zombie_atack_sound.set_volume(0.5)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.GRASS_TILE = pg.image.load("grass.png").convert()
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.targets = pg.sprite.Group()
        self.health_packs = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == "H":
                    self.health_pack = HealthPack(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)
        self.minimap = pg.Surface((75,75))
        self.minimap.fill(WHITE)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.dead = []
        self.all_sprites.update()
        for mob in self.mobs:
            if mob in self.dead:
                mob.remove(self.all_sprites)
        self.camera.update(self.player)
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if not self.mute:
                self.zombie_atack_sound.play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.deaths += 1
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            # hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
                if mob.health <= 0:
                    mob.image = self.mob_splat
                    self.dead.append(mob)
            mob.vel = vec(0, 0)
        hit = pg.sprite.spritecollide(self.player, self.health_packs, True)
        if hit:
            self.player.health += NUM_HEAL
        if len(self.mobs) == 0:
            self.map_no += 1
            with open("save.txt", "w") as f:
                f.write(str(self.map_no))
            self.new()
        pg.draw.circle(self.minimap, BLUE, (int(self.player.hit_rect.x / 8), int(self.player.hit_rect.y)), 5)
        for mob in self.mobs:
            pg.draw.circle(self.minimap, RED, (int(mob.rect.x / 8), int(mob.rect.y)), 5)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.blit(self.bg, (0,0))
        font = pg.font.SysFont("comicsansms", 25)
        text = font.render("Mobs left: " + str(len(self.mobs)), False, WHITE)
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions
        self.render_fog()
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.screen.blit(text, (0, 40))
        for dead in self.dead:
            self.screen.blit(self.mob_splat, dead.pos)
        pg.display.update()
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_m:
                    if not self.mute:
                        self.mute = True
                        pg.mixer.music.pause()
                    else:
                        self.mute = False
                        pg.mixer.music.unpause()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        font = pg.font.Font("ZOMBIE.TTF", 50)
        text = font.render("R I S E  O F  T H E  Z O M B I E S", False, RED)
        text_rect = text.get_rect()
        text_rect.center = (int(WIDTH/ 2), int(HEIGHT / 2))
        self.screen.blit(text, text_rect)
        true = True
        pg.display.flip()
        while true:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    true = False
                if event.type == pg.QUIT:
                    pg.quit()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        font = pg.font.SysFont("comicsansms", 50)
        text = font.render("Kills: " + str(self.kills), False, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (int(WIDTH / 2), int(HEIGHT / 2))
        self.screen.blit(text, text_rect)
        text = font.render("Deaths: " + str(self.deaths), False, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (int(WIDTH / 2), int(HEIGHT / 2 + 55))
        self.screen.blit(text, text_rect)
        true = True
        pg.display.flip()
        while true:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    true = False
                if event.type == pg.QUIT:
                    pg.quit()

    def choose_weapon(self):
        self.screen.fill(BLACK)
        font = pg.font.SysFont("comicsansms", 50)
        text = font.render("Choose your weapon (P: pistol, S: shotgun, A: Assault Riffle)", False, WHITE)
        rect = text.get_rect()
        rect.center = (WIDTH / 2, HEIGHT / 2)
        self.screen.blit(text, rect)
        pg.display.update()
        true = True
        while true:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    true = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.weapon = "pistol"
                        true = False
                    if event.key == pg.K_s:
                        self.weapon = "shotgun"
                        true = False
                    if event.key == pg.K_a:
                        self.weapon = "AR"
                        true = False

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

# create the game object
g = Game()
g.show_start_screen()
g.choose_weapon()
while True:
    g.new()
    g.run()
    g.show_go_screen()
