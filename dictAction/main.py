from tts2 import *

dictation = input("Enter the dictation you desire to practice: ")
#dictation = text that is already in our collection? if statement to decided what dictation will contain

# punctuation 
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

# Converting dictation for the punctuations to be included in speech 
def replace_punctuation_with_words(text):

    for punctuation, punctuation_name in punctuation_dict.items():
        text = text.replace(punctuation, ' ' + punctuation_name + ' ')
    text = text.split()
    return " ".join(text)

dictation_to_be_read = replace_punctuation_with_words(dictation)

#reading of dictation
speak_slow(dictation_to_be_read)

# Replace word with punctuation 
def replace_word_with_punctuation(text):
    for punctuation, punctuation_name in punctuation_dict.items(): 
        text = text.replace(punctuation_name, " " + punctuation + " ")
    text = text.split()
    return " ".join(text)

#finding word count of original dictation
dictation_lst = replace_punctuation_with_words(dictation).split(" ")
word_count = len(dictation_lst)

#Alert when they try to correct. The error messages should appear as pop-ups (react????)

# function to read a text file 
def read_txt(filename):
    with open(filename, "r") as f:
        dictation_text = f.read()
    return dictation_text


#adding red to mistakes in student answer
def correct_text(student_answer):
    answer_lst = replace_punctuation_with_words(student_answer).split(" ")
    answer_length = len(answer_lst)
    if answer_length != word_count:
        difference = word_count - answer_length
        if difference > 0:
            print("You are missing", difference, "words. Please listen again carefully and make sure you write every word carefully before correcting.")
        else:
            print ("You have", difference, "extra words. Please listen again carefully and make sure you write every word carefully before correcting.")
    else:
        for i in dictation_lst:
            if dictation_lst[i] != answer_lst[i]:
                answer_lst[i] = "#FF5733"
                err_count +=1
        answer_str = " ".join(answer_lst)
        corrected_version = replace_word_with_punctuation(answer_str)
        return corrected_version 

err_count = 0
answer_lst = []
student_answer = input("Please start answering your answer...")
result = correct_text(answer_lst)

#calculating grade
def fraction_grade(err_count, word_count):
    right_answers = word_count - err_count 
    fraction_grade = str(right_answers) + "/" + str(word_count)
    return fraction_grade

def percentage_grade(err_count, word_count):
    right_answers = word_count - err_count
    grade = right_answers / word_count * 100
    return grade

percent_grade = percentage_grade(err_count, word_count)
print(percent_grade, "/100")

fraction_grade = fraction_grade(err_count, word_count)
print(fraction_grade) 

            

            
