import sys
import time


MEDIUM = 1
LONG = 1.5

class Effect:
    def __init__(self, duration=1):
        self.name = 'Effect'
        self.duration = duration
        self.remaining = self.duration
        self.target = None
        self.source = None
        self.debuff = True

    def is_present(self, entity):
        '''Check if effect is present on an entity'''
        return self in entity.status
    
    def apply(self, source, target):
        '''
        Apply effect from source entity to target entity, 
        or refresh duration if already present
        '''
        if not self.is_present(target):
            target.status.append(self)
            self.source = source
            self.target = target
        else:
            self.remaining = self.duration

    def tick_effect(self):
        '''
        Tick effect for the number of remaining turns, 
        or dissipate if effect is expiring
        '''
        if self.remaining > 0:
            self.apply_consequences()
            self.remaining -= 1
        else:
            self.dissipate()

    def apply_consequences(self):
        '''Activate effect consequences on the entity who has it'''
        pass

    def dissipate(self):
        '''Remove effect from the entity who has it'''
        if self.is_present(self.target):
            self.target.status.remove(self)
        



class Burning(Effect):
    def __init__(self):
        super().__init__(duration=2)
        self.name = 'Burning'
    
    def apply_consequences(self):
        '''Burn for 1 dmg each turn'''
        self.target.take_dmg(1, 'burning')
        print("You're burning! You take 1 damage.")
        time.sleep(LONG)


class Silenced(Effect):
    def __init__(self):
        super().__init__()
        self.name = 'Silenced'
    
    def apply_consequences(self):
        '''Prevent target from using anything else than "Attack"'''
        print("XXXXXXXXXXXXXXXXX")
        time.sleep(LONG)

        
        
