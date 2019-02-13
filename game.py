import os
import random
import sys
import time

from character import get_job
from monster import Goblin, Troll, Dragon


LONG = 1.5


class Game:
    def __init__(self):
        self.setup()
        self.monster = self.get_next_monster()
        os.system('clear')
        input(f"Welcome, {self.player.name}. "
              "Press [Enter] to start the game.")

        while (self.player.hp > 0 and
                (self.monster or self.monster_pool or self.boss)):
            self.print_header()

            self.player_turn()

            self.monster_turn()

            self.cleanup()

            self.print_footer()

        time.sleep(LONG)
        input("Congratulations! You've cleared the dungeon.")
        input("You win!")
        time.sleep(LONG)
        sys.exit()

    def setup(self):
        '''Spawn player, boss, and 5 monsters'''
        self.endgame = False
        self.player = get_job()
        self.boss = [Dragon()]
        self.monster_pool = [
            Goblin(), Goblin(), Goblin(), 
            Troll(), Troll()
            ]

    def get_next_monster(self):
        '''
        Return 2 Goblins, then 3 random monsters, then a boss.
        Return None if there are no monsters left.
        '''
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
        print('='*65)
        print(self.player)
        print('-'*65)
        print(self.monster.battlecry(), "\nA wild creature appears:")
        print(self.monster)
        print('-'*65)

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
        #         65 > random.randint(1,100):
        #     self.player.action_prompt()(self.player)
        # else:
        self.player.get_available_actions()
        self.player.build_action_prompt()(self.monster)

    def monster_turn(self):
        ''' Make monster physically attack (75% chance), or rest.'''
        if not self.monster.just_died:
            if 75 > random.randint(1,100):
                self.monster.attack(self.player)
            else:
                self.monster.rest()

    def cleanup(self):
        '''
        Check for player status: apply consequences or expire.
        Check for dead monster. Give xp and level player up.
        Get next monster.
        '''
        if self.player.status:
            for debuff in self.player.status:
                debuff.tick_effect()
        if self.monster.just_died:
            self.player.get_xp(self.monster)
            self.monster = self.get_next_monster()

    def print_footer(self):
        '''
        Print relevant footer, depending or enemies remaining
        If no monster of boss left, do nothing
        '''
        print('\n'+'='*65)
        if self.boss:
            _remaining = len(self.monster_pool) + len(self.boss)
            input(f"{_remaining} enemies remaining. "
                  "Press [Enter] to continue. ")
            return
        elif (not self.endgame and self.monster is not None and
                 self.monster.name == "Dragon"):
            print("You have awakened the ancient Dragon!")
            time.sleep(LONG)
            time.sleep(LONG)
            input(f"Brace yourself, {self.player.name}. "
                  "Press [Enter] to go ahead. ")
            self.endgame = True
        elif self.endgame and self.monster is not None:
            print("Press [Enter] to continue. ")

if __name__ == "__main__":
    Game()