# -*- coding: utf-8 -*-
import json
import sys
import os
import pygame
import random
import math

from classes.Spritesheet import Spritesheet


class Menu:
    def __init__(self, screen, dashboard, level, sound):
        # 初始化菜单
        self.screen = screen  # 游戏屏幕
        self.sound = sound  # 声音系统
        self.start = 0  # 菜单状态：0=主菜单，1=游戏中，2=游戏结束
        self.inSettings = False  # 是否在设置菜单中
        self.state = 0  # 当前选中的菜单项
        self.level = level  # 关卡对象
        self.music = True  # 音乐开关
        self.sfx = True  # 音效开关
        self.currSelectedLevel = 1  # 当前选中的关卡
        self.levelNames = []  # 关卡名称列表
        self.inChoosingLevel = False  # 是否在选择关卡界面
        self.dashboard = dashboard  # 仪表盘对象
        self.levelCount = 0  # 关卡总数
        self.language = "zh"  # 默认语言为中文
        self.spritesheet = Spritesheet("./img/title_screen.png")  # 加载标题屏幕图片
        self.menu_banner = pygame.image.load("./img/chinese_title.png").convert_alpha()
        self.menu_dot = self.spritesheet.image_at(  # 加载菜单选择点
            0, 150, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )
        self.menu_dot2 = self.spritesheet.image_at(  # 加载菜单未选择点
            20, 150, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )

        # 定义菜单文本
        self.menu_texts = {
            "zh": {
                "choose_level": "选择关卡",
                "settings": "设置",
                "exit": "退出",
                "music": "音乐",
                "sfx": "音效",
                "language": "语言",
                "back": "返回",
                "on": "开启",
                "off": "关闭",
                "chinese": "中文",
                "english": "英文",
                "resolution": "分辨率",
                "current_res": "当前分辨率"
            },
            "en": {
                "choose_level": "Choose Level",
                "settings": "Settings",
                "exit": "Exit",
                "music": "Music",
                "sfx": "SFX",
                "language": "Language",
                "back": "Back",
                "on": "ON",
                "off": "OFF",
                "chinese": "Chinese",
                "english": "English"
            }
        }

        # 动画相关属性
        self.animation_timer = 0  # 动画计时器
        self.animation_speed = 0.1  # 动画速度
        self.characters = []  # 角色列表
        self.init_animation_characters()  # 初始化动画角色

        self.loadSettings("./settings.json")  # 加载游戏设置

        self.resolutions = [(800, 600), (1024, 768), (1280, 720)]
        self.current_res_index = 0

    def init_animation_characters(self):
        # 初始化动画角色
        # 马里奥
        mario = {
            'x': 100,
            'y': 400,
            'width': 32,
            'height': 32,
            'speed': 2,
            'direction': 1,
            'jumping': False,
            'jump_speed': 0,
            'gravity': 0.5,
            'sprite': self.level.sprites.spriteCollection.get("mario_idle").image
        }

        # 敌人
        enemies = []
        for i in range(3):
            enemy = {
                'x': 300 + i * 100,
                'y': 400,
                'width': 32,
                'height': 32,
                'speed': 1,
                'direction': -1,
                'sprite': self.level.sprites.spriteCollection.get("goomba-1").image
            }
            enemies.append(enemy)

        self.characters = [mario] + enemies

    def update_animation(self):
        # 更新动画
        self.animation_timer += self.animation_speed

        # 更新马里奥
        mario = self.characters[0]
        # 左右移动
        mario['x'] += mario['speed'] * mario['direction']
        # 到达边界时改变方向
        if mario['x'] < 50 or mario['x'] > 750:
            mario['direction'] *= -1
        # 跳跃
        if not mario['jumping'] and random.random() < 0.01:  # 1%的概率跳跃
            mario['jumping'] = True
            mario['jump_speed'] = -10
        # 应用重力
        if mario['jumping']:
            mario['y'] += mario['jump_speed']
            mario['jump_speed'] += mario['gravity']
            if mario['y'] >= 400:  # 落地
                mario['y'] = 400
                mario['jumping'] = False
                mario['jump_speed'] = 0

        # 更新敌人
        for enemy in self.characters[1:]:
            # 左右移动
            enemy['x'] += enemy['speed'] * enemy['direction']
            # 到达边界时改变方向
            if enemy['x'] < 50 or enemy['x'] > 750:
                enemy['direction'] *= -1
            # 与马里奥互动
            if abs(enemy['x'] - mario['x']) < 50 and abs(enemy['y'] - mario['y']) < 50:
                if mario['jumping']:  # 如果马里奥在跳跃，踩扁敌人
                    enemy['y'] = 450  # 将敌人移出屏幕
                else:  # 如果马里奥在地面，被敌人碰到
                    mario['y'] = 450  # 将马里奥移出屏幕
                    self.sound.play_sfx("die")  # 播放死亡音效

    def draw_animation(self):
        # 绘制动画角色
        for character in self.characters:
            if character['y'] < 450:  # 只绘制在屏幕内的角色
                self.screen.blit(character['sprite'], (character['x'], character['y']))

    def get_text(self, key):
        # 获取当前语言的文本
        return self.menu_texts[self.language][key]

    def loadSettings(self, url):
        # 加载游戏设置
        try:
            with open(url) as jsonData:
                data = json.load(jsonData)
                if data["sound"]:  # 音乐设置
                    self.music = True
                    self.sound.music_channel.play(self.sound.soundtrack, loops=-1)
                else:
                    self.music = False
                if data["sfx"]:  # 音效设置
                    self.sfx = True
                    self.sound.allowSFX = True
                else:
                    self.sound.allowSFX = False
                    self.sfx = False
                if "language" in data:  # 语言设置
                    self.language = data["language"]
        except (IOError, OSError):
            self.music = False
            self.sound.allowSFX = False
            self.sfx = False
            self.saveSettings("./settings.json")

    def saveSettings(self, url):
        # 保存游戏设置
        data = {
            "sound": self.music,
            "sfx": self.sfx,
            "language": self.language
        }
        with open(url, "w") as outfile:
            json.dump(data, outfile)

    def drawMenu(self):
        # 绘制主菜单
        self.drawDot()  # 绘制选择点
        self.dashboard.drawText(self.get_text("choose_level"), 180, 280, 24, (255,255,255))
        self.dashboard.drawText(self.get_text("settings"), 180, 320, 24, (255,255,255))
        self.dashboard.drawText(self.get_text("exit"), 180, 360, 24, (255,255,255))

    def drawMenuBackground(self, withBanner=True):
        # 绘制菜单背景
        # 绘制天空背景
        for y in range(0, 13):
            for x in range(0, 20):
                self.screen.blit(
                    self.level.sprites.spriteCollection.get("sky").image,
                    (x * 32, y * 32),
                )
        # 绘制地面
        for y in range(13, 15):
            for x in range(0, 20):
                self.screen.blit(
                    self.level.sprites.spriteCollection.get("ground").image,
                    (x * 32, y * 32),
                )
        # 绘制标题横幅
        if withBanner:
            self.screen.blit(self.menu_banner, (150, 80))
        # 绘制装饰元素
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_1").image, (14 * 32, 12 * 32)
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_2").image, (15 * 32, 12 * 32)
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_2").image, (16 * 32, 12 * 32)
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_2").image, (17 * 32, 12 * 32)
        )
        self.screen.blit(
            self.level.sprites.spriteCollection.get("bush_3").image, (18 * 32, 12 * 32)
        )

        # 绘制动画角色
        if not self.inSettings and not self.inChoosingLevel:
            self.update_animation()
            self.draw_animation()

    def drawSettings(self):
        # 绘制设置菜单
        self.drawDot()  # 绘制选择点
        self.dashboard.drawText(self.get_text("music"), 180, 280, 24)
        if self.music:
            self.dashboard.drawText(self.get_text("on"), 340, 280, 24)
        else:
            self.dashboard.drawText(self.get_text("off"), 340, 280, 24)
        self.dashboard.drawText(self.get_text("sfx"), 180, 320, 24)
        if self.sfx:
            self.dashboard.drawText(self.get_text("on"), 340, 320, 24)
        else:
            self.dashboard.drawText(self.get_text("off"), 340, 320, 24)
        self.dashboard.drawText(self.get_text("language"), 180, 360, 24)
        if self.language == "zh":
            self.dashboard.drawText(self.get_text("chinese"), 340, 360, 24)
        else:
            self.dashboard.drawText(self.get_text("english"), 340, 360, 24)
        self.dashboard.drawText(self.get_text("resolution"), 180, 400, 24)
        self.dashboard.drawText(f"{self.resolutions[self.current_res_index][0]}x{self.resolutions[self.current_res_index][1]}", 340, 400, 24)
        self.dashboard.drawText(self.get_text("back"), 180, 440, 24)

    def drawDot(self):
        # 绘制菜单选择点
        if self.state == 0:  # 选择关卡选项
            self.screen.blit(self.menu_dot, (145, 273))
            self.screen.blit(self.menu_dot2, (145, 313))
            self.screen.blit(self.menu_dot2, (145, 353))
            self.screen.blit(self.menu_dot2, (145, 393))
        elif self.state == 1:  # 设置选项
            self.screen.blit(self.menu_dot, (145, 313))
            self.screen.blit(self.menu_dot2, (145, 273))
            self.screen.blit(self.menu_dot2, (145, 353))
            self.screen.blit(self.menu_dot2, (145, 393))
        elif self.state == 2:  # 退出选项
            self.screen.blit(self.menu_dot, (145, 353))
            self.screen.blit(self.menu_dot2, (145, 273))
            self.screen.blit(self.menu_dot2, (145, 313))
            self.screen.blit(self.menu_dot2, (145, 393))
        elif self.state == 3:  # 返回选项
            self.screen.blit(self.menu_dot, (145, 393))
            self.screen.blit(self.menu_dot2, (145, 273))
            self.screen.blit(self.menu_dot2, (145, 313))
            self.screen.blit(self.menu_dot2, (145, 353))

    def chooseLevel(self):
        # 进入关卡选择界面
        self.drawMenuBackground(False)  # 绘制不带横幅的背景
        self.inChoosingLevel = True  # 设置状态为选择关卡
        self.levelNames = self.loadLevelNames()  # 加载关卡名称
        self.drawLevelChooser()  # 绘制关卡选择器

    def drawBorder(self, x, y, width, height, color, thickness):
        # 绘制边框
        pygame.draw.rect(self.screen, color, (x, y, width, thickness))  # 上边框
        pygame.draw.rect(self.screen, color, (x, y + width, width, thickness))  # 下边框
        pygame.draw.rect(self.screen, color, (x, y, thickness, width))  # 左边框
        pygame.draw.rect(self.screen, color, (x + width, y, thickness, width + thickness))  # 右边框

    def drawLevelChooser(self):
        # 绘制关卡选择器
        j = 0
        offset = 75  # 边框偏移量
        textOffset = 90  # 文本偏移量
        for i, levelName in enumerate(self.loadLevelNames()):
            if self.currSelectedLevel == i + 1:  # 当前选中的关卡
                color = (255, 255, 255)  # 白色
            else:
                color = (150, 150, 150)  # 灰色
            if i < 3:  # 第一行关卡
                self.dashboard.drawText(levelName, 175 * i + textOffset, 100, 12)
                self.drawBorder(175 * i + offset, 55, 125, 75, color, 5)
            else:  # 第二行关卡
                self.dashboard.drawText(levelName, 175 * j + textOffset, 250, 12)
                self.drawBorder(175 * j + offset, 210, 125, 75, color, 5)
                j += 1

    def loadLevelNames(self):
        # 加载关卡名称列表
        files = []
        res = []
        for r, d, f in os.walk("./levels"):  # 遍历levels目录
            for file in f:
                files.append(os.path.join(r, file))
        for f in files:
            res.append(os.path.split(f)[1].split(".")[0])  # 提取关卡名称
        self.levelCount = len(res)  # 更新关卡总数
        return res

    def checkInput(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                # 添加调试输出
                print(f"Key pressed: {pygame.key.name(event.key)}")
                
                # 修复方向键处理
                if event.key in [pygame.K_UP, pygame.K_w]:  # 上
                    self.state = max(0, self.state - 1)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:  # 下
                    self.state = min(2, self.state + 1)
                    
                # 修复回车键处理
                elif event.key == pygame.K_RETURN:
                    if self.state == 0:  # 开始游戏
                        self.start = 1
                    elif self.state == 1:  # 设置
                        self.inSettings = True
                    elif self.state == 2:  # 退出
                        pygame.quit()
                        sys.exit()

    def update(self):
        # 更新菜单状态

        self.checkInput()  # 检查输入
        if self.inChoosingLevel:  # 如果正在选择关卡
            return

        self.drawMenuBackground()  # 绘制菜单背景
        self.dashboard.update()  # 更新仪表盘

        if not self.inSettings:  # 如果不在设置菜单中
            self.drawMenu()  # 绘制主菜单
        else:
            self.drawSettings()  # 绘制设置菜单