from collections import OrderedDict
import os
import random
import sys
import time

from ability import (DrainLife, Greenify, Obliterate,
                     ExtraHP, CounterAttack, Brutalize,
                     Cleanse, Pray, FinalWish,
                     Hide, Trap, Snipe)
from fighter import Fighter
from weapon import (Axe, Dagger, Bow,
                    show_weapons)


SHORT, MEDIUM, LONG = 0.5, 1, 1.5

ABILITIES = {
    'Sorcerer': [DrainLife, Greenify, Obliterate],
    'Warrior': [ExtraHP, CounterAttack, Brutalize],
    'Hunter': [Hide, Trap, Snipe],
    'Priest': [Cleanse, Pray, FinalWish]
    }

def show_jobs():
    '''Show information about available jobs'''
    os.system('clear')
    print("""\
=========================================================================
JOB INFORMATION | Start at L1, and learn a new ability at L2 and L3.
-------------------------------------------------------------------------
◊ [W]arrior:   +1 Toughness, +1 Attack Power
               L1: +4 base HP (Passive)
               L2: Counter-attack (Passive) - An eye for an eye!
               L3: [B]rutalize - Steal target's weapon and use it!

◊ [S]orcerer:  +2 Ability Power
               L1: [D]rain Life - Deal dmg, and heal yourself
               L2: [G]reenify - Target loses all special powers
               L3: [O]bliterate - Deal massive damage

◊ [P]riest:    +1 Toughness, +10% Dodge Chance
               L1: [C]leanse - Remove all debuffs
               L2: [P]ray - Heal yourself for a small amount
               L3: [F]inal wish - Next death, resurrect with 2-5 health

◊ [H]unter:    +10% Hit Chance, +10% Dodge Chance
               L1: [H]ide - Boost evasion, next attack/ability will crit 
               L2: [T]rap - Lay a trap that can stun attackers
               L3: [S]nipe - Deal +3/+4 dmg, and ignore target defense
=========================================================================""")
    return get_job()


def get_job():
    '''Create player with chosen job'''
    choices = {
        'w': Warrior,
        's': Sorcerer,
        'p': Priest,
        'h': Hunter,
        'c': show_jobs
        }
    print('Choose your job:')
    job_choice = input(
        "[W]arrior, [S]orcerer, "
        "[P]riest, [H]unter, "
        "or [C] to show job characteristics\n"
        "> "
        ).lower()
    if job_choice in choices:
        return choices[job_choice]()
    else:
        return get_job()


class Character(Fighter):
    def __init__(self):
        super().__init__()
        self.name = input("Character's name:\n> ").strip().title()
        self.status = []
        self.level = 1
        self.hp = 10
        self.max_hp = 10
        self.xp = 0
        self.max_xp = 5
        self.weapon = self._get_weapon()
        self.abilities = self._get_abilities()
        self.get_available_actions()

    def __str__(self):
        _header_string = (
            f"{self.name}, Level {self.level} {self.job}, "
            f"HP: {self.hp}/{self.max_hp}, "
            f"XP: {self.xp}/{self.max_xp}, "
            f"Weapon: {self.weapon.name}"
            )
        if self.status:
            _statuses = ', '.join([d.name for d in self.status])
            _header_string = (
                f"*** {_statuses.upper()} *** \n" + _header_string)
        return _header_string

    def _get_weapon(self):
        '''Let player pick a weapon'''
        _choices = {
            'a': Axe,
            'b': Bow,
            'd': Dagger
            }
        print('Choose your weapon:')
        _weapon_choice = input(
            "[A]xe, [B]ow, [D]agger, "
            "or [W] to show weapon characteristics\n"
            "> "
            ).lower()
        if _weapon_choice in _choices:
            return _choices[_weapon_choice]()
        elif _weapon_choice == 'w':
            show_weapons()
            return self._get_weapon()
        else:
            return self._get_weapon()

    def get_xp(self, target):
        '''
        Increase player XP by amount given by target.
        Check player XP and levels up if he has enough.
        Extra XP from previous level is carried over to the next
        level, which require 1 more XP every time.
        '''
        self.xp += target.xp
        print(f"\nYou get {target.xp} XP.")
        time.sleep(MEDIUM)
        if self.xp >= self.max_xp:
            self.level += 1
            self.xp -= self.max_xp
            self.max_xp += 1
            time.sleep(MEDIUM)
            print(f"\nDING! You reach Level {self.level}!")
            self._level_up()

    def _level_up(self):
        '''
        Increse player characteristics, and make him learn new 
        spells, depending on current level
        '''
        if self.level == 2:
            self.attack_power += 1
            self.ability_power += 1
            print("\nYou gain +1 Attack Power, and +1 Ability Power!")
            time.sleep(MEDIUM)
            print(f"You learn {self.abilities['2'].name}!")
            time.sleep(LONG)
        if self.level == 3:
            self.toughness += 1
            self.dodge_chance += 10
            print("\nYou gain +1 Toughness, and +10% Dodge Chance!")
            time.sleep(MEDIUM)
            print(f"You learn {self.abilities['3'].name}!")
            time.sleep(LONG)

    def die(self, cause='combat'):
        '''
        Print death message and exit
        Unless player is Priest, and is reviving.
        '''
        messages = {
            'combat': [
                "The damage is fatal. You die!",
                "This is too much to take! You're dead.",
                "You bleed to death. RIP!",
                "You were deleted from the game. Adios!" 
                ],
            'burning': [
                "You burn to death.",
                "The fire damage is fatal. You're dead."
                ],
            'confusion': [
                "How silly! You killed yourself.",
                "Bravo! You died of stupidity!"
                ]
            }
        msg = random.choice(messages[cause])
        time.sleep(LONG+MEDIUM)
        print("\n"+msg)
        time.sleep(LONG)
        if self.job == 'Priest':
            if self.reviving:
                print("\nThe Mighty Gods heard your prayer.")
                time.sleep(SHORT)
                print("You are given another chance.")
                time.sleep(SHORT)
                print("\nRESURRECTION!!!")
                self.heal(random.randint(6,10))
                self.reviving = False
                time.sleep(LONG)
        else:
            sys.exit()

    def rest(self, target):  # useless but required target argument
        '''Print heal message and heal player for 1 hp'''
        print("\nYou rest, and regenerate 1 HP!")
        self.heal(1)
        time.sleep(SHORT)

    def attack(self, target):
        '''
        Player physical attack phase: he can hit or miss 
        (if target dodges successfully).
        If attack hits, deal damage, otherwise, carry on.
        '''
        print(f"\nYou draw your {self.weapon.name.lower()}...", end='')
        sys.stdout.flush()
        if self.hits(self.weapon, target):
            time.sleep(SHORT)
            print(f" and hit the {target.name}!")
            dmg = self.get_atk_dmg(self.weapon, target)
            time.sleep(MEDIUM)
            print(f"You deal {dmg} damage to the "
                  f"{target.color} {target.name}!")
            target.take_dmg(dmg)
        else:
            time.sleep(SHORT)
            print(f" but the {target.color} {target.name} "
                  "dodges your attack.")
        time.sleep(LONG)

    def quit_game(self):
        time.sleep(0.5)
        print("\nYou flee like a coward!")
        sys.exit()

    def _get_abilities(self):
        '''
        Populate player ability dictionary with instances of ability
        objects, depending on player's job.
        Set each ability's user attribute to point to player object.
        Player abilities attribute looks like: {
            '1': <Ability1 object>,
            '2': <Ability2 object>,
            '3': <Ability3 object>
            }
        '''
        _abilities = {}
        for index, level in enumerate(['1', '2', '3']):
            _abilities[level] = ABILITIES[self.job][index]()
        for ability in _abilities.values():
            ability.user = self
        return _abilities

    def get_available_actions(self, frozen=False, silenced=False):
        '''
        Build and return a list of available actions based on player
        level, and taking into account possible status effects.
        Action will only be added if:
            its timer is zero (ability not on cooldown)
            it has some uses left
            it is not passive
            player has sufficient level
        Each action is a tuple containing:
            the key to be pressed by player to exectute the action
            a list containing:
                the "name" string to be shown on the action prompt
                the function object to be executed later on
        '''
        _actions = []
        if frozen:
            _actions.append(('w', ['[W]ait, completely powerless',
                                       lambda *args: None]))
        else:
            _actions.append(('a', ['[A]ttack', self.attack]))
        if not frozen and not silenced:
            for (level, ability) in self.abilities.items():
                if (int(level) <= self.level and
                        not ability.is_passive and 
                        ability.timer == 0 and
                        ability.number_of_uses > 0
                        ):
                    _display_name = (
                        ability.name 
                        + f" ({ability.number_of_uses})" 
                        + f" // Cooldown: {ability.cooldown}"
                        )
                    _actions.append((
                        ability.key,
                        [_display_name, ability.use]
                        ))
            _actions.append(('r', ['[R]est', self.rest]))

        _actions.append(('q', ['[Q]uit', self.quit_game]))
        self.actions = OrderedDict(_actions)

    def build_action_prompt(self):
        '''
        Print custom action prompt depending on job.
        Return action to take (a function).
        '''
        for action in self.actions:
            print(self.actions[action][0])
        _choice = None
        while _choice not in self.actions:
            _choice = input("\nWhat will you do? > ").lower()
        return self.actions[_choice][1]


class Warrior(Character):
    def __init__(self):
        self.job = "Warrior"
        super().__init__()
        self.hp = 14
        self.max_hp = 14
        self.toughness += 1
        self.attack_power += 1


class Sorcerer(Character):
    def __init__(self):
        self.job = "Sorcerer"
        super().__init__()
        self.ability_power += 2


class Priest(Character):
    def __init__(self):
        self.job = "Priest"
        super().__init__()
        self.toughness += 1
        self.dodge_chance += 10
        self.reviving = False


class Hunter(Character):
    def __init__(self):
        self.job = "Hunter"
        super().__init__()
        self.hit_chance += 10
        self.dodge_chance += 10

        self.spell_1_name = "[H]ide"
        self.spell_1_casts = 2
        self.spell_2_name = "[T]rap"
        self.spell_2_casts = 2
        self.spell_3_name = "[S]nipe"
        self.spell_3_casts = 1

    def __str__(self):
        _header_string = super().__str__()
        if self.hidden:
            _header_string = ("--- Hidden --- \n" 
                             + _header_string)
        return _header_string

    def spell_1(self,target):
        if not self.hidden:
            print("Poof! You hide yourself in the shadows.")
            self.hidden = True
        else: 
            print("You are already hiding.")
            self.spell_1_casts += 1

    def spell_2(self, target):
        print("You lay a trap on the ground!")
        self.laid_trap = True

    def spell_3(self, target):
        dmg = self.get_atk_dmg(self.weapon, target) + 2
        print(f"You fire a deadly shot at the {target.name}! "
              f"You hit it for {dmg} damage.")
        target.hp -= dmg
