from cs50 import get_float


def main():
    n = get_money()
    
    cents = round(n * 100)
    quarters = 25
    dimes = 10
    nickels = 5
    pennies = 1
    coins = 0
    
    while quarters <= cents:
        coins += 1
        cents = cents - quarters
        
    while dimes <= cents:
        coins += 1
        cents = cents - dimes
        
    while nickels <= cents:
        coins += 1
        cents = cents - nickels
        
    while pennies <= cents:
        coins += 1
        cents = cents - pennies
        
    print(f"{coins}")


def get_money():
    while True:
        m = get_float("Change owed ? ")
        if m > 0:
            break
    return m
    
    
main()