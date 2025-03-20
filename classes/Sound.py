import pygame


class Sound:
    def __init__(self, sound_enabled=True):
        self.sound_enabled = sound_enabled
        if self.sound_enabled:
            try:
                # 加载音效
                self.coin = pygame.mixer.Sound('./sounds/coin.wav')
                self.jump = pygame.mixer.Sound('./sounds/jump.wav')
                self.die = pygame.mixer.Sound('./sounds/die.wav')
                self.kick = pygame.mixer.Sound('./sounds/kick.wav')
                self.bump = pygame.mixer.Sound('./sounds/bump.wav')
                self.powerup = pygame.mixer.Sound('./sounds/powerup.wav')
                self.powerdown = pygame.mixer.Sound('./sounds/powerdown.wav')
                self.stomp = pygame.mixer.Sound('./sounds/stomp.wav')
                self.time_warning = pygame.mixer.Sound('./sounds/time_warning.wav')
                self.game_over = pygame.mixer.Sound('./sounds/game_over.wav')
                self.extra_life = pygame.mixer.Sound('./sounds/extra_life.wav')
                
                # 加载音乐
                pygame.mixer.music.load('./sounds/music.mp3')
                
                # 设置音量
                self.set_volume(1.0)
            except pygame.error:
                print("Warning: Could not load sound files. Game will run without sound.")
                self.sound_enabled = False

    def play_sfx(self, sound_name):
        if not self.sound_enabled:
            return
            
        try:
            if sound_name == 'coin':
                self.coin.play()
            elif sound_name == 'jump':
                self.jump.play()
            elif sound_name == 'die':
                self.die.play()
            elif sound_name == 'kick':
                self.kick.play()
            elif sound_name == 'bump':
                self.bump.play()
            elif sound_name == 'powerup':
                self.powerup.play()
            elif sound_name == 'powerdown':
                self.powerdown.play()
            elif sound_name == 'stomp':
                self.stomp.play()
            elif sound_name == 'time_warning':
                self.time_warning.play()
            elif sound_name == 'game_over':
                self.game_over.play()
            elif sound_name == 'extra_life':
                self.extra_life.play()
        except pygame.error:
            pass

    def play_music(self):
        if not self.sound_enabled:
            return
            
        try:
            pygame.mixer.music.play(-1)  # -1表示循环播放
        except pygame.error:
            pass

    def stop_music(self):
        if not self.sound_enabled:
            return
            
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass

    def set_volume(self, volume):
        if not self.sound_enabled:
            return
            
        try:
            # 设置所有音效的音量
            self.coin.set_volume(volume)
            self.jump.set_volume(volume)
            self.die.set_volume(volume)
            self.kick.set_volume(volume)
            self.bump.set_volume(volume)
            self.powerup.set_volume(volume)
            self.powerdown.set_volume(volume)
            self.stomp.set_volume(volume)
            self.time_warning.set_volume(volume)
            self.game_over.set_volume(volume)
            self.extra_life.set_volume(volume)
            
            # 设置音乐的音量
            pygame.mixer.music.set_volume(volume)
        except pygame.error:
            pass
