import random
import time


SHORT, MEDIUM, LONG = 0.5, 1, 1.5


class Ability:
    def __init__(self):
        self.name = 'Ability'
        self.user = None
        self.level = 1
        self.number_of_uses = 2
        self.cooldown = 1
        self.timer = 0
        self.miss_chance = 5
        self.passive = False

    def use(self, target):
        '''
        Activate ability , and subtract one use.
        Then, put the ability on cooldown.
        '''
        self._activate(target)
        self.number_of_uses -= 1
        self.timer = self.cooldown

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
        There is a small chance to miss, causing 0 damage.
        '''
        if random.randint(1,100) <= self.miss_chance:
            time.sleep(MEDIUM)
            print("Critical miss!")
            return 0
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
