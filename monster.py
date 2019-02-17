import os
import random
import sys
import time

from effect import Burning, Confused, Frozen, Silenced
from fighter import Fighter
from weapon import (KungFu, Axe, Dagger, Bow,
                    Lightsaber, Railgun)


SHORT, MEDIUM, LONG = 0, 0, 0

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
    " dies!",
    "'s poor soul finally ascends to the Heavens.",
    " falls to the ground, lifeless.",
    " screams in agony, and collapses!",
    " succumbs to his wounds!",
    " runs away in despair, and bleeds to death.",
    " is no more!"
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
        self.debuff = self.get_debuff()     #debuff class, not instance
        self.debuff_chance = 100
        self.allowed_weapons = ["level_0"]
        self.weapon = self.get_weapon()
        self.just_died = False
        self.is_stunned = False
        self.preparing = False

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
            return COLORS[self.color][1]

    def apply_effect(self, target):
        '''
        If successful, apply debuff to target:
        Check if instances of class self.debuff (the type of debuff
        corresponding to the monster's color) are present in
        target's status. If so, refresh their durations.
        Otherwise, instanciate new debuff and put it on target.
        '''
        if self.debuff_chance >= random.randint(1,100):
            _debuffs_present = [debuff for debuff in target.status if 
                                isinstance(debuff, self.debuff)]
            if _debuffs_present:
                for debuff in _debuffs_present:
                    debuff.remaining = debuff.duration
                print(f"Refreshed: {debuff.name}")
                time.sleep(MEDIUM)
            else:
                target.status.append(self.debuff(target))
                time.sleep(SHORT)
                print(f"\nThe {self.name}'s attack "
                      f"{self.attack_effect}!")

    def get_attack_effect(self):
        '''Return relevant attack descriptor depending on color'''
        return COLORS[self.color][0]

    def get_weapon(self):
        '''
        Instanciate weapon object according to 
        which ones are allowed, depending on monster type
        '''
        lst = [wp for lvl in self.allowed_weapons for wp in WEAPONS[lvl]]
        weapon = random.choice(lst)
        return weapon()

    def die(self, cause=None):
        '''Print monster death message'''
        message = random.choice(DEATH_MESSAGES)
        time.sleep(LONG)
        print(f"\n{self.battlecry()}! "
              f"The {self.color} {self.name}{message}")
        self.just_died = True

    def rest(self):
        '''Print random rest message, and heal monster for 1 hp'''
        msg = random.choice(REST_MESSAGES)
        print(f"\nThe {self.color} {self.name} {msg}, "
              "and regenerates 1 HP!")
        self.heal(1)
        time.sleep(LONG)

    def attack(self, target):
        '''
        Make monster attack target using weapon.
        Attacks can: 
            hit target,
                dealing damage
                and try to apply effects
            miss, if target dodges, and do nothing
        '''
        print(f"\nThe {self.color} {self.name} attacks!")
        time.sleep(MEDIUM)
        print("You try to dodge the attack...", end='')
        sys.stdout.flush()
        if self.hits(self.weapon, target):
            time.sleep(SHORT)
            print(" but you fail!")
            dmg = self.get_atk_dmg(self.weapon, target)
            time.sleep(MEDIUM)
            print(f"The {self.color} {self.name} "
                  f"hits you for {dmg} HP.")
            target.take_dmg(dmg)
            if self.color != 'green':
                self.apply_effect(target)
        else:
            time.sleep(SHORT)
            print(" and succeed!")
        time.sleep(LONG)

    def prepare(self, target):
        '''
        The first time, do nothing, but set a "preparing" flag.
        The second time, deal target a large amount of damage.
        Can be missed (15% chance).
        '''
        if not self.preparing:
            print(f"\nThe {self.name} starts concentrating his powers.")
            self.preparing = True
        else:
            print(f"\nThe {self.name} unleashes his fury... ", end='')
            self.preparing = False
            sys.stdout.flush()
            if 85 >= random.randint(1,100):
                dmg = 2 * self.get_atk_dmg(self.weapon, target)
                time.sleep(MEDIUM)
                print(f"You take {dmg} dmg!")
                target.take_dmg(dmg)
                if self.color != 'green':
                    self.apply_effect(target)
            else:
                time.sleep(SHORT)
                print("but misses his attack!")
        time.sleep(LONG)


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
        self.sound = 'bwaaah'
        self.allowed_weapons = ["level_1", "level_2"]
        self.weapon = self.get_weapon()
        self.toughness = 25
        self.attack_power = 150


class Dragon(Monster):
    def __init__(self):
        super().__init__(min_hp=6, max_hp=10,
                         min_xp=5, max_xp=8)
        self.name = 'Dragon'
        self.sound = "grrrr"
        while self.color == 'green':
            self.color = random.choice(list(COLORS.keys()))
        self.allowed_weapons = ["level_2", "level_3"]
        self.weapon = self.get_weapon()
        self.toughness = 50
        self.attack_power = 200
