from openai import OpenAI
from gtts import gTTS
import pygame
import os

# OpenAI API key
client = OpenAI(api_key="XYZ")


def speak(text):

    tts = gTTS(text)

    filename = "response.mp3"

    tts.save(filename)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue


def chat():

    user = input("You (patient): ")

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[
            {"role": "system", "content": "You are a medical receptionist."},
            {"role": "user", "content": user}
        ]
    )

    reply = response.choices[0].message.content

    print("\nAI:", reply)

    speak(reply)


while True:

    chat()
