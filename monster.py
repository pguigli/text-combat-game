import random
from combat import Combat

COLORS = [('green', ),
          ('white', 'freezes you', 'frozen'),
          ('red', 'sets you on fire', 'burning'),
          ('spectral', 'confuses you', 'confused'),
          ('black', 'silences you', 'silenced')]

WEAPONS = ['claws', 'bow', 'dagger', 'axe', 'lightsaber', 'railgun']


class Monster(Combat):
    
    def __init__(self):
        Combat.__init__(self)
        self.get_monster_stats()
        self.get_monster_hp()
        self.get_monster_xp()
        self.job = "Jobless"

    def __str__(self):
        return (f"{self.color.title()} {self.__class__.__name__}, "
                f"HP: {self.hp}, XP: {self.xp}, Weapon: {self.weapon.title()}")

    def battlecry(self):
        return self.sound.upper() + "!"

    def get_monster_stats(self, c_start=0, sound='roar',
                          min_hp=1, max_hp=1, 
                          min_xp=5, max_xp=5, 
                          min_dmg=1, max_dmg=1,
                          attack_dice=6, dodge_dice=6, 
                          w_start=1, w_end=4):
        self.category = random.choice(COLORS[c_start:])
        self.color = self.category[0]
        self.debuff = self.get_debuff()
        self.attack_effect = self.get_attack_effect()
        self.min_hp = min_hp
        self.max_hp = max_hp
        self.min_xp = min_xp
        self.max_xp = max_xp
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.attack_dice = attack_dice
        self.dodge_dice = dodge_dice
        self.weapon = random.choice(WEAPONS[w_start-1:w_end])
        self.sound = sound

    def get_debuff(self):
        if self.color == 'green':
            return None
        else:
            return self.category[2]

    def get_attack_effect(self):
        if self.color == 'green':
            return None
        else:
            return self.category[1]

    def get_monster_hp(self):
        self.hp = random.randint(self.min_hp, self.max_hp)

    def get_monster_xp(self):
        self.xp = random.randint(self.min_xp, self.max_xp)

    def on_hit_effect(self, target):
        if self.color != 'green':
            print("\nThe {} {}'s attack ".format(self.color, self.__class__.__name__)
                  + self.attack_effect + "!")
            if not self.debuff in target.status:
                target.status.append(self.debuff)
            if self.debuff == 'burning':
                target.burn_duration = 2
            elif self.debuff == 'silenced':
                target.silence_duration = 2
            

class Goblin(Monster):
    pass


class Troll(Monster):
   
    def __init__(self):
        Monster.__init__(self)
        self.get_monster_stats(0, 'bwah', 3, 5, 3, 5, 2, 3, w_end=5)
        self.get_monster_hp()
        self.get_monster_xp()


class Dragon(Monster):

    def __init__(self):
        Monster.__init__(self)
        self.get_monster_stats(1, 'grrrrr', 5, 10, 5, 10, 2, 5, w_start=3, w_end=6)
        self.get_monster_hp()
        self.get_monster_xp()