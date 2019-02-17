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
◊  Kung-Fu:      dmg: 1-2
◊  [A]xe:        dmg: 2-4
◊  [B]ow:        dmg: 2-3     Dodge chance: + 10%   Crit chance + 5%
◊  [D]agger:     dmg: 2-3     Hit chance: + 10%
◊  Lightsaber:   dmg: 3-5     Hit chance: + 10%
◊  Railgun:      dmg: 4-7     Hit chance: + 10%     Dodge chance: + 10%
=========================================================================""")


class Weapon:
    def __init__(self):
        self.name = "Weapon"
        self.min_dmg = 1
        self.max_dmg = 2
        self.hit_chance = 90
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
        self.max_dmg = 4
        self.crit_chance = 5


class Dagger(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Dagger"
        self.min_dmg = 2
        self.max_dmg = 3
        self.hit_chance = 100


class Bow(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Bow"
        self.min_dmg = 2
        self.max_dmg = 3
        self.crit_chance = 10
        self.is_ranged = True


class Lightsaber(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Lightsaber"
        self.min_dmg = 3
        self.max_dmg = 5
        self.hit_chance = 100


class Railgun(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Railgun"
        self.min_dmg = 4
        self.max_dmg = 7
        self.hit_chance = 100
        self.is_ranged = True
