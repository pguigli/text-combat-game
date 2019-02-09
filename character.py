import random
from combat import Combat


class Character(Combat):
    
    def __init__(self):
        Combat.__init__(self)
        self.name = input("Character's name:\n> ").strip().title()
        self.weapon = self.get_weapon()
        self.get_player_stats() 
        self.show_help_colors()
        self.job = 'Jobless'
        self.laid_trap = False
        self.hidden = False
        self.status = []
        self.level = 1
        self.revive = False
            
    def __str__(self):
        header_string = (f"{self.name}, Level {self.level} {self.job}, "
                        f"HP: {self.hp}/{self.base_hp}, XP: {self.xp}/{self.xpn}, "
                        f"Weapon: {self.weapon.title()}")
        if self.hidden:
            header_string = ("--- Hidden --- \n" 
                             + header_string)
        if self.status:
            header_string = (f"*** {', '.join(self.status).upper()} *** \n"
                             + header_string)
        return header_string
        
    
    def get_weapon(self):
        print('Choose your weapon:')
        weapon_choice = input('[A]xe, [B]ow, [D]agger, or [W] to show weapon characteristics\n> ').lower()
        if weapon_choice in 'abdw' and weapon_choice != '':
            if weapon_choice == 'a':
                return 'axe'
            elif weapon_choice == 'b':
                return 'bow'
            elif weapon_choice == 'd':
                return 'dagger'
            elif weapon_choice == 'w':
                self.show_weapons()
                return self.get_weapon()
        else:
            return self.get_weapon()

    @staticmethod
    def show_weapons():
        print('-'*90)
        print('Weapons:')
        print('-'*90)
        print(' ◊  [A]xe: \t +1 max. damage,   +1 min. damage.')
        print(' ◊  [B]ow: \t +1 max. damage,   +1 dodge chance.')
        print(' ◊  [D]agger: \t +1 max. damage,   +1 hit chance.')
        print(' ◊  Lightsaber:  +2 max. damage,   +1 hit chance.')
        print(' ◊  Railgun: \t +3 max. damage,   +1 min. damage,   +1 dodge chance.')
        print('-'*90)

    def get_player_stats(self, hp=10, base_hp=10, 
                         xp=0, xpn=5,
                         min_dmg=1, max_dmg=1,
                         attack_dice=6, dodge_dice=6,
                         killed_a_monster=False):
        self.base_hp = base_hp
        self.hp = hp
        self.xp = xp
        self.xpn = xpn
        self.attack_dice = attack_dice
        self.dodge_dice = dodge_dice
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.killed_a_monster = killed_a_monster
        
    def rest(self):
        if self.hp < self.base_hp:
            self.hp += 1
    
    def leveled_up(self):
        if self.xp >= self.xpn:
            self.level += 1
            self.xp -= self.xpn
            self.xpn += 1
            return True
                
    def show_help_colors(self):
        display_help = input("Do you want to learn about monster colors? [y/n]\n> ").lower()
        if display_help == 'y':        
            print('-'*90)
            print('Monster colors:')
            print('-'*90)
            print(" ◊  Green: \t Default color. No special attribute.\n")
            print(" ◊  Red:   \t Monster's attacks have a chance to set you on fire;")
            print("           \t 'burning': Player burns for 1 damage each turn, for 2 turns.\n")
            print(" ◊  White: \t Monster's attacks have a chance to freeze you;")
            print("           \t 'frozen': Player can't perform any action next turn.\n")
            print(" ◊  Black: \t Monster's attacks have a chance to silence you;")
            print("           \t 'silenced': Player loses all of his job attributes for 1 turn.\n")
            print(" ◊  Spectral: \t Monster's attacks have a chance to confuse you;")
            print("              \t 'confused': Player has a 50% to hurt himself next time he attacks.")
            print('-'*90)
            
        elif display_help == 'n' or display_help == '':
            pass
        else:
            self.show_help_colors()
            

class Warrior(Character):
    
    def __init__(self):
        Character.__init__(self)
        self.get_player_stats(14, 14)
        self.job = self.__class__.__name__
        self.spell_2_name = "Counter-Attack"
        self.spell_3_name = "[Z]erker"
        self.spell_3_casts = 1
        
    def spell_3(self, target):
        dmg = self.get_dmg(self.weapon, self)*2
        hurt = int(dmg/2)
        print("You enter a frenzy, dealing {} damage to the {}, and {} to yourself."
              .format(dmg, target.__class__.__name__, hurt))
                                                                 

class Sorcerer(Character):
    
    def __init__(self):
        Character.__init__(self)
        self.job = self.__class__.__name__
        self.spell_1_name = "[D]rain Life"
        self.spell_1_casts = 2
        self.spell_2_name = "[G]reenify"
        self.spell_2_casts = 1
        self.spell_3_name = "[B]last"
        self.spell_3_casts = 1
        
    def spell_1(self, target):
        dmg = self.get_dmg(self.weapon, self)
        print("You leech {} {}'s life for {} damage.".format(target.color, target.__class__.__name__, dmg))
        target.hp -= dmg
        if self.hp < self.base_hp:
            print("You regen {} hp.".format(dmg)) 
            if self.hp <= self.base_hp - dmg:
                self.hp += dmg
            else:
                self.hp = self.base_hp
        
    def spell_2(self, target):
        if target.color != 'green':
            print("You cast Greenify! The {} {} becomes green and loses his powers.".format(target.color,
                                                                                            target.__class__.__name__))
            setattr(target, "color", "green")

    def spell_3(self, target):
        dmg = self.get_dmg(self.weapon, self) + random.randint(3,4)
        print("You blast {} {} and inflict a whopping {} damage.".format(target.color, target.__class__.__name__, dmg))
        target.hp -= dmg


class Priest(Character):
    
    def __init__(self):
        Character.__init__(self)
        self.job = self.__class__.__name__
        self.spell_1_name = "[C]ure"
        self.spell_1_casts = 2
        self.spell_2_name = "[P]ray"
        self.spell_2_casts = 3
        self.spell_3_name = "[F]inal wish"
        self.spell_3_casts = 1
        
    def spell_1(self, target):
        print("You cure yourself of all status ailments! (removed: {}.)".format(", ".join(self.status)))
        self.status = []
            
    def spell_2(self, target):
        dmg = self.get_dmg(self.weapon, self)
        print("You heal yourself for {} hp.".format(dmg))
        if self.hp <= self.base_hp - dmg:
            self.hp += dmg
        else:
            self.hp = self.base_hp
            
    def spell_3(self, target):
        if not self.revive:
            print("You implore the Gods to grant you a final wish!")
            self.revive = True
    
                                                     
class Hunter(Character):
    
    def __init__(self):
        Character.__init__(self)
        self.job = self.__class__.__name__
        self.spell_1_name = "[H]ide"
        self.spell_1_casts = 2
        self.spell_2_name = "[T]rap"
        self.spell_2_casts = 2
        self.spell_3_name = "[S]nipe"
        self.spell_3_casts = 1
        
    def spell_1(self,target):
        if not self.hidden:
            print("Poof! You hide yourself in the shadows.")
            self.hidden = True
        else: 
            print("You are already hiding.")
            self.spell_1_casts += 1
    
    def spell_2(self, target):
        print("You lay a trap on the ground!")
        self.laid_trap = True

    def spell_3(self, target):
        dmg = self.get_dmg(self.weapon, self) + 2                            
        print("You fire a deadly shot at the {}! You hit it for {} damage.".format(target.__class__.__name__, dmg))
        target.hp -= dmg
