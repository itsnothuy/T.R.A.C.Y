import pyttsx3

def speak_text(text):
    engine = pyttsx3.init()
    # Adjust voice properties as needed
    engine.setProperty('rate', 150)    # Speed
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()
if __name__ == "__main__":
    speak_text("Hello! I can speak now!")
