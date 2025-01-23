import random

MAX_LINES = 3
MAX_BET = 1000
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "7": 2,
    "$": 3,
    "%": 5,
    "&": 10,
    "#": 15,
    "@": 20,
    "?": 25,
    "W": 10  # Wild symbol
}

symbol_values = {
    "7": 200,
    "$": 100,
    "%": 50,
    "&": 20,
    "#": 10,
    "@": 5,
    "?": 1,
    "W": 0  # Wild has no standalone value
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        base_symbol = None
        is_winner = True
        wild_count = 0
        for column in columns:
            symbol_to_check = column[line]
            if symbol_to_check == "W":
                wild_count += 1
            else:
                if base_symbol is None:
                    base_symbol = symbol_to_check
                elif symbol_to_check != base_symbol:
                    is_winner = False
                    break
        if is_winner and base_symbol == "7" and wild_count > 0:
            is_winner = False
        if is_winner and base_symbol is not None:
            winnings += values[base_symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, frequency in symbols.items():
        all_symbols.extend([symbol] * frequency)

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
                print(f"Thank you for your deposit.")
                return amount
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a valid number.")


def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines you would like to bet on ({MIN_BET} - {MAX_LINES}) or press 'q' to quit: ").lower()
        if lines == "q":
            return None
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                return lines
            else:
                print(f"Please enter a number between {MIN_BET} and {MAX_LINES}.")
        else:
            print("Please enter a valid number.")


def get_bet():
    while True:
        amount = input(f"What amount would you like to bet on each line (${MIN_BET} - ${MAX_BET}) or press 'q' to quit: ").lower()
        if amount == "q":
            return None
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                return amount
            else:
                print(f"Amount must be between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a valid number.")


def spin(balance, lines, bet):
    total_bet = bet * lines
    print(f"You are spinning with a total bet of ${total_bet} on {lines} lines.")
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)
    balance += winnings - total_bet
    print(f"You won ${winnings}.")
    print(f"Your current balance is ${balance}")
    if winning_lines:
        print(f"You won on lines:", *winning_lines)
    else:
        print("No winning lines.")
    return balance


def main():
    balance = deposit()

    while True:
        print(f"Your current balance is: ${balance}")
        lines = get_number_of_lines()
        if lines is None:
            print(f"Thank you for playing! You walked away with ${balance}.")
            break

        bet = get_bet()
        if bet is None:
            print(f"Thank you for playing! You walked away with ${balance}.")
            break

        total_bet = lines * bet
        if total_bet > balance:
            print(f"You do not have enough to bet that amount. Your current balance is ${balance}.")
            continue

        balance = spin(balance, lines, bet)

        while True:
            choice = input("Press Enter to spin again with the same amount, 'b' to go back, or 'q' to quit: ").lower()
            if choice == "q":
                print(f"Thank you for playing! You walked away with ${balance}.")
                return
            elif choice == "b":
                break
            else:
                if total_bet > balance:
                    print(f"You do not have enough to bet that amount. Your current balance is ${balance}.")
                    break
                balance = spin(balance, lines, bet)

main()
