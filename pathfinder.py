import os
import random
import readchar
import time

LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
NUMBERS = list(range(1, 27))
ORDER = random.choice(["LETTER FIRST", "NUMBER FIRST"])


def sequence():
    for number, letter in enumerate(LETTERS, 1):
        if ORDER == "LETTER FIRST":
            yield letter
            yield number
        else:
            yield number
            yield letter


SEQUENCE = list(sequence())
ERRORS = 0
TIMES = []

display_msg = f"Use numpad to select quadrant, begin with {SEQUENCE[0]}"

index = 0
item = SEQUENCE[0]
try:
    for index, item in enumerate(SEQUENCE):
        correct = False
        while not correct:
            quadrant_values = [item]

            for _ in range(3):
                r = random.randint(1, 4)
                match r:
                    case 1:
                        # random thing
                        choice = random.choice(LETTERS + NUMBERS)
                        while choice in quadrant_values or choice == item:
                            choice = random.choice(LETTERS + NUMBERS)

                        quadrant_values.append(choice)
                    case 2:
                        # match alpha or num
                        for _ in range(100):
                            if isinstance(item, int):
                                choice = random.choice(NUMBERS)
                            else:
                                choice = random.choice(LETTERS)

                            if choice not in quadrant_values and choice != item:
                                break

                        quadrant_values.append(choice)
                    case 3:
                        # Close value
                        for _ in range(100):
                            choice = random.choice(
                                SEQUENCE[max(0, index - 2) : index + 5]
                            )
                            if choice not in quadrant_values and choice != item:
                                break

                        quadrant_values.append(choice)
                    case 4:
                        # close same alpha/num val
                        for _ in range(100):
                            choice = random.choice(
                                SEQUENCE[max(0, index - 2) : index + 5]
                            )
                            if (
                                type(choice) == type(item)
                                and item != choice
                                and choice not in quadrant_values
                            ):
                                break

                        quadrant_values.append(choice)

            random.shuffle(quadrant_values)

            os.system("clear")
            print(display_msg)
            print(quadrant_values[0], " " * 10, quadrant_values[1])
            print()
            print(quadrant_values[2], " " * 10, quadrant_values[3])

            start = time.time()
            user_guess = int(readchar.readchar())
            end = time.time()

            TIMES.append(end - start)

            match user_guess:
                case 7:
                    correct = quadrant_values[0] == item
                case 9:
                    correct = quadrant_values[1] == item
                case 1:
                    correct = quadrant_values[2] == item
                case 3:
                    correct = quadrant_values[3] == item
                case _:
                    correct = False
                    TIMES.pop()

            if correct:
                display_msg = f"Correct, took {end-start:.2f}s"
            else:
                display_msg = "kill yourself"
                ERRORS += 1
except ValueError:
    pass

print(f"{ERRORS=}")
print(f"avg time: {sum(TIMES) / len(TIMES)}")
print(f"Distance: {index + 1} - {item}")
