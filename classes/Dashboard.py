import pygame
import os
from classes.Spritesheet import Spritesheet
from classes.Sound import Sound


class Dashboard:
    def __init__(self, filePath, size, screen):
        # 初始化仪表盘
        self.screen = screen  # 游戏屏幕
        self.size = size  # 字体大小
        self.state = "menu"  # 当前状态
        self.time = 0  # 游戏时间
        self.currentLevel = 1  # 当前关卡
        self.coins = 0  # 金币数量
        self.lives = 3  # 生命值
        self.topScore = 0  # 最高分
        self.score = 0  # 当前分数
        self.levelName = ""  # 关卡名称
        self.spritesheet = Spritesheet(filePath)  # 加载字体图片
        self.loadFont()  # 加载字体
        self.sound = Sound()  # 声音系统
        self.sound.set_volume(0.5)  # 设置音量为50%
        self.sound.play_music()  # 播放背景音乐
        # 添加中文字体支持
        self.chinese_font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", size)

    def loadFont(self):
        # 加载字体
        self.charSprites = {}  # 字符精灵字典
        # 加载英文字符
        for i in range(0, 10):  # 数字0-9
            self.charSprites[str(i)] = self.spritesheet.image_at(
                i * self.size, 0, 2, colorkey=[255, 0, 220], ignoreTileSize=True
            )
        # 加载字母A-Z
        for i in range(10, 36):  # 字母A-Z
            self.charSprites[chr(55 + i)] = self.spritesheet.image_at(
                i * self.size, 0, 2, colorkey=[255, 0, 220], ignoreTileSize=True
            )
        # 加载特殊字符
        self.charSprites["-"] = self.spritesheet.image_at(
            36 * self.size, 0, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )
        self.charSprites["*"] = self.spritesheet.image_at(
            37 * self.size, 0, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )
        self.charSprites["!"] = self.spritesheet.image_at(
            38 * self.size, 0, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )
        self.charSprites[" "] = self.spritesheet.image_at(
            39 * self.size, 0, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )

    def drawText(self, text, x, y, size, color=(255,255,255)):
        # 修改中文显示逻辑
        text_surface = self.chinese_font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def createText(self, text, size, color=(255,255,255)):
        # 指定中文字体路径，例如使用系统自带的SimHei.ttf
        font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", size)
        textSurface = font.render(text, True, color)
        return textSurface

    def update(self):
        # 更新仪表盘
        self.drawText("MARIO", 200, 10, 15)
        self.drawText(str(self.score), 200, 25, 15)
        self.drawText("@", 200, 40, 15)
        self.drawText(str(self.coins), 225, 40, 15)
        self.drawText("!*!  " + str(self.lives), 300, 10, 15)
        self.drawText("WORLD " + str(self.levelName), 380, 10, 15)
        self.drawText("1-1", 395, 25, 15)
        self.drawText("TIME", 470, 10, 15)
        self.drawText(str(self.time), 485, 25, 15)
        self.drawText("TOP SCORE", 500, 10, 15)
        self.drawText(str(self.topScore), 500, 25, 15)

    def updateTimer(self):
        # 更新计时器
        if self.state == "start":
            self.time -= 1
            if self.time <= 0:
                self.state = "end"
                self.sound.play_sfx("time_warning", 1)
                self.sound.play_sfx("game_over", 1)

    def updateCoins(self):
        # 更新金币数量
        self.coins += 1
        if self.coins == 100:
            self.lives += 1
            self.coins = 0
            self.sound.play_sfx("extra_life", 1)

    def updateScore(self, points):
        # 更新分数
        self.score += points
        if self.score > self.topScore:
            self.topScore = self.score

    def updateLives(self):
        # 更新生命值
        self.lives -= 1
        if self.lives <= 0:
            self.state = "end"
            self.sound.play_sfx("game_over", 1)
        else:
            self.sound.play_sfx("die", 1)

    def reset(self):
        # 重置仪表盘
        self.state = "menu"
        self.time = 0
        self.currentLevel = 1
        self.coins = 0
        self.lives = 3
        self.score = 0
        self.levelName = ""
