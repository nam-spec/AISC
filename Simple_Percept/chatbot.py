class LibraryChatbot:
    def __init__(self):
        self.books = {
            "python": {"author": "John", "available": True},
            "ai": {"author": "Russell", "available": True},
            "ml": {"author": "Andrew", "available": False}
        }

    def perceive(self, query):
        return query.lower()

    def decide(self, query):
        if "search" in query:
            return self.search_book(query)
        elif "issue" in query:
            return self.issue_book(query)
        elif "return" in query:
            return self.return_book(query)
        elif "author" in query:
            return self.show_author(query)
        elif "timing" in query:
            return "Library timings: 9 AM to 5 PM"
        else:
            return "Sorry, I didn't understand your query."

    def search_book(self, query):
        for book in self.books:
            if book in query:
                if self.books[book]["available"]:
                    return f"Book '{book}' is available."
                else:
                    return f"Book '{book}' is currently issued."
        return "Book not found."

    def issue_book(self, query):
        for book in self.books:
            if book in query:
                if self.books[book]["available"]:
                    self.books[book]["available"] = False
                    return f"You have issued '{book}'."
                else:
                    return f"'{book}' is already issued."
        return "Book not found."

    def return_book(self, query):
        for book in self.books:
            if book in query:
                self.books[book]["available"] = True
                return f"'{book}' has been returned."
        return "Book not found."

    def show_author(self, query):
        for book in self.books:
            if book in query:
                return f"Author of '{book}' is {self.books[book]['author']}."
        return "Book not found."

    def act(self, response):
        print("Chatbot:", response)


# ------------ MAIN PROGRAM WITH USER INPUT -----------
agent = LibraryChatbot()

while True:
    user_query = input("\nAsk something (or type 'exit'): ")

    if user_query.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    percept = agent.perceive(user_query)
    response = agent.decide(percept)
    agent.act(response)
