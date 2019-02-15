import os
import random
import sys
import time

from character import get_job
from monster import (Goblin, Troll, Dragon,
                     show_color_help)



    # def get_available_actions(self):
    #     '''Return available actions depending on status'''
    #     actions = [self.attack, self.rest, self.quit_game]
    #     if 'Silenced' in [d.name for d in self.status]:
    #         actions.remove(self.rest)
    #     return [self.attack, self.quit_game]




class Game:

    # CORE GAME LOOP
    def __init__(self):
        os.system('clear')
        self.setup()

        # RUNS WHILE PLAYER ALIVE AND AT LEAST ONE ENEMY REMAINS
        while self.player.hp > 0 and (self.monster or self.monster_pool or self.boss):

            # PRINT HEADER WITH PLAYER / MONSTER INFO
            os.system('clear')
            print('='*60)
            print(self.player)
            print('-'*60)
            print(self.monster.battlecry(), "\nA wild creature appears:")
            print(self.monster)
            print('-'*60)

            #PLAYER TURN
            self.player_turn()
            print()

            #MONSTER TURN
            self.monster_turn()
            print()

            #CLEANUP
            self.cleanup()
            if not self.player.killed_a_monster:
                print('-'*60)
                input('End of turn. Press [Enter] to continue.')

        # IF PLAYER REMAINS
        if self.player.hp > 0:
            time.sleep(1)
            print("\nCongrats! You defeated all the monsters! You win!")
            time.sleep(1)

        # IF ONE ENEMY REMAINS
        elif self.monster or self.monster_pool or self.boss:
            time.sleep(1)
            print("\nYou're dead!")
            time.sleep(1)

        sys.exit()

    # SPAWNS PLAYER AND MONSTERS
    def setup(self):
        self.endgame = False
        self.player = get_job()
        show_color_help()
        self.monster_pool = [Goblin(), Goblin(), Goblin(), Troll(), Troll()]
        self.boss = [Dragon()]
        self.monster = self.get_next_monster()

        input("Press [Enter] to start the game.")

    # GETS 2 GOBLINS, THEN NEXT RANDOM MONSTER, AND THEN BOSS
    def get_next_monster(self):
        if len(self.monster_pool) > 3:
            return self.monster_pool.pop(0)
        elif len(self.monster_pool) > 0:
            random_monster_id = self.monster_pool.index(random.choice(self.monster_pool))
            return self.monster_pool.pop(random_monster_id)
        else:
            try:
                return self.boss.pop(0)
            except IndexError:
                return None

    # MONSTER TURN
    def monster_turn(self):
        self.player.killed_a_monster = False

        # IF PLAYER (STILL) CONFUSED, IT FINALLY WEARS OFF 
        if 'confused' in self.player.status:
            self.player.status.remove('confused')


        # MONSTER ATTACK PHASE
        if self.monster.hp > 0:

            # IF MONSTER DOES ATTACK
            if random.randint(1,100) > 30:
            
                # HE CAN HIT OR MISS
                if self.monster.hits(self.monster.weapon, self.player):
                    time.sleep(1.5)
                    print(f"The {self.monster.color} {self.monster.name} "
                        f"attacks you with his {self.monster.weapon.name}!")

                    # HE MAY OR MAY NOT FALL IN THE TRAP
                    try:
                        if self.player.laid_trap:
                            if random.randint(0, 100) > 30:
                                time.sleep(1)
                                print(f"CLING! The {self.monster.name} "
                                    "steps on the trap, gets stunned and takes 1 damage!")
                                self.monster.hp -= 1
                                self.player.laid_trap = False
                                return
                    except AttributeError:
                        pass

                    # IF ATTACK GOES THROUGH, PLAYER TRIES TO DODGE
                    time.sleep(1.5)
                    print("\nYou try to dodge the attack...", end='')

                    # DODGE SUCCESSFUL = END MONSTER'S TURN
                    if self.player.dodges(self.player.weapon):
                        time.sleep(0.5)
                        print(" and succeed!")
                        time.sleep(1.5)

                    # MONSTER ACTUALLY HITS (DODGE FAILS)
                    else:
                        time.sleep(0.5)
                        print(" but you fail!")
                        dmg = self.monster.get_atk_dmg(self.monster.weapon, self.player)
                        self.player.take_dmg(dmg)
                        time.sleep(1)
                        print(f"The {self.monster.color} {self.monster.name} "
                            f"hits you for {dmg} HP.")

                        # MONSTER CAN APPLY ON-HIT EFFECT
                        time.sleep(0.5)
                        if random.randint(0, 100) > 50:
                            self.monster.debuff.apply(self.monster, self.player)
                            time.sleep(1.5)

                    # WARRIOR COUNTER-ATTACK (MIN LVL 2)
                    if self.player.job == "Warrior":
                        if self.player.max_xp > 5:
                            if random.randint(0, 100) >= 60:
                                print("\nCounter-attack!")
                                self.player_attack_phase()

            # IF MONSTER DOESN'T ATTACK, HE RESTS  
            else:
                time.sleep(1.5)
                self.monster.rest()
                time.sleep(1.5)

        # IF PLAYER SPENT 1 TURN SILENCED, RESTORE HIS POWERS
        try:
            self.player.silence_duration -= 1
            if self.player.silence_duration == 0:
                del self.player.silence_duration
                if 'silenced' in self.player.status:
                    self.player.status.remove('silence')
                self.player.job = self.player.old_job
                if self.player.job == "Warrior":
                    self.player.max_hp = 14
                    if self.player.hp_diff < 0:
                        self.player.hp += 4
        except AttributeError:
            pass

    #PLAYER TURN
    def player_turn(self):
        time.sleep(0.5)

        # CHECK FOR BURNING STATUS
        try:
            if self.monster.debuff.is_present(self.player):
                self.monster.debuff.tick()
        except AttributeError:
            pass

        # CHECK FOR FROZEN STATUS (PASS TURN UNLESS PLAYER CURES IT)
        if 'frozen' in self.player.status:
            print("You are frozen! Can't do anything!")
            time.sleep(1)
            if self.player.job == "Priest" and self.player.spell_1_casts > 0:
                if input("Luckily you're a Priest. Use [C]ure? [y/n]\n> ").lower() in 'cy':
                    self.player.spell_1(self.player)
                    self.player.spell_1_casts -= 1
                    time.sleep(0.5)
                else:
                    return
            else:
                self.player.status.remove('frozen')
                return

        # CHECK FOR SILENCED STATUS
        if 'silenced' in self.player.status:
            print("You are silenced!")
            time.sleep(1)
            if self.player.old_job == "Priest" and self.player.spell_1_casts > 0:
                if input("Luckily you're a Priest. Use [C]ure? [y/n]\n> ").lower() in 'cy':
                    self.player.spell_1(self.player)
                    self.player.spell_1_casts -= 1
                    self.player.job = self.player.old_job
                    if self.player.job == "Warrior":
                        self.player.max_hp = 14
                        if self.player.hp_diff < 0:
                            self.player.hp += 4
                    time.sleep(0.5)

            else:
                self.player.status.remove('silenced')

        # MAIN PHASE
        print("\nYour turn! What will you do?")
        self.player_main_phase()

    # PLAYER MAIN ACTION PHASE
    def player_main_phase(self):

        # PROMPTS PLAYER FOR ACTION
        self.action_prompt()

        # PHYSICAL ATTACK PHASE
        if self.action == 'a':

            # IF PLAYER IS CONFUSED, HE MIGHT HURT HIMSELF
            if 'confused' in self.player.status:
                self.player.status.remove('confused')
                if random.randint(0, 100) > 50:
                    time.sleep(0.5)
                    print("\nYou're so confused!")
                    time.sleep(0.5)
                    dmg = self.player.get_atk_dmg(self.player.weapon, self.monster)
                    print(f"You trip and fall down head first on your {self.player.weapon.name}, "
                          f"hurting yourself for {dmg} damage!")
                    self.player.take_dmg(dmg, source='confused')
                    time.sleep(1)

                    # IN CASE PLAYER DIES OF CONFUSION
                    if self.player.hp <= 0:
                        print("Silly you... you killed yourself! You lose!")
                        sys.exit()
                else:
                    self.player_attack_phase()
            else:
                self.player_attack_phase()

        # REST
        elif self.action == 'r':
            self.player.rest()

        # QUIT
        elif self.action == 'q':
            time.sleep(0.5)
            print("\nYou flee like a coward!")
            sys.exit()

        # CAST PHASE DEPENDING ON JOB
        else:
            self.player_cast_phase('Sorcerer', 'd', 'g', 'b')
            self.player_cast_phase('Priest', 'c', 'p', 'f')
            self.player_cast_phase('Hunter', 'h', 't', 's')
            self.player_cast_phase('Warrior', None, None, 'z')

    # PLAYER SPELL CAST PHASE
    def player_cast_phase(self, what_job, action1, action2, action3):

        # RESTRICTS ACTIONS TO SPECIFIC JOB
        if self.player.job == what_job:

            # CAST SPELL LVL 1
            if self.action == action1:
                if self.player.spell_1_casts > 0:
                    self.player.spell_1(self.monster)
                    self.player.spell_1_casts -= 1
                else:
                    print("You can't cast this spell anymore!")
                    self.player_main_phase()

            # CAST SPELL LVL 2
            elif self.action == action2:
                if self.player.spell_2_casts > 0:
                    self.player.spell_2(self.monster)
                    self.player.spell_2_casts -= 1

                else:
                    print("You can't cast this spell anymore!")
                    self.player_main_phase()
                    
            # CAST SPELL LVL 3
            elif self.action == action3:
                if self.player.spell_3_casts > 0:
                    self.player.spell_3(self.monster)
                    self.player.spell_3_casts -= 1

                else:
                    print("You can't cast this spell anymore!")
                    self.player_main_phase()

    # CUSTOM ACTION PROMPT DEPENDING ON JOB
    def action_prompt(self):

        # CASE OF SORCERER, PRIEST AND HUNTER
        if not self.player.job in ["Warrior", 'Jobless']:

            # DISPLAY RELEVANT SPELLS (IF LVL 1, LVL 2, OR LVL 3)
            if self.player.max_xp == 5:
                action = input("\n[A]ttack" 
                               f"\n{self.player.spell_1_name} ({self.player.spell_1_casts})"
                               "\n[R]est"
                               "\n[Q]uit\n"
                               "\n> ")
            elif self.player.max_xp == 6:
                action = input("\n[A]ttack"
                               f"\n{self.player.spell_1_name} ({self.player.spell_1_casts})"
                               f"\n{self.player.spell_2_name} ({self.player.spell_2_casts})"
                               "\n[R]est"
                               "\n[Q]uit\n"
                               "\n> ")
            else:
                action = input("\n[A]ttack"
                               f"\n{self.player.spell_1_name} ({self.player.spell_1_casts})"
                               f"\n{self.player.spell_2_name} ({self.player.spell_2_casts})"
                               f"\n{self.player.spell_3_name} ({self.player.spell_3_casts})"
                               "\n[R]est"
                               "\n[Q]uit\n"
                               "\n> ")

        # CASE OF WARRIOR OR 'JOBLESS' (NO ACTIVE SPELL UNTIL LVL 3)
        elif self.player.job == "Warrior":
            if self.player.max_xp > 6:
                action = input("\n[A]ttack"
                               f"\n{self.player.spell_3_name} ({self.player.spell_3_casts})"
                               "\n[R]est"
                               "\n[Q]uit\n"
                               "\n> ")
            else:
                action = input('\n[A]ttack \n[R]est \n[Q]uit\n\n> ')
        else:
            action = input('\n[A]ttack \n[R]est \n[Q]uit\n\n> ')

        # MAKE SURE THAT ONLY JOB ALLOWED ACTIONS ARE SELECTED
        for job, allowed_actions in {'Jobless': 'arq',
                                     'Warrior': 'arqz',
                                     'Sorcerer': 'arqdgb',
                                     'Priest': 'arqcpf',
                                     'Hunter': 'arqhts'}.items():
            if self.player.job == job:
                if action in allowed_actions and action != '':
                    self.action = action
                else:
                    self.action_prompt()

    # PLAYER PHYSICAL ATTACK PHASE
    def player_attack_phase(self):
        time.sleep(0.5)
        print(f"\nYou draw your {self.player.weapon.name} "
              f"to attack the {self.monster.name}...", end='')

        # PLAYER HITS
        if self.player.hits(self.player.weapon, self.monster):
            time.sleep(0.5)
            print(" and hit!")
            time.sleep(1)
            print(f"The {self.monster.name} tries to dodge...", end='')
            sys.stdout.flush()

            # MONSTER DODGES
            if self.monster.dodges(self.monster.weapon):
                time.sleep(0.5)
                print(" and succeeds!")

            # MONSTER DODGE FAILS
            else:
                time.sleep(0.5)
                print(" but he fails!")
                dmg = self.player.get_atk_dmg(self.player.weapon, self.monster)
                self.monster.take_dmg(dmg)
                time.sleep(1)
                print(f"You hit it for {dmg} HP.")

        # PLAYER MISSES
        else:
            sys.stdout.flush()
            time.sleep(0.5)
            print(" but you miss!")

    # DEAD MONSTER CLEANUP
    def cleanup(self):

        # IF PRIEST DIES AFTER USING REVIVE
        try:
            if self.player.hp <= 0 and self.player.revive:
                print("You die.")
                time.sleep(1)
                print("The Mighty Gods heard your prayer. You are given another chance.")
                print("RESURRECTION!")
                self.player.hp += random.randint(2,5)
                self.player.revive = False
                time.sleep(1)
        except AttributeError:
            pass

        if self.monster.hp <= 0:
            time.sleep(1.5)
            print(f"You have defeated the {self.monster.color} {self.monster.name}!")
            self.player.killed_a_monster = True
            time.sleep(0.5)
            print(f"You gain {self.monster.xp} XP!")
            self.player.xp += self.monster.xp

            # PLAYER LEVELS UP
            self.player.check_xp()

            self.monster = self.get_next_monster()
            print('\n'+'='*60)

            # PRINTS RELEVANT FOOTER
            if len(self.boss) != 0:
                remaining = len(self.monster_pool) + len(self.boss)
                input(f"{remaining} enemies remaining. Press [Enter] to go ahead. ")
            else:
                if self.endgame == False:
                    input("You've woken up the ancient Dragon! Press [Enter] to go ahead. ")
                    self.endgame = True
                else:
                    input("You've cleared the dungeon.")

if __name__ == '__main__':
    Game()