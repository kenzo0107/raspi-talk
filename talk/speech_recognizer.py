import speech_recognition as sr

# speech_recognition は使用時無料


class SpeechRecognizer:
    def __init__(self, audio_file, language):
        self.audio_file = audio_file
        self.language = language
        self.client = sr.Recognizer()

    def recognize(self):
        with sr.AudioFile(self.audio_file) as source:
            audio_text = self.client.listen(source)
            text = self.client.recognize_google(audio_text, language='ja')
            return text


if __name__ == '__main__':
    recognizer = SpeechRecognizer('record.wav', language='ja')
    text = recognizer.recognize()
    print(text)
