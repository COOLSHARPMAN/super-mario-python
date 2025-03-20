import pygame
import json
import os
from config.game_config import GameConfig

class LevelEditor:
    def __init__(self):
        pygame.init()
        self.config = GameConfig()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Super Mario Level Editor")
        
        # 加载精灵
        self.sprites = {
            'ground': pygame.image.load('./img/ground.png'),
            'sky': pygame.image.load('./img/sky.png'),
            'bush_1': pygame.image.load('./img/bush_1.png'),
            'bush_2': pygame.image.load('./img/bush_2.png'),
            'bush_3': pygame.image.load('./img/bush_3.png'),
            'cloud_1_1': pygame.image.load('./img/cloud_1_1.png'),
            'cloud_1_2': pygame.image.load('./img/cloud_1_2.png'),
            'cloud_1_3': pygame.image.load('./img/cloud_1_3.png'),
            'cloud_2_1': pygame.image.load('./img/cloud_2_1.png'),
            'cloud_2_2': pygame.image.load('./img/cloud_2_2.png'),
            'cloud_2_3': pygame.image.load('./img/cloud_2_3.png'),
            'pipeL': pygame.image.load('./img/pipeL.png'),
            'pipeR': pygame.image.load('./img/pipeR.png'),
            'pipe2L': pygame.image.load('./img/pipe2L.png'),
            'pipe2R': pygame.image.load('./img/pipe2R.png'),
            'coin': pygame.image.load('./img/coin.png'),
            'mushroom': pygame.image.load('./img/mushroom.png'),
            'star': pygame.image.load('./img/star.png'),
            'goomba': pygame.image.load('./img/goomba.png'),
            'koopa': pygame.image.load('./img/koopa.png'),
            'coin_box': pygame.image.load('./img/coin_box.png'),
            'random_box': pygame.image.load('./img/random_box.png'),
            'coin_brick': pygame.image.load('./img/coin_brick.png'),
            'platform': pygame.image.load('./img/platform.png'),
            'spike': pygame.image.load('./img/spike.png'),
            'spring': pygame.image.load('./img/spring.png'),
            'checkpoint': pygame.image.load('./img/checkpoint.png'),
            'flag': pygame.image.load('./img/flag.png'),
        }
        
        # 编辑器状态
        self.current_tile = 'ground'
        self.current_layer = 'ground'
        self.current_entity = None
        self.grid_size = 32
        self.scroll_x = 0
        self.scroll_y = 0
        self.selected_tool = 'tile'  # tile, entity, special
        self.level_data = {
            "length": 100,
            "level": {
                "layers": {
                    "sky": {"x": [0, 100], "y": [0, 2]},
                    "ground": {"x": [0, 100], "y": [2, 15]}
                },
                "objects": {
                    "bush": [],
                    "cloud": [],
                    "pipe": [],
                    "sky": [],
                    "ground": [],
                    "platform": [],
                    "spike": [],
                    "spring": [],
                    "checkpoint": [],
                    "flag": []
                },
                "entities": {
                    "CoinBox": [],
                    "Goomba": [],
                    "Koopa": [],
                    "coin": [],
                    "coinBrick": [],
                    "RandomBox": [],
                    "Mushroom": [],
                    "Star": [],
                    "MovingPlatform": [],
                    "FallingPlatform": [],
                    "SpikeTrap": [],
                    "SpringPlatform": []
                },
                "special_effects": {
                    "wind_zones": [],
                    "speed_zones": [],
                    "gravity_zones": [],
                    "checkpoints": [],
                    "powerup_spawns": []
                }
            }
        }
        
        # 工具栏
        self.toolbar_width = 200
        self.toolbar_height = 600
        self.toolbar_rect = pygame.Rect(600, 0, self.toolbar_width, self.toolbar_height)
        
        # 颜色
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        
        # 字体
        self.font = pygame.font.Font(None, 24)

    def draw_toolbar(self):
        pygame.draw.rect(self.screen, self.GRAY, self.toolbar_rect)
        
        # 绘制工具选择按钮
        tools = ['tile', 'entity', 'special']
        y = 10
        for tool in tools:
            color = self.GREEN if self.selected_tool == tool else self.WHITE
            text = self.font.render(tool.capitalize(), True, color)
            self.screen.blit(text, (610, y))
            y += 30
        
        y += 20
        
        # 根据选择的工具显示不同的选项
        if self.selected_tool == 'tile':
            # 绘制当前选择的图块
            self.screen.blit(self.sprites[self.current_tile], (610, y))
            y += 40
            
            # 绘制图块选择按钮
            for tile_name in self.sprites.keys():
                if tile_name in ['ground', 'sky', 'bush_1', 'bush_2', 'bush_3', 
                               'cloud_1_1', 'cloud_1_2', 'cloud_1_3',
                               'cloud_2_1', 'cloud_2_2', 'cloud_2_3',
                               'pipeL', 'pipeR', 'pipe2L', 'pipe2R']:
                    button_rect = pygame.Rect(610, y, 32, 32)
                    pygame.draw.rect(self.screen, self.WHITE, button_rect)
                    self.screen.blit(self.sprites[tile_name], (610, y))
                    if pygame.mouse.get_pos()[0] >= 610 and pygame.mouse.get_pos()[0] <= 642 and \
                       pygame.mouse.get_pos()[1] >= y and pygame.mouse.get_pos()[1] <= y + 32:
                        if pygame.mouse.get_pressed()[0]:
                            self.current_tile = tile_name
                    y += 40
                    
        elif self.selected_tool == 'entity':
            # 绘制实体选择按钮
            entities = ['coin', 'mushroom', 'star', 'goomba', 'koopa', 
                       'coin_box', 'random_box', 'coin_brick']
            for entity in entities:
                button_rect = pygame.Rect(610, y, 32, 32)
                pygame.draw.rect(self.screen, self.WHITE, button_rect)
                self.screen.blit(self.sprites[entity], (610, y))
                if pygame.mouse.get_pos()[0] >= 610 and pygame.mouse.get_pos()[0] <= 642 and \
                   pygame.mouse.get_pos()[1] >= y and pygame.mouse.get_pos()[1] <= y + 32:
                    if pygame.mouse.get_pressed()[0]:
                        self.current_entity = entity
                y += 40
                
        elif self.selected_tool == 'special':
            # 绘制特殊效果选择按钮
            specials = ['platform', 'spike', 'spring', 'checkpoint', 'flag']
            for special in specials:
                button_rect = pygame.Rect(610, y, 32, 32)
                pygame.draw.rect(self.screen, self.WHITE, button_rect)
                self.screen.blit(self.sprites[special], (610, y))
                if pygame.mouse.get_pos()[0] >= 610 and pygame.mouse.get_pos()[0] <= 642 and \
                   pygame.mouse.get_pos()[1] >= y and pygame.mouse.get_pos()[1] <= y + 32:
                    if pygame.mouse.get_pressed()[0]:
                        self.current_entity = special
                y += 40

    def draw_grid(self):
        for x in range(0, 800 - self.toolbar_width, self.grid_size):
            pygame.draw.line(self.screen, self.WHITE, (x, 0), (x, 600), 1)
        for y in range(0, 600, self.grid_size):
            pygame.draw.line(self.screen, self.WHITE, (0, y), (800 - self.toolbar_width, y), 1)

    def save_level(self, filename):
        os.makedirs('levels', exist_ok=True)
        with open(f'levels/{filename}.json', 'w') as f:
            json.dump(self.level_data, f, indent=4)

    def load_level(self, filename):
        try:
            with open(f'levels/{filename}.json', 'r') as f:
                self.level_data = json.load(f)
        except FileNotFoundError:
            print(f"Level {filename} not found")

    def add_entity(self, x, y):
        if self.current_entity:
            if self.current_entity in ['coin', 'mushroom', 'star']:
                self.level_data['level']['entities'][self.current_entity.capitalize()].append([x, y])
            elif self.current_entity in ['goomba', 'koopa']:
                self.level_data['level']['entities'][self.current_entity.capitalize()].append([x, y])
            elif self.current_entity in ['coin_box', 'random_box', 'coin_brick']:
                self.level_data['level']['entities'][self.current_entity.capitalize()].append([x, y])
            elif self.current_entity in ['platform', 'spike', 'spring', 'checkpoint', 'flag']:
                self.level_data['level']['objects'][self.current_entity].append([x, y])

    def remove_entity(self, x, y):
        # 移除实体
        for entity_type in self.level_data['level']['entities'].values():
            if [x, y] in entity_type:
                entity_type.remove([x, y])
        
        # 移除特殊对象
        for obj_type in self.level_data['level']['objects'].values():
            if [x, y] in obj_type:
                obj_type.remove([x, y])

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.save_level('level1')
                    elif event.key == pygame.K_l:
                        self.load_level('level1')
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_1:
                        self.selected_tool = 'tile'
                    elif event.key == pygame.K_2:
                        self.selected_tool = 'entity'
                    elif event.key == pygame.K_3:
                        self.selected_tool = 'special'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键点击
                        mouse_pos = pygame.mouse.get_pos()
                        if mouse_pos[0] < 600:  # 在编辑区域内
                            grid_x = (mouse_pos[0] + self.scroll_x) // self.grid_size
                            grid_y = (mouse_pos[1] + self.scroll_y) // self.grid_size
                            if self.selected_tool == 'tile':
                                if self.current_layer == 'ground':
                                    self.level_data['level']['objects']['ground'].append([grid_x, grid_y])
                                elif self.current_layer == 'sky':
                                    self.level_data['level']['objects']['sky'].append([grid_x, grid_y])
                            else:
                                self.add_entity(grid_x, grid_y)
                    elif event.button == 3:  # 右键点击
                        mouse_pos = pygame.mouse.get_pos()
                        if mouse_pos[0] < 600:  # 在编辑区域内
                            grid_x = (mouse_pos[0] + self.scroll_x) // self.grid_size
                            grid_y = (mouse_pos[1] + self.scroll_y) // self.grid_size
                            if self.selected_tool == 'tile':
                                # 移除图块
                                for layer in ['ground', 'sky']:
                                    if [grid_x, grid_y] in self.level_data['level']['objects'][layer]:
                                        self.level_data['level']['objects'][layer].remove([grid_x, grid_y])
                            else:
                                self.remove_entity(grid_x, grid_y)
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        self.scroll_x = max(0, self.scroll_x - 32)
                    else:
                        self.scroll_x = min(100 * 32 - 600, self.scroll_x + 32)

            # 绘制
            self.screen.fill(self.BLACK)
            self.draw_grid()
            
            # 绘制已放置的图块和实体
            for layer in ['ground', 'sky']:
                for x, y in self.level_data['level']['objects'][layer]:
                    screen_x = x * self.grid_size - self.scroll_x
                    screen_y = y * self.grid_size - self.scroll_y
                    if 0 <= screen_x < 600 and 0 <= screen_y < 600:
                        self.screen.blit(self.sprites[self.current_tile], (screen_x, screen_y))
            
            # 绘制实体
            for entity_type, entities in self.level_data['level']['entities'].items():
                for x, y in entities:
                    screen_x = x * self.grid_size - self.scroll_x
                    screen_y = y * self.grid_size - self.scroll_y
                    if 0 <= screen_x < 600 and 0 <= screen_y < 600:
                        sprite_name = entity_type.lower()
                        if sprite_name in self.sprites:
                            self.screen.blit(self.sprites[sprite_name], (screen_x, screen_y))
            
            # 绘制特殊对象
            for obj_type, objects in self.level_data['level']['objects'].items():
                if obj_type not in ['ground', 'sky']:
                    for x, y in objects:
                        screen_x = x * self.grid_size - self.scroll_x
                        screen_y = y * self.grid_size - self.scroll_y
                        if 0 <= screen_x < 600 and 0 <= screen_y < 600:
                            if obj_type in self.sprites:
                                self.screen.blit(self.sprites[obj_type], (screen_x, screen_y))
            
            self.draw_toolbar()
            
            # 显示帮助信息
            help_text = [
                "Controls:",
                "1: Tile Tool",
                "2: Entity Tool",
                "3: Special Tool",
                "Left Click: Place",
                "Right Click: Remove",
                "Mouse Wheel: Scroll",
                "S: Save level",
                "L: Load level",
                "ESC: Exit"
            ]
            y = 500
            for text in help_text:
                text_surface = self.font.render(text, True, self.WHITE)
                self.screen.blit(text_surface, (610, y))
                y += 25

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    editor = LevelEditor()
    editor.run() 