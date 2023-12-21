##import Chatbot
from Chatbot import Chatbot, GPTBot
from api_key import API_KEY
import os

os.environ["OPENAI_API_KEY"] = API_KEY


def main():
    user_name = "Annie"
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

    print("Ask me anything or type 'exit' to end the conversation.")

    while True:
        query = input("You: ")
        response = chat.answer(query, user_name)
        print(f"Bot: {response}")

        if query.lower().strip() == 'exit':
            break

    chat.save_conversation_history()


if __name__ == "__main__":
    #
    # main()
    bot = GPTBot(API_KEY)

    while True:
        query = input("You: ")

        if query.lower().strip() == "exit" or query.lower().strip() == "quit":
            break

        response = bot.answer(query)
        print(f"Bot: {response}")

    

