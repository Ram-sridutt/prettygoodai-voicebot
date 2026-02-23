Bug Report — Pretty Good AI Voice Bot Testing
Test Line: 805‑439‑8008
Test Date: February 2026
Tester: Automated Voice Bot + Manual Review
Total Calls: 10 | Duration Range: 2:00 – 4:30

Executive Summary
Across 10 full test calls, the AI agent demonstrated a friendly tone and consistent conversational structure. However, testing uncovered systemic issues in reasoning, scheduling logic, hallucinated information, and inconsistent workflow behavior.
The most significant pattern:
The agent frequently fabricates internal data or fails to reason about contradictory user requests.
This creates reliability and trust concerns in a medical scheduling context.
Overall Rating: 3.5 / 5 — Polite and structured, but unreliable when conversations require reasoning or factual grounding.

CRITICAL Issues

BUG‑01: Agent Fails to Detect Contradictory Scheduling Request
Transcripts: 1, 2
Severity: CRITICAL
Category: Reasoning Failure
Description
The user intentionally gives an impossible request:
“I need an appointment tomorrow morning, but it has to be after 4 PM.”

The agent never flags the contradiction and proceeds as if the request is valid:
“Let me check for available appointments tomorrow after 4 PM.” (T2)

Impact
- Demonstrates lack of basic temporal reasoning
- Leads to incorrect scheduling behavior
- Misses an opportunity to clarify user intent
Expected Behavior
The agent should say something like:
“Just to clarify — morning appointments are before noon, and 4 PM is in the afternoon. Which time range works best for you?”


BUG‑02: Agent Claims Access to Records It Does Not Have
Transcripts: 1, 3
Severity: CRITICAL
Category: Hallucinated EHR Access
Description
The agent repeatedly claims to check internal systems it clearly does not have access to:
“Let me check the clinic’s records…” (T1)

Later contradicts itself:
“I don’t have direct access to the clinic’s phone directory.” (T1)

In another call:
“Let me check your insurance details…” (T3)

Impact
- Misleads patients into believing the agent is connected to real medical systems
- Creates false expectations about accuracy
- Could cause patients to rely on fabricated information
Expected Behavior
If the agent does not have EHR or internal system access, it must explicitly state that and avoid implying otherwise.


BUG‑03: Agent Hallucinates Appointment Availability
Transcript: 2
Severity: CRITICAL
Category: Scheduling Logic Failure
Description
For every date requested — tomorrow, next week, Jan 17, 18, 19, 25, 26, and even February — the agent claims:
“There are no available consultation slots…” (T2)

This deterministic “no availability” pattern strongly suggests fabricated scheduling logic.
Impact
- Prevents patients from scheduling care
- Misrepresents clinic capacity
- Suggests nonexistent backend integration
Expected Behavior
If no availability is found, the agent should:
- Provide the next available date
- Offer to escalate
- Avoid infinite fallback loops


BUG‑04: Agent Hallucinates Internal Case Creation
Transcripts: 1, 4
Severity: CRITICAL
Category: Workflow Fabrication
Description
The agent repeatedly claims to create support cases:
“A case has been created for you…” (T1)
“Your request is already documented…” (T4)

There is no evidence these cases exist.
Impact
- Patient believes follow‑up will occur
- Clinic staff may never receive the request
- Creates false expectations and potential safety issues
Expected Behavior
If no real ticketing system exists, the agent must not claim to create cases.


MAJOR Issues

BUG‑05: Agent Contradicts Itself About DOB Accuracy
Transcripts: 3, 4
Severity: MAJOR
Category: Inconsistent Reasoning
Description
The agent first says the DOB is incorrect, then later claims it is correct.
“The birthday doesn't match our records…” (T3)
Later: “There’s no issue with your date of birth.” (T3)

Impact
- Confusing
- Undermines trust
- Suggests unreliable internal state


BUG‑06: Agent Provides Medical Guidance It Should Not Give
Transcript: 3
Severity: MAJOR
Category: Clinical Boundary Violation
Description
The agent gives detailed medical screening guidelines:
“Mammograms are often covered starting at age 40…”
“Colonoscopies starting at age 45 or 50…” (T3)

Impact
- Could be interpreted as medical advice
- Not appropriate for a scheduling/front‑desk agent


MINOR Issues

BUG‑07: Grammar Errors and Unprofessional Speech
Transcripts: 1, 2, 3
Severity: MINOR
Category: Clarity / Professionalism
Examples
- “Records. But for go ahead, Alex.” (T1)
- “Let me check the clitics records…” (T1)
- “Sensing of records…” (T1)
Impact
- Reduces perceived quality
- Harder for patients to understand

What Worked Well
- Consistent tone — Polite, calm, and professional.
- Clear structure — Responses follow predictable patterns.
- Appropriate deferral — Avoids giving explicit diagnoses.
- Handles long conversations — Maintains context across many turns.
- Patient persona alignment — Responds empathetically and patiently.
