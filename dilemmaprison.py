import random
import sys

class Prisoner:
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def betray_trust(self):
        return True if self.score < 3 else False
    def betray_random(self):
        return True if random.random() < .6 else False
    def change_score(self, num):
        self.score += num

# Load data
def load_data(filename):
    file = open(filename)
    names = file.read()
    file.close()
    return names.split("\n")

# Menu function
def menu():
    print()
    print("(1) Next round")
    print("(2) Rules")
    print("(3) Theory")
    print("(4) Reset")
    print("(0) Exit")
    while True:
        putin = input("Input: ")
        if putin.isnumeric():
            putin = int(putin)
            if putin in [0,1,2,3,4]:
                return putin

def generate_matches():
    pairs = []
    pri_temp = prisoners.copy()
    while len(pri_temp) > 1:
        pair = random.sample(pri_temp, 2)
        for p in pair:
            pri_temp.remove(p)
        pairs.append(pair)
    if len(pri_temp) == 1:
        pairs.append(pri_temp[0]) # the last guy
    print("\nNext up:")
    for p in pairs:
        if isinstance(p, list):
            print(p[0].name.upper(), "vs", p[1].name.upper())
        else:
            print("Not participating:", p.name)
    return pairs

def games(pairs):
    print("\nThe results:")
    for p in pairs:
        if isinstance(p, list): # ignore loner if exists
            betray0 = False
            betray1 = False
            if rnd == 1:
                betray0 = p[0].betray_random()
                betray1 = p[1].betray_random()
            else:
                betray0 = p[0].betray_trust()
                betray1 = p[1].betray_trust()
            if betray0 and betray1: # nothing happens
                print(p[0].name, "and", p[1].name, "BETRAY each other")
            if betray0 and not betray1: # 0 betrays 1
                print(p[0].name, "BETRAYS", p[1].name)
                p[0].change_score(3)
                p[1].change_score(-2)
            if not betray0 and betray1: # 1 betrays 0
                print(p[1].name, "BETRAYS", p[0].name)
                p[0].change_score(-2)
                p[1].change_score(3)
            if not betray0 and not betray1: # players ally
                print(p[0].name, "and", p[1].name, "ALLY")
                p[0].change_score(2)
                p[1].change_score(2)

# reset the game
def reset():
    rnd = 1
    prisoners.clear()
    
    # Get the number of prisoners
    while True:
        prisoner_count = input("The number of prisoners: ")
        if prisoner_count.isnumeric():
            prisoner_count = int(prisoner_count)
            break
        else:
            continue

    # Generate prisoners
    
    startingscore = 3
    for i in range(prisoner_count):
        name = random.choice(names)
        names.remove(name)
        prisoners.append(Prisoner(name, startingscore))
    return rnd

names = load_data("names.txt")

# Text data
rules = '''
RULES OF THE GAME

Prisoner's dilemma is a game where two contestants play against one another.
They can choose either "ally" or "betray".

- If both choose ally, they get both 2 points.
- If both choose betray, they don't get or lose any points.
- If one betrays and other allies, betrayer gets 3 points and allier loses 2.

This is continued with mixed pairs round after round.
If contestant's points drop to 0, they lose.
If they get 9 points, they win.

These rules are inspired by the video game Zero Escape: VLR.'''
theory = '''
THEORY OF WINNING

My theory is that everyone can SAFELY win the game and get to 9 points if they
set common rules and co-operate. This purpose of this program is to test it.

The rule is simple: everyone betrays if they are in immediate danger of losing
(e.g. have less than 3 points) and allies in any other case. In other words,
they ally as much as they can, but never risk losing points on the brink of
defeat and thus never lose.

In the first round betraying is random. This is because the contestants
didn't have time to agree on the rules before that.

Nobody is allowed to leave if everyone doesn't have 9 points or more. This
is enforced by social pressure and the fact that there's nothing to GAIN
by leaving people behind.

This theory is based on the assumption that nobody wants to be
an asshole for no reason.'''

rnd = 0
prisoners = []
restart = False

rnd = reset()

# Main loop
while True:
    print("\n-------\nRound", rnd, "\n-------\n")
    for p in prisoners:
        flavor = ""
        if p.score < 3:
            flavor = "(DANGER)"
        if p.score > 8:
            flavor = "(WINNER)"
        print(p.name, p.score, flavor)

    pairs = generate_matches()

    # Main menu
    while True:
        choice = menu()
        if choice == 0:
            sys.exit()
        elif choice == 1:
            break
        elif choice == 2:
            print(rules)
        elif choice == 3:
            print(theory)
        elif choice == 4:
            restart = True
            break

    if restart:
        rnd = reset()
        restart = False
        continue

    games(pairs)

    rnd += 1
