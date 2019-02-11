import os
import random
import sys
import time

from fighter import Fighter
from weapon import (Axe, Dagger, Bow,
                    show_weapons)


SHORT, MEDIUM, LONG = 0.5, 1, 1.5


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
               L3: [Z]erker - Deal 2x dmg, but hurt yourself

◊ [S]orcerer:  +2 Magic Power
               L1: [D]rain Life - Deal dmg, and heal yourself
               L2: [G]reenify - Target loses all special powers
               L3: [B]last - Blast target for +3/+4 dmg

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
        self.weapon = self.get_weapon()
        self.job = "Jobless"
        self.killed_a_monster = False
        self.status = []
        self.level = 1
        self.hp = 10
        self.max_hp = 10
        self.xp = 0
        self.max_xp = 5
        self.spell_2_name = None
        self.spell_3_name = None

    def __str__(self):
        header_string = (
            f"{self.name}, Level {self.level} {self.job}, "
            f"HP: {self.hp}/{self.max_hp}, "
            f"XP: {self.xp}/{self.max_xp}, "
            f"Weapon: {self.weapon.name}"
            )
        if self.status:
            header_string = (
                f"*** {', '.join(self.status).upper()} *** \n"
                + header_string)
        return header_string

    def get_weapon(self):
        '''Let player pick a weapon'''
        choices = {
            'a': Axe,
            'b': Bow,
            'd': Dagger
            }
        print('Choose your weapon:')
        weapon_choice = input(
            "[A]xe, [B]ow, [D]agger, "
            "or [W] to show weapon characteristics\n"
            "> "
            ).lower()
        if weapon_choice in choices:
            return choices[weapon_choice]()
        elif weapon_choice == 'w':
            show_weapons()
            return self.get_weapon()
        else:
            return self.get_weapon()

    def check_xp(self):
        '''Check player XP and levels up if he has enough'''
        if self.xp >= self.max_xp:
            self.level += 1
            self.xp -= self.max_xp
            self.max_xp += 1
            self.level_up()

    def level_up(self):
        '''Make player more powerful and learn new spells'''
        if self.level == 2:
            print("\nLEVEL UP! You gain +1 Attack Power, "
                  "and +1 Magic Power!")
            self.attack_power += 1
            self.magic_power += 1
            time.sleep(MEDIUM)
            print(f"You learn {self.spell_2_name}!")
            time.sleep(MEDIUM)
        if self.level == 3:
            print("\nLEVEL UP! You gain +1 Toughness, "
                  "and +10% Dodge Chance!")
            self.toughness += 1
            self.dodge_chance += 10
            time.sleep(MEDIUM)
            print(f"You learn {self.spell_3_name}!")
            time.sleep(MEDIUM)

    def die(self, cause='combat'):
        '''Print death message and exit'''
        messages = {
            'combat': [
                "The damage is fatal. You die!",
                "This is too much to take! You're dead.",
                "You bleed to death." 
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
        print(msg)
        time.sleep(LONG)
        sys.exit()

    def rest(self):
        print("\nYou rest, and regenerate 1 HP!")
        self.heal(1)
        time.sleep(SHORT)

    def attack(self, weapon, target):
        pass

    def quit_game(self):
        time.sleep(0.5)
        print("\nYou flee like a coward!")
        sys.exit()

class Warrior(Character):
    def __init__(self):
        super().__init__()
        self.job = "Warrior"
        self.hp = 14
        self.max_hp = 14
        self.toughness += 1
        self.attack_power += 1
        
        self.spell_2_name = "Counter-Attack"
        self.spell_3_name = "[Z]erker"
        self.spell_3_casts = 1

    def spell_3(self, target):
        dmg = self.get_atk_dmg(self.weapon, target)*2
        hurt = int(dmg/2)
        print("You enter a frenzy, "
              f"dealing {dmg} damage to the {target.name}, "
              f"and {hurt} to yourself.")
        target.hp -= dmg
        self.hp -= hurt


class Sorcerer(Character):
    def __init__(self):
        super().__init__()
        self.job = "Sorcerer"
        self.magic_power += 2
        
        self.spell_1_name = "[D]rain Life"
        self.spell_1_casts = 2
        self.spell_2_name = "[G]reenify"
        self.spell_2_casts = 1
        self.spell_3_name = "[B]last"
        self.spell_3_casts = 1

    def spell_1(self, target):
        dmg = self.get_atk_dmg(self.weapon, target)
        print(f"You leech {target.color} {target.name}'s life "
              f"for {dmg} damage.")
        target.hp -= dmg
        if self.hp < self.max_hp:
            print(f"You regen {dmg} hp.") 
            if self.hp <= self.max_hp - dmg:
                self.hp += dmg
            else:
                self.hp = self.max_hp

    def spell_2(self, target):
        if target.color != 'green':
            print(f"You cast Greenify! The {target.color} {target.name} "
                  "becomes green and loses all his powers.")
            setattr(target, "color", "green")

    def spell_3(self, target):
        dmg = self.get_atk_dmg(self.weapon, target) + random.randint(3,4)
        print(f"You blast {target.color} {target.name} "
              f"and inflict a whopping {dmg} damage.")
        target.hp -= dmg

    #def level_up(self):
        


class Priest(Character):
    def __init__(self):
        super().__init__()
        self.job = "Priest"
        self.toughness += 1
        self.dodge_chance += 10
        self.revive = False

        self.spell_1_name = "[C]ure"
        self.spell_1_casts = 2
        self.spell_2_name = "[P]ray"
        self.spell_2_casts = 3
        self.spell_3_name = "[F]inal wish"
        self.spell_3_casts = 1

    def spell_1(self, target):
        status = ", ".join(self.status)
        print(f"You cure yourself of all status ailments! (removed: '{status}')")
        self.status = []

    def spell_2(self, target):
        dmg = self.get_atk_dmg(self.weapon, target)
        print(f"You heal yourself for {dmg} hp.")
        if self.hp <= self.max_hp - dmg:
            self.hp += dmg
        else:
            self.hp = self.max_hp

    def spell_3(self, target):
        if not self.revive:
            print("You implore the Gods to grant you a final wish!")
            self.revive = True


class Hunter(Character):
    def __init__(self):
        super().__init__()
        self.job = "Hunter"
        self.hit_chance += 10
        self.dodge_chance += 10
        self.laid_trap = False
        self.hidden = False
        
        self.spell_1_name = "[H]ide"
        self.spell_1_casts = 2
        self.spell_2_name = "[T]rap"
        self.spell_2_casts = 2
        self.spell_3_name = "[S]nipe"
        self.spell_3_casts = 1

    def __str__(self):
        header_string = super().__str__()
        if self.hidden:
            header_string = ("--- Hidden --- \n" 
                             + header_string)
        return header_string


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



# if self.level == 2:
#             print("\nLEVEL UP! You gain +1 Attack Power, "
#                     "and +1 Magic Power!")
#             self.attack_power += 1
#             self.magic_power += 1
#             time.sleep(MEDIUM)
#             print(f"You learn {self.spell_2_name}!")
#         time.sleep(MEDIUM)
        
#         if self.player.level == 3:
#             print("\nLEVEL UP! You gain +1 Toughness, "
#                     "and +10% Dodge Chance!")
#             self.player.toughness += 1
#             self.player.dodge_chance += 10
#             time.sleep(MEDIUM)
#             print(f"You learn {self.player.spell_3_name}!")
#         time.sleep(MEDIUM)