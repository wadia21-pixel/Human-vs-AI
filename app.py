import json
import os
import random
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).parent
DATA_FILE = APP_DIR / "leaderboard.json"

st.set_page_config(
    page_title="Human Intelligence vs Artificial Intelligence",
    page_icon="🩵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# These are original demonstration scenarios and paired responses.
# "AI" is a stylistic label for the game, not a claim about actual authorship.
QUESTIONS = [
    {
        "scenario": "Your best friend has been unusually quiet all week. When you ask what's wrong, they say, “I'm fine,” but you can tell they're hurting.",
        "responses": [
            {
                "label": "Response A",
                "text": "You don't have to explain everything right now. I can sit with you, even if we don't talk. And if you want to tell me later, I'm here. You don't have to carry it all alone.",
                "kind": "human",
            },
            {
                "label": "Response B",
                "text": "It may be helpful to communicate your feelings with someone you trust. Consider taking time for self-care and seeking support if the situation continues.",
                "kind": "ai",
            },
        ],
    },
    {
        "scenario": "A student studies hard for an important exam but receives a much lower mark than expected. They tell you, “Maybe I'm just not good enough.”",
        "responses": [
            {
                "label": "Response A",
                "text": "One exam can't decide what you're capable of. I know it hurts when you worked so hard and didn't get what you hoped for. Take tonight to breathe. Tomorrow, we'll figure out what went wrong together.",
                "kind": "human",
            },
            {
                "label": "Response B",
                "text": "A disappointing result does not necessarily reflect your overall ability. You can review your mistakes, identify areas for improvement, and develop a structured study plan for future assessments.",
                "kind": "ai",
            },
        ],
    },
    {
        "scenario": "Someone's beloved pet has died. They say, “The house feels so empty without them.”",
        "responses": [
            {
                "label": "Response A",
                "text": "I'm so sorry. It's strange how a little life can fill every corner of a home, isn't it? You'll probably keep expecting to hear their paws or see them in their usual spot. I wish I could make this hurt less.",
                "kind": "human",
            },
            {
                "label": "Response B",
                "text": "Losing a pet can be a significant emotional experience. Maintaining a routine, preserving meaningful memories, and talking with supportive people may help you cope with the grief.",
                "kind": "ai",
            },
        ],
    },
    {
        "scenario": "A person feels left out after seeing their friends spend time together without inviting them. They ask, “Am I that easy to forget?”",
        "responses": [
            {
                "label": "Response A",
                "text": "Ouch. I can see why that would sting, especially when it's people you care about. Please don't turn their invitation into a measure of your worth. You deserve friendships where you feel wanted, not like you have to beg for a place.",
                "kind": "human",
            },
            {
                "label": "Response B",
                "text": "Being excluded can lead to feelings of rejection. It may be useful to discuss your concerns with your friends and consider whether these relationships are meeting your social and emotional needs.",
                "kind": "ai",
            },
        ],
    },
    {
        "scenario": "A family member is overwhelmed by expectations and says, “I'm tired of trying to make everyone proud.”",
        "responses": [
            {
                "label": "Response A",
                "text": "Then you can rest for a minute. You don't have to earn love by being perfect, and you don't have to keep proving yourself every single day. I'm proud of you for making it this far, even if nobody has said it lately.",
                "kind": "human",
            },
            {
                "label": "Response B",
                "text": "Constant pressure to meet expectations can contribute to stress. Setting realistic goals, communicating boundaries, and balancing responsibilities with rest may help improve your well-being.",
                "kind": "ai",
            },
        ],
    },
]


def load_leaderboard():
    try:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        pass
    return []


def save_result(username, human_score, ai_score, correct):
    entries = load_leaderboard()
    entries.append({
        "username": username,
        "human_score": human_score,
        "ai_score": ai_score,
        "correct": correct,
        "total": len(QUESTIONS),
        "finished_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    entries.sort(key=lambda x: (x.get("human_score", 0), x.get("correct", 0)), reverse=True)
    try:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(entries[:100], f, indent=2, ensure_ascii=False)
    except OSError:
        st.warning("Your score couldn't be saved to the leaderboard. Check folder permissions.")


def start_game(username):
    order = list(range(len(QUESTIONS)))
    random.shuffle(order)
    st.session_state.game = {
        "username": username.strip(),
        "order": order,
        "index": 0,
        "human_score": 0,
        "ai_score": 0,
        "correct": 0,
        "answers": [],
        "question_started": time.time(),
        "finished": False,
        "saved": False,
    }
    st.session_state.page = "game"


def finish_game():
    game = st.session_state.game
    game["finished"] = True
    if not game["saved"]:
        save_result(game["username"], game["human_score"], game["ai_score"], game["correct"])
        game["saved"] = True
    st.session_state.page = "results"


def next_question():
    game = st.session_state.game
    game["index"] += 1
    if game["index"] >= len(QUESTIONS):
        finish_game()
    else:
        game["question_started"] = time.time()


def answer_question(choice_kind):
    game = st.session_state.game
    q_index = game["order"][game["index"]]
    question = QUESTIONS[q_index]
    chosen = next(r for r in question["responses"] if r["label"] == choice_kind)
    correct = chosen["kind"] == "ai"
    if correct:
        game["human_score"] += 1
        game["correct"] += 1
    else:
        game["ai_score"] += 1
    game["answers"].append({
        "scenario": question["scenario"],
        "chosen": chosen["label"],
        "correct": correct,
        "ai_response": next(r["label"] for r in question["responses"] if r["kind"] == "ai"),
    })
    next_question()


# ---- Styling ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
.stApp { background: linear-gradient(180deg, #eff8ff 0%, #f7fbff 55%, #f1f8f4 100%); }
.block-container { max-width: 850px; padding-top: 2rem; padding-bottom: 3rem; }
.hero {
  background: linear-gradient(135deg, #d8efff, #e1f2e8);
  border: 1px solid #c7e5f3; border-radius: 26px; padding: 28px 26px;
  text-align: center; box-shadow: 0 10px 28px rgba(80, 140, 180, .10);
}
.hero h1 { color: #234e70; font-size: clamp(1.8rem, 4vw, 2.7rem); line-height: 1.12; margin: 0.2rem 0 0.7rem; }
.hero p { color: #42647c; font-size: 1.05rem; margin-bottom: .2rem; }
.pill { display: inline-block; background: #fff; color: #49748f; border-radius: 999px; padding: 5px 12px; font-size: .82rem; font-weight: 800; }
.info-card {
  background: rgba(255,255,255,.92); border: 1px solid #d8eaf4; border-radius: 20px;
  padding: 19px 21px; margin: 12px 0; box-shadow: 0 5px 18px rgba(80, 140, 180, .06);
}
.scenario { background: #e9f5ff; border-left: 5px solid #76b8e2; border-radius: 15px; padding: 18px; color: #244d6a; font-size: 1.05rem; }
.response {
  background: #fff; border: 1px solid #d9e9f2; border-radius: 17px; padding: 17px 18px;
  min-height: 135px; color: #36566b; line-height: 1.65;
}
.small-muted { color: #688296; font-size: .9rem; }
.score-card { background: white; border: 1px solid #d7e9f2; border-radius: 18px; padding: 17px; text-align:center; }
.score-number { font-size: 2rem; color: #2c709b; font-weight: 900; }
div.stButton > button {
  border-radius: 13px; border: 1px solid #b9d9e9; min-height: 2.8rem;
  font-weight: 800; color: #285a78; background: #e2f2fc;
}
div.stButton > button:hover { border-color: #79b8dc; color: #204e6b; background: #d2eafb; }
div[data-testid="stFormSubmitButton"] button {
  border-radius: 13px; background: #cde8d9; border: 1px solid #a8d4bd; color: #285e45; font-weight: 900;
}
hr { border-color: #d7e8f0; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"
if "game" not in st.session_state:
    st.session_state.game = None

st.markdown("""
<div class="hero">
  <div class="pill">🩵 THINK • FEEL • GUESS</div>
  <h1>Human Intelligence<br>vs Artificial Intelligence</h1>
  <p>Can you spot the response that sounds like AI?</p>
</div>
""", unsafe_allow_html=True)
st.write("")

# ---- Home / rules / login ----
if st.session_state.page == "home":
    st.markdown("### 🌷 How to play")
    st.markdown("""
    <div class="info-card">
      <b>01 · Read the scenario</b><br>Each round presents an emotional, real-life situation.
      <hr>
      <b>02 · Compare two responses</b><br>One is written in a more personal, emotionally expressive style; the other uses a more generalized, AI-like style.
      <hr>
      <b>03 · Find the AI-style response</b><br>Choose Response A or Response B before the timer runs out.
      <hr>
      <b>04 · Score points</b><br>If you identify the AI-style response, <b>Human Intelligence gets 1 point</b>. If you miss it, <b>Artificial Intelligence gets 1 point</b>.
      <hr>
      <b>05 · Finish all five rounds</b><br>Your results and your place on the leaderboard will appear at the end.
    </div>
    """, unsafe_allow_html=True)
    st.caption("⏱️ Each question has 30 seconds. The game uses sample responses and does not verify actual authorship.")
    st.markdown("### ✨ Player login")
    with st.form("login_form"):
        username = st.text_input("Choose a player name", max_chars=24, placeholder="e.g. BlueStar")
        agreed = st.checkbox("I understand the rules and I'm ready to play.")
        submitted = st.form_submit_button("Start the challenge 🩵", use_container_width=True)
    if submitted:
        clean_name = username.strip()
        if not clean_name:
            st.error("Please enter a player name first.")
        elif not agreed:
            st.error("Please confirm that you've read the rules.")
        else:
            start_game(clean_name)
            st.rerun()

    st.markdown("---")
    st.markdown("### 🏆 Leaderboard")
    leaderboard = load_leaderboard()
    if leaderboard:
        for i, row in enumerate(leaderboard[:10], start=1):
            st.markdown(
                f"**{i}. {row.get('username','Player')}** — "
                f"Human {row.get('human_score', 0)} : {row.get('ai_score', 0)} AI "
                f"<span class='small-muted'> · {row.get('correct', 0)}/5 correct</span>",
                unsafe_allow_html=True,
            )
    else:
        st.info("No scores yet. Be the first to claim the top spot!")
    st.caption("Leaderboard scores are stored in leaderboard.json on the computer running this app.")

# ---- Game ----
elif st.session_state.page == "game" and st.session_state.game:
    game = st.session_state.game
    idx = game["index"]
    q = QUESTIONS[game["order"][idx]]
    total = len(QUESTIONS)
    elapsed = time.time() - game["question_started"]
    remaining = max(0, 30 - int(elapsed))
    st.progress((idx) / total, text=f"Round {idx + 1} of {total}")
    c1, c2, c3 = st.columns(3)
    c1.metric("🧠 Human", game["human_score"])
    c2.metric("🤖 AI", game["ai_score"])
    c3.metric("⏱️ Seconds left", remaining)
    st.markdown("### 💭 Read the scenario")
    st.markdown(f"<div class='scenario'>{q['scenario']}</div>", unsafe_allow_html=True)
    st.write("")
    st.markdown("### Which response sounds more like AI?")
    responses = q["responses"]
    if random.random() < -1:  # no-op: keep response order stable during reruns
        responses = list(reversed(responses))
    cols = st.columns(2)
    for col, response in zip(cols, responses):
        with col:
            st.markdown(f"**{response['label']}**")
            st.markdown(f"<div class='response'>{response['text']}</div>", unsafe_allow_html=True)
            if st.button(f"Choose {response['label']}", key=f"answer_{idx}_{response['label']}", use_container_width=True):
                answer_question(response["label"])
                st.rerun()

    if remaining <= 0:
        st.warning("Time's up! This round goes to Artificial Intelligence.")
        game["ai_score"] += 1
        game["answers"].append({
            "scenario": q["scenario"],
            "chosen": "No answer",
            "correct": False,
            "ai_response": next(r["label"] for r in q["responses"] if r["kind"] == "ai"),
        })
        next_question()
        st.rerun()
    else:
        # Refresh the countdown display.
        time.sleep(1)
        st.rerun()

# ---- Results ----
elif st.session_state.page == "results" and st.session_state.game:
    game = st.session_state.game
    st.markdown("## 🎉 Challenge complete!")
    st.markdown(f"Well played, **{game['username']}**. Here's how you did.")
    a, b, c = st.columns(3)
    with a:
        st.markdown(f"<div class='score-card'><div>🧠 Human</div><div class='score-number'>{game['human_score']}</div><div>/ 5 points</div></div>", unsafe_allow_html=True)
    with b:
        st.markdown(f"<div class='score-card'><div>🤖 AI</div><div class='score-number'>{game['ai_score']}</div><div>/ 5 points</div></div>", unsafe_allow_html=True)
    with c:
        st.markdown(f"<div class='score-card'><div>🎯 Correct</div><div class='score-number'>{game['correct']}</div><div>/ 5 guesses</div></div>", unsafe_allow_html=True)

    if game["human_score"] > game["ai_score"]:
        st.success("Human Intelligence wins this round! Your emotional radar was sharp. 🩵")
    elif game["ai_score"] > game["human_score"]:
        st.info("Artificial Intelligence wins this round! The AI-style responses fooled you this time.")
    else:
        st.warning("It's a tie! Human and Artificial Intelligence finish level.")

    st.markdown("### 🔎 Round review")
    for i, item in enumerate(game["answers"], start=1):
        mark = "✅" if item["correct"] else "❌"
        with st.expander(f"{mark} Round {i}: {'Correct guess' if item['correct'] else 'Missed it'}"):
            st.write(item["scenario"])
            st.write(f"**Your choice:** {item['chosen']}")
            st.write(f"**AI-style response:** {item['ai_response']}")
    st.caption("This game compares writing styles. Real human and AI writing can overlap, so the labels are illustrative rather than scientifically definitive.")

    st.markdown("### 🏆 Updated leaderboard")
    leaderboard = load_leaderboard()
    for i, row in enumerate(leaderboard[:10], start=1):
        st.write(f"{i}. **{row.get('username','Player')}** — Human {row.get('human_score', 0)} : {row.get('ai_score', 0)} AI")

    if st.button("Play again 🔄", use_container_width=True):
        st.session_state.game = None
        st.session_state.page = "home"
        st.rerun()
    if st.button("Back to start page", use_container_width=True):
        st.session_state.game = None
        st.session_state.page = "home"
        st.rerun()
