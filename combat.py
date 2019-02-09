import random
import character


class Combat:
    
    def __init__(self):
        self.attack_dice = 6
        self.dodge_dice = 6
        self.min_dmg = 1
        self.max_dmg = 1
    
    def attack_hits(self, weapon):
        roll = random.randint(1, self.attack_dice)
        if weapon == 'railgun':
            pass
        elif weapon == 'lightsaber':
            roll += 1
        elif weapon == 'axe':
            pass
        elif weapon == 'dagger':
            roll += 1
        elif weapon == 'bow':
            pass
        else:
            pass
        return roll > 2
        
    def dodge(self, weapon, player): 
        roll = random.randint(1, self.dodge_dice)
        if player.hidden:
            roll += 1
        if weapon == 'railgun':
            roll += 1
        elif weapon == 'lightsaber':
            pass
        elif weapon == 'axe':
            pass
        elif weapon == 'dagger':
            pass
        elif weapon == 'bow':
            roll += 1
        else:
            pass
        return roll > 4
        
    def get_dmg(self, weapon, player):
        if weapon == 'railgun':
            dmg = random.randint(self.min_dmg+1, self.max_dmg+3)
        elif weapon == 'lightsaber':
            dmg = random.randint(self.min_dmg, self.max_dmg+2)
        elif weapon == 'axe':
            dmg = random.randint(self.min_dmg+1, self.max_dmg+1)
        elif weapon == 'dagger':
            dmg = random.randint(self.min_dmg, self.max_dmg+1)
        elif weapon == 'bow':
            dmg = random.randint(self.min_dmg, self.max_dmg+1)
        else:
            dmg = random.randint(self.min_dmg, self.max_dmg)
        if self.job == "Hunter" and ( random.randint(1,10) > 7 or player.hidden ):
            print("*Critical strike!*")
            player.hidden = False
            return 2*dmg
        else:
            return dmg
            
            
            