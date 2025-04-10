import streamlit as st

# --- Redirect if not logged in ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in first.")
    st.stop()

st.set_page_config(page_title="Instructions", layout="centered")

st.title("📝 Code Hunt - Instructions")

# --- Rulebook Styling ---
st.markdown("---")
st.markdown("### 📘 RULEBOOK")

st.markdown("#### 1. GENERAL GUIDELINES")
st.markdown("##### 1.1 Participation Guidelines")
st.markdown("""
- This is an individual event. No teams are allowed.  
- Registration must be completed before the deadline with valid student identification.  
- The event will be conducted in hybrid mode. Participants must be present at the venue.  
- Participants must behave respectfully with peers, volunteers, and organizers.  
""")

st.markdown("##### 1.2 Eligibility")
st.markdown("""
- Only registered individuals may participate in the event.  
""")

st.markdown("##### 1.3 Code of Conduct")
st.markdown("""
- Maintain professionalism and integrity at all times.  
- Any form of misconduct, harassment, or disruption will result in disqualification.  
- Unfair practices or tampering with the event process is strictly prohibited.  
""")

st.markdown("#### 2. EVENT FORMAT")
st.markdown("**Round 1: Digital Quest**")
st.markdown("""
- Duration: 60 minutes  
- Format: Logical puzzles and multiple-choice questions focused on programming, tech knowledge, and reasoning  
- Participants with the highest scores will qualify for Round 2  
""")

st.markdown("**Round 2: The Cipher Hunt**")
st.markdown("""
- Duration: 2 to 3 hours  
- Format: A series of logic puzzles, ciphers, riddles, and code-cracking challenges  
- Participants will solve one clue after another in a progressive format  
- This round tests logical thinking, attention to detail, and time management  
""")

st.markdown("#### 3. DOs AND DON’Ts")
st.markdown("**✅ DOs**")
st.markdown("""
- Follow the instructions and structure of both rounds  
- Maintain ethical behaviour and honesty  
- Listen to all announcements made by the organizing team  
""")

st.markdown("**❌ DON’Ts**")
st.markdown("""
- Do not use mobile phones, smart devices, or the internet unless permitted  
- Do not copy or plagiarize any answers or solutions  
- Avoid use of AI-generated content unless permitted and fully understood  
- Do not attempt to disrupt or interfere with the event setup or process  
- Do not ignore instructions or feedback from organizers or volunteers  
""")

st.markdown("#### 4. EVALUATION CRITERIA")
st.markdown("""
Participants will be evaluated on:  
- **Round 1**: Accuracy and time taken to solve the puzzles and MCQ questions  
- **Round 2**:  
    - Logical reasoning and problem-solving approach  
    - Correctness of solutions  
""")

st.markdown("#### 5. DISQUALIFICATION CRITERIA")
st.markdown("""
Disqualification will occur if a participant:  
- Uses unauthorized devices or resources  
- Behaves unethically or disrupts the event  
- Fails to follow instructions or meet submission requirements  
""")

st.markdown("#### 6. EVENT ETIQUETTE & FINAL NOTES")
st.markdown("""
- Participants must follow all instructions given by organizers and volunteers  
- Maintain discipline and avoid causing disturbances during rounds  
- The organizing team reserves the right to alter or adjust the event format if required  
""")

st.markdown("*By registering, participants agree to comply with all rules and conditions outlined in this rulebook.*")

st.markdown("---")

# --- Start Quiz Button ---
if st.button("✅ I have read the instructions. Start Quiz"):
    year = st.session_state.get("year")
    if year == "1st Year":
        st.switch_page("pages/Quiz_1st.py")
    elif year == "2nd Year":
        st.switch_page("pages/Quiz_2nd.py")
    elif year == "3rd Year":
        st.switch_page("pages/Quiz_3rd.py")
    else:
        st.error("Year not selected. Please login again.")
