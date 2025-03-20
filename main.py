import pygame
import sys
from classes.Dashboard import Dashboard  # 导入仪表盘类
from classes.Level import Level  # 导入关卡类
from classes.Menu import Menu  # 导入菜单类
from classes.Sound import Sound  # 导入声音类
from entities.Mario import Mario  # 导入马里奥角色类
from config.game_config import GameConfig  # 导入游戏配置类

def main():
    # 加载游戏配置
    config = GameConfig()
    
    # 初始化Pygame游戏引擎
    pygame.init()
    
    # 设置游戏窗口
    window_size = (config.get('window.width'), config.get('window.height'))
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption(config.get('window.title'))
    
    # 尝试初始化音频系统
    try:
        pygame.mixer.init()
        sound_enabled = True
    except pygame.error:
        print("警告：无法初始化音频系统。游戏将在无声模式下运行。")
        sound_enabled = False
    
    # 创建游戏核心对象
    dashboard = Dashboard("./img/font.png", 8, screen)  # 创建仪表盘
    sound = Sound(sound_enabled)  # 创建声音系统
    level = Level(screen, dashboard, sound_enabled)  # 创建关卡
    menu = Menu(screen, dashboard, level, sound)  # 创建菜单
    mario = Mario(0, 0, level, screen, dashboard, sound, config.get('game.gravity'))  # 创建马里奥角色
    
    # 游戏主循环
    clock = pygame.time.Clock()
    while True:
        # 清空屏幕
        screen.fill((0, 0, 0))
        
        # 处理游戏事件（简化事件处理）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 更新游戏状态
        if menu.start == 0:  # 显示主菜单
            menu.update()
        elif menu.start == 1:  # 游戏进行中
            level.drawLevel(mario.camera, mario)
            dashboard.update()
            mario.update()
        elif menu.start == 2:  # 显示游戏结束菜单
            menu.draw()
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
