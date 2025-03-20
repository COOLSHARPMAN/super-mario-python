import pygame
import sys
from classes.Dashboard import Dashboard  # 导入Dashboard类
from classes.Level import Level  # 导入Level类
from classes.Menu import Menu  # 导入Menu类
from classes.Sound import Sound  # 导入Sound类
from entities.Mario import Mario  # 导入Mario类
from config.game_config import GameConfig

def main():
    # 加载游戏配置
    config = GameConfig()
    
    # 初始化Pygame
    pygame.init()
    
    # 设置窗口
    window_size = (config.get('window.width'), config.get('window.height'))
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption(config.get('window.title'))
    
    # 尝试初始化音频系统
    try:
        pygame.mixer.init()
        sound_enabled = True
    except pygame.error:
        print("Warning: Audio system not available. Game will run without sound.")
        sound_enabled = False
    
    # 创建游戏对象
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = Sound(sound_enabled)
    level = Level(screen, dashboard, sound_enabled)
    menu = Menu(screen, dashboard, level, sound)
    mario = Mario(0, 0, level, screen, dashboard, sound, config.get('game.gravity'))
    
    # 游戏主循环
    while True:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    if menu.start == 0:  # 在主菜单时
                        if menu.state == 0:  # 选择关卡
                            menu.chooseLevel()
                        elif menu.state == 1:  # 设置
                            menu.inSettings = True
                        elif menu.state == 2:  # 退出
                            pygame.quit()
                            sys.exit()
                    menu.start = 1
                if menu.start == 2:  # 游戏结束时
                    menu.start = 0
                    mario.__init__(0, 0, level, screen, dashboard, sound, config.get('game.gravity'))
                    level.__init__(screen, dashboard, sound_enabled)
        
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

if __name__ == "__main__":
    main()
