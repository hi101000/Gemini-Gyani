import ai
from google import genai
from google.genai import types
from google.generativeai import types
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QFileDialog, QLabel
from PySide6.QtCore import Qt
import functions
import os
from re import search
import base64
import pathlib
from dotenv import load_dotenv
import io
import httpx

load_dotenv()

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.file = None
        self.instructions = "You are a helpful ai assistant called Gyani, who can assist the user in a number of ways beyond merely engaging in conversation. You do have access to the most recent news through the functions provided to you."
        funcs = [functions.leave, functions.get_news, functions.open_app, functions.open_website, functions.get_headlines]
        self.setWindowTitle("Gyani AI Assistant")
        self.client = genai.Client(api_key=os.getenv("API_KEY"))
        config = {
            "tools":funcs
        }
        self.model="gemini-2.0-flash"
        self.chat = self.client.chats.create(model=self.model, config=config)
        self.server = False #Is the pdf file stored in google's server or on a website?

        # Layout
        layout = QVBoxLayout()

        # Message display
        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        layout.addWidget(self.message_display)

        # Message input
        self.message_input = QLineEdit()
        layout.addWidget(self.message_input)

        # Send button
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        self.file_lbl = QLabel("Attached File: ")
        layout.addWidget(self.file_lbl)

        pdf_btn = QPushButton("Attach a File")
        pdf_btn.clicked.connect(self.attach_file)
        layout.addWidget(pdf_btn)

        self.setLayout(layout)

    def send_message(self):
        message = self.message_input.text()
        if self.file == None:
            if message:
                self.message_display.append(f"You: {message}\n\n")
                self.message_input.clear()
            self.message_display.append(f"System: {self.chat.send_message(message).text}\n\n")
        else:
            if message:
                self.message_display.append(f"You: {message}\n\n")
                self.message_input.clear()
                if not self.server:
                    #self.message_display.append(f"System: {self.model.generate_content([{'mime_type': 'application/pdf', 'data': self.file}, message])}\n\n")
                    pass
                else:
                    self.message_display.append(f"System: {self.client.models.generate_content(contents=[self.file, message], model=self.model).text}\n\n")
            self.file.delete()
            self.client.files.delete(name=self.file.name)
            self.file = None
            self.file_lbl.setText("Attached File: ")

    def attach_file(self):
        root = os.path.abspath('.').split(os.path.sep)[0]+os.path.sep
        path = QFileDialog.getOpenFileName(self, 'Open file', f'{root}', "Any File (*.*)")
        fname = path[0]
        if search(".pdf$", fname) != None:
            with open(fname, "rb") as f:
                self.file = base64.standard_b64encode(f.read()).decode("utf-8")
        elif search(".jpg$", fname) != None:
            pass
        else:
            return
        if(fname != ''):
            media = pathlib.Path(__file__).parents[1] / "third_party"
            self.file = self.client.files.upload(file=fname)
            self.server = True
        self.file_lbl.setText("Attached File: "+fname)

    def attach_pdf_web(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec())
