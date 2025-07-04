from flask import Flask, render_template, request, jsonify
import openai
import os
from openai import OpenAI
from dotenv import load_dotenv

openai.api_key =os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

SYSTEM_PROMPT = """
You are PizzaBot, a friendly assistant for a pizza delivery service. 
Help customers order pizzas,show menu with cost in indian rupee list list format,
ask quantity of the ordered product and show the total amount of the orders,
ask mobile number and addres and near pointed location for order delivery,handle complaints,
assigned order number for each orders,notify the time to prepare the food and answer delivery-related questions.
Understand and respond to user inputs clearly and accurately.
Summarize user requests or information when appropriate.
Infer user intent to classify queries or extract key information.
Transform user input when needed (e.g., correct grammar or translate).
Expand short prompts into detailed, contextually relevant responses.
Maintain a conversational flow with iterative prompt refinement.
Be polite, clear, and keep track of the conversation.
"""

# Store message history per session (simple in-memory for demo)
chat_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    chat_history.append({"role": "user", "content": user_input})

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
