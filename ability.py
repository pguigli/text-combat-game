import random
import sys
import time


SHORT, MEDIUM, LONG = 0.5, 1, 1.5


class Ability:
    def __init__(self):
        self.name = 'Ability'
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
            time.sleep(MEDIUM)
            print("Damn! You totally messed up!")

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
        _base_dmg = 2 * self.user.ability_power - target.toughness
        dmg = random.randint(_base_dmg-1, _base_dmg+1)
        return dmg if dmg > 0 else 1


class DrainLife(Ability):
    '''Deal direct damage to target, and heal for the same amount'''
    
    def __init__(self):
        super().__init__()
        self.name = '[D]rain Life'
        self.key = 'd'

    def _activate(self, target):
        dmg = self.get_dmg(target)
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
        self.number_of_uses = 2
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
        self.cooldown = 1

    def _activate(self, target):
        _base_dmg = self.get_dmg(target)
        dmg = 2*_base_dmg - target.toughness
        print("You focus all your powers, and unleash your wrath "
              f"on the poor {target.name}.")
        time.sleep(MEDIUM)
        print(f"You inflict a whopping {dmg} damage!")
        time.sleep(MEDIUM)
        target.take_dmg(dmg)
