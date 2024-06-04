class User:
    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = pin
        self.balance = 0
        self.transactions = []

    def verify_pin(self, entered_pin):
        return self.pin == entered_pin

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        self.add_transaction(f"Deposited: ${amount}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
            return False
        else:
            self.balance -= amount
            self.add_transaction(f"Withdrawn: ${amount}")
            return True

    def transfer(self, amount, target_user):
        if amount > self.balance:
            print("Insufficient funds")
            return False
        else:
            self.balance -= amount
            target_user.balance += amount
            self.add_transaction(f"Transferred: ${amount} to {target_user.user_id}")
            target_user.add_transaction(f"Received: ${amount} from {self.user_id}")
            return True


class ATM:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def add_user(self, user):
        self.users[user.user_id] = user

    def authenticate_user(self, user_id, pin):
        user = self.users.get(user_id)
        if user and user.verify_pin(pin):
            self.current_user = user
            return True
        else:
            return False

    def get_current_user(self):
        return self.current_user

    def reset_session(self):
        self.current_user = None


class TransactionHistory:
    @staticmethod
    def show_history(user):
        transactions = user.get_transactions()
        if not transactions:
            print("No transactions found")
        else:
            for transaction in transactions:
                print(transaction)


class Withdraw:
    @staticmethod
    def withdraw_amount(user, amount):
        if user.withdraw(amount):
            print(f"Withdrawn: ${amount}")
        else:
            print("Withdrawal failed")


class Deposit:
    @staticmethod
    def deposit_amount(user, amount):
        user.deposit(amount)
        print(f"Deposited: ${amount}")


class Transfer:
    @staticmethod
    def transfer_amount(user, amount, target_user):
        if user.transfer(amount, target_user):
            print(f"Transferred: ${amount} to {target_user.user_id}")
        else:
            print("Transfer failed")


def main():
    atm = ATM()
    atm.add_user(User('user1', '1234'))
    atm.add_user(User('user2', '5678'))

    while True:
        print("\nWelcome to the ATM!")
        user_id = input("Enter your user ID: ")
        pin = input("Enter your PIN: ")

        if atm.authenticate_user(user_id, pin):
            print("\nAuthentication successful!")
            while True:
                print("\n1. Transaction History")
                print("\n2. Withdraw")
                print("\n3. Deposit")
                print("\n4. Transfer")
                print("\n5. Quit")
                choice = input("Choose an option: ")

                if choice == '1':
                    TransactionHistory.show_history(atm.get_current_user())
                elif choice == '2':
                    amount = float(input("Enter amount to withdraw: "))
                    Withdraw.withdraw_amount(atm.get_current_user(), amount)
                elif choice == '3':
                    amount = float(input("Enter amount to deposit: "))
                    Deposit.deposit_amount(atm.get_current_user(), amount)
                elif choice == '4':
                    target_user_id = input("Enter the target user ID: ")
                    target_user = atm.users.get(target_user_id)
                    if target_user:
                        amount = float(input("Enter amount to transfer: "))
                        Transfer.transfer_amount(atm.get_current_user(), amount, target_user)
                    else:
                        print("Target user not found")
                elif choice == '5':
                    atm.reset_session()
                    print("Session ended. Thank you for using the ATM!")
                    break
                else:
                    print("Invalid option")
        else:
            print("Authentication failed. Please try again.")


if __name__ == "__main__":
    main()

