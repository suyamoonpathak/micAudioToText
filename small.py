import speech_recognition as sr

def convert_wav_to_text(audio_file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)  # Record the entire audio file

        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Speech recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Web Speech API; {e}"

if __name__ == "__main__":
    wav_file_path = "recording2.wav"
    text_result = convert_wav_to_text(wav_file_path)
    print("Converted Text:")
    print(text_result)
