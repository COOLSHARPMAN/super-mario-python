class Command:
    def execute(self, menu):
        pass

class MoveUpCommand(Command):
    def execute(self, menu):
        if menu.inChoosingLevel:
            if menu.currSelectedLevel > 3:
                menu.currSelectedLevel -= 3
        elif menu.state > 0:
            menu.state -= 1

class InputHandler:
    def __init__(self):
        self.key_bindings = {
            pygame.K_UP: MoveUpCommand(),
            pygame.K_w: MoveUpCommand(),
            # 绑定其他操作...
        }

    def handle_input(self, event, menu):
        if event.type == pygame.KEYDOWN:
            command = self.key_bindings.get(event.key)
            if command:
                command.execute(menu) 