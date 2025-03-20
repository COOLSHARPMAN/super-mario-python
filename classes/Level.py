import json
import pygame

from classes.Sprites import Sprites
from classes.Tile import Tile
from entities.Coin import Coin
from entities.CoinBrick import CoinBrick
from entities.Goomba import Goomba
from entities.Mushroom import RedMushroom
from entities.Koopa import Koopa
from entities.CoinBox import CoinBox
from entities.RandomBox import RandomBox


class Level:
    def __init__(self, screen, sound, dashboard):
        self.sprites = Sprites()
        self.dashboard = dashboard
        self.sound = sound
        self.screen = screen
        self.level = None
        self.levelLength = 0
        self.entityList = []
        # 添加精灵组
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        # 视口范围
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = screen.get_width()
        self.viewport_height = screen.get_height()

    def loadLevel(self, levelname):
        with open("./levels/{}.json".format(levelname)) as jsonData:
            data = json.load(jsonData)
            self.loadLayers(data)
            self.loadObjects(data)
            self.loadEntities(data)
            self.levelLength = data["length"]

    def loadEntities(self, data):
        try:
            [self.addCoinBox(x, y) for x, y in data["level"]["entities"]["CoinBox"]]
            [self.addGoomba(x, y) for x, y in data["level"]["entities"]["Goomba"]]
            [self.addKoopa(x, y) for x, y in data["level"]["entities"]["Koopa"]]
            [self.addCoin(x, y) for x, y in data["level"]["entities"]["coin"]]
            [self.addCoinBrick(x, y) for x, y in data["level"]["entities"]["coinBrick"]]
            [self.addRandomBox(x, y, item) for x, y, item in data["level"]["entities"]["RandomBox"]]
        except:
            # if no entities in Level
            pass

    def loadLayers(self, data):
        layers = []
        for x in range(*data["level"]["layers"]["sky"]["x"]):
            layers.append(
                (
                        [
                            Tile(self.sprites.spriteCollection.get("sky"), None)
                            for y in range(*data["level"]["layers"]["sky"]["y"])
                        ]
                        + [
                            Tile(
                                self.sprites.spriteCollection.get("ground"),
                                pygame.Rect(x * 32, (y - 1) * 32, 32, 32),
                            )
                            for y in range(*data["level"]["layers"]["ground"]["y"])
                        ]
                )
            )
        self.level = list(map(list, zip(*layers)))

    def loadObjects(self, data):
        for x, y in data["level"]["objects"]["bush"]:
            self.addBushSprite(x, y)
        for x, y in data["level"]["objects"]["cloud"]:
            self.addCloudSprite(x, y)
        for x, y, z in data["level"]["objects"]["pipe"]:
            self.addPipeSprite(x, y, z)
        for x, y in data["level"]["objects"]["sky"]:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("sky"), None)
        for x, y in data["level"]["objects"]["ground"]:
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("ground"),
                pygame.Rect(x * 32, y * 32, 32, 32),
            )

    def updateEntities(self, cam):
        # 更新视口位置
        self.viewport_x = int(cam.pos.x)
        self.viewport_y = int(cam.pos.y)
        
        # 只更新在视口内的实体
        for entity in self.entityList:
            if self.isInViewport(entity):
                entity.update(cam)
                if entity.alive is None:
                    self.entityList.remove(entity)
                    if entity in self.all_sprites:
                        self.all_sprites.remove(entity)
                    if entity in self.enemies:
                        self.enemies.remove(entity)
                    if entity in self.items:
                        self.items.remove(entity)
                    if entity in self.blocks:
                        self.blocks.remove(entity)

    def isInViewport(self, entity):
        # 检查实体是否在视口内
        entity_rect = entity.rect
        return (entity_rect.right > self.viewport_x and 
                entity_rect.left < self.viewport_x + self.viewport_width and
                entity_rect.bottom > self.viewport_y and 
                entity_rect.top < self.viewport_y + self.viewport_height)

    def drawLevel(self, camera):
        try:
            # 只绘制视口内的内容
            start_x = max(0, int(camera.pos.x))
            end_x = min(self.levelLength, int(camera.pos.x + self.viewport_width // 32 + 1))
            start_y = 0
            end_y = min(15, int(self.viewport_height // 32 + 1))

            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    if self.level[y][x].sprite is not None:
                        if self.level[y][x].sprite.redrawBackground:
                            self.screen.blit(
                                self.sprites.spriteCollection.get("sky").image,
                                ((x + camera.pos.x) * 32, y * 32),
                            )
                        self.level[y][x].sprite.drawSprite(
                            x + camera.pos.x, y, self.screen
                        )
            
            # 使用精灵组绘制实体
            self.all_sprites.draw(self.screen)
            self.updateEntities(camera)
        except IndexError:
            return

    def addCloudSprite(self, x, y):
        try:
            for yOff in range(0, 2):
                for xOff in range(0, 3):
                    self.level[y + yOff][x + xOff] = Tile(
                        self.sprites.spriteCollection.get("cloud{}_{}".format(yOff + 1, xOff + 1)), None, )
        except IndexError:
            return

    def addPipeSprite(self, x, y, length=2):
        try:
            # add pipe head
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("pipeL"),
                pygame.Rect(x * 32, y * 32, 32, 32),
            )
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("pipeR"),
                pygame.Rect((x + 1) * 32, y * 32, 32, 32),
            )
            # add pipe body
            for i in range(1, length + 20):
                self.level[y + i][x] = Tile(
                    self.sprites.spriteCollection.get("pipe2L"),
                    pygame.Rect(x * 32, (y + i) * 32, 32, 32),
                )
                self.level[y + i][x + 1] = Tile(
                    self.sprites.spriteCollection.get("pipe2R"),
                    pygame.Rect((x + 1) * 32, (y + i) * 32, 32, 32),
                )
        except IndexError:
            return

    def addBushSprite(self, x, y):
        try:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("bush_1"), None)
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("bush_2"), None
            )
            self.level[y][x + 2] = Tile(
                self.sprites.spriteCollection.get("bush_3"), None
            )
        except IndexError:
            return

    def addCoinBox(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        coin_box = CoinBox(
            self.screen,
            self.sprites.spriteCollection,
            x,
            y,
            self.sound,
            self.dashboard,
        )
        self.entityList.append(coin_box)
        self.all_sprites.add(coin_box)
        self.blocks.add(coin_box)

    def addRandomBox(self, x, y, item):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        random_box = RandomBox(
            self.screen,
            self.sprites.spriteCollection,
            x,
            y,
            item,
            self.sound,
            self.dashboard,
            self
        )
        self.entityList.append(random_box)
        self.all_sprites.add(random_box)
        self.blocks.add(random_box)

    def addCoin(self, x, y):
        coin = Coin(self.screen, self.sprites.spriteCollection, x, y)
        self.entityList.append(coin)
        self.all_sprites.add(coin)
        self.items.add(coin)

    def addCoinBrick(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        coin_brick = CoinBrick(
            self.screen,
            self.sprites.spriteCollection,
            x,
            y,
            self.sound,
            self.dashboard
        )
        self.entityList.append(coin_brick)
        self.all_sprites.add(coin_brick)
        self.blocks.add(coin_brick)

    def addGoomba(self, x, y):
        goomba = Goomba(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        self.entityList.append(goomba)
        self.all_sprites.add(goomba)
        self.enemies.add(goomba)

    def addKoopa(self, x, y):
        koopa = Koopa(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        self.entityList.append(koopa)
        self.all_sprites.add(koopa)
        self.enemies.add(koopa)

    def addRedMushroom(self, x, y):
        mushroom = RedMushroom(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        self.entityList.append(mushroom)
        self.all_sprites.add(mushroom)
        self.items.add(mushroom)
