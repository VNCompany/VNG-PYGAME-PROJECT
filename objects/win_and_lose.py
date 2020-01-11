class ResScreen:
    def __init__(self, image):
        self.image = image
        self.xy = (-800, 0)

    def update(self):
        if self.xy[0] < -8:
            self.xy = (self.xy[0] + 18, self.xy[1])
