import auth
from auth import create_account
from auth import login
from auth import admin_login
def main_menu():
    while True:
        print("\nWelcome To BABS Microfinance Bank💳💳")
        print("1. Create account")
        print("2. Login")
        print("3. Admin Login")
        print("4. Exit")
        choose = input("Enter a number(1-4): ")
        if choose == "1":
            create_account()
            break
        elif choose == "2":
            login()
            break
        elif choose == "3":
            admin_login()

main_menu()