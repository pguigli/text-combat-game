import os
import random
import time

from effect import Burning, Confused, Frozen, Silenced
from fighter import Fighter
from weapon import (KungFu, Axe, Dagger, Bow,
                    Lightsaber, Railgun)


SHORT, MEDIUM, LONG = 0.5, 1, 1.5

COLORS = {
    'green': [None, None],
    'white': ['freezes you', Frozen],
    'red': ['sets you on fire', Burning],
    'spectral': ['confuses you', Confused],
    'black': ['silences you', Silenced]
    }

WEAPONS = {
    'level_0': [KungFu],
    'level_1': [Axe, Dagger, Bow],
    'level_2': [Lightsaber],
    'level_3': [Railgun]
    }

REST_MESSAGES = [
    "is in no mood to attack",
    "looks at you with disdain",
    "takes a nap",
    "wanders around nervously",
    "can't be bothered",
    "arrogantly ignores you",
    "scratches his nose"
    ]

DEATH_MESSAGES = [
    "dies!",
    "loses his life.",
    "meets his Maker; he's in a better place, now."
    "screams in agony, and collapses!",
    "succumbs to his wounds!",
    "runs away in despair, and bleeds to death.",
    "breathes his last... RIP!"
    ]

def show_color_help():
    display_help = input("Do you want to learn about monster colors? [y/n]\n> ").lower()
    if display_help == 'y':
        os.system('clear')
        print("""\
------------------------------------------------------------------------
MONSTER COLOR INFORMATION
------------------------------------------------------------------------
◊ Green:    Default color. No special attribute.

◊ Red:      Monster's attacks may set you on fire;
            'burning': Burn for 1 damage each turn.
            Duration: [2 turns]

◊ White:    Monster's attacks may freeze you;
            'frozen': Can't perform any action.
            Duration: [1 turn]

◊ Black:    Monster's attacks may silence you;
            'silenced': Lose all special powers.
            Duration: [1 turn]

◊ Spectral: Monster's attacks may confuse you;
            'confused': Chance to hurt yourself on attacking / cast
            Duration: [2 turns]
------------------------------------------------------------------------""")

    elif display_help == 'n' or display_help == '':
        return
    else:
        return show_color_help()


class Monster(Fighter):

    def __init__(self, min_hp=1, max_hp=1,
                       min_xp=1, max_xp=2):
        super().__init__()
        self.name = 'Monster'
        self.sound = 'roar'
        self.hp = random.randint(min_hp, max_hp)
        self.max_hp = max_hp
        self.xp = random.randint(min_xp, max_xp)
        self.color = random.choice(list(COLORS.keys()))
        self.attack_effect = self.get_attack_effect()
        self.debuff = self.get_debuff()
        self.allowed_weapons = ["level_0"]
        self.weapon = self.get_weapon()

    def __str__(self):
        return (f"{self.color.title()} {self.name}, "
                f"HP: {self.hp}, XP: {self.xp}, Weapon: {self.weapon.name}")

    def battlecry(self):
        '''Return monster battlecry'''
        return self.sound.upper() + "!"

    def get_debuff(self):
        '''Get relevant power depending on monster color'''
        if self.color == 'green':
            return None
        else:
            return COLORS[self.color][1]()

    def get_attack_effect(self):
        '''Return relevant attack descriptor depending on color'''
        return COLORS[self.color][0]

    def on_hit_effect(self, target):        ### DEPRECATED
        if self.color != 'green':
            print(f"\nThe {self.color} {self.name}'s attack "
                  + self.attack_effect + "!")
            if not self.debuff in target.status:
                target.status.append(self.debuff)
            if self.debuff == 'burning':
                target.burn_duration = 2
            elif self.debuff == 'silenced':
                target.silence_duration = 2

    def get_weapon(self):
        lst = [wp for lvl in self.allowed_weapons for wp in WEAPONS[lvl]]
        weapon = random.choice(lst)
        return weapon()

    def die(self, cause=None):
        '''Print monster death message'''
        message = random.choice(DEATH_MESSAGES)
        print(f"{self.battlecry()}! The {self.color} {self.name} {message}.")

    def rest(self):
        msg = random.choice(REST_MESSAGES)
        print(f"\nThe {self.color} {self.name} {msg}, "
                  "and regenerates 1 HP!")
        self.heal(1)
        time.sleep(SHORT)

    def attack(self, weapon, target):
        pass

class Goblin(Monster):
    def __init__(self):
        super().__init__(min_hp=1, max_hp=2,
                         min_xp=2, max_xp=3)
        self.name = 'Goblin'
        self.allowed_weapons = ["level_0", "level_1"]
        self.weapon = self.get_weapon()


class Troll(Monster):
    def __init__(self):
        super().__init__(min_hp=3, max_hp=5,
                         min_xp=3, max_xp=5)
        self.name = 'Troll'
        self.allowed_weapons = ["level_1", "level_2"]
        self.weapon = self.get_weapon()
        self.toughness += 1
        self.attack_power += 1


class Dragon(Monster):
    def __init__(self):
        super().__init__(min_hp=6, max_hp=10,
                         min_xp=5, max_xp=8)
        self.name = 'Dragon'
        while self.color == 'green':
            self.color = random.choice(list(COLORS.keys()))
        self.allowed_weapons = ["level_1", "level_2", "level_3"]
        self.weapon = self.get_weapon()
        self.toughness += 2
        self.attack_power += 1
