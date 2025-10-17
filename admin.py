import store
from store import load_data
from store import save_data
import datetime
from datetime import datetime

def admin_menu(admin_name):
    while True:
        data = load_data()
        admin_data = data["admin"]
        admin = next((s for s in admin_data if s["admin"] == admin_name), None)
        print(f"\n--------Welcome Admin: {admin["admin"]}---------\n")
        print("1. View all bank users")
        print("2. Search for User detail")
        print("3. Freeze / Unfreeze")
        print("4. Delete User Account")
        print("5. View all Transaction")
        print("6. Add/Deduct User Balance")
        print("7. Add New Admin")
        print("8. Remove Admin")
        print("9. Logout")
        try:
            choose = input("Enter a number(1-8): ")
            if choose == "1":
                view_users()
                continue
            elif choose == "2":
                search_user()
                continue
            elif choose == "3":
                freeze_unfreeze()
                continue
            elif choose == "4":
                delete()
                continue
            elif choose == "5":
                view_trans()
                continue
            elif choose == "6":
                add_money(admin_name)
                continue
            elif choose == "7":
                add_admin()
                continue
            elif choose == "8":
                remove_admin(admin_name)
                continue
            elif choose == "9":
                print("Looged Out✅")
                break
            else:
                print("Enter (1-9)\n")
                continue
        except ValueError:
            print("Enter Numbers Only\n")



def view_users():
    data = load_data()
    users = data.get("user", [])
    if not users:
        print("No User found")
    print("\nAll Bank Users 👥👥\n")
    for s in users:
        print(f"Name: {s["name"]} | Account Number: {s["account_no"]} | User Pin: {s['pin']} | Status : {s["status"]}")
        
def search_user():
    data = load_data()
    users = data.get("user", [])
    print("\nSearch For User Details 👤\n")
    try:
        check_user = int(input("Enter Account Number: "))
        user = next((s for s in users if s["account_no"] == check_user), None)
        if not user:
            print("User Not Found❌\n")
            return
        
        print("User Details")
        print(f"Name: {user["name"]} | Account Number: {user["account_no"]} | User Pin {user["pin"]} | Status: {user["status"]}")
        print(f"Account Balance: {user["bal"]:,}")
        trans = user.get("trans", [])
        print("🧾User Transaction History")
        for s in trans:
            print(f"\nTransaction Type: {s.get("type", "N/A")}")
            sender = s.get("sender")
            if isinstance(sender, list) and len(sender) == 2:
                print(f"Sender: {sender[0]} (Acct: {sender[1]})")
            elif isinstance(sender, list):
                print("Sender: Incomplete sender info")
            elif isinstance(sender, str):
                print(f"Sender: {sender}")

            receiver = s.get("receiver")
            if isinstance(receiver, list) and len(receiver) == 2:
                print(f"Receiver: {receiver[0]} (Acct: {receiver[1]})")
            elif isinstance(receiver, list):
                print("Receiver: Incomplete receiver info")
            elif isinstance(receiver, str):
                print(f"Receiver: {receiver}")
            print(f"Amount: {s.get("amount", 0)}")
            print(f"Balance After: {s.get("bal_after", 0)}")
            print(f"Date: {s.get("date", "Unknown")}\n")
    except ValueError:
        print("Enter Only Numbers ❗❗\n")
    except KeyboardInterrupt:
        print("Keyboard Intercepted❗❗\n")

def freeze_unfreeze():
    data = load_data()
    users = data.get("user", [])
    print("\nFreeze/Unfreeze User Account\n")
    try:
        check_acc = int(input("Enter User Account Nummber: "))
        user = next((s for s in users if s["account_no"] == check_acc), None)
        print(f"User Name: {user["name"]}")
        if user:
            stat_chng = input("Freeze/Unfreeze Account: ")
            if stat_chng == "Freeze" or stat_chng == "F":
                if user["status"] == "Active":
                    user["status"] = "Frozen"
                    print("Account Freezed")
                    save_data(data)
                else:
                    print("Account Frozen Already ❗\n")
            elif stat_chng == "Unfreeze" or stat_chng == "UF":
                if user["status"] == "Frozen":
                    user["status"] = "Active"
                    print("Account Unfreezed")
                    save_data(data)
                else:
                    print("Account isnt Freezed")
            else:
                print("Enter Freeze/UnFreeze")
        else:
            print("User Not Found ❗❗")           
    except ValueError:
        print("Enter Only Numbers ❗❗\n")
    except KeyboardInterrupt:
        print("Keyboard Intercepted❗❗\n")

def delete():
    data = load_data()
    user_data = data.get("user", [])
    try:
        check_user = int(input("Enter User Account Number: "))
        user = next((s for s in user_data if s["account_no"] == check_user), None)
        if user:
           while True:
                confirm = input("Are you sure you want to delete account(Yes/No): ").strip().capitalize()
                if confirm == "Y" or confirm == "Yes":
                    user_data.remove(user)
                    save_data(data)
                    print("User Account deleted Successfully✅\n")
                    break
                elif confirm == "N" or confirm == "No":
                    print("Deletion Cancelled ✅\n")
                    break
                else:
                    print("Enter (Y/N) or (Yes/No)")
        else:
            print("User Not Found❌")
    except ValueError:
        print("Enter Only Numbers ❗❗\n")
    except KeyboardInterrupt:
        print("Keyboard Intercepted❗❗\n")


def view_trans():
    data = load_data()
    users = data.get("user", [])
    if users:
        print("All Users Transaction")
        for s in users:
            print(f"User: {s["name"]} ({s["account_no"]})")
            trans = s.get("trans", [])
            for s in trans:
                print(f"\nTransaction Type: {s["type"]}")
                if "sender" in s and isinstance(s["sender"], list):
                    print(f"Sender details : Name: {s["sender"][0]} Account Number: {s["sender"][1]}")
                if "receiver" in s and isinstance(s["receiver"], list):
                    print(f"Recipent details : Name: {s["receiver"][0]} Account Number: {s["receiver"][1]}")
                print(f"Balance After: {s["bal_after"]}")
                print(f"Date: {s["date"]}\n")

def add_admin():
    data = load_data()
    admin = data.get("admin", [])
    name = input("Enter New Admin Name: ").strip().capitalize()
    while True:
        pin = int(input("Enter 4 Digits Pin: "))
        if len(str(pin)) == 4:
            print("Pin Set Successfully✅\n")
            print(f"New Admin Added. Name: {name} Pin: {pin}")
            break
        else:
            print("Pin Must Be 4 digits")
        
    new_admin = {
        "admin" : name,
        "pin" : pin
    }
    admin.append(new_admin)
    save_data(data)

def remove_admin(admin_name):
    data = load_data()
    admins = data.get("admin", [])
    
    c_admin = next((s for s in admins if s["admin"] == admin_name), None)

    if not c_admin:
        print("Current admin not found ❌")
        return

    if c_admin["admin"] != "Babs":
        print("Only Babs can remove other admins ❗")
        return

    print("\nRemove Admin\n")
    check_admin = input("Enter Admin Name to Remove: ").strip().capitalize()

    if check_admin == "Babs":
        print("You can't remove this admin. He is the boss 😂😂")
        return

    target = next((s for s in admins if s["admin"] == check_admin), None)

    if not target:
        print("Admin Not Found ❗")
        return

    confirm = input(f"Are you sure you want to delete {check_admin}? (Y/N): ").strip().upper()
    if confirm == "Y":
        admins.remove(target)
        save_data(data)
        print(f"Admin '{check_admin}' removed successfully ✅")
    else:
        print("Action cancelled ❗")

def add_money(admin_name):
    data = load_data()
    user_data = data.get("user", [])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_acc = int(input("Enter User Account Number: "))
    c_user = next((s for s in user_data if s["account_no"] == user_acc), None)
    if c_user:
        print(f"USER NAME: {c_user["name"]}")
        while True:
            try:
                confirm = input("Do you want to add/deduct money(A/D): ").strip().upper()
                if confirm == "A":
                    deposit = int(input("Enter amount: "))
                    if deposit > 0 and deposit <= 1000000:
                        c_user["bal"] += deposit
                        receipt = {
                            "type": "Admin deposit",
                            "adminName" : admin_name,
                            "amount" : deposit,
                            "bal_after": c_user["bal"],
                            "date" : timestamp
                        }
                        if not "trans" in c_user:
                            c_user["trans"] = []
                        c_user["trans"].append(receipt)
                        save_data(data)
                        break
                    else:
                        print("Enter A Valid Number ❗")
                elif confirm == "D":
                    withdraw = int(input("Enter amount: "))
                    if withdraw > 0 and withdraw <= c_user["bal"]:
                        c_user["bal"] -= withdraw
                        receipt = {
                            "type" : "Admin deduct",
                            "adminName" : admin_name,
                            "amount" : withdraw,
                            "bal_after" : c_user["bal"],
                            "date" : timestamp
                        }
                        if not "trans" in c_user:
                            c_user["trans"] = []
                        c_user["trans"].append(receipt)
                        save_data(data)
                        print("Done✅")
                        break
                    else:
                        print("Enter A Valid Number ❗")
                else:
                    print("Enter (A/D)")
            except ValueError:
                print("Enter Numbers Only ❗")