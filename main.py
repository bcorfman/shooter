import pyxel
from core.pyxel_ext import Sprite, MoveDelta, PingPongMode, Delay, Delete

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

NUM_STARS = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5

ENEMY_WIDTH = 8
ENEMY_HEIGHT = 8

WINDOW_WIDTH = 120
WINDOW_HEIGHT = 160

enemies = []


def update_entities(entities):
    for entity in entities:
        entity.update()


def draw_entities(entities):
    for entity in entities:
        entity.draw()


class Background:
    def __init__(self):
        self.stars = []
        for _ in range(NUM_STARS):
            self.stars.append(
                (
                    pyxel.rndi(0, pyxel.width - 1),
                    pyxel.rndi(0, pyxel.height - 1),
                    pyxel.rndf(1, 2.5),
                )
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.stars):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.stars[i] = (x, y, speed)

    def draw(self):
        for x, y, speed in self.stars:
            pyxel.pset(x, y, STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW)


class Enemy(Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.is_alive = True
        self.do(MoveDelta((60, 0), secs=1, mode=PingPongMode))
        self.do(Delay())

    def update(self):
        if self.y > pyxel.height - 1:
            self.is_alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, self.w * self.dir, self.h, 0)


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Space Shooter")
        self.scene = SCENE_TITLE
        pyxel.images[0].set(
            0,
            0,
            [
                "00c00c00",
                "0c7007c0",
                "0c7007c0",
                "c703b07c",
                "77033077",
                "785cc587",
                "85c77c58",
                "0c0880c0",
            ],
        )
        pyxel.images[0].set(
            8,
            0,
            [
                "00088000",
                "00ee1200",
                "08e2b180",
                "02882820",
                "00222200",
                "00012280",
                "08208008",
                "80008000",
            ],
        )
        self.background = Background()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        self.background.update()
        self.update_play_scene()

    def update_play_scene(self):
        if pyxel.frame_count % 6 == 0:
            loc_x, loc_y = pyxel.rndi(0, pyxel.width - ENEMY_WIDTH), 0
            ship = Enemy(loc_x, loc_y)
            enemies.append(ship)

        update_entities(enemies)

    def draw(self):
        pyxel.cls(0)
        self.background.draw()
        self.draw_play_scene()

    def draw_play_scene(self):
        draw_entities(enemies)


App()
