import speech_recognition as sr

class Listener:

    def __init__(self):
        self.listener = sr.Recognizer()
        self.microphone = sr.Microphone()
    def listen(self):
        with self.microphone as source:
            self.listener.adjust_for_ambient_noise(source)
            print("listening...")
            voice = self.listener.listen(source)
            command = self.listener.recognize_faster_whisper(voice)
            command = command.lower()
            return command

if __name__ == '__main__':
    listener = Listener()
    listener.listen()