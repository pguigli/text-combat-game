import random
import sys
import time

from character import Character


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
        print("\nPhew! The fire went off.")
        time.sleep(MEDIUM)


class Silenced(Effect):
    def __init__(self, target):
        super().__init__(target=target)
        self.name = 'Silenced'
    
    def _apply_consequences(self):
        '''
        Prevent target from using anything else than "Attack"
        Reset all stats to base stats, temporarily.
        If target was warrior (+4 base HP), remove the extra
        health too, temporarily. 
        '''
        self._pre_silence_stats = {
            'hit': self.target.hit_chance,
            'dodge': self.target.dodge_chance,
            'attack': self.target.attack_power,
            'ability': self.target.ability_power,
            'toughness': self.target.toughness
            }
        self.target.actions = self.target.get_available_actions(silenced=True)
        self.target.hit_chance = 80
        self.target.dodge_chance = 20
        self.target.attack_power = 1
        self.target.ability_power = 1
        self.target.toughness = 0
        if self.target.job == 'Warrior':
            if self.target.hp > 10:
                self.extra_hp = self.target.hp - 10
                self.target.hp = 10
            self.target.max_hp = 10
        time.sleep(SHORT)
        print("You are silenced! You forget what "
              f"it means to be a {self.target.job}...")
        time.sleep(LONG)

    def _clear_effect(self):
        '''Restore all target's available actions and stats'''
        self.target.actions = self.target.get_available_actions()
        self.target.hit_chance = self._pre_silence_stats['hit']
        self.target.dodge_chance = self._pre_silence_stats['dodge']
        self.target.attack_power = self._pre_silence_stats['attack']
        self.target.ability_power = self._pre_silence_stats['ability']
        self.target.toughness = self._pre_silence_stats['toughness']
        if self.target.job == 'Warrior':
            self.target.max_hp = 14
            self.target.hp += self.extra_hp
        time.sleep(SHORT)
        print(f"\nYou finally remember how to {self.target.job}.")
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
        self.target.actions = self.target.get_available_actions(frozen=True)
        time.sleep(SHORT)
        print("You are frozen... You can't even move a finger!")
        time.sleep(LONG)

    def _clear_effect(self):
        '''Restore all target's available actions'''
        self.target.actions = self.target.get_available_actions()
        time.sleep(SHORT)
        print("\nAs you slowly thaw, you're free to move again!")
        time.sleep(MEDIUM)
