#This Chatbot uses Classes to get a Json file that contains questions and answers.
import json
import os

class Chatbot:
    def __init__(self, question_answers):
        with open(question_answers, 'r') as file:
            self.question_answers = json.load(file)
        self.no_answer = []
        self.conversation_history = {}  
        self.user_name = None
        self.load_conversation_history()  


    def get_user_name(self):
        if not self.user_name:
            self.user_name = input("Hello! What's your name? ")
        return self.user_name

    def answer(self, query):
        if query.lower().strip() == 'exit':
            self.save_conversation_history()
            return "Goodbye! Your conversation history has been saved."

        for ind, question in enumerate(self.question_answers["questions"]):
            if question.lower().strip() == query.lower().strip():
                answer = self.question_answers["answers"][ind]
                conversation = {"role": "user", "content": query}
                self.conversation_history.setdefault(self.user_name, []).append(conversation)
                conversation = {"role": "ai", "content": answer}
                self.conversation_history.setdefault(self.user_name, []).append(conversation)
                return answer

        self.no_answer.append(query)
        conversation = {"role": "user", "content": query}
        self.conversation_history.setdefault(self.user_name, []).append(conversation)
        conversation = {"role": "ai", "content": "I don't have any answer, please ask another question."}
        self.conversation_history.setdefault(self.user_name, []).append(conversation)
        return "I don't have any answer, please ask another question."

    def save_conversation_history(self):
        filename = "all_conversation_history.json"  
        with open(filename, 'w') as file:
            json.dump(self.conversation_history, file)


    def load_conversation_history(self):
        if os.path.exists("all_conversation_history.json"):  
            with open("all_conversation_history.json", 'r') as file:
                loaded_history = json.load(file)
                if isinstance(loaded_history, dict):  
                    self.conversation_history = loaded_history
                else:
                    self.conversation_history = {}
        else:
            self.conversation_history = {}

    def format_history(self):
        formatted_history = []
        if self.user_name in self.conversation_history:
            user_conversation = self.conversation_history[self.user_name]
            for i in range(0, len(user_conversation), 2):
                formatted_conversation = {}
                formatted_conversation["role"] = user_conversation[i]["role"]
                formatted_conversation["content"] = user_conversation[i]["content"]
                formatted_history.append(formatted_conversation)
                formatted_conversation = {}
                formatted_conversation["role"] = user_conversation[i + 1]["role"]
                formatted_conversation["content"] = user_conversation[i + 1]["content"]
                formatted_history.append(formatted_conversation)
        return formatted_history
    
def main():
    file_location = r"C:\Users\USER\Documents\question_answer.json"
    chat = Chatbot(file_location)
    user_name = chat.get_user_name()
    chat.load_conversation_history()

    print(f"Hello, {user_name}!")

    if chat.conversation_history:
        print("Here's a summary of our previous conversation:")
        formatted_history = chat.format_history()
        for conversation in formatted_history:
            role = conversation["role"]
            content = conversation["content"]
            print(f"{role.capitalize()}: {content}")
        print("Let's continue our conversation.")
    else: 
        print("Ask me anything or type 'exit' to end the conversation.")

    while True:
        query = input("You: ")
        response = chat.answer(query)
        print(f"Bot: {response}")

        if query.lower().strip() == 'exit':
            break

    chat.save_conversation_history()
    

if __name__ == "__main__":
    main()

