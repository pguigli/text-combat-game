import os
import random
import sys
import time

from character import get_job
from monster import Goblin, Troll, Dragon


SHORT, MEDIUM, LONG = 0, 0, 0


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
        input("Congratulations! You've cleared the dungeon. > ")
        print("You win!")
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
        Update (decrement) all ability timers.
        If Priest is Frozen/Silenced, he can cleanse it, if his Cleanse
        ability is ready and has uses left.
        Then, prompt for player action.
        Act depending on player choice:
            physical attack,
            spell cast,
            rest,
            quit.
        '''
        for ability in self.player.abilities.values():
            ability.update_timer()
        _effect_names = [d.name for d in self.player.status]
        if (("Frozen" in _effect_names or "Silenced" in _effect_names) and
                self.player.status and
                self.player.job == "Priest" and
                self.player.abilities['1'].number_of_uses > 0 and
                self.player.abilities['1'].timer == 0
                ):
            print(f"You are {', '.join(_effect_names)}!")
            time.sleep(MEDIUM)
            print("\nLuckily you're a Priest!")
            time.sleep(SHORT)
            _choice = ''
            if input("Use [C]leanse? [y/n]\n> ").lower() in 'cy':
                self.player.abilities['1'].use(self.monster)
        time.sleep(SHORT)
        self.player.build_action_prompt()(self.monster)

    def monster_turn(self):
        '''
        Make monster physically attack (60% chance), 
        rest (25%), or prepare a devastating attack (15%).
        If monster prepared his attack: next turn, he will
        automatically cast prepare again, unleashing the attack.
        If monster attacks normally:
            - Player may "Counter-Attack" if he is a Warrior and meets 
              the conditions (proper level, and not silenced/frozen).
            - Monster may activate hunter's trap. He loses his turn, 
              and will be stunned next turn.
        
        '''
        if not self.monster.just_died:
            roll = random.randint(1,100)
            if roll <= 60 and not self.monster.preparing:
                if (self.player.job == 'Hunter' and
                        self.player.laid_trap and
                        60 >= random.randint(1,100)):
                    self.player.abilities['2'].detonate_trap(self.monster)
                    self.monster.is_stunned = True
                elif self.monster.is_stunned:
                    print(f"\nThe {self.monster.name} is stunned.")
                    time.sleep(MEDIUM)
                else:
                    self.monster.attack(self.player)
                if self.player.job == 'Warrior':
                    self.player.abilities['2'].use(self.monster)
            elif 60 < roll <= 85 and not self.monster.preparing:
                self.monster.rest()
            else:
                self.monster.prepare(self.player)

    def cleanup(self):
        '''
        If player was defending, it wears off.
        Check for dead monster. Give xp and level player up.
        Get next monster.
        Generate all player's available actions.
        Check for player status: apply effects (possibly, 
        remove actions), or make effects expire.
        '''
        if self.player.defending:
            self.player.toggle_defend(self.player)
        if self.monster.just_died:
            self.player.get_xp(self.monster)
            self.monster = self.get_next_monster()
        self.player.get_available_actions()
        if self.player.status:
            for effect in self.player.status:
                effect.tick_effect()


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
            input("Press [Enter] to continue. ")


if __name__ == "__main__":
    Game()