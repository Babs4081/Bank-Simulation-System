import store
import datetime
from datetime import datetime
from store import save_data
from store import load_data


def main_menu(acc_no):
    while True:
        data = load_data()
        user_data = data["user"]
        user = next((s for s in user_data if s["account_no"] == acc_no), None)
        if not user:
            print("User Not Found")
            return
        print("\nWelcome To Babs Microfinance Bank💳💳")
        print(f"-------- User Name: {user["name"]} ")
        print(f"---------Balance: ${user["bal"]:,} ")
        print(f"---------Account Status: {user["status"]}")
        print(f"---------Account Number: {user["account_no"]}")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Transfer Money")
        print("4. View All Transactions")
        print("5. Change Pin")
        print("6. Logout")
        choose = input("Enter your choice(1-6): ")
        if choose == "1":
            deposit(user["account_no"])
            continue
        elif choose == "2":
            withdraw(user["account_no"])
            continue
        elif choose == "3":
            transfer(user["account_no"])
            continue
        elif choose == "4":
            view_trans(user["account_no"])
            continue
        elif choose == "5":
            change_pin(user["account_no"])
            continue
        elif choose == "6":
            logout()
            break

def deposit(acc_no):
    data = load_data()
    user_data = data["user"]
    user = next((s for s in user_data if s["account_no"] == acc_no), None)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        if user:
            if user["status"] == "Active":
                while True:
                    check_pin = int(input("Enter Pin: "))
                    if user["pin"] == check_pin:
                        deposit = int(input("Enter Amount To Deposit: "))
                        if deposit >= 1000001:
                            print("Contact Bank To Deposit Huge Amount")
                        elif deposit > 0 :
                            user["bal"] += deposit
                            trans = {
                                "type": "deposit",
                                "amount" : deposit,
                                "bal_after": user["bal"],
                                "date" : timestamp
                            }
                            if not "trans" in user:
                                user["trans"] = []
                            user["trans"].append(trans)
                            save_data(data)
                            print(f"${deposit} has been added to balance ✅. New Balance: {user["bal"]}")
                            break
                        else:
                            print("Enter A valid Number\n")
                    else: 
                        print("Invalid Pin❌")
            else:
                print("Account Frozen ❗. Contact Bank To Unfreeze Account")
        else:
            print("User Not Found ❌")
    except ValueError:
        print("Enter Numbers Only")
    except KeyboardInterrupt:
        print("Keyboard Interupted")

def withdraw(acc_no):
    data = load_data()
    user_data = data["user"]
    user = next((s for s in user_data if s["account_no"] == acc_no), None)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if user:
        if user["status"] == "Active":
            while True:
                try:
                    check_pin = int(input("Enter Pin: "))
                    if user["pin"] == check_pin:
                        withdrawal = int(input("Enter Amount To Withdraw: "))
                        if  withdrawal > 0 and withdrawal <= user["bal"]:
                            user["bal"] -= withdrawal
                            trans = {
                                "type" : "Withdrawal",
                                "amount" : withdrawal,
                                "bal_after" : user["bal"],
                                "date" : timestamp
                            }
                            if not "trans" in user:
                                user["trans"] = []
                            user["trans"].append(trans)
                            save_data(data)
                            print(f"\n${withdrawal} has been deducted from balance✅. New Balance: ${user["bal"]}\n")
                            break
                        else:
                            print("Enter A Valid Number ❗\n")
                    else:
                        print("Invalid Pin❌\n")
                except ValueError:
                    print("Enter On Numbers ❗❗\n")
                except KeyboardInterrupt:
                    print("Keyboard Interupted\n")
        else:
            print("Account Frozen ❗. Contact Bank To Unfreeze Account")
    else:
        print("User Not Found❌")

def transfer(acc_no):
    data = load_data()
    user_data = data["user"]
    user = next((s for s in user_data if s["account_no"] == acc_no), None)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if user:
        if user["status"] == "Active":
            while True:
                try:
                    recipent_acc = int(input("Enter Recipent Account Number: "))
                    recipent = next((s for s in user_data if s["account_no"] == recipent_acc), None)
                    if recipent:
                        print(f"Recipent Name: {recipent["name"]}")
                        amount = int(input("Enter Amount To Transfer: "))
                        if amount > 0 and amount <= user["bal"]:
                            check_pin = int(input("Enter Pin: "))
                            if user["pin"] == check_pin:
                                user["bal"] -= amount
                                recipent["bal"] +=  amount
                                trans = {
                                    "type" : "Transfer",
                                    "receiver" : (recipent["name"], recipent_acc),
                                    "amount" : amount,
                                    "bal_after" : user["bal"],
                                    "date" : timestamp
                                }
                                trans_out = {
                                    "type" : "Received",
                                    "sender" : (user["name"], user["account_no"]),
                                    "amount" : amount,
                                    "bal_after" : recipent["bal"],
                                    "date" : timestamp
                                }
                                if not "trans" in user:
                                    user["trans"] = []
                                user["trans"].append(trans)
                                if not "trans" in recipent["trans"]:
                                    recipent["trans"] = []
                                recipent["trans"].append(trans_out)
                                save_data(data)
                                print(f"${amount} transfered successfully✅\n")
                                break
                            else:
                                print("Invalid Pin❌\n")
                        else:
                            print("Enter a Valid Number ❗❗")
                    else:
                        print("Account Not Found❗❗")
                except ValueError:
                    print("Enter Numbers Only ❗❗\n")
                except KeyboardInterrupt:
                    print("Keyboard Interupted ❗\n")
        else:
            print("Account Frozen ❗. Contact Bank To Unfreeze Account")
    else:
        print("User Not Found❌")
def view_trans(acc_no):
    data = load_data()
    user_data = data["user"]
    user = next((s for s in user_data if s["account_no"] == acc_no), None)
    trans = user.get("trans", [])
    if not trans:
        print("No transaction found ❗")
        return
    print(f"\n🧾Transaction History For {user["name"]} | Account Number : {user["account_no"]}\n")
    for s in trans: 
        print(f"Transaction Type:{s.get("type", "N/A")}")
        if "sender" in s and isinstance(s["sender"], list):
            print(f"Sender details: Name: {s["sender"][0]} Account Number: {s["sender"][1]}")
        if "receiver" in s and isinstance(s["receiver"], list):
            print(f"Recipent details: Name: {s["receiver"][0]}  Account Number: {s["receiver"][1]}")
        print(f"Amount: ${s.get("amount", 0)}")
        print(f"Balance After: {s.get("bal_after", 0)}")
        print(f"Date: {s.get("date", "Unknown")}\n")

def change_pin(acc_no):
    data = load_data()
    user_data = data["user"]
    user = next((s for s in user_data if s["account_no"] == acc_no), None)
    while True:
        if user:
            print("\nChange Pin\n")
            try:
                check_pin = int(input("Enter Previous Pin: "))
                if user["pin"]  == check_pin:
                    new_pin = int(input("Enter New Pin: "))
                    if new_pin == user["pin"]:
                        print("New Pin cant be the same with Previous Pin ❗")
                    elif len(str(new_pin)) == 4:
                        user["pin"] = new_pin
                        save_data(data)
                        print(f"Pin reset successfully✅. New Pin: {user["pin"]}")
                        break
                    else:
                        print("Pin Must Be 4 Digits ❗❗")
                else:
                    print("Invalid Pin ❌")
                    break
            except ValueError:
                print("Enter Numbers Only ❗❗")
            except KeyboardInterrupt:
                print("Keyboard Interupted ❗❗")
                        
def logout():
    import main
    from main import main_menu
    print("Logging Out✅")
    main_menu()

                   

