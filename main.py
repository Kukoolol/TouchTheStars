from flask import Flask, render_template, request, jsonify
from flask_ngrok import run_with_ngrok
import base64
from PIL import Image
import pytesseract
import pyfirmata
import time
from ChatbotVerse import chatbotVerse as cbv

app = Flask(__name__)
text_list = "Skibidi"
import os


def init_chat_model():
    trainer = cbv.modelTrain()
    intents = trainer.loadIntents('intents.json')
    words, classes = trainer.preprocess_save_Data(intents)
    train_x, train_y = trainer.prepareTrainingData(words, classes)
    model = trainer.createModel(train_x, train_y, save_path='cbv_model.model')
    predictor = cbv.modelPredict('intents.json', 'cbv_model.model')
    return predictor



def run_chat_bot(message,predictor):
    running = True
    while running:  
        msg = input('You: ')
        if msg == 'quit':
            running = False
        else:
            response = predictor.chatbot_response(msg)
            return response

pred = init_chat_model




def extract_text_from_image(image_path):
    # Open the image file
   
    with Image.open(image_path) as img:
        # Perform OCR on the image
        text = pytesseract.image_to_string(img)
        print("text",text)
        return text.strip()

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        os.remove("test.jpeg")
    except FileNotFoundError:
        pass
    image = request.form.get("image")
    byte_data = image[22:].encode('utf-8')

    with open("test.jpeg", "wb") as fh:
        fh.write(base64.b64decode(byte_data))
    image_path = 'test.jpeg'
    
    extracted_text = extract_text_from_image(image_path)
    return jsonify({"extracted_text": extracted_text})



@app.route('/')
def index():
    return render_template('index.html')



import sqlite3
import csv



def initdb():
    conn = sqlite3.connect('braillelearning.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS phrases (
        id INTEGER PRIMARY KEY,
        phrase TEXT,
        brailleequivalent TEXT
    )
    ''')
    with open('braillelearning.db', 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            cursor.execute('INSERT OR IGNORE INTO phrases (id, phrase, braille_equivalent) VALUES (?, ?, ?)', row)
    conn.commit()
    conn.close()


def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
    braille = convert_text_to_braille(text)
    return render_template('result.html', original=text, braille=braille)

def convert_text_to_braille(text):
    return "⠮ " + " ⠁ ".join(text)

@app.route('/learn')
def learn():
    conn = sqlite3.connect('braille_learning.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM phrases')
    phrases = cursor.fetchall()
    conn.close()
    return render_template('learn.html', phrases=phrases)

    
def generate_response(input):
    
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTA5NDU3NjYtZThhMC00YWViLThjY2ItNjQxMGQ5YjJkOTNkIiwidHlwZSI6ImFwaV90b2tlbiJ9.6bBDFaJt31ekb8qG_sMC0OybxmN2b_iTM_z_-L16DZM"}
    
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": f"Respond to this message by acting as a casual person replying to this:{input} with a random on context paragraph related ot the text.,",
        "chatbot_global_action": "be an astronaut in a casual conversation",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 50,  # Increase token limit for more detailed recommendations
        "fallback_providers": ""
    }
    
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    
    if 'openai' in result and 'generated_text' in result['openai']:
        return result['openai']['generated_text']
    else:
        return "Sorry, I couldn't generate a recommendation at this moment."

# Route for handling food recommendation queries
@app.route('/llmoutput', methods=['POST'])
def llm_response():
    randomm = request.form.get("random")  # Get the food input from the form
    if randomm:
        recommendation = generate_response(randomm)
        return jsonify({"response": recommendation})
    return jsonify({"response": "No input received."})

if __name__=='__main__':

    app.run(port = 5000, host='0.0.0.0')
    
    












# Path to Tesseract executable (change this if needed)
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
class TextExtractor:
    def __init__(self, image_path):
        self.image_path = image_path
    
    def open_image(self):
        return Image.open(self.image_path)
    
    def extract_text(self, image):
        return pytesseract.image_to_string(image)
    
    def clean_text(self, text):
        return text.strip()
    
    def print_text(self, text):
        print("Extracted Text:")
        print(text)




# Path to the image file
def print_ext_text(extracted_text):
    text_list = [char for char in extracted_text]
    print(text_list)
#Print hte extracted text

def char_to_braille(char):
    braille_dict = {
        'a': [[1, 0], [0, 0], [0, 0]],
        'b': [[1, 0], [1, 0], [0, 0]],
        'c': [[1, 0], [0, 1], [0, 0]],
        'd': [[1, 0], [0, 1], [1, 0]],
        'e': [[1, 0], [0, 0], [1, 0]],
        'f': [[1, 0], [1, 1], [0, 0]],
        'g': [[1, 0], [1, 1], [1, 0]],
        'h': [[1, 0], [1, 0], [1, 0]],
        'i': [[0, 1], [1, 0], [0, 0]],
        'j': [[0, 1], [1, 0], [1, 0]],
        'k': [[1, 1], [0, 0], [0, 0]],
        'l': [[1, 1], [1, 0], [0, 0]],
        'm': [[1, 1], [0, 1], [0, 0]],
        'n': [[1, 1], [0, 1], [1, 0]],
        'o': [[1, 1], [0, 0], [1, 0]],
        'p': [[1, 1], [1, 1], [0, 0]],
        'q': [[1, 1], [1, 1], [1, 0]],
        'r': [[1, 1], [1, 0], [1, 0]],
        's': [[0, 1], [1, 1], [0, 0]],
        't': [[0, 1], [1, 1], [1, 0]],
        'u': [[1, 1], [0, 0], [1, 1]],
        'v': [[1, 1], [1, 0], [1, 1]],
        'w': [[0, 1], [1, 0], [1, 1]],
        'x': [[1, 1], [0, 1], [1, 1]],
        'y': [[1, 1], [0, 1], [1, 1]],
        'z': [[1, 1], [0, 0], [1, 1]],
        '0': [[0, 1], [1, 0], [1, 1]],
        '1': [[1, 0], [0, 0], [0, 1]],
        '2': [[1, 0], [1, 0], [0, 1]],
        '3': [[1, 0], [0, 1], [0, 1]],
        '4': [[1, 0], [0, 1], [1, 1]],
        '5': [[1, 0], [0, 0], [1, 1]],
        '6': [[1, 0], [1, 1], [0, 1]],
        '7': [[1, 0], [1, 1], [1, 1]],
        '8': [[1, 0], [1, 1], [0, 1]],
        '9': [[0, 1], [1, 0], [0, 1]],
        '!': [[0, 0], [1, 1], [0, 1]],
        '?': [[0, 0], [1, 1], [1, 0]],
        ',': [[0, 0], [0, 1], [0, 0]],
        '.': [[0, 0], [1, 0], [1, 0]],
        ' ': [[0, 0], [0, 0], [0, 0]]
    }
    return braille_dict.get(char.lower(), [[0, 0], [0, 0], [0, 0]])

def text_to_braille(text):
    result = []
    for char in text:
        result.append(char_to_braille(char))
    return result

def print_braille(braille):
    for i in range(3):
        line = ''
        for cell in braille:
            line += '1' if cell[i][0] else '0'
            line += '1' if cell[i][1] else '0'
        print(line)

@app.route('/gptbraille', methods=['POST'])
def gptbraille():
    braille_representation = text_to_braille(generate_response())
    print("\nBraille representation:")







    
    

# board = pyfirmata.Arduino('/dev/cu.usbmodem11101')



# while True:

#     for braille in braille_representation:
#         board.digital[2].write(braille[0][0])
#         board.digital[3].write(braille[0][1])
#         board.digital[4].write(braille[1][0])
#         board.digital[5].write(braille[1][1])
#         board.digital[6].write(braille[2][0])
#         board.digital[7].write(braille[2][1])






app = Flask(__name__)


 













def randomreq(randomm):
    a = generate_response(randomm)
    text_list = a
    return a


@app.route('/generate_practice_paragraph', methods=['POST'])
def generate_paragraph():
    randomm = request.form.get("input")  # Get the input from the frontend
    if randomm:
        recommendation = randomreq(randomm)

        # Send the generated text to the serial port
          # Send data through the serial port
        text_list = recommendation
        return jsonify({"response": recommendation})
    return jsonify({"response": "No input received."})

# Make sure to close the serial connection when the application ends


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')

    
import serial

SerialObj = serial.Serial('/dev/cu.usbmodem1101') # COMxx  format on Windows
                  
SerialObj.baudrate = 9600  # set Baud rate to 9600
SerialObj.bytesize = 8   # Number of data bits = 8
SerialObj.parity  ='N'   # No parity
SerialObj.stopbits = 1   # Number of Stop bits = 1
time.sleep(5)
for letter in text_list:
     SerialObj.write(letter.lower().encode())    #transmit 'A' (8bit) to micro/Arduino
     time.sleep(5)


