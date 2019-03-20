This is a text-based combat game that I wrote in python3.7 to practice object-oriented programming, general Python, and have fun!  
In this game, you must fight your way through a succession of several enemies to win, using various spells and attacks.

**How to run the game:**  
`python3.7 game.py`

---
# Player / Monster stats
* Attack power (increases damage of basic attacks)
* Ability power (increases damage of magic-based abilities)
* Hit chance (how likely you are to hit your attacks)
* Dodge chance (how likely you are from dodging attacks)
* Toughness (reduces incoming damage)

Each turn, you may choose among several actions:
1. Attack
2. Use abilities
3. Defend: reduce incoming damage this turn
4. Rest: regen a small amount of HP, but attacks you receive may crit!
5. Quit

---

# Jobs (Classes):

Each class has 3 abilities that they can learn as they level up. You start with your first ability at level 1, learn the second at level 2, and the third at level 3.

All abilities have a very small chance to (critically) fail!

## Warrior  
**Stats:**  
Increased toughness, base HP, and attack power.

**Abilities:**
1. `Extra HP` (passive). You start with a larger HP pool.
2. `Counter-attack` (passive). You have a chance to automatically retaliate after being attacked.
3. `Brutalize`. You steal the enemy's weapon and use it against him, with added damage.

## Priest
**Stats:**  
Increased toughness, ability power, and dodge chance.

**Abilities:**  
1. `Cleanse`. You remove all negative status ailments. Usable when Frozen and Silenced.
2. `Pray`. Heal yourself for a small amount. Can crit for 2x heal value.
3. `Final Wish`. Next death, you revive and are healed for a small amount.

## Hunter
**Stats:**  
Increased hit chance and dodge chance.

**Abilities:**  
1. `Hide`. Vanish at the end of your turn, gaining extra evasion. Next successful attack of Snipe ability will crit.
2. `Trap`. Lay a trap on the ground, that has a chance to damage and stun enemies until the end of next turn.
3. `Snipe`. A powerful attack that can't be dodged, using the Railgun weapon. If Hidden, the shot will deal critical damage.

## Sorcerer
**Stats:**  
Highly increased ability power.

**Abilities:**  
1. `Leech`. You deal damage, and heal yourself for the same amount.
2. `Greenify`. The enemy looses all his special attributes.
3. `Obliterate`. A very powerful magic attack.

---
# Weapons:

You may choose from 3 starter weapons:
* `Axe`: more powerful
* `Bow`: ranged (more evasive), more chances to crit
* `Dagger`: more accurate

Monster will also have 3 more available weapons:
* `Kung-Fu`: basically, no weapon
* `Lightsaber`: very powerful, very accurate
* `Railgun`: ranged (more evasive), most powerful, very accurate

All weapons have a very small creit chance.

# Monsters
You will encounter 3 enemy tiers, each more powerful and more resilient than the previous. Enemy types include goblins, trolls, and so on.

Monsters may attack, regen HP, or prepare a powerful attack.

More importantly, each monster will have a special affixes (or "powers"), that need to be taken into account if you want to survive. On hit, each attack has a chance to apply a debuff, depending on the monster's color.

Enemies can be:
* `Green`: no special attributes. You're lucky.
* `Red`: attacks may make you burn, taking damage each turn.
* `White`: attack may freeze you, preventing you from doing anything.
* `Black`: attacks may silence you, preventing you from using abilities, and removing any special bonus due to your job/class.
* `Spectral`: attack may traumatize you, preventing you from attacking or defending. 

# Notes

This game is not very well balanced yet. Feel free to fix the numbers, or to implement your own mechanics.  
If you do, please let me know, I'd be happy to see whatever you come up with!