#i need to create a password checker that will check how strong is the password
#it will check if the password is empty
#it will check if the password is less than 8 characters
import random
import string

# ===================== FUNCTION: Generate Password =====================
def generate_password(min_lenght, number=True, special_characters=True, exclude=""):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation

    characters = letters
    if number:
        characters += digits
    if special_characters:
        characters += special

    # Feature 7: remove excluded characters
    characters = [c for c in characters if c not in exclude]

    pwd = ""
    meet_chriteria = False
    has_number = False
    has_special = False

    while not meet_chriteria:
        new_char = random.choice(characters)
        pwd += new_char

        if new_char in digits:
            has_number = True
        elif new_char in special:
            has_special = True

        if len(pwd) >= min_lenght:
            meet_chriteria = True
            if number:
                meet_chriteria = has_number
            if special_characters:
                meet_chriteria = meet_chriteria and has_special

    return pwd


# ===================== FUNCTION: Check Strength =====================
def check_strength(pwd):
    length = len(pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_special = any(c in string.punctuation for c in pwd)

    score = sum([has_upper, has_lower, has_digit, has_special])

    if length < 6:
        return "Very Weak ❌"
    elif length < 8 or score <= 1:
        return "Weak ⚠️"
    elif length < 10 or score == 2:
        return "Medium 🟡"
    elif length >= 10 and score == 3:
        return "Strong ✅"
    elif length >= 12 and score == 4:
        return "Very Strong 🔒"
    else:
        return "Strong ✅"


# ===================== FUNCTION: Password Statistics =====================
def show_statistics(pwd):
    print("\n--- Password Statistics ---")
    print("Total length      : " + str(len(pwd)))
    print("Uppercase letters : " + str(sum(c.isupper() for c in pwd)))
    print("Lowercase letters : " + str(sum(c.islower() for c in pwd)))
    print("Numbers           : " + str(sum(c.isdigit() for c in pwd)))
    print("Special characters: " + str(sum(c in string.punctuation for c in pwd)))


# ===================== FUNCTION: Crack Time =====================
def crack_time(pwd):
    combinations = 95 ** len(pwd)
    # calculates total possible combinations based on password length

    seconds = combinations / 1_000_000_000
    # assumes attacker tries 1 billion passwords per second

    if seconds < 60:                                # less than 60 seconds
        return "less than a minute"

    elif seconds < 3600:                            # less than 1 hour (3600 seconds)
        return str(int(seconds // 60)) + " minutes"

    elif seconds < 86400:                           # less than 1 day (86400 seconds)
        return str(int(seconds // 3600)) + " hours"

    elif seconds < 2_592_000:                       # less than 1 month (30 days)
        return str(int(seconds // 86400)) + " days"

    elif seconds < 31_536_000:                      # less than 1 year (365 days)
        return str(int(seconds // 2_592_000)) + " months"

    elif seconds < 3_153_600_000:                   # less than 100 years
        return str(int(seconds // 31_536_000)) + " years"

    else:                                           # more than 100 years
        return "centuries 🔒 (uncrackable)"

# ===================== MAIN PROGRAM =====================

# Show guide first
print("""
========================================
       PASSWORD STRENGTH GUIDE
========================================
  WEAK        — 6-7 chars,  1-2 types
  MEDIUM      — 8-10 chars, 2-3 types
  STRONG      — 11-13 chars, all 4 types
  VERY STRONG — 14+ chars,  all 4 types
========================================
""")

# Ask for input
min_lenght = int(input("Enter the minimum length of the password: "))
has_number = input("Do you want numbers? (y/n): ").lower() == "y"
has_special = input("Do you want special characters? (y/n): ").lower() == "y"

# Feature 7: excluded characters
exclude = input("Enter any characters you want to EXCLUDE (or press Enter to skip): ")

# Feature 3: common passwords to check against
common = ["password123", "123456", "qwerty", "admin", "letmein", "welcome"]

# Feature 1: regenerate loop
while True:
    pwd = generate_password(min_lenght, has_number, has_special, exclude)
    strength = check_strength(pwd)

    # Feature 3: common password warning
    if pwd in common:
        print("Warning: This password is too common, regenerating...")
        continue

    print("\nThe generated password is: " + pwd)
    print("Password strength        : " + strength)

    # Feature 5: statistics
    show_statistics(pwd)

    # Feature 6: crack time
    print("Estimated crack time     : " + crack_time(pwd))

    # Feature 2: copy to clipboard
    try:
        import pyperclip
        pyperclip.copy(pwd)
        print("Password copied to clipboard! ✅")
    except:
        print("(Install pyperclip to enable clipboard copying)")

    # Feature 4: save to file
    save = input("\nDo you want to save this password to a file? (y/n): ").lower()
    if save == "y":
        with open("passwords.txt", "a") as f:
            f.write(pwd + "\n")
        print("Password saved to passwords.txt! ✅")

    # Feature 1: ask to regenerate
    again = input("\nGenerate another password? (y/n): ").lower()
    if again != "y":
        print("\nGoodbye! Stay secure 🔒")
        break