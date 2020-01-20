class Infinity:
    speeds_k = 7
    speeds_old_k = 4
    healths_k = 5
    healths_old_k = 3
    add_enemy_k = 2

    speeds_c = 0
    speeds_old_c = 0
    healths_c = 0
    healths_old_c = 0
    add_enemy_c = 0

    pre_speed = 5
    pre_health = "1:1"

    def __init__(self, speeds: list, healths: list, start_count: int):
        self.speeds = speeds
        self.healths = healths
        self.pre_speed = speeds[-1]
        self.pre_health = healths[-1]
        self.enemy_count = start_count

    def update(self):
        if self.speeds_c < self.speeds_k:
            self.speeds_c += 1
        else:
            self.speeds_c = 0
            self.pre_speed += 1
            self.speeds.append(self.pre_speed)

        if self.speeds_old_c < self.speeds_old_k:
            self.speeds_old_c += 1
        else:
            self.speeds_old_c = 0
            self.speeds.append(self.pre_speed)

        if self.add_enemy_c < self.add_enemy_k:
            self.add_enemy_c += 1
        else:
            self.add_enemy_c = 0
            self.enemy_count += 1

        if self.healths_c < self.healths_k:
            self.healths_c += 1
        else:
            self.healths_c = 0
            hc = [int(v) for v in self.pre_health.split(":")]
            self.pre_health = str(hc[0] + 1) + ":" + str((hc[0] + 1) * 2)
            self.healths.append(self.pre_health)

        if self.healths_old_c < self.healths_old_k:
            self.healths_old_c += 1
        else:
            self.healths_old_c = 0
            hc = [int(v) for v in self.pre_health.split(":")]
            self.pre_health = str(hc[0] + 1) + ":" + str((hc[0] + 1) * 2)
            self.healths.append(self.pre_health)
