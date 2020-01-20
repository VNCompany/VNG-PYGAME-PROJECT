class ResScreen:
    def __init__(self, image, speed=40):
        self.image = image
        self.xy = (-1800, 0)
        self.speed = speed

    def update(self):
        if self.xy[0] < 0:
            self.xy = (self.xy[0] + self.speed, self.xy[1])
