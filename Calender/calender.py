import os
import sys
import datetime
import colorama
from colorama import Fore, Back

colorama.init()

# Remainder structure
class Remainder:
    def __init__(self, dd, mm, note):
        self.dd = dd
        self.mm = mm
        self.note = note

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to set color
def set_color(foreground=Fore.WHITE, background=Back.BLACK):
    print(foreground + background, end='')

# Function to print the month and year
def print_date(mm, yy):
    month_names = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]
    print(f"---------------------------")
    print(f"{month_names[mm-1]} , {yy}")
    print(f"---------------------------")

# Check if year is a leap year
def check_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# Get number of days in a month
def get_number_of_days(month, year):
    if month == 2:
        return 29 if check_leap_year(year) else 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

# Get name of the day of the week
def get_day_name(day):
    return ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][day]

# Get day of the week number (0=Sunday, 1=Monday, etc.)
def get_day_number(day, mon, year):
    date = datetime.date(year, mon, day)
    return date.weekday()

# Get the name of the day
def get_day(dd, mm, yy):
    if not (1 <= mm <= 12):
        return "Invalid month value"
    if not (1 <= dd <= get_number_of_days(mm, yy)):
        return "Invalid date"
    if yy >= 1600:
        day = get_day_number(dd, mm, yy)
        return get_day_name(day)
    else:
        return "Please give year more than 1600"

# Check if there is a note for a given date
def check_note(dd, mm):
    try:
        with open("note.dat", "rb") as file:
            while True:
                data = file.read(54)  # Size of Remainder object
                if not data:
                    break
                R = Remainder(int.from_bytes(data[:2], 'little'),
                              int.from_bytes(data[2:4], 'little'),
                              data[4:].decode().strip())
                if R.dd == dd and R.mm == mm:
                    return True
    except FileNotFoundError:
        return False
    return False

# Print the month with all days
def print_month(mon, year):
    if not (1 <= mon <= 12):
        print("INVALID MONTH")
        input("Press Enter to continue...")
        return
    if year < 1600:
        print("INVALID YEAR")
        input("Press Enter to continue...")
        return

    clear_screen()
    print_date(mon, year)
    print("S   M   T   W   T   F   S   ")

    first_day = get_day_number(1, mon, year)
    days_in_month = get_number_of_days(mon, year)

    # Print leading spaces
    for _ in range(first_day):
        print("    ", end="")

    # Print days of the month
    for day in range(1, days_in_month + 1):
        if check_note(day, mon):
            set_color(foreground=Fore.WHITE, background=Back.RED)
        print(f"{day:2}", end=" ")
        set_color()
        if (day + first_day) % 7 == 0:
            print()
    print("\nPress 'n' for Next, 'p' for Previous, 'q' to Quit")

# Add a note
def add_note():
    clear_screen()
    print("Enter the date (DD/MM): ", end="")
    try:
        dd, mm = map(int, input().split())
        if not (1 <= dd <= 31) or not (1 <= mm <= 12):
            print("Invalid date or month")
            input("Press Enter to continue...")
            return
    except ValueError:
        print("Invalid input format")
        input("Press Enter to continue...")
        return

    print("Enter the Note (50 characters max): ", end="")
    note = input()
    try:
        with open("note.dat", "ab") as file:
            file.write(dd.to_bytes(2, 'little'))
            file.write(mm.to_bytes(2, 'little'))
            file.write(note.ljust(50).encode())
        print("Note saved successfully")
    except Exception as e:
        print(f"Failed to save note: {e}")
    input("Press Enter to continue...")

# Show notes for a given month
def show_notes(mm):
    clear_screen()
    try:
        with open("note.dat", "rb") as file:
            notes_found = False
            index = 0
            while True:
                data = file.read(54)  # Size of Remainder object
                if not data:
                    break
                R = Remainder(int.from_bytes(data[:2], 'little'),
                              int.from_bytes(data[2:4], 'little'),
                              data[4:].decode().strip())
                if R.mm == mm:
                    print(f"Note {index + 1} Day {R.dd}: {R.note}")
                    notes_found = True
                    index += 1
            if not notes_found:
                print("This month contains no notes")
    except FileNotFoundError:
        print("Error in opening the file")
    input("Press Enter to continue...")

# Main function
def main():
    while True:
        clear_screen()
        print("1. Find Out the Day")
        print("2. Print all the days of the month")
        print("3. Add Note")
        print("4. EXIT")
        try:
            choice = int(input("ENTER YOUR CHOICE: "))
        except ValueError:
            print("Invalid choice. Please enter a number.")
            continue

        if choice == 1:
            print("Enter date (DD MM YYYY): ", end="")
            try:
                dd, mm, yy = map(int, input().split())
                print(f"Day is: {get_day(dd, mm, yy)}")
            except ValueError:
                print("Invalid date format.")
            input("Press Enter to continue...")

        elif choice == 2:
            print("Enter month and year (MM YYYY): ", end="")
            try:
                mm, yy = map(int, input().split())
                while True:
                    print_month(mm, yy)
                    ch = input().strip().lower()
                    if ch == 'n':
                        if mm == 12:
                            mm = 1
                            yy += 1
                        else:
                            mm += 1
                    elif ch == 'p':
                        if mm == 1:
                            mm = 12
                            yy -= 1
                        else:
                            mm -= 1
                    elif ch == 'q':
                        break
                    elif ch == 's':
                        show_notes(mm)
                    else:
                        print("Invalid input. Use 'n', 'p', 's', or 'q'.")
            except ValueError:
                print("Invalid input format.")
            input("Press Enter to continue...")

        elif choice == 3:
            add_note()

        elif choice == 4:
            sys.exit()

if __name__ == "__main__":
    main()
