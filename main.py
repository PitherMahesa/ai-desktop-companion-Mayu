
import customtkinter as ctk
import mss
from PIL import Image
import pytesseract
import pyttsx3
import base64
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

engine = pyttsx3.init()

app = ctk.CTk()
app.title("AI Desktop Companion")
app.geometry("600x650")

screen_text = ""

def capture_screen():
    global screen_text

    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

    screen_text = pytesseract.image_to_string(image)

    output.delete("1.0", "end")
    output.insert("end", screen_text)

    status.configure(text="Screen captured successfully!")

def ask_ai():
    question = question_input.get()

    if not question.strip():
        return

    if not screen_text.strip():
        status.configure(text="Capture your screen first.")
        return

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=(
                "Analyze this extracted desktop text:\n"
                + screen_text[:12000]
                + "\n\nUser question: "
                + question
            )
        )

        answer = response.output_text

        output.insert("end", "\n\nAI:\n" + answer)
        engine.say(answer)
        engine.runAndWait()

    except Exception as error:
        status.configure(text=f"Error: {error}")

title = ctk.CTkLabel(
    app,
    text="AI Desktop Companion",
    font=("Arial", 25, "bold")
)
title.pack(pady=20)

capture_button = ctk.CTkButton(
    app,
    text="Capture Desktop",
    command=capture_screen
)
capture_button.pack(pady=10)

output = ctk.CTkTextbox(app, width=540, height=300)
output.pack(pady=15)

question_input = ctk.CTkEntry(
    app,
    width=500,
    placeholder_text="Ask something about your screen..."
)
question_input.pack(pady=10)

ask_button = ctk.CTkButton(
    app,
    text="Ask AI",
    command=ask_ai
)
ask_button.pack(pady=10)

status = ctk.CTkLabel(app, text="Ready")
status.pack(pady=10)

app.mainloop()
