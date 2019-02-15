import os
import random
import time


SHORT, MEDIUM, LONG = 0.5, 1, 1.5


def show_weapons():
    os.system('clear')
    print("""\
=========================================================================
WEAPON INFORMATION | Choose from Axe, Bow, Dagger. Others are reserved.
-------------------------------------------------------------------------
◊  Kung-Fu:      dmg: 1-1
◊  [A]xe:        dmg: 2-2
◊  [B]ow:        dmg: 1-2     Dodge chance: + 10%
◊  [D]agger:     dmg: 1-2     Hit chance: + 10%
◊  Lightsaber:   dmg: 2-4     Hit chance: + 10%     Ignores defenses
◊  Railgun:      dmg: 3-5     Hit chance: + 10%     Dodge chance: + 10%
=========================================================================""")


class Weapon:
    def __init__(self):
        self.name = "Weapon"
        self.min_dmg = 1
        self.max_dmg = 1
        self.hit_chance = 80
        self.crit_chance = 5
        self.is_ranged = False

    @property
    def hits(self):
        '''Check if weapon hits'''
        return self.hit_chance > random.randint(1,100)

    @property
    def crits(self):
        '''Check if weapon crits'''
        return self.crit_chance > random.randint(1,100)

    def get_dmg(self, will_crit=False):
        '''Return weapon damage, with crit possibility'''
        dmg = random.randint(self.min_dmg, self.max_dmg)
        if self.crits or will_crit:
            dmg *= 2
            print("CRITICAL STRIKE!")
            time.sleep(SHORT)
        return dmg


class KungFu(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Kung-Fu"


class Axe(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Axe"
        self.min_dmg = 2
        self.max_dmg = 2


class Dagger(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Dagger"
        self.max_dmg = 2
        self.hit_chance = 90


class Bow(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Bow"
        self.max_dmg = 2
        self.is_ranged = True


class Lightsaber(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Lightsaber"
        self.min_dmg = 2
        self.max_dmg = 4
        self.hit_chance = 90


class Railgun(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Railgun"
        self.min_dmg = 3
        self.max_dmg = 5
        self.hit_chance = 90
        self.is_ranged = True
