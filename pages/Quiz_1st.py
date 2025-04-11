import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- CONFIG ---
st.set_page_config(page_title="Code Hunt Quiz", layout="wide")
EXCEL_FILE = "login_data1.xlsx"

# --- LIGHT / DARK THEME ---
theme_toggle = st.sidebar.toggle("Dark Theme", value=True)
theme_mode = "dark" if theme_toggle else "light"

# --- THEMING STYLES ---
if theme_mode == "dark":
    primary_color = "#00ff88"
    bg_color = "#111111"
    question_bg = "#1a1a1a"
    text_color = "white"
else:
    primary_color = "#0080ff"
    bg_color = "#ffffff"
    question_bg = "#f1f1f1"
    text_color = "#111111"

st.markdown(f"""
<style>
    body {{ background-color: {bg_color}; color: {text_color}; }}
    .question-box {{
        background-color: {question_bg};
        color: {text_color};
        padding: 25px;
        border-radius: 15px;
        animation: fadeIn 0.4s ease-in-out;
        margin-bottom: 20px;
    }}
    .timer-box {{
        background-color: #000000;
        color: {primary_color};
        font-size: 16px;
        font-weight: bold;
        padding: 6px 14px;
        border-radius: 8px;
        margin-bottom: 5px;
        display: inline-block;
        animation: pulse 1s infinite alternate;
    }}
    @keyframes pulse {{
        0% {{box-shadow: 0 0 10px {primary_color};}}
        100% {{box-shadow: 0 0 20px {primary_color};}}
    }}
</style>
""", unsafe_allow_html=True)

# --- QUESTIONS ---
all_questions = [
    {"question": "Which keyword is used to define a function in Python?", "options": ["func", "def", "function", "lambda"], "answer": "def"},
    {"question": "HTML stands for?", "options": ["HyperText Markup Language", "HighText Machine Language", "HyperTool Markup Language", "None"], "answer": "HyperText Markup Language"},
    {"question": "What is the capital of India?", "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"], "answer": "Delhi"},
    {"question": "2 + 2 * 2 = ?", "options": ["6", "8", "4", "10"], "answer": "6"},
    {"question": "Which company owns Android?", "options": ["Apple", "Microsoft", "Google", "IBM"], "answer": "Google"},
    {"question": "CSS is used for?", "options": ["Styling", "Logic", "Database", "Structure"], "answer": "Styling"},
    {"question": "What is 10^2?", "options": ["100", "20", "1000", "10"], "answer": "100"},
    {"question": "Which tag is used for bold text in HTML?", "options": ["<b>", "<stronger>", "<bold>", "<text-bold>"], "answer": "<b>"},
    {"question": "RAM is ___ memory?", "options": ["Volatile", "Non-volatile", "Permanent", "ROM"], "answer": "Volatile"},
    {"question": "Python is ___ typed language?", "options": ["Statically", "Dynamically", "Both", "None"], "answer": "Dynamically"}
]

# --- SESSION INIT ---
if "questions" not in st.session_state:
    st.session_state.questions = random.sample(all_questions, len(all_questions))
    for q in st.session_state.questions:
        random.shuffle(q["options"])
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.quiz_completed = False
    st.session_state.start_time = datetime.now()
    st.session_state.end_time = st.session_state.start_time + timedelta(hours=1)
    st.session_state.submitted_flag = False
    st.session_state.review_mode = False
    st.session_state.flags = set()
    st.session_state.username = "User"  # Replace with actual username if available
    st.session_state.logged_in = True

questions = st.session_state.questions

# --- LOGIN CHECK ---
if not st.session_state.get("logged_in", False):
    st.warning("Please login from the Home page.")
    st.stop()

# --- AUTOREFRESH TIMER ---
st_autorefresh(interval=1000, key="timer_refresh")

# --- TIME HANDLING ---
time_remaining = st.session_state.end_time - datetime.now()
if time_remaining.total_seconds() <= 0 and not st.session_state.quiz_completed:
    st.warning("⏰ Time's up! Auto-submitting...")
    st.session_state.quiz_completed = True
    if not st.session_state.submitted_flag:
        save_score_with_details(st.session_state.username, st.session_state.answers, questions)
        save_result_summary(st.session_state.username, st.session_state.answers, questions)
        st.success("⏱ Time expired. Quiz auto-submitted.")
        st.balloons()
        st.session_state.submitted_flag = True
    time_remaining = timedelta(seconds=0)

# --- SAVE HELPERS ---
def save_score_with_details(username, answers, questions):
    records = []
    for i, q in enumerate(questions):
        selected = answers.get(i, "Not Answered")
        correct = q["answer"]
        status = "Correct" if selected == correct else "Wrong"
        records.append({
            "Question": q["question"],
            "Selected Answer": selected,
            "Correct Answer": correct,
            "Result": status,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    df_user = pd.DataFrame(records)
    file_exists = os.path.exists(EXCEL_FILE)  
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a' if file_exists else 'w', if_sheet_exists='replace') as writer:
        df_user.to_excel(writer, sheet_name=username, index=False)

def save_result_summary(username, answers, questions):
    score = sum(1 for i, q in enumerate(questions) if answers.get(i) == q["answer"])
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    duration = str(datetime.now() - st.session_state.start_time).split('.')[0]
    new_entry = pd.DataFrame([{"Name": username, "Score": score, "Time": time, "Duration": duration}])
    try:
        existing = pd.read_excel(EXCEL_FILE, sheet_name="Results")
        updated = pd.concat([existing, new_entry], ignore_index=True)
    except:
        updated = new_entry
    file_exists = os.path.exists(EXCEL_FILE) with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a' if file_exists else 'w', if_sheet_exists='replace') as writer:
        updated.to_excel(writer, sheet_name="Results", index=False)

def save_draft_answer(q_index, question_text, selected_answer, username):
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=f"{username}_Draft")
    except:
        df = pd.DataFrame(columns=["Question Number", "Question", "Selected Answer", "Time"])

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([{
        "Question Number": q_index + 1,
        "Question": question_text,
        "Selected Answer": selected_answer,
        "Time": time_now
    }])

    df = df[df["Question Number"] != q_index + 1]
    df = pd.concat([df, new_entry], ignore_index=True)

    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=f"{username}_Draft", index=False)

top_cols = st.columns([2, 5, 2])

with top_cols[0]:
    st.markdown(
        f"<div style='background-color:{question_bg}; padding:6px 14px; border-radius:8px; color:{text_color}; font-weight:bold; font-size:16px;'>"
        f" Logged in as: <span style='color:{primary_color}'>{st.session_state.username}</span>"
        f"</div>", 
        unsafe_allow_html=True
    )

with top_cols[2]:
    st.markdown(f"<div class='timer-box'>⏱ {str(time_remaining).split('.')[0]}</div>", unsafe_allow_html=True)
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.experimental_rerun()

# --- PROGRESS BAR ---
answered_count = len([k for k in st.session_state.answers if st.session_state.answers[k] != ""])
progress = answered_count / len(questions)
st.progress(progress, text=f"Answered: {answered_count}/{len(questions)}")

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("### 🧭 Jump to Question")
cols = st.sidebar.columns(5)
for i in range(len(questions)):
    ans = i in st.session_state.answers
    flag = i in st.session_state.flags
    current = i == st.session_state.current_question
    emoji = "🚩" if flag else ("✅" if ans else "❌")
    label = f"{i+1:02}"
    style = f"font-weight:bold; color:{'white' if current else 'black'}; background-color:{'#ff7f50' if current else '#dddddd'}; border-radius:6px; padding:5px; text-align:center;"
    if cols[i % 5].button(f"{emoji} {label}", key=f"jump_{i}"):
        st.session_state.current_question = i

# --- FLAG TOGGLE ---
q_index = st.session_state.current_question
if q_index in st.session_state.flags:
    if st.sidebar.button("🚫 Unflag This Question"):
        st.session_state.flags.remove(q_index)
else:
    if st.sidebar.button("🚩 Flag This Question"):
        st.session_state.flags.add(q_index)

if st.sidebar.button("🔍 Show Unanswered"):
    unanswered = [str(i+1) for i in range(len(questions)) if i not in st.session_state.answers]
    st.sidebar.info("Unanswered: " + ", ".join(unanswered) if unanswered else "All answered ✅")

# --- MAIN / REVIEW ---
if not st.session_state.review_mode:
    q = questions[q_index]
    st.markdown(f"## Question {q_index + 1} of {len(questions)}")
    st.markdown(f"<div class='question-box'><b>{q['question']}</b></div>", unsafe_allow_html=True)

    prev_answer = st.session_state.answers.get(q_index)
    answer = st.radio("Your Answer:", q["options"],
        index=q["options"].index(prev_answer) if prev_answer in q["options"] else None,
        key=f"q{q_index}"
    )

    if answer and prev_answer != answer:
        st.session_state.answers[q_index] = answer
        save_draft_answer(q_index, q["question"], answer, st.session_state.username)

    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        nav = st.columns([1, 1])
        if nav[0].button("⬅️ Previous", use_container_width=True) and q_index > 0:
            st.session_state.current_question -= 1
        if q_index < len(questions) - 1:
            if nav[1].button("Next ➡️", use_container_width=True):
                st.session_state.current_question += 1
        else:
            if nav[1].button("Review ✅", use_container_width=True):
                st.session_state.review_mode = True
else:
    st.markdown("## 📝 Review Your Answers")
    for i, q in enumerate(questions):
        user_ans = st.session_state.answers.get(i, "Not Answered")
        st.markdown(f"**Q{i+1}: {q['question']}**")
        st.markdown(f"- Your Answer: `{user_ans}`")
    if st.button("Submit Quiz ✅"):
        if not st.session_state.submitted_flag:
            save_score_with_details(st.session_state.username, st.session_state.answers, questions)
            save_result_summary(st.session_state.username, st.session_state.answers, questions)
            st.success("🎉 Your quiz has been submitted successfully!")
            score = sum(1 for i, q in enumerate(questions) if st.session_state.answers.get(i) == q["answer"])
            if score == len(questions):
                st.snow()
            st.balloons()
            st.session_state.quiz_completed = True
            st.session_state.submitted_flag = True
