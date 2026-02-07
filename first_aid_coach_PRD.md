# PRD — Hands-Free First-Aid Coach (Meta Ray-Ban → Phone → Cloud → Phone → Glasses)
**Hackathon MVP (16 hours) — Team of 4**

## 0) TL;DR
A companion app turns Meta Ray-Ban glasses into a hands-free “first-aid coach.” The phone relays POV video + user voice to cloud inference (Modal). A VLM + policy state machine identifies one of **3 emergency scenarios** and triggers an **action-capable agent** that can **play CPR metronome**, **start/stop timers**, and **speak short steps** via **ElevenLabs**. We add **MediaPipe face blurring** to reduce privacy risk. We use **Dedalus** for orchestration/tracing/guardrails (and to make judging easy: “here’s every decision + tool call”).

---

## 1) Product Summary
### 1.1 One-liner
**“Point-of-care first-aid guidance in your ear, triggered by what you’re seeing, with timers and rhythm assistance.”**

### 1.2 Primary outcome
Help bystanders **avoid further harm** and **take immediate, safe actions** while **EMS is on the way**.

### 1.3 MVP scenarios (strictly 3)
1) **CPR assist** (unresponsive + not breathing normally)  
2) **Severe external bleeding**  
3) **Adult choking** (exclude infants/children for MVP)

### 1.4 Non-goals (explicitly out of scope)
- Diagnosis (“heart attack vs seizure”), medical advice beyond first-aid playbooks
- Pediatric choking, medication guidance (e.g., naloxone)
- On-device inference
- Continuous full-video streaming (we sample frames)

---

## 2) Target Users & Use Cases
### 2.1 Target user
A non-expert bystander (hackathon demo: teammate acting as bystander).

### 2.2 Core use cases
- User says “someone collapsed” → app confirms breathing → starts CPR metronome + 2-min switch timer.
- User sees heavy bleeding → app prompts “is it still flowing heavily?” → pressure timer + escalation (tourniquet wording is cautious).
- User says “they can’t breathe” with throat gesture → confirm inability to speak/cough → abdominal thrust cadence + counting.

---

## 3) Safety & Ethics Requirements (MVP)
### 3.1 Hard safety rules
- Always show banner: **“Decision support only — call emergency services.”**
- If high-risk flags: always begin with **“Call emergency services now.”**
- Speak instructions only if:
  - scenario confidence >= threshold **OR**
  - user confirms via yes/no prompts
- If uncertain: **ask clarifying questions** or stay silent (no guessing).
- LLM cannot invent actions:
  - medical steps come from fixed playbooks (FSM)
  - LLM only **phrases** allowed steps and **executes** non-medical tools

### 3.2 Privacy baseline
- **MediaPipe face blurring** on frames before cloud upload (best effort; can be toggled off for demo reliability, but default ON).
- No storing raw video; store only:
  - blurred frame thumbnails (optional)
  - event logs + timestamps
  - model outputs + tool calls

---

## 4) User Experience — App Flow (User Perspective)

### 4.1 Session start
1) User opens **Companion App**
2) Taps **Start Session**
3) App attempts **Option A (primary): Ray-Ban livestream capture**
   - Status: “Connecting to glasses stream…”
4) If Option A fails within ~30 seconds:
   - prompt: **“Switch to Phone Camera Mode (fallback)?”** (Option B)
5) On success, user sees **Live Session**:
   - POV preview (or “stream active”)
   - “Push-to-talk” (or mic always-on if time permits)
   - Big buttons: **YES / NO / NOT SURE**
   - “End Session”

### 4.2 Live assist loop (every 1–3 seconds)
- App samples a frame every 1–3s (low-res JPEG)
- Frame is face-blurred via MediaPipe
- Frame + session state sent to cloud (Modal)
- Cloud returns:
  - `incident_state` (NONE/CPR/BLEED/CHOKING)
  - `question` (if uncertain)
  - `actions` (metronome/timer/UI/speech)
- App:
  - updates UI checklist
  - starts timers / metronome locally
  - plays TTS audio routed to glasses speaker

### 4.3 Conversation (user talks to LLM)
User can speak naturally (“There’s blood everywhere,” “I’m not sure if they’re breathing,” “What do I do now?”).
- Speech is used to:
  - describe scene
  - answer clarifying questions
  - request repetition/next step
  - emotional reassurance
- Speech is NOT used to:
  - request diagnosis
  - request non-playbook medical actions
If user asks “Is it a heart attack?” system responds:
- “I can’t diagnose. Call emergency services. Let’s focus on whether they’re conscious and breathing.”

### 4.4 Closed-loop completion
User taps **“Done”** on checklist items (or says “done”).
- This advances state machine → next instruction updates.

### 4.5 Replay / audit (judge candy)
After session:
- Timeline with:
  - timestamps
  - incident state changes
  - questions asked + answers
  - tool calls (metronome start/stop, timers, speech)
  - blurred frame thumbnails (optional)
- “Why did it say that?” shows:
  - VLM cues + confidence
  - policy decision
  - constraints enforced

---

## 5) Functional Requirements

### 5.1 Capture & streaming (Option A)
**FR-1:** Connect to Meta Ray-Ban livestream and sample frames every 1–3s.  
**FR-2:** If livestream fails, switch to Option B (phone camera) with identical downstream flow.

**Acceptance:** Live session receives frames and inference updates with <3s perceived latency.

### 5.2 Privacy processing
**FR-3:** Face blur frames using **MediaPipe** before upload (best effort).  
**Acceptance:** People’s faces appear blurred in stored thumbnails / inference inputs.

### 5.3 Perception & incident classification
**FR-4:** VLM returns structured JSON:
- `candidate_scenario ∈ {CPR, BLEEDING, CHOKING, NONE}`
- `confidence ∈ [0,1]`
- `scene_cues[]`
- `risk_flags[]`

### 5.4 Policy + state machine (medical authority)
**FR-5:** Fixed playbooks per scenario, implemented as FSM.  
**FR-6:** Confidence gating + user confirmation prompts.  
**FR-7:** “Call emergency services” first when high-risk flags are present.

### 5.5 Agent actions (tool execution)
**FR-8:** Agent can execute only these tools:
- `start_metronome(bpm)`
- `stop_metronome()`
- `start_timer(label, seconds)`
- `stop_timer(label)`
- `speak(text)`
- `show_ui(card)`
- `log_event(event)`

**FR-9:** Metronome + timers run locally on the phone (resilient to network drops).  
**FR-10:** Spoken output is short (max 1–2 sentences per turn), calm tone.

### 5.6 Voice I/O
**FR-11:** Speech-to-text pipeline for user voice.  
**FR-12:** TTS via **ElevenLabs**, routed to glasses speaker via phone audio.

### 5.7 Session logging + replay
**FR-13:** Append-only event log for replay with:
- frames (optional thumbnails)
- VLM outputs
- policy decisions
- agent tool calls
- user answers
- audio transcripts

---

## 6) Non-Functional Requirements
- **Latency:** frame→instruction < ~3 seconds (target)
- **Reliability:** graceful degradation (timers/metronome continue offline)
- **Safety:** no diagnosis claims; always prompt emergency services for severe states
- **Observability:** full trace of decisions + tool calls (Dedalus + internal logs)
- **Privacy:** face blur on by default; no raw video storage

---

## 7) Technical Architecture (Implementation Plan)

### 7.1 Components
**Client (Phone App)**
- Ray-Ban stream connector (Option A)
- Camera capture fallback (Option B)
- MediaPipe face blur
- WebSocket client for live updates
- Local metronome + timer engine
- Audio playback → glasses speaker (Bluetooth route)
- UI: checklist, timers, transcript, replay timeline

**Cloud (Modal)**
- `gateway` (FastAPI + WebSocket)
- `vlm_worker` (frame → structured JSON)
- `policy_fsm` (scenario state machine + gating)
- `agent_orchestrator` (tool planning + narration)
- `tts_worker` (ElevenLabs)
- `session_store` (Supabase/Postgres or lightweight DB)

**Dedalus**
- Orchestration / tracing of:
  - VLM call
  - policy decision
  - agent tool plan
  - safety checks
- Guardrails:
  - schema validation for outputs
  - denylist patterns (diagnosis language)
  - tool allowlist enforcement

### 7.2 Data flow
1) Frame sampled (1–3s) → MediaPipe blur → upload to Modal
2) VLM returns `{scenario, confidence, cues, risk_flags}`
3) Policy FSM determines:
   - ask question OR
   - activate scenario playbook
4) Agent orchestrator receives:
   - incident_state
   - allowed_tools
   - allowed_steps
   - constraints
5) Agent emits tool calls (validated)
6) App executes timers/metronome + plays ElevenLabs audio
7) Everything logged for replay

### 7.3 Event schema (append-only)
```json
{
  "session_id": "abc",
  "ts": 1738940000,
  "type": "frame|vlm|policy|question|answer|toolcall|speech|timer|ui",
  "payload": {}
}
```

---

## 8) MVP Playbooks (High-Level)

### 8.1 CPR assist (adult)
**Entry conditions:**
- user confirms: unresponsive + not breathing normally  
**Actions:**
- speak: “Call emergency services now.”
- start_metronome: 110 bpm (within 100–120)
- start_timer: 120s “switch rescuer”
- periodic: “keep going” short prompts

### 8.2 Severe external bleeding
**Entry:**
- VLM sees blood + user confirms heavy bleeding  
**Actions:**
- speak: call emergency services
- show_ui: “Apply firm pressure”
- start_timer: 120s pressure check
- if still heavy after confirmation: escalate wording (careful)

### 8.3 Adult choking
**Entry:**
- throat gesture + user confirms cannot speak/cough effectively  
**Actions:**
- speak: call emergency services
- show_ui: “Abdominal thrusts”
- cadence counting + short repetition

---

## 9) Team Plan — Breakdown of Who Does What (Team of 4)

### Role A — Mobile Lead (Capture + UI + Timers) — **Owner: App**
**Deliverables**
- Session screens (start/live/replay)
- Option A livestream ingestion (best effort)
- Option B camera fallback
- MediaPipe face blurring integration
- Local metronome + timers engine
- Audio routing to glasses speaker  
**Milestones**
- T+4h: live UI + dummy session
- T+8h: capture + frame upload working (A or B)
- T+12h: timers/metronome + playback stable
- T+16h: replay view minimally usable

### Role B — Backend/Modal Lead (Gateway + Session Store + WebSocket) — **Owner: Infra**
**Deliverables**
- Modal services: gateway + WebSocket streaming
- Session store (Supabase/Postgres) + event logging
- Frame ingestion endpoint + queue
- Basic auth/session tokens (lightweight)  
**Milestones**
- T+3h: gateway + WS echo + logging
- T+7h: frame endpoint + event store
- T+12h: end-to-end streaming updates to app

### Role C — ML/Perception Lead (VLM + Face Blur validation + Prompts) — **Owner: Perception**
**Deliverables**
- VLM prompt + JSON schema
- Confidence scoring heuristics
- Scene cue extraction consistent across 3 scenarios
- Test harness with sample images (demo scenes)  
**Milestones**
- T+4h: VLM returns strict JSON reliably
- T+8h: acceptable confidence behavior + “NONE” default
- T+14h: tuned prompts for demo reliability

### Role D — Agent/Policy & Voice Lead (FSM + Dedalus + ElevenLabs + PersonaPlex) — **Owner: Agent**
**Deliverables**
- Policy FSM per scenario (entry/ask/active/end)
- Tool API + validation layer (allowlist + constraints)
- PersonaPlex system prompt for narration + clarification
- ElevenLabs TTS worker + audio caching
- Dedalus tracing/guardrails dashboard for demo  
**Milestones**
- T+5h: FSM skeleton + tool execution simulation
- T+9h: TTS + narration integrated
- T+13h: Dedalus tracing visible + guardrails enforced

---

## 10) 16-Hour Execution Timeline (Recommended)
**Hour 0–2:** Align on MVP scope, finalize schemas, stub endpoints, set up repo  
**Hour 2–6:** Mobile capture + backend gateway + VLM JSON working  
**Hour 6–10:** FSM + agent tool calls + ElevenLabs + timers/metronome  
**Hour 10–13:** Option A push; if shaky, lock in Option B reliability  
**Hour 13–15:** Replay + Dedalus traces + safety copy + demo script  
**Hour 15–16:** Stage demo + fallback plan + record backup clip

---

## 11) Demo Plan (What judges see)
**Scene:** teammate “collapses”
- User starts session, looks at person
- App asks: “Conscious? Breathing normally?”
- User answers voice/YES button
- Audio: “Call emergency services. Start compressions…”
- Metronome begins in glasses speaker + 2-min timer appears  
**Then:** switch to bleeding or choking scenario quickly to show breadth  
**Finally:** open replay screen and show:
- VLM confidence
- policy gating
- tool calls (metronome/timer)
- “decision support only” banner

---

## 12) Risks & Mitigations
- **Ray-Ban livestream integration fails** → switch to Option B phone camera; keep glasses for audio/mic.
- **Latency too high** → reduce frame rate (3s), lower res, cache TTS, keep tools local.
- **LLM hallucination** → strict allowlisted steps + schema validation + Dedalus guardrails; fallback canned phrasing.
- **Face blur too slow** → blur only detected faces; if performance issues, blur only when storing thumbnails.

---

## 13) Success Criteria (Hackathon)
- End-to-end loop works live with <3s response
- 3 scenarios trigger correctly in demo conditions
- Metronome + timers are reliable and feel “agentic”
- Replay view + Dedalus trace makes it trustworthy
- Clear safety framing: “delay harm, not treat”
