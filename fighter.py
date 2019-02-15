import random
import sys

from effect import Hidden


class Fighter:
    def __init__(self):
        self.hit_chance = 80 
        self.dodge_chance = 20
        self.attack_power = 1
        self.ability_power = 1
        self.toughness = 0
        self.hidden = False
        self.hp = None
        self.max_hp = None

    def hits(self, weapon, target):
        '''
        Check if entity hits the target using his weapon,
        based on weapon hit chance, and target dodge chance
        '''
        return (self.hit_chance > random.randint(1,100) 
                and weapon.hits
                and not target.dodges(target.weapon))

    def dodges(self, weapon): 
        '''
        Check if entity dodges an attack, depending on his 
        equipped weapon (ranged weapons increase dodge chance)
        '''
        add_dodge = 0
        if weapon.is_ranged:
            add_dodge = 10
        return self.dodge_chance + add_dodge > random.randint(1,100)

    def get_atk_dmg(self, weapon, target, pierce=False):
        '''
        Return damage value depending on entities stats and weapon
        Damage cannot be 0, minimum damage set to 1
        A piercing attack ignores target's toughness.
        If attacker is hiding, attack will crit.
        '''
        if self.hidden:
            w_dmg = weapon.get_dmg(will_crit=True)
            dmg = (w_dmg * self.attack_power)
            if not pierce:
                dmg -= target.toughness
            return dmg if dmg > 0 else 1
        dmg = (weapon.get_dmg() * self.attack_power)
        if not pierce:
            dmg -= target.toughness
        return dmg if dmg > 0 else 1
    
    def die(self, cause=None):
        pass

    def take_dmg(self, damage, source='combat'):
        '''
        Reduce hp by 'damage' coming from 'source',
        and check for death.
        If Hunter took damage and was hiding, clear hiding.
        '''
        if damage < self.hp:
            self.hp -= damage
            try:
                if self.job == "Hunter" and self.hidden:
                    _hidden_effects = [
                        h for h in self.status 
                        if isinstance(h, Hidden)
                        ]
                    for h in _hidden_effects:
                        h.clear_effect()
                        self.status.remove(h)
            except AttributeError:
                pass
        else:
            self.hp = 0
            self.die(cause=source)

    def heal(self, amount):
        '''Increase hp by 'amount', but can't go past the maximum'''
        if self.hp <= (self.max_hp - amount):
            self.hp += amount
        else:
            self.hp = self.max_hp
