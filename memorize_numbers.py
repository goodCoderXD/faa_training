import random
import time
import os
import pandas as pd
import readchar

from rich.console import Console

console = Console()

ROUNDS = 1
CORRECT_AND_FAST = 0
NUMBERS = []

# Starting difficutly
LENGTH = 6
DELAY = 0.9
BACKWARDS = False
UNIQUE = True
RANDOM_LENGTH = True

# Difficulty upgrade
FLIP_DIRECTION = False
SWITCH_UNIQUE = False
MIN_STREAK = 5
MIN_ACCURACY = 0.9

RECORD = []
CORRECT_GUESSES = 0
TOTAL = 0
ERRORS = 0
BREAK_ON_ERRORS = 0

TRAIN_MODE = True

if not TRAIN_MODE:
    MIN_STREAK = 1
    BREAK_ON_ERRORS = 3


def set_next_difficulty():
    global LENGTH, BACKWARDS, UNIQUE

    # Difficulty steps:
    # +unique
    # +backward
    # +length
    while True:
        if not UNIQUE and LENGTH < 10 and SWITCH_UNIQUE:
            print("Difficulty upgrade: it's now unique numbers only!")
            time.sleep(0.5)
            UNIQUE = True
            yield

        if not BACKWARDS and FLIP_DIRECTION:
            print("Difficulty upgrade: it's now backwards!")
            time.sleep(0.5)
            BACKWARDS = True
            yield

        print(
            "Difficulty upgrade: +1 to length, numbers are forward and not necessarily unique!"
        )
        time.sleep(1)
        LENGTH += 1
        if FLIP_DIRECTION:
            BACKWARDS = False
        if SWITCH_UNIQUE:
            UNIQUE = False

        yield


def generate_sequence():
    global NUMBERS

    NUMBERS = []

    if RANDOM_LENGTH:
        if random.randint(0, 1):
            __ = range(LENGTH)
        else:
            weights = list(range(max(4, LENGTH - 1), LENGTH + 1))
            __ = range(random.choices(weights, weights=weights)[0])
    else:
        __ = range(LENGTH)

    for _ in __:
        next_number = random.randint(0, 9)
        while UNIQUE and next_number in NUMBERS:
            next_number = random.randint(0, 9)

        NUMBERS.append(next_number)


def display_sequence():
    for i, number in enumerate(NUMBERS):
        os.system("clear")
        print(number)
        time.sleep(DELAY)
        os.system("clear")
        if i != (len(NUMBERS) - 1):
            time.sleep(0.1)


def get_answer() -> bool:
    global CORRECT_AND_FAST, TOTAL, CORRECT_GUESSES, start, end, LAST_GUESS_RIGHT, LAST_GUESS_FAST, ERRORS
    start = time.time()
    if BACKWARDS:
        numbers = NUMBERS[::-1]
    else:
        numbers = NUMBERS

    for number in numbers:
        user_guess = readchar.readchar()
        if user_guess == str(number):
            os.system("clear")
        else:
            LAST_GUESS_RIGHT = False
            LAST_GUESS_FAST = False
            end = time.time()
            console.print(
                f"[bold red]kill yourself it was {number} and you typed {user_guess}, full sequence was {numbers}[/bold red]"
            )
            time.sleep(3)

            CORRECT_AND_FAST = 0
            TOTAL += 1
            ERRORS += 1
            return False

    end = time.time()

    threshold = max(1.0, LENGTH / 2)
    fast_enough = (end - start) <= threshold

    print(f"Correct, took: {end - start:.2f}s, need {threshold}")
    time.sleep(DELAY)

    LAST_GUESS_RIGHT = True
    LAST_GUESS_FAST = fast_enough

    if fast_enough:
        CORRECT_AND_FAST += 1
        CORRECT_GUESSES += 0.5

    CORRECT_GUESSES += 0.5
    TOTAL += 1
    return fast_enough


DIFFICULTY_SETTER = set_next_difficulty()

while True:
    try:
        os.system("clear")
        print(
            f"ROUND: {ROUNDS} LENGTH: {LENGTH} ({'backwards' if BACKWARDS else 'forwards'}) {UNIQUE=} STREAK: {CORRECT_AND_FAST}"
        )
        if TOTAL:
            print(f"Accuracy: {CORRECT_GUESSES/TOTAL:.4f}")

        if BREAK_ON_ERRORS and ERRORS >= BREAK_ON_ERRORS:
            raise KeyboardInterrupt()
        generate_sequence()
        print("ready?")
        time.sleep(2)
        os.system("clear")
        display_sequence()
        os.system("clear")
        print(f"Answer ({'backwards' if BACKWARDS else 'forwards'}):")

        get_answer()

        RECORD.append(
            (
                time.time(),
                "".join(map(str, NUMBERS)),
                LAST_GUESS_RIGHT,
                LAST_GUESS_FAST,
                ROUNDS,
                CORRECT_GUESSES / TOTAL,
                LENGTH,
                BACKWARDS,
                UNIQUE,
                end - start,
            )
        )

        ROUNDS += 1

        if (
            CORRECT_AND_FAST
            and CORRECT_AND_FAST >= MIN_STREAK
            and (
                (CORRECT_GUESSES / TOTAL) >= MIN_ACCURACY
                or CORRECT_AND_FAST >= MIN_STREAK * 3
            )
        ):
            next(DIFFICULTY_SETTER)
            CORRECT_AND_FAST = 0
            TOTAL = 0
            CORRECT_GUESSES = 0

    except KeyboardInterrupt:
        print()
        pd.DataFrame(
            data=RECORD,
            columns=[
                "time",
                "prompt",
                "was_user_guess_correct",
                "was_user_guess_fast",
                "total_round",
                "accuracy",
                "length",
                "is_backwards",
                "is_unique",
                "time_to_answer",
            ],
        ).to_csv("./last-run.csv")
        break
