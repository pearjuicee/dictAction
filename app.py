import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

def normalize_text(text):
    words = text.strip().split()
    return words

def calculate_grade(original_text, student_answer):
    original_words = normalize_text(original_text)
    student_words = normalize_text(student_answer)

    total_words = len(original_words)
    marked_words = []
    correct_count = 0
    error_words = []

    max_length = max(len(original_words), len(student_words))

    for i in range(max_length):
        if i < len(original_words) and i < len(student_words):
            orig_curr = original_words[i]
            student_curr = student_words[i]

            if orig_curr == student_curr:
                marked_words.append({
                    "word": student_curr,
                    "status": "correct",
                    "color": "black"
                })
                correct_count += 1
            else:
                marked_words.append({
                    "word": student_curr,
                    "status": "incorrect",
                    "correct_word": orig_curr,
                    "color": "red"
                })
        elif i < len(original_words):
            marked_words.append({
                "word": "___",
                "status": "missing",
                "correct_word": original_words[i],
                "color": "red"

            })

        else:
            marked_words.append({
                "word": student_words[i],
                "status": "extra",
                "correct_word": None,
                "color": "red"
            })
    score_fraction = f"{correct_count}/{total_words}"
    percentage = int((correct_count / total_words) * 100)

    return marked_words, score_fraction, percentage


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

            
"""@app.route('/Beginner')
def beginner():
    return render_template('Beginner.html')

@app.route('/random_dictation', methods=['POST'])
def random_dictation(): 
    # Choose a random dictation 
    try:
        dictation_key = random.choice(list(DICTATIONS['beginner'].keys()))
        filep
ACID = ht"""
        

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
    try: 
        dictation_text = display_correct_text()
     
    except Exception as e:
        error_message = f"Error displaying results: {str(e)}"
        print(error_message)
        return error_message, 500
    
    return render_template('UserInput.html', text=dictation_text)

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
        # Read original dictation text
        with open(os.path.join(COLLECTION_DIRECTORY, 'user_dictation.txt'), 'r', encoding='utf-8') as file:
            original_text = file.read()
        
        # Read student's answer
        with open(os.path.join(COLLECTION_DIRECTORY, 'answer.txt'), 'r', encoding='utf-8') as file:
            student_answer = file.read()
        
        # Calculate grade and get marked words with detailed feedback
        marked_words, score_fraction, percentage = calculate_grade(original_text, student_answer)
        
        return render_template('CorrectionResult.html',
                             original_text=original_text,
                             marked_words=marked_words,
                             score_fraction=score_fraction,
                             percentage=percentage)
     
    except Exception as e:
        error_message = f"Error during grading: {str(e)}"
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