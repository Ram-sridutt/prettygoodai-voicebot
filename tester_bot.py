from openai import OpenAI
from gtts import gTTS
import pygame
import time

client = OpenAI(api_key="XYZ")


scenarios = [

"I want to book an appointment for tomorrow",

"My name is John Smith and I want appointment at 3pm",

"I need to refill my blood pressure medication",

"What are your office hours?",

"Do you accept Aetna insurance?",

"I want to cancel my appointment",

"I need urgent appointment today",

"Where is your clinic located?",

"Can I reschedule my appointment?",

"My prescription ran out what should I do?"

]


def speak(text, filename):

    tts = gTTS(text)

    tts.save(filename)

    pygame.init()

    pygame.mixer.init()

    pygame.mixer.music.load(filename)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():

        continue


def ask_ai(message):

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[
            {"role": "system", "content": "You are a medical receptionist."},
            {"role": "user", "content": message}
        ]

    )

    return response.choices[0].message.content


def run_test():

    transcript = ""

    for i, scenario in enumerate(scenarios):

        print("\nPATIENT:", scenario)

        reply = ask_ai(scenario)

        print("AI:", reply)

        transcript += f"\nPATIENT: {scenario}\nAI: {reply}\n"

        speak(reply, f"response_{i}.mp3")

        time.sleep(1)

    with open("transcript.txt", "w") as file:

        file.write(transcript)

    print("\nTranscript saved.")


run_test()
