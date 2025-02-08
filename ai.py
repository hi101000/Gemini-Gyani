from io import BytesIO

import google.generativeai as genai
#import function_call_processing as fcp
import base64

def get_document(pdf_file):
    pass

def call(message:str, chat:genai.ChatSession)->str:
    response = chat.send_message(message)
    print(response.candidates)
    return response.text

if __name__ == '__main__':
    #genai.configure(api_key="AIzaSyBqYC_db8v_t6qrnR_Zn6ktJJD4ZUSbyDM")
    #model = genai.GenerativeModel("gemini-1.5-flash", tools=funcs)
    #chat = model.start_chat(enable_automatic_function_calling=True)
    #response = chat.send_message(input("User> "))
    #print(response.text)
    pass