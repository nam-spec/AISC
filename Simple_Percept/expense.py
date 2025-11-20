class FinanceAgent:

    def __init__(self):
        self.expenses = {
            "food": 0,
            "travel": 0,
            "shopping": 0,
            "bills": 0,
            "other": 0
        }

    def perceive(self, category, amount):
        return {"category": category, "amount": amount}

    def decide(self, percept):
        category = percept["category"]
        amount = percept["amount"]

        # Add expense
        self.expenses[category] += amount

        # Generate suggestions (rules)
        total = sum(self.expenses.values())
        advice = ""

        if self.expenses["food"] > 0.4 * total:
            advice += "High spending on food. Try cooking at home.\n"

        if self.expenses["shopping"] > 0.3 * total:
            advice += "Reduce shopping to control budget.\n"

        if total > 50000:
            advice += "Warning: Monthly spending is too high!\n"

        if advice == "":
            advice = "Expense recorded. You're within limits."

        return advice

    def act(self, msg):
        print("Advisor:", msg)

    def summary(self):
        print("\n----- Monthly Summary -----")
        for k, v in self.expenses.items():
            print(f"{k.capitalize()}: {v}")
        print(f"Total: {sum(self.expenses.values())}")

agent = FinanceAgent()

while True:
    print("\nEnter expense (type 'exit' to stop):")
    cat = input("Category (food/travel/shopping/bills/other): ")

    if cat == "exit":
        break

    amount = int(input("Amount: "))

    percept = agent.perceive(cat, amount)
    response = agent.decide(percept)
    agent.act(response)

agent.summary()
