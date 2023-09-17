import os
import time
import readchar
import random

CHARS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

HIGH_SIMILARITY_MATRIX = [
    ["B", "P", "R"],
    ["B", "3", "8"],
    ["S", "3", "8"],
    ["8", "9", "6"],
    ["8", "5"],
    ["C", "G", "O", "Q", "0"],
    ["T", "7", "I", "1"],
    ["J", "7", "S"],
    ["S", "5"],
    ["0", "O", "Q", "D"],
    ["S", "5", "Z"],
    ["I", "1"],
    ["U", "V", "Y"],
    ["4", "A"],
    ["F", "E"],
    ["N", "M", "W"],
    ["F", "H", "L"],
    ["Z", "X", "N"],
    ["W", "H"],
    ["K", "X", "N"],
    ["W", "K", "V"],
    ["Y", "K", "V"],
    ["E", "3", "T"],
]

# Do swaps
# abc -> acb

LENGTH = 5

CORRECT = 0
TOTAL = 0
TIMES = []

TIME_START = time.time()

while True:
    random.shuffle(CHARS)
    left_side = CHARS[:LENGTH]
    right_side = left_side[:]

    if random.random() >= 0.5:
        match random.randint(1, 3):
            case 1:
                # Swap two chars
                i1 = random.randint(0, LENGTH - 1)
                i2 = random.randint(0, LENGTH - 1)
                right_side[i1], right_side[i2] = right_side[i2], right_side[i1]
            case 2:
                # just replace w/ random
                i1 = random.randint(0, LENGTH - 1)
                right_side[i1] = random.choice(CHARS)
            case 3:
                # replace with high similarity char
                selection = random.choice(HIGH_SIMILARITY_MATRIX)
                random.shuffle(selection)
                c1, c2 = selection[:2]
                i1 = random.randint(0, LENGTH - 1)
                left_side[i1] = c1
                right_side[i1] = c2
            case _:
                pass

        # different

    ANSWER = ["d", "s"][left_side == right_side]

    print("ready?")
    time.sleep(2)
    os.system("clear")

    if TOTAL:
        print(
            f"ROUND: {TOTAL}, ACC: {(CORRECT / TOTAL):5f}, Avg Time: {sum(TIMES) / len(TIMES):.5f}s"
        )
        if (now := time.time()) - TIME_START > 15 * 60 and random.randint(1, 15) == 1:
            print(
                "Total time:",
                int(now - TIME_START) // 60,
                ":",
                int(now - TIME_START) % 60,
            )
            exit()
    else:
        print(f"ROUND: {TOTAL}")
    print("S = Same, D = Diff")
    print("".join(left_side), " " * 20, "".join(right_side))
    start = time.time()
    user_guess = readchar.readchar()
    end = time.time()
    TIMES.append(end - start)
    TOTAL += 1
    if ANSWER == user_guess:
        CORRECT += 1
        print("Correct!")
        print(f"Answered in {TIMES[-1]:2f}")
    else:
        print("Kill yourself, you said:", {"s": "Same", "d": "Diff"}[user_guess])
