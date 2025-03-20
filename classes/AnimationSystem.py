class CharacterState:
    def update(self, character):
        pass

class WalkingState(CharacterState):
    def update(self, character):
        character['x'] += character['speed'] * character['direction']
        if character['x'] < 50 or character['x'] > 750:
            character['direction'] *= -1

class JumpingState(CharacterState):
    def update(self, character):
        character['y'] += character['jump_speed']
        character['jump_speed'] += character['gravity']
        if character['y'] >= 400:
            character['y'] = 400
            character['state'] = WalkingState()

class AnimationSystem:
    def __init__(self):
        self.states = {
            'walking': WalkingState(),
            'jumping': JumpingState()
        }

# 在Menu类中替换原有动画逻辑 