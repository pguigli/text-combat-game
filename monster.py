import os
import random

from fighter import Fighter
from weapon import (KungFu, Axe, Dagger, Bow,
                    Lightsaber, Railgun)


COLORS = {
    'green': [None, None],
    'white': ['freezes you', 'frozen'],
    'red': ['sets you on fire', 'burning'],
    'spectral': ['confuses you', 'confused'],
    'black': ['silences you', 'silenced']
    }

WEAPONS = {
    'level_0': [KungFu],
    'level_1': [Axe, Dagger, Bow],
    'level_2': [Lightsaber],
    'level_3': [Railgun]
    }

SLACK_MESSAGES = [
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
--------------------------------------------------------------------------------
Monster colors:
--------------------------------------------------------------------------------
◊ Green:    Default color. No special attribute.

◊ Red:      Monster's attacks have a chance to set you on fire;
            'burning': Player burns for 1 damage each turn, for 2 turns.

◊ White:    Monster's attacks have a chance to freeze you;
            'frozen': Player can't perform any action next turn.

◊ Black:    Monster's attacks have a chance to silence you;
            'silenced': Player loses all of his job attributes for 1 turn.

◊ Spectral: Monster's attacks have a chance to confuse you;
            'confused': Player has a 50% to hurt himself next time he attacks.
--------------------------------------------------------------------------------""")

    elif display_help == 'n' or display_help == '':
        return
    else:
        return show_color_help()


class Monster(Fighter):

    def __init__(self, hp_min=1, hp_max=1,
                       xp_min=1, xp_max=2):
        super().__init__()
        self.name = 'Monster'
        self.sound = 'roar'
        self.hp = random.randint(hp_min, hp_max)
        self.xp = random.randint(xp_min, xp_max)
        self.color = random.choice(list(COLORS.keys()))
        self.attack_effect = self.get_attack_effect()
        self.debuff = self.get_debuff()
        self.allowed_weapons = ["level_0"]
        self.weapon = self.get_weapon()

    def __str__(self):
        return (f"{self.color.title()} {self.name}, "
                f"HP: {self.hp}, XP: {self.xp}, Weapon: {self.weapon.name}")

    def battlecry(self):
        return self.sound.upper() + "!"

    def get_debuff(self):
        return COLORS[self.color][1]

    def get_attack_effect(self):
        return COLORS[self.color][0]

    def on_hit_effect(self, target):
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

    def die(self, cause='.'):
        '''Print monster death message'''
        message = random.choice(DEATH_MESSAGES)
        print(f"The {self.color} {self.name} {message}.")


class Goblin(Monster):
    def __init__(self):
        super().__init__(hp_min=1, hp_max=2,
                         xp_min=2, xp_max=3)
        self.name = 'Goblin'
        self.allowed_weapons = ["level_0", "level_1"]
        self.weapon = self.get_weapon()


class Troll(Monster):
    def __init__(self):
        super().__init__(hp_min=3, hp_max=5,
                         xp_min=3, xp_max=5)
        self.name = 'Troll'
        self.allowed_weapons = ["level_1", "level_2"]
        self.weapon = self.get_weapon()
        self.toughness += 1
        self.attack_power += 1


class Dragon(Monster):
    def __init__(self):
        super().__init__(hp_min=6, hp_max=10,
                         xp_min=5, xp_max=8)
        self.name = 'Dragon'
        while self.color == 'green':
            self.color = random.choice(list(COLORS.keys()))
        self.allowed_weapons = ["level_1", "level_2", "level_3"]
        self.weapon = self.get_weapon()
        self.toughness += 2
        self.attack_power += 1
