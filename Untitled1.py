#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import google.generativeai as genai

# Configure the Gemini API (Make sure you set up your API key)
genai.configure(api_key="AIzaSyB0iGj0GDB9667QCnKiZC4XRUEoDCmnS60")

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

# Function to handle chat history
def chat():
    print("Welcome to AI Chatbot! Type 'exit' to end the chat.")
    history = []  # Store chat history

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        
        # Add user input to history
        history.append({"role": "user", "parts": [user_input]})

        # Generate response
        response = model.generate_content(user_input)

        # Store chatbot response in history
        history.append({"role": "assistant", "parts": [response.text]})

        print(f"Chatbot: {response.text}")

# Run the chatbot
if __name__ == "__main__":
    chat()


# In[ ]:




