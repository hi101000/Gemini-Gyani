from google import genai
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QFileDialog, QLabel
from PySide6.QtCore import Qt
import functions
import os
from re import search
import base64
import pathlib
import sys
import listener
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch, ToolCodeExecution
from PySide6.QtGui import QTextCursor
import webbrowser

class ClickableTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:  # Check if left mouse button was clicked
            # Map the mouse position to the text cursor position
            cursor = self.cursorForPosition(event.position().toPoint())
            char_format = cursor.charFormat()
            if char_format.isAnchor():  # Check if the cursor is on a link
                url = char_format.anchorHref()
                if 'https://' or "http://" in url:
                    webbrowser.open(url)  # Open the link in the default web browser
                else:
                    webbrowser.open('https://'+url)
        super().mouseReleaseEvent(event)

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.file = None
        google_search_tool = Tool(
            google_search=GoogleSearch()
        )
        self.instructions = ""
        tools = [
            {'google_search': {}},
            {'code_execution': {}},
            {'function_declarations': [functions.leave, functions.get_news, functions.open_app, functions.open_website, functions.get_headlines, functions.wikipedia_summary]}
        ]
        self.setWindowTitle("Gyani AI Assistant")
        self.client = genai.Client(api_key=os.getenv("API_KEY"))
        config = {
            "tools": [functions.leave, functions.get_news, functions.open_app, functions.open_website, functions.get_headlines, functions.wikipedia_summary],
            "system_instruction": "You are a helpful ai assistant called Gyani, who can assist the user in a number of ways beyond merely engaging in conversation. You do have access to recent events through the provided tools. You can also generate code, write essays/speeches, and do other helpful things for the user. When you respond with code, you will enclose it in `` (e.g. `import tkinter as tk`)"
        }
        self.model="gemini-2.0-flash"
        self.chat = self.client.chats.create(model=self.model, config=config)
        self.server = False #Is the pdf file stored in google's server or on a website?

        # Layout
        layout = QVBoxLayout()

        # Message display
        self.message_display = ClickableTextEdit()
        self.message_display.setReadOnly(True)
        #self.message_display.cursorPositionChanged.connect(self.handle_link_click)
        layout.addWidget(self.message_display)

        # Message input
        self.message_input = QLineEdit()
        layout.addWidget(self.message_input)

        # Send button
        send_button = QPushButton("Send")
        send_button.clicked.connect(lambda: self.send_message())
        layout.addWidget(send_button)

        self.file_lbl = QLabel("Attached File: ")
        layout.addWidget(self.file_lbl)

        pdf_btn = QPushButton("Attach a File")
        pdf_btn.clicked.connect(self.attach_file)
        layout.addWidget(pdf_btn)

        self.file_input = QLineEdit()
        layout.addWidget(self.file_input)

        self.message_display.setMarkdown("")

        self.audio_btn = QPushButton("record audio")
        self.listener = listener.Listener()
        self.audio_btn.clicked.connect(lambda: self.send_message(self.listener.listen()))
        layout.addWidget(self.audio_btn)

        self.setLayout(layout)

    # ...existing code...

    def send_message(self, prompt = ""):
        if prompt == "":
            message = self.message_input.text()
        else:
            message = prompt
        if self.file == None:
            if self.file_input.text() == "":
                if message:
                    self.message_display.setMarkdown(self.message_display.toMarkdown() + f"\n\nYou: {message}\n\n")
                    self.message_input.clear()
                    self.message_display.setMarkdown(
                        self.message_display.toMarkdown() + 
                        f"System: {self.chat.send_message(message).text}\n\n"
                    )
                    print(self.message_display.toPlainText())
            else:
                import httpx
                from google.genai import types
                url = self.file_input.text()
                doc_data = httpx.get(url).content
                if message:
                    self.message_display.setMarkdown(self.message_display.toMarkdown() + f"\n\nYou: {message}\n\n")
                    self.message_input.clear()
                    response = self.client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[
                            types.Part.from_bytes(
                                data=doc_data,
                                mime_type='application/pdf',
                            ),
                            message])
                    self.message_display.setMarkdown(
                        self.message_display.toMarkdown() + 
                        f"System: {response.text}\n\n"
                    )
        else:
            if message:
                self.message_display.setMarkdown(self.message_display.toMarkdown() + f"\n\nYou: {message}\n\n")
                self.message_input.clear()
                self.message_display.setMarkdown(
                    self.message_display.toMarkdown() + 
                    f"System: {self.client.models.generate_content(contents=[self.file, message], model=self.model).text}\n\n"
                )

            self.client.files.delete(name=self.file.name)
            self.file = None
            self.file_lbl.setText("Attached File: ")
            self.server = False

# ...existing code...

    def attach_file(self):
        root = os.path.abspath('.').split(os.path.sep)[0]+os.path.sep
        path = QFileDialog.getOpenFileName(self, 'Open file', f'{root}', "Any File (*.*)")
        fname = path[0]
        if search("(.pdf$|.jpg$|.jpeg$|.png$|.txt$|.py$|.java$|.c$|.cpp$|.go$|.sh$|.env$)", fname) != None:
            with open(fname, "rb") as f:
                self.file = base64.standard_b64encode(f.read()).decode("utf-8")
        else:
            return
        if(fname != ''):
            media = pathlib.Path(__file__).parents[1] / "third_party"
            self.file = self.client.files.upload(file=fname)
            self.server = True
            self.file_lbl.setText("Attached File: "+fname)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.send_message()

    def attach_pdf_web(self):
        if self.file_lbl.text() == "":
            pass

    def handle_link_click(self):
        cursor = self.message_display.textCursor()
        char_format = cursor.charFormat()
        if char_format.isAnchor():  # Check if the cursor is on a link
            url = char_format.anchorHref()
            webbrowser.open(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec())
