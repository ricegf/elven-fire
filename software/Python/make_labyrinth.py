import random

from elvenfire import ELFError
from elvenfire.labyrinth.rooms import Room, SecretRoom

def main():

    numrooms = 30
    secretchance = 0.8
    level = 1
    for i in range(numrooms):

        if random.random() < secretchance:
            print(Room(level, i))
        else:
            print(SecretRoom(level, i))


if __name__ == '__main__':
    main()
