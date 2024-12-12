import speech_recognition as sr
from flask import Flask, jsonify, request

# Initialize recognizer
r = sr.Recognizer()

app = Flask(__name__)

def record_text():
    try:
        with sr.Microphone() as source2:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source2, duration=0.2)
            
            # Listen for audio input
            print("Listening... Speak now.")
            
            # Listen for audio input
            audio2 = r.listen(source2)
            
            try:
                # Attempt to recognize speech
                MyText = r.recognize_google(audio2)
                print(f"Recognized Text: {MyText}")
                return MyText
            
            except sr.UnknownValueError:
                print("Could not understand the audio. Please try again.")
                return None
            
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition; {e}")
                return None
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def output_text(text):
    if text:  # Only write non-empty text
        try:
            with open("output.txt", "a") as f:
                f.write(text + "\n")
            print("Text successfully written to output.txt")
        except IOError as e:
            print(f"Error writing to the file: {e}")

@app.route('/record', methods=['GET'])
def record():
    """
    Route to handle speech recognition and return recognized text.
    """
    text = record_text()
    if text:
        output_text(text)  # Save recognized text to file
        return jsonify({"status": "success", "recognized_text": text}), 200
    else:
        return jsonify({"status": "failure", "message": "Could not recognize speech."}), 400

if __name__ == "__main__":
    app.run(debug=True)
