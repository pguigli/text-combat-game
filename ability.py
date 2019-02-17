import math
import random
import sys
import time

from effect import Hidden
from weapon import Railgun

SHORT, MEDIUM, LONG = 0.5, 1, 1.5


class Ability:
    def __init__(self):
        self.name = 'Ability'
        self.key = None
        self.user = None
        self.number_of_uses = 2
        self.cooldown = 1
        self.timer = 0
        self.miss_chance = 5
        self.is_passive = False

    def use(self, target):
        '''
        Activate ability, and subtract one use.
        There is a small chance to miss, resulting in a wasted turn.
        Then, put the ability on cooldown.
        '''
        if random.randint(1,100) > self.miss_chance:
            self._activate(target)
            self.number_of_uses -= 1
            self.timer = self.cooldown
        else:
            print("\nYou start casting "
                  f"{self.name.replace('[', '').replace(']', '')}...")
            sys.stdout.flush()
            time.sleep(SHORT)
            print("CRITICAL FAIL!")
            time.sleep(LONG)
            print("Damn! You totally messed up!\n")
            time.sleep(MEDIUM)

    def update_timer(self):
        '''Decrement ability timer (0 means ability is available)'''
        if self.timer > 0:
            self.timer -= 1

    def _activate(self, target):
        '''Activate ability effects'''
        pass

    def get_dmg(self, target):
        '''
        Return ability damage, based on user ability power
        and target toughness, with a minimum of 1.
        '''
        _base_dmg = 2 * self.user.ability_power / 100
        _base_dmg = math.floor(_base_dmg * (100-target.toughness) / 100)
        dmg = random.randint(_base_dmg-1, _base_dmg+1)
        return dmg if dmg > 0 else 1


class Leech(Ability):
    '''Deal direct damage to target, and heal for the same amount'''
    
    def __init__(self):
        super().__init__()
        self.name = '[L]eech'
        self.key = 'l'

    def _activate(self, target):
        dmg = self.get_dmg(target) + 1
        print(f"You leech the {target.color} {target.name}'s "
              f"vital essence, dealing {dmg} damage.")
        time.sleep(MEDIUM)
        print(f"You regen {dmg} HP.")
        target.take_dmg(dmg)
        self.user.heal(dmg)


class Greenify(Ability):
    '''
    Permanently change target color to "Green". Target loses his special power
    (debuff) and can't apply effects anymore.
    '''
    
    def __init__(self):
        super().__init__()
        self.name = '[G]reenify'
        self.key = 'g'
        self.timer = 0
        self.cooldown = 3

    def _activate(self, target):
        if target.color != 'green':
            print(f"You cast Greenify! The {target.color} {target.name} "
                  "becomes green and loses all his powers.")
            target.color = 'green'
            target.attack_effect = None
            target.debuff = None
        else:
            print("You cast Greenify... But it doesn't "
                  "affect the green monster... obviously!")
        time.sleep(MEDIUM)


class Obliterate(Ability):
    '''
    Deal massive damage to target.
    Damage = base damage*2 - target toughness
    '''
    
    def __init__(self):
        super().__init__()
        self.name = '[O]bliterate'
        self.key = 'o'
        self.number_of_uses = 1

    def _activate(self, target):
        _base_dmg = self.get_dmg(target)
        dmg = 2 * _base_dmg
        print("You focus all your powers, and unleash your wrath "
              f"on the poor {target.name}.")
        time.sleep(MEDIUM)
        print(f"You inflict a whopping {dmg} damage!")
        time.sleep(MEDIUM)
        target.take_dmg(dmg)


class ExtraHP(Ability):
    def __init__(self):
        super().__init__()
        self.is_passive = True


class CounterAttack(Ability):
    '''
    Give a passive 35% chance to get a free, automatic
    attack phase, if user was damaged this turn.
    Only works if player Lvl >= 2, and if he is not Silenced or Frozen.
    '''
    
    def __init__(self):
        super().__init__()
        self.name = 'Counter-Attack'
        self.is_passive = True

    def _activate(self, target):
        if (self.user.level >= 2 and 35 >= random.randint(1,100) and
                "Silenced" not in [d.name for d in self.user.status] and
                "Frozen" not in [d.name for d in self.user.status]):
            time.sleep(SHORT)
            print("\nCOUNTER-ATTACK!")
            time.sleep(MEDIUM)
            self.user.attack(target)


class Brutalize(Ability):
    '''
    Permanently disarm target. 
    Target gets a random Level 0 or Level 1 weapon instead.
    Then, user attacks target using the stolen weapon (once).
    This can't be dodged or missed.
    Of course, it works with all weapons, even reserved.
    Finally, user gets his original weapon back.
    '''

    def __init__(self):
        super().__init__()
        self.name = '[B]rutalize'
        self.key = 'b'
        self.number_of_uses = 1

    def _activate(self, target):
        sys.stdout.flush()
        stolen_weapon = target.weapon
        target.allowed_weapons = ["level_0", "level_1"]
        target.weapon = target.get_weapon()
        print(f"\nYou leap on the {target.name}, ", end='')
        time.sleep(MEDIUM)
        print(f"and brutally disarm the beast!")
        time.sleep(LONG)
        print(f"You attack him with his own {stolen_weapon.name}!")
        time.sleep(LONG)
        dmg = self.user.get_atk_dmg(stolen_weapon, target) + 2
        print(f"The {target.color} {target.name} takes {dmg} damage.")
        target.take_dmg(dmg)
        time.sleep(LONG)


class Cleanse(Ability):
    '''
    Cancel negative changes made by negative effects.
    Remove all negative effects from user's status.
    Usable when silenced or frozen.
    '''

    def __init__(self):
        super().__init__()
        self.name = '[C]leanse'
        self.key = 'c'
        self.cooldown = 2

    def _activate(self, target):
        for effect in self.user.status:
            if effect.is_debuff:
                print(f"You cleansed yourself of {effect.name}!\n")
                effect.clear_effect()
                self.user.status.remove(effect)
                time.sleep(SHORT)
        time.sleep(SHORT)
        self.user.get_available_actions()


class Pray(Ability):
    '''
    Restore some HP to user. 10% chance to crit.
    '''

    def __init__(self):
        super().__init__()
        self.name = '[P]ray'
        self.key = 'p'
        self.cooldown = 2

    def _activate(self, target):
        heal = math.floor(2 * self.user.ability_power/100 + 1)
        heal += random.choice([-1, 0, 1])
        print("You start praying...")
        time.sleep(LONG)
        if 10 >= random.randint(1,100):
            print("CRITICAL!")
            heal *= 2
            time.sleep(SHORT)
        print(f"You heal yourself for {heal} hp.")
        self.user.heal(heal)
        time.sleep(LONG)


class FinalWish(Ability):
    '''
    Revive the user next time he dies, with 6-10 hp
    '''

    def __init__(self):
        super().__init__()
        self.name = '[F]inal Wish'
        self.key = 'f'
        self.number_of_uses = 1

    def _activate(self, target):
        print("You implore the Gods to grant you a final wish!")
        self.user.reviving = True
        time.sleep(LONG)


class Hide(Ability):
    '''
    Hide the user, granting +50% dodge chance.
    Fade upon attacking, or using Snipe. Fade upon taking damage.
    Next attack has increased hit chance.
    Next successful attack will crit.
    '''

    def __init__(self):
        super().__init__()
        self.name = '[H]ide'
        self.key = 'h'
        self.cooldown = 5
        self.is_passive = False

    def _activate(self, target):
        print("You look around to find cover...")
        self.user.status.append(Hidden(self.user))
        time.sleep(LONG)


class Trap(Ability):
    '''
    Lay a trap on the ground (usable when hidden).
    (see game.py for implementation)
    Next time target attacks, 60% chance to activate the trap:
        taking normal user attack damage
        wasting his current turn
        being unable to do anything next turn
    '''

    def __init__(self):
        super().__init__()
        self.name = '[T]rap'
        self.key = 't'
        self.number_of_uses = 1

    def _activate(self, target):
        print("You lay a trap on the ground.")
        self.user.laid_trap = True
        time.sleep(LONG)
    
    def detonate_trap(self, target):
        self.user.laid_trap = False
        print(f"\nCLING! The {target.name} "
              "steps on the trap and gets stunned!")
        time.sleep(LONG)
        dmg = self.user.get_atk_dmg(self.user.weapon, target)
        time.sleep(MEDIUM)
        print(f"Your trap deals {dmg} damage!")
        target.take_dmg(dmg)


class Snipe(Ability):
    '''
    Deal damage with Railgun, instead of weapon.
    Pierce through target's defense (ignore toughness).
    Always crits if user was hiding.
    Cancel hiding is user was hidden.
    '''

    def __init__(self):
        super().__init__()
        self.name = '[S]nipe'
        self.key = 's'
        self.number_of_uses = 1

    def _activate(self, target):
        print("You carefully aim your Railgun shot...", end='')
        sys.stdout.flush()
        time.sleep(MEDIUM)
        print(" BAM!!!!")
        time.sleep(MEDIUM)
        dmg = self.user.get_atk_dmg(Railgun(), target, pierce=True)
        print(f"You sniped the {target.color} {target.name} "
              f"for {dmg} damage!!")
        target.take_dmg(dmg)
        time.sleep(LONG)
