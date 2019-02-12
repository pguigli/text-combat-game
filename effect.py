from collections import OrderedDict
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
            self._clear_effect()
            self.target.status.remove(self)
            print(f"{self.name} expired.")
            #input(f"Removed {self}")
            #input(f"Status after: {self.target.status}")
            time.sleep(MEDIUM)

    def _clear_effect(self):
        '''Cancel any temporary change made by the effect'''
        pass

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
        time.sleep(SHORT)
        print("You're burning! You take 1 damage.")
        time.sleep(LONG)

    def _clear_effect(self):
        '''Print that player is not burning anymore'''
        time.sleep(SHORT)
        print("Phew! The fire went off.")
        time.sleep(MEDIUM)


class Silenced(Effect):
    def __init__(self, target):
        super().__init__(target=target)
        self.name = 'Silenced'
    
    def _apply_consequences(self):
        '''
        Prevent target from using anything else than "Attack"
        If target was warrior (+4 base HP), he loses the extra
        health too, temporarily. 
        '''
        if self.target.name == 'Warrior':
            if self.target.hp > 10:
                self.extra_hp = self.target.hp - 10
                self.target.hp = 10
            self.target.max_hp = 10
        self.before_silenced = self.target.possible_actions
        self.target.possible_actions = OrderedDict([
            ('a', ['[A]ttack', self.target.attack]),
            ('q', ['[Q]uit', self.target.quit_game])
            ])
        time.sleep(SHORT)
        print("You are silenced! You forget what "
              f"it means to be a {self.target.name}...")
        time.sleep(LONG)

    def _clear_effect(self):
        '''Restore all target's available actions'''
        self.target.possible_actions = self.before_silenced
        if self.target.name == 'Warrior':
            self.target.max_hp = 14
            self.target.hp += self.extra_hp
        time.sleep(SHORT)
        print(f"You finally remember how to {self.target.name}.")
        time.sleep(MEDIUM)


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
        '''Prevent target from performing any action at all'''
        self.before_frozen = self.target.possible_actions
        self.target.possible_actions = OrderedDict([
            ('w', ['[W]ait, completely powerless', lambda *args: None]),
            ('q', ['[Q]uit', self.target.quit_game ])
            ])
        time.sleep(SHORT)
        print("You are frozen... You can't even move a finger!")
        time.sleep(LONG)

    def _clear_effect(self):
        '''Restore all target's available actions'''
        self.target.possible_actions = self.before_frozen
        time.sleep(SHORT)
        print("As you slowly thaw, you're free to move again!")
        time.sleep(MEDIUM)
