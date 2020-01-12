class Level:
    def __init__(self, id: int,
                 image,
                 quality: int,
                 enemy: int,
                 is_boss_level: bool,
                 enemy_speed=3):
        self.id = id
        self.image = image
        self.quality = quality
        self.enemy = enemy
        self.is_boss_level = is_boss_level
        self.enemy_speed = enemy_speed
