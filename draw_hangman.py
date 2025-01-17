def draw (misses, wrong):

    if misses == 0:
        for i in range(8):
            print(" ")
        print("\nWrong guesses:")
        print(*wrong, sep=",")
    elif misses == 1:
        for i in range(7):
            print(" ")
        print("/ \\")
        print("\nWrong guesses:")
        print(*wrong, sep=",")
    elif misses == 2:
        for i in range(2):
            print(" ")
        for i in range(5):
            print(" |")
        print("/ \\")
        print("\nWrong guesses:")
        print(*wrong, sep=",")
    elif misses == 3:
        print(" ")
        print("_" * 7)
        for i in range(5):
            print(" |")
        print("/ \\")
        print("\nWrong guesses:")
        print(*wrong, sep=",")
    elif misses == 4:
        print(" ")
        print("_" * 7)
        print(" |    |")
        print(" |    O")
        for i in range(3):
            print(" |")
        print("/ \\")
        print("\nWrong guesses:")
        print(*wrong, sep=",")
    elif misses == 5:
        print(" ")
        print("_" * 7)
        print(" |    |")
        print(" |    O")
        print(" |    |")
        print(" |    |")
        print(" |")
        print("/ \\")
        print("\nWrong guesses:")
        print(*wrong, sep=",")
    elif misses == 6:
        print(" ")
        print("_" * 7)
        print(" |    |")
        print(" |    O")
        print(" |   \\|/")
        print(" |    |")
        print(" |")
        print("/ \\")
        print("\nWrong guesses:")
        print(*wrong, sep=",")
    elif misses == 7:
        print(" ")
        print("_" * 7)
        print(" |    |")
        print(" |    O")
        print(" |   \\|/")
        print(" |    |")
        print(" |   / \\")
        print("/ \\")
        print("\nWrong guesses:")
        print(*wrong, sep=",")
    else:
        print("\nGame Over")
        print("\nWrong guesses:")
        print(*wrong, sep=",")

    


wrong = ["a", "b", "c"]
for i in range(9):
    draw(i, wrong)
