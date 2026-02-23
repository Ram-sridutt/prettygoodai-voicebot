import os
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load OpenAI key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Ensure transcripts folder exists
os.makedirs("transcripts", exist_ok=True)

# CONFIG: Set your scenario here
SCENARIO_TEXT = ("Paste the scenario here.")

def log_turn(call_sid: str, speaker: str, text: str):
    """Append a single conversational turn to a transcript file."""
    filename = f"transcripts/{call_sid}.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{speaker}: {text}\n")

@app.route("/voice", methods=["POST"])
def voice():
    """
    FIRST CONTACT:
    The bot should NOT speak first as a patient doesn't until the agent greets.
    It should wait for the agent's greeting.
    """
    call_sid = request.form.get("CallSid")

    resp = VoiceResponse()

    # Listen first — do NOT speak yet
    gather = Gather(
        input="speech",
        action="/handle_agent?turn=1",
        method="POST",
        timeout=5
    )
    gather.say("")  # silent gather
    resp.append(gather)

    # Fallback if no speech detected
    resp.say("Sorry, I didn't hear anything. Goodbye.")
    resp.hangup()

    return Response(str(resp), mimetype="text/xml")

@app.route("/handle_agent", methods=["POST"])
def handle_agent():
    """
    Handles the agent's spoken response.
    On turn 1: respond with the scenario.
    On later turns: respond using OpenAI.
    """
    call_sid = request.form.get("CallSid")
    agent_speech = request.form.get("SpeechResult", "")
    turn = int(request.args.get("turn", 1))

    resp = VoiceResponse()

    # If Twilio didn't capture any speech
    if not agent_speech:
        resp.say("Sorry, I didn't catch that. Goodbye.")
        resp.hangup()
        return Response(str(resp), mimetype="text/xml")

    # Log the agent's turn
    log_turn(call_sid, "AGENT", agent_speech)

    # Inject the scenario
    if turn == 1:
        patient_reply = SCENARIO_TEXT

    else:
        # SUBSEQUENT TURNS: Use OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a patient speaking to a medical office AI agent. "
                        "Be concise, realistic, and stay in character. "
                        "Your goal is to test the agent's limits and uncover issues."
                    )
                },
                {
                    "role": "user",
                    "content": f"The agent said: {agent_speech}. Respond as the patient."
                }
            ]
        )

        patient_reply = completion.choices[0].message.content.strip()

    # Log the patient's reply
    log_turn(call_sid, "PATIENT", patient_reply)

    # Speak the reply and listen again
    gather = Gather(
        input="speech",
        action=f"/handle_agent?turn={turn + 1}",
        method="POST",
        timeout=5
    )
    gather.say(patient_reply)
    resp.append(gather)

    # Fallback if no speech detected
    resp.say("Thanks, that's all I needed. Goodbye.")
    resp.hangup()

    return Response(str(resp), mimetype="text/xml")

if __name__ == "__main__":
    app.run(port=5000, debug=True)