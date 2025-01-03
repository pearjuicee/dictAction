import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Define the directory where we'll store dictation files
COLLECTION_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dict_collection')
os.makedirs(COLLECTION_DIRECTORY, exist_ok=True)

def display_correct_text():
    # Read the current dictation text
    dictation_filename = app.config.get('CURRENT_DICTATION')
    if not dictation_filename:
        return "No dictation text found", 400
        
    filepath = os.path.join(COLLECTION_DIRECTORY, dictation_filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # Skip header and separator, get actual dictation text
        dictation_text = ''.join(lines)
    return dictation_text

            

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
        
        # Create the full filepath
        filename = "user_dictation.txt"
        filepath = os.path.join(COLLECTION_DIRECTORY, filename)
        
        # Save the text with proper formatting
        with open(filepath, 'w', encoding='utf-8') as file:
            # Add a header with timestamp
            file.write(user_text)  # Write the actual dictation text
            
        # Store the filename for later use
        app.config['CURRENT_DICTATION'] = filename
        
    except Exception as e:
        # Provide more detailed error handling
        error_message = f"Error saving dictation: {str(e)}"
        print(error_message)
        return error_message, 500
       
    return redirect(url_for('input'))

@app.route('/input')
def input():
    """try: 
        dictation_text = display_correct_text()
     
    except Exception as e:
        error_message = f"Error displaying results: {str(e)}"
        print(error_message)
        return error_message, 500"""
    
    sample_text = "hi i am a computer science student"
    
    return render_template('UserInput.html', text=sample_text)

@app.route('/correct', methods=['POST'])
def correct():
    user_answer = request.form.get('userAnswer')
    
    try:
        # Read the original dictation text
        dictation_filepath = os.path.join(COLLECTION_DIRECTORY, 'user_dictation.txt')
        with open(dictation_filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            original_text = ''.join(lines)
            
        # Save the user's answer with reference to original
        answer_filename = "answer.txt"
        answer_filepath = os.path.join(COLLECTION_DIRECTORY, answer_filename)
        
        with open(answer_filepath, 'w', encoding='utf-8') as file:
            file.write(user_answer)
            
        # Store filenames for grading
        app.config['CURRENT_ANSWER'] = answer_filename
            
    except Exception as e:
        error_message = f"Error processing answer: {str(e)}"
        print(error_message)
        return error_message, 500
        
    return redirect(url_for('grading'))

@app.route('/grading')
def grading():
    try: 
        dictation_text = display_correct_text()
        return render_template('CorrectionResult.html', text=dictation_text)
     
    except Exception as e:
        error_message = f"Error displaying results: {str(e)}"
        print(error_message)
        return error_message, 500
    
@app.route('/result')
def result():
    try: 
        dictation_text = display_correct_text()
        return render_template('ResultPage.html', text=dictation_text)
     
    except Exception as e:
        error_message = f"Error displaying results: {str(e)}"
        print(error_message)
        return error_message, 500
    

if __name__ == '__main__':
    app.run(debug=True)