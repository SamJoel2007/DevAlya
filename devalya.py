from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from PIL import Image as PILImage, ImageTk 
from tkinter import *
import subprocess
import anthropic
import random
import base64
import time 
import os 

# CONFIG
anthropic_api_key = ""
elevenlabs_api_key = ""
Alya_prompt = """
Your name is Alya, you are a skillful developer. You have skills in HTML, CSS, JS, & BOOTSTRAP.
Your job is to generate code based on the user's prompt. You will be given a prompt, and you will generate code based on that prompt.
Remember that you must only generate the code, and nothing else. Do not include any explanations or comments in your code.
Always generate complete, fully working code. Never leave code incomplete or cut off mid-way.

User's Prompt: 
"""

greetings = [
    "Hello! I'm Alya, your AI code generator. What would you like to build today?",
    "Hi there! I'm Alya, your AI code generator. What project are you working on?",
    "Hey! I'm Alya, your AI code generator. What kind of code do you need help with?",
    "Welcome! I'm Alya, your AI code generator. What can I assist you with today?"
]

class DevAlya:
    def generate_code(self, user_prompt):
        DevAlya.talk(self, "Generating code for you, please wait...")
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=8096,
            messages=[
                {"role": "user", "content": Alya_prompt + user_prompt}
            ]
        )
        generated_code = response.content[0].text.strip()
        DevAlya.talk(self, "Code generated successfully! Saving it to index.html")
        DevAlya.save_code(self, generated_code)

    def save_code(self, code):
        with open("index.html", "w") as file:
            file.write(code)

    def wait(self, seconds):
        time.sleep(seconds)

    def talk(self, message):
        try:
            client = ElevenLabs(api_key=elevenlabs_api_key)  # FIX 2: correct variable name (was ELEVENLABS_API_KEY)
            audio = client.text_to_speech.convert(
                text=message,
                voice_id="d2R8EPtwKe5obmujTQ7h",
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            play(audio)
        except Exception:
            print(message)

    def app(self):
        def greet():
            greeting = random.choice(greetings)
            self.talk(greeting)

        # Create the main window
        self.root = Tk()
        self.root.title("DevAlya - AI Code Generator")
        self.root.geometry("800x500")
        self.root.configure(bg='black')
        greet()

        # Title label
        self.input_label = Label(self.root, text="DevAlya AI", font=("Arial", 16), bg='black', fg='white')
        self.input_label.pack(pady=20)

        # FIX 3: PILImage instead of Image, self.image in PhotoImage, Label instead of tk.Label
        self.image = PILImage.open("alya.ico")
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = Label(self.root, image=self.photo)
        self.label.image = self.photo
        self.label.pack()

        Label(self.root, text="Type your request below and generate your code, and make sure to leave a star on the github repo :)", font=("Arial", 10), bg='black', fg='white').pack(pady=5, anchor='w')
        Label(self.root, text="Website: https://devwithsam.space", font=("Arial", 10), bg='black', fg='white').pack(pady=5, anchor='w')
        Label(self.root, text="Built with Love and Caffeine", font=("Arial", 10), bg='black', fg='white').pack(pady=10, anchor='w')
        Label(self.root, text="", font=("Arial", 10), bg='black', fg='white').pack(pady=5, anchor='w')

        self.input_entry = Entry(self.root, width=50, bg='gray', fg='white', font=("Arial", 14))
        self.input_entry.pack(pady=20, anchor='s')

        self.generate_button = Button(self.root, text="Generate Code", command=lambda: self.generate_code(self.input_entry.get()), bg='gray', fg='white', font=("Arial", 14))
        self.generate_button.pack(pady=20, anchor='s')

        self.root.mainloop()


if __name__ == "__main__":
    dev_alya = DevAlya()
    dev_alya.app()