


class Account:
    allowed = 200
    def __init__(self, name, card_no, balance):
        self.name = name
        self.card_no = card_no
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def deposit(self, amount):
        self.balance += amount

    def getBalance(self):
        return self.balance

    def getName(self):
        return self.name

    def getCard(self):
        return self.card_no


