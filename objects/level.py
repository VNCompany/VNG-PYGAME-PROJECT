class Level:
    def __init__(self, id: int,
                 image,
                 m_prob: float,
                 enemy: int,
                 is_boss_level: bool,
                 enemy_speeds: list,
                 enemy_healths: list):
        self.id = id
        self.image = image
        self.m_prob = m_prob
        self.enemy = enemy
        self.is_boss_level = is_boss_level
        self.enemy_speeds = enemy_speeds
        self.enemy_healths = enemy_healths
