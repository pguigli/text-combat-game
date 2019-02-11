import random
import sys
import time


SHORT, MEDIUM, LONG = 0.5, 1, 1.5


class Effect:
    def __init__(self, duration=1):
        self.name = 'Effect'
        self.duration = duration
        self.remaining = self.duration
        self.apply_chance = 60
        self.target = None
        self.source = None
        self.debuff = True

    def is_present(self, entity):
        '''Check if effect is present on an entity'''
        return self in entity.status
    
    def apply(self, source, target):
        '''
        Apply effect, if successful, from source entity
        to target entity, or refresh duration if already present.
        '''
        if self.apply_chance > random.randint(1,100):
            if not self.is_present(target):
                target.status.append(self)
                self.source = source
                self.target = target
                print(f"The {self.source.name}'s attack "
                      f"{self.source.attack_effect}!")
            else:
                self.remaining = self.duration

    def tick_effect(self):
        '''
        Tick effect, if present, for the number of remaining turns, 
        or dissipate if effect is expiring
        '''
        if self.remaining > 0:
            self._apply_consequences()
            self.remaining -= 1
        else:
            self._dissipate()

    def _apply_consequences(self):
        '''Activate effect consequences on the entity who has it'''
        pass

    def _dissipate(self):
        '''Remove effect from the entity who has it'''
        if self.is_present(self.target):
            self.target.status.remove(self)


class Burning(Effect):
    def __init__(self):
        super().__init__(duration=2)
        self.name = 'Burning'
    
    def apply_consequences(self):
        '''Burn target for 1 dmg each turn'''
        self.target.take_dmg(1, source='burning')
        print("You're burning! You take 1 damage.")
        time.sleep(LONG)


class Silenced(Effect):
    def __init__(self):
        super().__init__()
        self.name = 'Silenced'
    
    def apply_consequences(self):
        '''Prevent target from using anything else than "Attack"'''
        print("Applying Silenced")
        time.sleep(LONG)


class Confused(Effect):
    def __init__(self):
        super().__init__(duration=2)
        self.name = 'Confused'

    def apply_consequences(self):
        '''
        Target has 60% chance to hurt itself 
        when attacking or casting a spell
        "'''
        print("Apply Confused")
        time.sleep(LONG)


class Frozen(Effect):
    def __init__(self):
        super().__init__()
        self.name = 'Frozen'

    def apply_consequences(self):
        '''Prevent target from performing any action'''
        print("Applying Frozen")
        time.sleep(LONG)
