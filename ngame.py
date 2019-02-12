import os
import random
import sys
import time

from character import get_job
from monster import Goblin, Troll, Dragon


class Game:
    def __init__(self):
        self.setup()
        self.monster = self.get_next_monster()
        input("Press [Enter] to start the game.")

        while (self.player.hp > 0 and
                (self.monster or self.monster_pool or self.boss)):
            self.print_header()
            
            self.player_turn()
            
            self.monster_turn()
            
            self.print_footer()
            
            self.cleanup()
            
            self.print_footer()

        sys.exit()

    def setup(self):
        '''Spawn player, boss, and 5 monsters'''
        self.player = get_job()
        self.boss = [Dragon()]
        self.monster_pool = [
            Goblin(), Goblin(), Goblin(), 
            Troll(), Troll()
            ]

    def get_next_monster(self):
        '''Return 2 Goblins, then 3 random monsters, then a boss'''
        if len(self.monster_pool) > 3:
            return self.monster_pool.pop(0)
        elif len(self.monster_pool) > 0:
            _rand_monster = random.choice(self.monster_pool)
            _rand_id = self.monster_pool.index(_rand_monster)
            return self.monster_pool.pop(_rand_id)
        else:
            try:
                return self.boss.pop(0)
            except IndexError:
                return None

    def print_header(self):
        '''Print header with information about player and monster'''
        os.system('clear')
        print('='*60)
        print(self.player)
        print('-'*60)
        print(self.monster.battlecry(), "\nA wild creature appears:")
        print(self.monster)
        print('-'*60)

    def player_turn(self):
        '''
        Prompt for player action.
        Act depending on player choice:
            physical attack,
            spell cast,
            rest,
            quit.
        '''
        # if "Confused" in [d.name for d in self.player.status] and
        #         60 > random.randint(1,100):
        #     self.player.action_prompt()(self.player)
        # else:
        self.player.action_prompt()(self.monster)

    def monster_turn(self):
        '''
        Monster can only physically attack, or rest.
        '''
        if 75 > random.randint(1,100):
            self.monster.attack(self.player)
        else:
            self.monster.rest()

    def cleanup(self):
        '''
        Check for player status: apply consequences or expire.
        Check for dead monster. Give xp. Level player.
        Check for Priest revive.
        Get next monster.
        '''
        if self.player.status:
            for debuff in self.player.status:
                debuff.tick_effect()

    def print_footer(self):
        '''Print relevant footer, depending or enemies remaining'''
        pass


if __name__ == "__main__":
    Game()