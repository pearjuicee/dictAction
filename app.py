import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

COLLECTION_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dict_collection')
os.makedirs(COLLECTION_DIRECTORY, exist_ok=True)

@app.route('/')
def index():
    return render_template('WebPage.html')

@app.route('/choose')
def choose():
    return render_template('ChooseType.html')

@app.route('/process', methods=['POST'])
def process_text():
    user_text = request.form.get('message')
    try:
        # Save the text to a file
        filepath = os.path.join(COLLECTION_DIRECTORY, 'user_dictation')
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(user_text)
    except Exception as e:
        # Handle any errors that might occur
        print(f"Error saving file: {e}")
        return "There was an error saving your text", 500
       
    return redirect(url_for('input'))

@app.route('/input')
def input():
    return render_template('UserInput.html')
