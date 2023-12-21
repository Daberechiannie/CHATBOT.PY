import json
import os
import openai
from openai import OpenAI
from api_key import API_KEY
from os import getenv


 
# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=API_KEY
)


openai.api_key = API_KEY

class Chatbot:
    def __init__(self, question_answers):
        with open(question_answers, 'r') as file:
            self.question_answers = json.load(file)
        self.no_answer = []
        self.conversation_history = []
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
                conversation = {"question": query, "answer": answer}
                self.conversation_history.append(conversation)
                return answer

        self.no_answer.append(query)
        conversation = {"question": query, "answer": "I don't have any answer, please ask another question."}
        self.conversation_history.append(conversation)
        return "I don't have any answer, please ask another question."

    def save_conversation_history(self):
        if self.user_name:
            filename = f"{self.user_name}_conversation_history.json"
            with open(filename, 'w') as file:

                json.dump(self.conversation_history, file)
        else:
            print("User name not set. Conversation history cannot be saved.")


    def format_history(self):
        formatted_history = []
        for conversation in self.conversation_history:
            formatted_conversation = {}
            if "question" in conversation and "answer" in conversation:
                formatted_conversation["role"] = "user"
                formatted_conversation["content"] = conversation["question"]
                formatted_history.append(formatted_conversation)

                formatted_conversation = {}
                formatted_conversation["role"] = "ai"
                formatted_conversation["content"] = conversation["answer"]
                formatted_history.append(formatted_conversation)
        return formatted_history

    
    
VERBOSE = True
CHAT_WINDOW= 4

def run_through(message):
    print(message)
    return


class GPTBot(Chatbot):
    def __init__(self, api_key):
       self.api_key = api_key 
        
    def answer(self,query, user_name="Annie"):
        
        user_message = {"role": "user", "content": query} 
        chat_history = [user_message]
        response= client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
            messages=chat_history,
        )

        print(response.choices[0].message.content)
        response = response.choices[0].message


        return response.content



