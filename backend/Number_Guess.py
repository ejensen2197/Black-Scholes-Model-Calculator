def Number_Guess():
    print(" ")
    print(" ")
    print("NUMBER GUESS")
    print("Guess a number between 1 and 10.")

    number_to_guess = random.randint(1, 10)
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if guess == number_to_guess:
            print("Congratulations! You've guessed the number.")
            return
        elif guess < number_to_guess:
            print("Too low! Try again.")
        else:
            print("Too high! Try again.")

        attempts += 1

    print(f"Sorry, you've used all {max_attempts} attempts. The number was {number_to_guess}.")