import game_constants

class Ball:
    def __init__(self, x: float, y: float, radius: float, ):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = game_constants.BALL_MAX_VEL
        self.y_vel = 0
        self.color = game_constants.BALL_COLOR

    # TO DO
    def draw(self, window):
        pass

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

