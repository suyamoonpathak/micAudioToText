import speech_recognition as sr
import keyboard

def main():
    recognizer = sr.Recognizer()

    print("Press 'Q' to start/stop listening...")
    listening = False

    while True:
        if keyboard.is_pressed('q'):
            listening = not listening
            print("Listening..." if listening else "Stopped listening...")
            keyboard.wait('q', suppress=True)  # Wait for the 'Q' key to be released

        if listening:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)

                try:
                    print("Recognizing...")
                    text = recognizer.recognize_google(audio, language="en")
                    print("You said:", text)
                except sr.UnknownValueError:
                    print("Sorry, could not understand audio.")
                except sr.RequestError as e:
                    print("Could not request results; check your network connection:", e)

if __name__ == "__main__":
    main()
