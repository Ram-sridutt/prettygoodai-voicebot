# Pretty Good AI Voicebot 

This project implements a fully functional telephony-based patient simulator using **Twilio**, **Flask**, and **OpenAI**.  
The bot receives calls, listens to the medical office AI agent, responds as a realistic patient, and logs full transcripts for evaluation.

This repository contains:

- A Flask server (`app.py`) that handles inbound call webhooks
- A multi-turn conversational loop between the agent and the simulated patient
- Automatic transcript logging per call
- Outbound call script (`make_call.py`)
- 10 patient scenarios designed to stress-test the agent
- A full bug report based on real call transcripts
- Architecture documentation

---

## Features

### Listen-first behavior  
The bot **does not speak first**. It waits for the medical office AI agent to greet the caller.

### Scenario injection  
The patient’s scenario is injected **after the agent’s first turn**, ensuring natural conversation flow.

### Multi-turn conversation loop  
Each agent response is sent to OpenAI, which generates a realistic patient reply.

### Transcript logging  
Every call produces a transcript file in `transcripts.txt`.

### Outbound call automation  
`make_call.py` places calls to the Pretty Good AI test line and enables call recording.

---

## Setup Instructions

1. Clone the repository
git clone <your-repo-url>
cd prettygoodai-voicebot

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Create a .env file 
OPENAI_API_KEY=sk-xxxx
TWILIO_ACCOUNT_SID=ACxxxx
TWILIO_AUTH_TOKEN=xxxx
TWILIO_CALLER_NUMBER=+1xxxxxxxxxx
TEST_NUMBER=+1xxxxxxxxxx
TWIML_URL=https://<your-ngrok-url>/voice

5. Start the Flask Server
python app.py

6. Start ngrok
ngrok http 5000
Update TWIML_URL in .env with your ngrok HTTPS URL.

7. Run outbound call script 
python make_call.py

---

Project Structure:

prettygoodai-voicebot/
│
├── app.py                 # Flask server + conversation loop
├── make_call.py           # Outbound call script
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
├── transcripts/           # Auto-generated call transcripts
└── BUG_REPORT.md          # BUG REPORT

TESTING: 
To test all scenarios: 
1. Replace SCENARIO_TEXT in app.py
2. Run make_call.py
3. Let the call finish naturally
4. Collect transcripts from /transcripts
5. Repeat for all 10 scenarios

BUG REPORT

A comprehensive bug report is included in this repository, detailing issues uncovered across all 10 test calls. The report covers:
- Identity and verification inconsistencies
- Scheduling and availability logic failures
- Hallucinated workflows and internal data
- Safety and clinical boundary concerns
- Insurance and policy handling issues
- Memory and context‑tracking problems
Each bug is clearly categorized, severity‑rated, and annotated with transcript numbers for fast reviewer navigation.