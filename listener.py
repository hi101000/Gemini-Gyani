import speech_recognition as sr

class Listener:

    def __init__(self):
        try:
            self.listener = sr.Recognizer()
            self.microphone = sr.Microphone()
        except:
            self.listener = None
            self.microphone = None
    def listen(self) -> str:
        if self.microphone is not None:
            with self.microphone as source:
                self.listener.adjust_for_ambient_noise(source)
                print("listening...")
                voice = self.listener.listen(source)
                command = self.listener.recognize_faster_whisper(voice)
                command = command.lower()
                return command
        else:
            return "there was an error in microphone configuration, so no command was received"

if __name__ == '__main__':
    listener = Listener()
    listener.listen()