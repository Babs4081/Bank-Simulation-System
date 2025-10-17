import store
import dash
import admin
from admin import admin_menu
import datetime
from datetime import datetime
from dash import main_menu
from store import save_data
from store import load_data
import random
def acc_gen():
    return random.randint(710000000,799999999)

def create_account():
    print("\nCreate An Account\n")
    acc_no = acc_gen()
    name = input("Enter Fullname: ").strip().capitalize()
    while True:
        try:
            deposit = int(input("Enter Amount to deposit: "))
            if deposit > 1000001 :
                print("Contact Bank To Deposit Huge Amount")
            elif deposit > 0 :
                print(f"${deposit} added successfully")
                break
            else:
                print("Enter A Valid")
        except ValueError:
            print("Enter Only Numbers ❗❗\n")
        except KeyboardInterrupt:
            print("Keyboard Interupted\n")
    while True:
        try:
            check_pin = int(input("Enter 4 digits pin: "))
            if len(str(check_pin)) == 4:
                pin = check_pin
                print(f"Pin Set Successfully. Pin: {check_pin}")
                break
            else:
                print("Pin Must Be 4 digits!!")
        except ValueError:
            print("Enter Numbers Only ❗❗\n")
        except KeyboardInterrupt:
            print("Keyboard Interupted\n")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_detail = {
        "account_no" : acc_no,
        "name" : name,
        "bal" : deposit,
        "pin" : pin,
        "status" : "Active",
        "trans" : []
    }
    data = load_data()
    data["user"].append(user_detail)
    save_data(data)

    data = load_data()
    user_data = data["user"]
    user = next((s for s in user_data if s["account_no"] == acc_no), None)
    if user:
        trans = {
            "type" : "deposit",
            "amount" : deposit,
            "bal_after": deposit,
            "date" : timestamp

        }
        if not "trans" in user:
            user["trans"] = []
        user["trans"].append(trans)
    save_data(data)
        


    main_menu(acc_no)

def login():
    print("\nLogin\n")
    data = load_data()
    user_data = data["user"]
    while True:
        try:
            check_user = int(input("Enter Your Account Number: "))
            user = next((s for s in user_data if s["account_no"] == check_user), None)
            if user:
                    check_pin = int(input("Enter Your pin: "))
                    if user["pin"] == check_pin:
                        print("Access Granted ✔\n")
                        main_menu(user["account_no"])
                        break
                    else:
                        print("Invalid Pin❌\n")
            else:
                print("User Not Found❌\n")
                choose = input("Do You Want To Create An Account(Yes/No): ")
                if choose == "Yes":
                    create_account()
                    break
                elif choose == "No":
                    print("GoodBye Gayy😒😒")
                    break
                else:
                        print("Enter (Yes/No)")
        except ValueError:
            print("Enter Number Only ❗❗")
        except KeyboardInterrupt:
            print("Keyboard Interupted\n")

def admin_login():
    print("\nAdmin Login\n")
    data = load_data()
    admins = data.get("admin", [])
    while True:
        try:
            check_admin = input("Enter Admin Name: ").capitalize()
            admin = next((s for s in admins if s["admin"] == check_admin))
            if admin["admin"]== check_admin:
                check_pin = int(input("Enter Pin: "))
                if admin["pin"] == check_pin:
                    print("\nAccess Granted ✅\n")
                    admin_menu(check_admin)
                    break
                else:
                    print("Invalid Pin❌\n")
                    break
            else:
                print("Admin Not Found ❗❗\n")
                break
        except Exception as e:
            print(e)