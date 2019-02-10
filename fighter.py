import random


class Fighter:
    def __init__(self):
        self.hit_chance = 80 
        self.dodge_chance = 20
        self.attack_power = 1
        self.magic_power = 1
        self.toughness = 0

    def hits(self, weapon, target):
        '''Check if entity hits target using weapon'''
        return (self.hit_chance > random.randint(1,100) 
                and weapon.hits
                and not target.dodges(target.weapon))

    def dodges(self, weapon): 
        '''Check if entity dodges an attack, depending on his range'''
        add_dodge = 0
        if weapon.is_ranged:
            add_dodge = 10
        return self.dodge_chance + add_dodge > random.randint(1,100)

    def get_atk_dmg(self, weapon, target):
        '''Return damage value depending on entities stats and weapon'''
        try:
            if self.hidden:
                w_dmg = weapon.get_dmg(will_crit=True)
                dmg = (w_dmg * self.attack_power) - target.toughness
                self.hidden = False
                return dmg
        except AttributeError:
            pass
        dmg = (weapon.get_dmg() * self.attack_power) - target.toughness
        return dmg