import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio_data)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        print("Speech service is unavailable. Check your connection.")
        return None


if __name__ == "__main__":
    print("Speak something into the mic...")
    user_text = recognize_speech()
    print(f"Recognized: {user_text}")
