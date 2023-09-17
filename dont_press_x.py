import random
import time
import os
import readchar

import select
import sys

import inputimeout

ROUND = 0
TIMEOUT = 0.9
INVERTED_PROBABILITY = 5

CHARS = list("ABCDEFGHIJKLMNOPQRSTUVWYZ0123456789!@#$%^&*()\\/><")
SIMILAR_TO_X = list("YK\\/%#><")
ALL_CHARS = CHARS + SIMILAR_TO_X

TIMES = []

TOTAL_X = 0
TOTAL_OTHER = 0
HANDLED_X_RIGHT = 0
HANDLED_OTHER_RIGHT = 0
CORRECT = 0

TOTAL_START = int(time.time())

while True:
    match random.randint(1, INVERTED_PROBABILITY):
        case 1:
            char = "X"
        case _:
            char = random.choice(ALL_CHARS)

    os.system("clear")
    print("Do not press anything if it's X, press enter on any other char.")
    if TIMES and ROUND:
        now = int(time.time())
        print(
            f"Avg Time: {sum(TIMES) / len(TIMES):.5f}s \n"
            f"X Accuracy: {HANDLED_X_RIGHT / max(1, TOTAL_X):.5f} \n"
            f"Other Accuracy: {HANDLED_OTHER_RIGHT / max(1, TOTAL_OTHER):.5f} \n"
            f"Round: {ROUND + 1} Time: {(now - TOTAL_START) // 60}:{(now - TOTAL_START) % 60}"
        )
        if (now - TOTAL_START) > 15 * 60 and random.randint(1, 15) == 1:
            sys.exit()
    print(char)
    start = time.time()
    if char != "X":
        try:
            inputimeout.inputimeout(timeout=TIMEOUT)
            user_guess = "\n"
        except inputimeout.TimeoutOccurred:
            user_guess = "x"

        TOTAL_OTHER += 1
    else:
        TOTAL_X += 1
        try:
            inputimeout.inputimeout(timeout=TIMEOUT)
            user_guess = "\n"
        except inputimeout.TimeoutOccurred:
            user_guess = "x"

    end = time.time()
    TIMES.append(end - start)

    match (user_guess, char == "X"):
        case ("\n", False):
            CORRECT += 1
            HANDLED_OTHER_RIGHT += 1
        case ("x", True):
            TIMES.pop()
            CORRECT += 1
            HANDLED_X_RIGHT += 1
        case ("x", False):
            # WRONG
            TIMES.pop()
        case ("\n", True):
            # WRONG
            TIMES.pop()
        case _:
            pass

    ROUND += 1
