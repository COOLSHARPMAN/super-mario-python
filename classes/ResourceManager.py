class ResourceManager:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._loaded_images = {}
            cls._instance._loaded_sounds = {}
        return cls._instance

    def get_image(self, path, **kwargs):
        if path not in self._loaded_images:
            sheet = Spritesheet(path)
            self._loaded_images[path] = sheet
        return self._loaded_images[path].image_at(**kwargs)

# 在Menu类初始化中改为：
def __init__(self, screen, dashboard, level, sound):
    self.resource = ResourceManager()
    self.menu_banner = self.resource.get_image(
        "./img/title_screen.png",
        x=0, y=60, zoom=2,
        colorkey=[255, 0, 220],
        ignoreTileSize=True,
        xTileSize=180,
        yTileSize=88
    ) 