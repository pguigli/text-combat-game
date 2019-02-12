import random
import sys
import time


SHORT, MEDIUM, LONG = 0.5, 1, 1.5


class Effect:
    def __init__(self, target=None, duration=1):
        self.name = 'Effect'
        self.duration = duration
        self.target = target
        self.remaining = self.duration
        self.debuff = True
    
    def tick_effect(self):
        '''
        Tick effect, for the number of remaining turns,
        or dissipate if effect is expiring
        '''
        if self.remaining > 0:
            self._apply_consequences()
            self.remaining -= 1
            #input(f"Remaining: {self.remaining}")
        else:
            #input(f"Status before: {self.target.status}")
            self.target.status.remove(self)
            print(f"{self.name} expired.")
            #input(f"Removed {self}")
            #input(f"Status after: {self.target.status}")
            time.sleep(MEDIUM)

    def _apply_consequences(self):
        '''Activate effect consequences on the entity who has it'''
        print("AHA!")
        time.sleep(LONG)


class Burning(Effect):
    def __init__(self, target):
        super().__init__(target=target, duration=2)
        self.name = 'Burning'
    
    def _apply_consequences(self):
        '''Burn target for 1 dmg each turn'''
        self.target.take_dmg(1, source='burning')
        print("You're burning! You take 1 damage.")
        time.sleep(LONG)


class Silenced(Effect):
    def __init__(self, target):
        super().__init__(target=target)
        self.name = 'Silenced'
    
    def _apply_consequences(self):
        '''Prevent target from using anything else than "Attack"'''
        print("[Silencing...]")
        time.sleep(LONG)


class Confused(Effect):
    def __init__(self, target):
        super().__init__(duration=2, target=target)
        self.name = 'Confused'

    def _apply_consequences(self):
        '''
        Target has 60% chance to hurt itself 
        when attacking or casting a spell
        "'''
        print("[Confusing...]")
        time.sleep(LONG)


class Frozen(Effect):
    def __init__(self, target):
        super().__init__(target=target)
        self.name = 'Frozen'

    def _apply_consequences(self):
        '''Prevent target from performing any action'''
        print("[Freezing...]")
        time.sleep(LONG)
