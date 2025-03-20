from pygame.transform import flip


class GoTrait:
    def __init__(self, animation, screen, camera, ent):
        # 初始化函数
        self.animation = animation  # 动画对象
        self.direction = 0  # 方向
        self.heading = 1  # 朝向
        self.accelVel = 0.4  # 加速度
        self.decelVel = 0.25  # 减速度
        self.maxVel = 3.0  # 最大速度
        self.screen = screen  # 屏幕对象
        self.boost = False  # 是否加速
        self.camera = camera  # 相机对象
        self.entity = ent  # 实体对象

    def update(self):
        # 更新函数
        if self.boost:
            # 如果加速
            self.maxVel = 5.0  # 最大速度增加
            self.animation.deltaTime = 4  # 动画时间调整
        else:
            self.animation.deltaTime = 7  # 动画时间调整
            if abs(self.entity.vel.x) > 3.2:
                # 如果速度超过3.2，则调整到3.2
                self.entity.vel.x = 3.2 * self.heading
            self.maxVel = 3.2  # 最大速度调整

        if self.direction != 0:
            # 如果方向不为0
            self.heading = self.direction  # 更新朝向
            if self.heading == 1:
                # 如果朝向为1
                if self.entity.vel.x < self.maxVel:
                    # 如果速度小于最大速度，则加速
                    self.entity.vel.x += self.accelVel * self.heading
            else:
                # 如果朝向为-1
                if self.entity.vel.x > -self.maxVel:
                    # 如果速度大于负最大速度，则加速
                    self.entity.vel.x += self.accelVel * self.heading

            if not self.entity.inAir:
                # 如果不在空中
                self.animation.update()  # 更新动画
            else:
                self.animation.inAir()  # 更新空中动画
        else:
            # 如果方向为0
            self.animation.update()  # 更新动画
            if self.entity.vel.x >= 0:
                # 如果速度非负
                self.entity.vel.x -= self.decelVel  # 减速
            else:
                self.entity.vel.x += self.decelVel  # 减速
            if int(self.entity.vel.x) == 0:
                # 如果速度为0
                self.entity.vel.x = 0  # 设置速度为0
                if self.entity.inAir:
                    # 如果在空中
                    self.animation.inAir()  # 更新空中动画
                else:
                    self.animation.idle()  # 更新静止动画
        if (self.entity.invincibilityFrames//2) % 2 == 0:
            # 如果无敌时间的半数为偶数
            self.drawEntity()  # 绘制实体

    def updateAnimation(self, animation):
        # 更新动画函数
        self.animation = animation  # 更新动画对象
        self.update()  # 调用更新函数

    def drawEntity(self):
        # 绘制实体函数
        if self.heading == 1:
            # 如果朝向为1
            self.screen.blit(self.animation.image, self.entity.getPos())  # 绘制实体
        elif self.heading == -1:
            # 如果朝向为-1
            self.screen.blit(
                flip(self.animation.image, True, False), self.entity.getPos()
            )
