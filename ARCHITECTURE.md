Architecture Document — Pretty Good AI Voice Bot

System Overview
This voice bot simulates a patient calling a medical office AI agent.
It uses Twilio Programmable Voice, Flask webhooks, and OpenAI to create a multi‑turn, realistic, testable phone conversation.
At a high level, the bot:
- Initiates an outbound call via Twilio
- Waits silently for the agent to speak first
- Receives the agent’s speech via Twilio <Gather input="speech">
- Logs the agent’s text
- Generates a patient response using GPT‑4o‑mini
- Speaks the response back to the agent
- Repeats this loop until the call ends
- Saves a full transcript for bug analysis

System Diagram
┌──────────────────────────────────────────────────────────────┐
│                        VOICE BOT SERVER                      │
│                         (Flask + Twilio)                     │
│                                                              │
│  ┌────────────────┐      ┌────────────────────────────────┐  │
│  │  /voice        │      │   /handle_agent (loop)         │  │
│  │  (listen first)│      │                                │  │
│  └────────────────┘      │  Twilio SpeechResult  ───────► │  │
│                          │                                │  │
│                          │        Agent text              │  │
│                          │                │               │  │
│                          │        GPT‑4o‑mini             │  │
│                          │                │               │  │
│                          │        Patient reply           │  │
│                          │                │               │  │
│                          │   Twilio <Say> (TTS) ────────► │  │
│                          └────────────────────────────────┘  │
│                                                              │
│                     Transcript Logging Layer                 │
│                     transcripts/Transcript n.txt             │
└──────────────────────────────────────────────────────────────┘


Key Design Choices
Why Twilio <Gather input="speech"> instead of Media Streams?
The challenge does not require real‑time audio streaming.
Twilio’s built‑in speech recognition is:
- simple
- reliable
- low‑latency
- requires no WebSocket server
- perfect for multi‑turn conversational testing
This keeps the architecture lightweight and easy to deploy.

Why Flask instead of FastAPI?
Flask is ideal for Twilio webhook‑based systems:
- synchronous request/response model matches Twilio’s expectations
- minimal boilerplate
- easy to run locally with ngrok
- perfect for a small, focused challenge project
Async WebSockets were unnecessary for this use case.

Why GPT‑4o‑mini for patient responses?
GPT‑4o‑mini is:
- fast
- inexpensive
- strong at conversational role‑play
- ideal for generating short, realistic patient replies
The patient persona does not require deep reasoning — it needs consistency, clarity, and natural tone.

Why OpenAI TTS via Twilio <Say> instead of custom audio synthesis?
Twilio’s <Say> uses high‑quality built‑in TTS voices.
This avoids:
- generating audio files
- converting formats
- streaming PCM/mulaw
- managing audio buffers
It keeps the system simple and robust.

Why ngrok for development?
Twilio requires a public URL for:
- /voice
- /handle_agent
ngrok provides:
- instant HTTPS tunneling
- no deployment required
- easy debugging
Perfect for rapid iteration.

Scenario‑based testing approach
Each call begins with a scenario injected after the agent’s first turn.
This allows:
- realistic patient behavior
- targeted stress‑testing
- reproducible bug discovery
- easy expansion (just change SCENARIO_TEXT)

Component Responsibilities
| app.py - Flask server, Twilio webhook handling, conversation loop
| /voice - First contact listen silently for agent greeting
| /handle_agent - Multi‑turn loop: log → generate → speak → listen
| make_call.py - Outbound call initiation + call recording
| transcripts/  - Stores per‑call transcripts using CallSid
| SCENARIO_TEXT - Defines the patient scenario for each test call


Detailed Call Flow
1. Outbound Call Initiation
make_call.py uses Twilio’s REST API:
- to: Pretty Good AI test number
- from_: your Twilio number
- url: /voice
- record=True: enables call recording

2. Twilio hits /voice
The bot:
- does not speak
- returns a <Gather input="speech">
- waits for the agent’s greeting
This ensures natural call flow.

3. Agent speaks first
Twilio sends the recognized text to:
/handle_agent?turn=1

4. Scenario Injection (Turn 1 Only)
The bot:
- logs the agent’s greeting
- responds with the selected scenario
- speaks it via <Say>
- starts a new <Gather>

5. Multi‑Turn Loop (Turns 2+)
For each agent turn:
- Twilio sends SpeechResult
- Bot logs it
- Bot sends it to GPT‑4o‑mini
- GPT generates a patient reply
- Bot logs the reply
- Bot speaks it
- Bot listens again
This continues until the agent ends the call or escalates.

6. Transcript Logging
Each call is saved as:
transcripts/Transcript n    .txt


Format:
AGENT: ...
PATIENT: ...
AGENT: ...
PATIENT: ...

Used for bug analysis and submission.


Limitations
- No real scheduling backend
- No real insurance verification
- No real medical record access
- OpenAI responses may vary slightly
- Twilio STT may mis-transcribe medical terms
These limitations are acceptable for the challenge.

Conclusion
This architecture provides:
- a stable telephony bot
- realistic patient simulation
- clean transcripts
- a simple, maintainable codebase
- a strong foundation for evaluating the Pretty Good AI agent
It meets all challenge requirements and is optimized for clarity, reliability, and ease of review.