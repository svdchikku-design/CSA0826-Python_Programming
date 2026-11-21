import random

# ---------- MODULE 1: Game Setup ----------
LEVELS = {
    "1": ("Easy",   1, 50,  10),
    "2": ("Medium", 1, 100, 7),
    "3": ("Hard",   1, 200, 5),
}

def setup_game():
    print("=== NUMBER GUESSING GAME ===")
    print("1. Easy   (1-50,  10 attempts)")
    print("2. Medium (1-100,  7 attempts)")
    print("3. Hard   (1-200,  5 attempts)")
    choice = input("Choose level (1/2/3): ").strip()
    while choice not in LEVELS:
        choice = input("Invalid! Enter 1, 2 or 3: ").strip()
    name, low, high, limit = LEVELS[choice]
    secret = random.randint(low, high)
    print(f"\n{name} level: guess {low} to {high}.")
    return secret, low, high, limit

# ---------- MODULE 2: Guess Loop ----------
def get_guess(low, high):
    while True:
        try:
            guess = int(input("Your guess: "))
            if low <= guess <= high:
                return guess
            print(f"Enter {low} to {high} only.")
        except ValueError:
            print("Enter a whole number.")

def play_round(secret, low, high, limit):
    used = 0
    while used < limit:
        print("Attempts left:", limit - used)
        guess = get_guess(low, high)
        used += 1
        if guess == secret:
            return True, used
        if guess < secret:
            print("Too low! Go higher.")
        else:
            print("Too high! Go lower.")
    return False, used

# ---------- MODULE 3: Score & Replay ----------
def calculate_score(used, limit):
    return (limit - used + 1) * 10

def show_result(won, used, limit, secret):
    if won:
        score = calculate_score(used, limit)
        print(f"\nCorrect! Score: {score}")
        return score
    print(f"\nGame over! It was {secret}.")
    return 0

def main():
    best = 0
    while True:
        secret, low, high, limit = setup_game()
        won, used = play_round(secret, low, high, limit)
        score = show_result(won, used, limit, secret)
        best = max(best, score)
        print(f"Best score so far: {best}")
        again = input("Play again? (y/n): ")
        if again.strip().lower() != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
