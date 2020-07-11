from cs50 import get_int


def main():
    n = get_height()
    
    for i in range(n):
        for d in range(n - i - 1):
            print(" ", end="")
        for j in range(i + 1):
            print("#", end="")
        print()
    

def get_height():
    while True:
        h = get_int("Height: ")
        if h > 0 and h < 9:
            break
    return h


main()