from flask import Blueprint, Flask, render_template, render_template_string, request, jsonify, redirect, url_for
from tts2 import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'


if __name__ == '__main__':
    app.run(debug=True, port=5000)

views = Blueprint('views', __name__, template_folder='templates')

# Converting dictation for the punctuations to be included in speech 
punctuation_dict = {
            '.': 'period',
            ',': 'comma',
            '!': 'exclamationmark',
            '?': 'questionmark',
            ';': 'semicolon',
            ':': 'colon',
            '"': 'quotationmark',
            '-': 'hyphen',
            '(': 'openparenthesis',
            ')': 'closeparenthesis',
            '[': 'opensquarebracket',
            ']': 'closesquarebracket'
        }

def replace_punctuation_with_words(text):
    for punctuation, punctuation_name in punctuation_dict.items():
        text = text.replace(punctuation, ' ' + punctuation_name + ' ')
    text = text.split()
    return " ".join(text)

def replace_word_with_punctuation(text):
    for punctuation, punctuation_name in punctuation_dict.items(): 
        text = text.replace(punctuation_name, " " + punctuation + " ")
    text = text.split()
    return " ".join(text)

@views.route('/', defaults={'page': 'WebPage'})
@views.route('/<page>')
def home(page):
    return render_template(f'{page}.html')


@views.route('/process')
def process():
    dictation = request.args.get('message')
    # punctuation 
    dictation_to_be_read = replace_punctuation_with_words(dictation)
    return render_template('UserInput.html', message=dictation_to_be_read)
#somehow turn TTS and store into the speed button

@views.route("/dictSelect1", methods=['POST'])
def dictSelect():
    button_pressed = request.form.get('button')
    message=""
    if button_pressed == "dict1_1":
        message = "My best friend's name is Lily. She has a big, white dog named Max. We like to play in the park. Lily is very kind and shares her toys with me. We both love eating ice cream on sunny days."
    elif button_pressed == "dict1_2":
        message = "The sun is bright and yellow. It makes flowers grow and rivers flow. Birds sing when the sun comes up. I love to play outside when the sun is shining. It makes me feel happy and warm."
    elif button_pressed == "dict1_3":
        message = "I have a small family. There are four people in my family. My dad, my mom, my little brother, and me. We live in a blue house. We like to watch movies and eat popcorn together."
    elif button_pressed == "dict1_4":
        message = "My best friend's name is Lily. She has a big, white dog named Max. We like to play in the park. Lily is very kind and shares her toys with me. We both love eating ice cream on sunny days."
    
    dictation_to_be_read = replace_punctuation_with_words(message)
    return render_template('UserInput.html', message=dictation_to_be_read)

"""
@views.route("/dictSelect2", methods=['POST'])
def dictSelect():
    button_pressed = request.form.get('button')
    message=""
    if button_pressed == "dict2_1":
        message = "Reading opens doors to uncharted worlds, offering a glimpse into the lives of characters from distant lands and times. Through the pages of a book, one can embark on adventures without leaving the comfort of home. It challenges our perspectives, enriches our vocabulary, and ignites our imagination. Every book holds the potential to transform the way we think and feel about the world around us."
    elif button_pressed == "dict2_2":
        message = "Teamwork is the cornerstone of success in both sports and life. When individuals come together to achieve a common goal, they share their strengths and compensate for each other's weaknesses. Effective communication and mutual respect are vital, as they foster an environment where everyone feels valued and empowered. The triumphs achieved through teamwork are not just victories but lessons in collaboration and unity."
    elif button_pressed == "dict2_3":
        message = "Gazing up at the night sky, one can't help but marvel at the vast expanse of the universe. Stars twinkle like diamonds scattered across a velvet cloth, each one a sun in its own right, perhaps with planets of its own. The constellations tell ancient stories, guiding explorers and inspiring poets. In the quiet of the night, the sky reminds us of our place in the cosmos, offering a perspective that is both humbling and exhilarating."
    elif button_pressed == "dict2_4":
        message = "A river's journey begins as a small trickle of water, emerging from a spring nestled in the mountains. As it travels down slopes and through valleys, it grows, fed by rainwater and melting snow. It carves through landscapes, shaping the earth with its persistent flow. Along its banks, ecosystems thrive, and civilizations develop, drawn by the life-giving waters. Finally, the river meets the sea, its waters mingling with the vastness of the ocean, completing a cycle that has endured for eons."
    
    dictation_to_be_read = replace_punctuation_with_words(message)
    return render_template('UserInput.html', message=dictation_to_be_read)
"""

@views.route("/read", methods=['POST'])
def read():
    button_pressed = request.form.get('button')
    message = request.form.get('message')
    if button_pressed == "slow":
        spoken = speak_slow(message)
    elif button_pressed == "normal":
        spoken = speak_normal(message)
    elif button_pressed == "fast":
        spoken = speak_fast(message)

    return render_template_string('UserInput.html', message=message)

@views.route('/correct', methods=['POST'])
def correct():
    student_answer = request.form.get('textarea')
    message = request.form.get('message')
    button_pressed = request.form.get('button')

    dictation_lst = message.split(" ")
    word_count = len(dictation_lst)

    if button_pressed == "paper":
        message = replace_word_with_punctuation(message)
        return render_template('ResultPage.html', message=message)

    elif button_pressed == "grade":
        err_count = 0
        answer_lst_copy = []
        message = replace_word_with_punctuation(message)
        answer_lst = replace_punctuation_with_words(student_answer).split(" ")
        answer_length = len(answer_lst)
        if answer_length != word_count:
            difference = word_count - answer_length
            if difference > 0:
                #the popup
                print("You are missing", difference, "words. Please listen again carefully and make sure you write every word carefully before correcting.")
            else:
                #alternate popup message
                print ("You have", difference, "extra words. Please listen again carefully and make sure you write every word carefully before correcting.")
        else:
            for i in range(len(dictation_lst)):
                if dictation_lst[i] != answer_lst[i]:
                    answer_lst_copy.append({"color":"texterror", "text":answer_lst[i]})
                    err_count +=1
            #answer_str = " ".join(answer_lst)
            #corrected_version = replace_word_with_punctuation(answer_str)
        return render_template('CorrectionResult.html', corrected_version=answer_lst_copy, message=message, err_count=err_count, word_count=word_count)

@views.route("/grading", methods=['POST'])
def grading(err_count, word_count):
    def fraction_grade(err_count, word_count):
        right_answers = word_count - err_count 
        fraction_grade = str(right_answers) + "/" + str(word_count)
        return fraction_grade
    
    def percentage_grade(err_count, word_count):
        right_answers = word_count - err_count
        grade = right_answers / word_count * 100
        return grade

    percent_grade = percentage_grade(err_count, word_count)

    fraction_graded = fraction_grade(err_count, word_count)

    return render_template("CorrectionResult.html", grade=fraction_graded)

app.register_blueprint(views)
