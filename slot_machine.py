import random

MAX_LINES = 3
MAX_BET = 500
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "7" : 2,
    "$" : 5,
    "%" : 8,
    "&" : 10,
    "#" : 13,
    "@" : 15
}

symbol_values = {
    "7" : 100,
    "$" : 80,
    "%" : 60,
    "&" : 40,
    "#" : 30,
    "@" : 20
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(lines)

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, frequency in symbols.items():
        for _ in range(frequency):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    
    return columns


def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, col in enumerate(columns):
            if i != len(columns) - 1:
                print(col[row], end=" | ")
            else:
                print(col[row], end=" ")
        print()


def deposit():
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0. ")
        else:
            print("Please enter a number. ")

    return amount


def get_number_of_liines():
    while True:
        lines = input("Enter the number of lines you would like to bet on (" + str(MIN_BET) + " - " + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Please enter a valid number of lines. ")
        else:
            print("Please enter a number. ")

    return lines


def get_bet():
    while True:
        amount = input("What amount would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between {MIN_BET} - {MAX_BET}. ")
        else:
            print("Please enter a number. ")

    return amount


def spin(balance, lines):
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"You do not have enought to bet that amount, your current balance is: ${balance}")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)
    print(f"You won ${winnings}")
    print(f"You won on line:", *winning_lines)
    return winnings - total_bet


def main():
    balance = deposit()
    lines = get_number_of_liines()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to spin (q to quit). ").lower()
        if answer == "q":
            break
        balance += spin(balance, lines)

    print(f"You left with ${balance}")
    

main()