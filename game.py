import os
import random
import sys
import time

from character import get_job
from monster import (Goblin, Troll, Dragon,
                     show_color_help)


class Game:

    # CORE GAME LOOP
    def __init__(self):
        os.system('clear')
        self.setup()

        # RUNS WHILE PLAYER ALIVE AND AT LEAST ONE ENEMY REMAINS
        while self.player.hp > 0 and (self.monster or self.monster_pool or self.boss):

            # PRINT HEADER WITH PLAYER / MONSTER INFO
            os.system('clear')
            print('='*90)
            print(self.player)
            print('-'*90)
            print(self.monster.battlecry(), "\nA wild creature appears:")
            print(self.monster)
            print('-'*90)

            #PLAYER TURN
            self.player_turn()
            print(' ')

            #MONSTER TURN
            self.monster_turn()
            print(' ')

            #CLEANUP
            self.cleanup()
            if not self.player.killed_a_monster:
                print('-'*90)
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
        self.monster_pool = [Goblin(), Troll(), Goblin(), Troll(), Goblin()]
        self.boss = [Dragon()]
        self.monster = self.get_next_monster()
        self.monster_actions = ["is in no mood to attack",
                                "looks at you with disdain",
                                "takes a nap",
                                "wanders around nervously",
                                "can't be bothered",
                                "arrogantly ignores you",
                                "scratches his nose"]

        self.monster_deaths = ["dies!",
                               "screams in agony, and collapses!",
                               f"takes a fatal blow from your {self.player.weapon}!",
                               "succumbs to his wounds!",
                               "runs away in despair, and bleeds to death.",
                               "breathes his last breath... RIP!"]

        input("Press [Enter] to start the game.")

    # GETS NEXT MONSTER FROM POOL, AND THEN BOSS
    def get_next_monster(self):
        if len(self.monster_pool) > 0:
            return self.monster_pool.pop(self.monster_pool.index(random.choice(self.monster_pool)))
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

        # MONSTER DEATH SCENARIOS
        if self.monster.hp <= 0:
            time.sleep(1.5)
            d = self.monster_deaths.pop(self.monster_deaths.index(random.choice(self.monster_deaths)))
            print(f"{self.monster.battlecry()}! The {self.monster.color} "
                  f"{self.monster.__class__.__name__} {d}")

        # MONSTER ATTACK PHASE
        else:

            # IF MONSTER DOES ATTACK
            if self.monster.attack_hits(self.monster.weapon):
                time.sleep(1.5)
                print(f"The {self.monster.color} {self.monster.__class__.__name__} "
                      f"attacks you with his {self.monster.weapon}!")

                # HE MAY OR MAY NOT FALL IN THE TRAP
                if self.player.laid_trap:
                    if random.randint(0, 100) > 30:
                        time.sleep(1)
                        print(f"CLING! The {self.monster.__class__.__name__} "
                              "steps on the trap, gets stunned and takes 1 damage!")
                        self.monster.hp -= 1
                        self.player.laid_trap = False
                        return

                # IF ATTACK GOES THROUGH, PLAYER TRIES TO DODGE
                time.sleep(1.5)
                print("\nYou try to dodge the attack...", end='')

                # DODGE SUCCESSFUL = END MONSTER'S TURN
                if self.player.dodge(self.player.weapon, self.player):
                    time.sleep(0.5)
                    print(" and succeed!")
                    time.sleep(1.5)
                    return

                # DODGE FAILS = PROCEED
                else:
                    time.sleep(0.5)
                    print(" but you fail!")
                    dmg = self.monster.get_dmg(self.monster.weapon, self.player)
                    self.player.hp -= dmg
                    time.sleep(1)
                    print(f"The {self.monster.color} {self.monster.__class__.__name__} "
                          f"hits you for {dmg} HP.")

                    # MONSTER CAN APPLY ON-HIT EFFECT
                    time.sleep(0.5)
                    if random.randint(0, 100) > 50:
                        self.monster.on_hit_effect(self.player)
                        time.sleep(1.5)

                    # CHECK FOR SILENCED STATUS
                    self.apply_debuff('silenced')

                # WARRIOR COUNTER-ATTACK (MIN LVL 2)
                if self.player.job == "Warrior":
                    if self.player.xpn > 5:
                        if random.randint(0, 100) >= 60:
                            print("\nCounter-attack!")
                            self.player_attack_phase()

            # IF MONSTER DOESN'T ATTACK  
            else:
                time.sleep(1.5)
                print(f"The {self.monster.color} {self.monster.__class__.__name__} "
                      + random.choice(self.monster_actions) + '...')
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
                    self.player.base_hp = 14
                    if self.player.hp_diff < 0:
                        self.player.hp += 4
        except AttributeError:
            pass

    #PLAYER TURN
    def player_turn(self):
        time.sleep(0.5)

        # CHECK FOR BURNING STATUS
        self.apply_debuff('burning')

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
                    self.player.job = self.player.old_job
                    if self.player.job == "Warrior":
                        self.player.base_hp = 14
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
                    dmg = self.player.get_dmg(self.player.weapon, self.player)
                    print(f"You trip and fall down head first on your {self.player.weapon}, "
                          f"hurting yourself for {dmg} damage!")
                    self.player.hp -= dmg
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
            time.sleep(0.5)
            print("\nYou rest, and regenerate 1 HP!")

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
            if self.player.xpn == 5:
                action = input("\n[A]ttack" 
                               f"\n{self.player.spell_1_name} ({self.player.spell_1_casts})"
                               "\n[R]est"
                               "\n[Q]uit\n"
                               "\n> ")
            elif self.player.xpn == 6:
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
            if self.player.xpn > 6:
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
                                     'Warrior': 'arq',
                                     'Sorcerer': 'arqdgb',
                                     'Priest': 'arqcpf',
                                     'Hunter': 'arqhts'}.items():
            if self.player.job == job:
                if action in allowed_actions and action != '':
                    self.action = action
                else:
                    self.action_prompt()

    # CHECK FOR 'BURNING' OR 'SILENCED', DEBUFF AND APPLIES THE CONSEQUENCES:
    def apply_debuff(self, debuff):
        if debuff in self.player.status:

            # BURNING?
            if debuff == 'burning':
                print("You're burning! You take 1 damage.")
                time.sleep(1.5)
                self.player.hp -= 1
                self.player.burn_duration -= 1
                if self.player.burn_duration == 0:
                    self.player.status.remove('burning')

                # IN CASE THE BURNING KILLS THE PLAYER
                if self.player.hp <= 0:
                    time.sleep(1)
                    print("The fire damage was fatal... You die!")

                    # IF PRIEST USED REVIVE
                    if self.player.revive:
                        print("RESURRECTION!")
                        print("The Mighty Gods heard your prayer. You are given another chance.")
                        self.player.hp += 1
                        self.player.revive = False
                        time.sleep(1)

                    # OTHERWISE
                    else:
                        time.sleep(1)
                        sys.exit()

            # SILENCED?
            elif debuff == 'silenced':
                if self.player.silence_duration == 2:
                    print("You lose all your special powers!")
                    time.sleep(1.5)
                    if self.player.job == "Warrior":
                            if self.player.hp > 10:
                                self.player.hp_diff = self.player.hp - self.player.base_hp
                                self.player.hp = 10 + self.player.hp_diff
                            self.player.base_hp = 10
                    if self.player.job != 'Jobless':
                        self.player.old_job = self.player.job
                        self.player.job = "Jobless"

    # PLAYER PHYSICAL ATTACK PHASE
    def player_attack_phase(self):
        time.sleep(0.5)
        print(f"\nYou draw your {self.player.weapon} "
              f"to attack the {self.monster.__class__.__name__}...", end='')

        # PLAYER HITS
        if self.player.attack_hits(self.player.weapon):
            time.sleep(0.5)
            print(" and hit!")
            time.sleep(1)
            print(f"The {self.monster.__class__.__name__} tries to dodge...", end='')
            sys.stdout.flush()

            # MONSTER DODGES
            if self.monster.dodge(self.monster.weapon, self.player):
                time.sleep(0.5)
                print(" and succeeds!")

            # MONSTER DODGE FAILS
            else:
                time.sleep(0.5)
                print(" but he fails!")
                dmg = self.player.get_dmg(self.player.weapon, self.player)
                self.monster.hp -= dmg
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
        if self.player.hp <= 0 and self.player.revive:
            print("You die.")
            time.sleep(1)
            print("The Mighty Gods heard your prayer. You are given another chance.")
            print("RESURRECTION!")
            self.player.hp += random.randint(2,5)
            self.player.revive = False
            time.sleep(1)


        if self.monster.hp <= 0:
            time.sleep(1.5)
            print(f"You have defeated the {self.monster.color} {self.monster.__class__.__name__}!")
            self.player.killed_a_monster = True
            time.sleep(0.5)
            print(f"You gain {self.monster.xp} XP!")
            self.player.xp += self.monster.xp

            # PLAYER LEVELS UP
            if self.player.leveled_up():
                time.sleep(1)
                if self.player.level == 2:
                    print("\nLEVEL UP! You gain +1 max. damage, and +2 accuracy!")
                    self.player.max_dmg += 1
                    self.player.attack_dice += 2
                    time.sleep(1)
                    print(f"You learn {self.player.spell_2_name}!")
                time.sleep(1)
                if self.player.level == 3:
                    print("\nLEVEL UP! You gain +1 max. damage, and +2 evasion!")
                    self.player.max_dmg += 1
                    self.player.dodge_dice += 2
                    time.sleep(1)
                    print(f"You learn {self.player.spell_3_name}!")
                time.sleep(1)


            self.monster = self.get_next_monster()
            print('\n'+'='*90)

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


Game()
