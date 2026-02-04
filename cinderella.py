import streamlit as st

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Cinderella Quiz",
    page_icon="https://upload.wikimedia.org/wikipedia/en/thumb/e/ef/Swiffer_logo.svg/250px-Swiffer_logo.svg.png",
    layout="wide"
)


# ------------------ SESSION STATE ------------------
if "started" not in st.session_state:
    st.session_state.started = False

if "current_step" not in st.session_state:
    st.session_state.current_step = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""

if "game_over" not in st.session_state:
    st.session_state.game_over = False


# ==================================================
# INTRO PAGE (WITH IMAGE)
# ==================================================
if not st.session_state.started:

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown("<div style='margin-top:-40px;'></div>", unsafe_allow_html=True)

        st.image("main-teaser.jpg", use_container_width=True)

        st.markdown("""
        <div style="text-align: center;">
            <h1>Cinderella Knowledge Quiz</h1>
            <p style="font-size:18px;">
                Test your knowledge and become a Cinderella expert!
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Start Quiz", use_container_width=True, type="primary"):
            st.session_state.started = True
            st.rerun()

    st.stop()


# ==================================================
# QUESTIONS
# ==================================================

questions = [

    "How many bottles are produced per month?",

    "How many variants do we currently produce?",

    "What are the colors of the variants?",

    "Where do we produce Cinderella?",

    "To which markets do we ship?",

    "What makes Cinderella special?",

    "Time between PC and SOP?",

    "Are you excited for Cinderella's launch?"
]


choices = [

    ["A: 800k", "B: 1000k", "C: 1200k", "D: 1400k"],

    ["A: 1", "B: 2", "C: 3", "D: 4"],

    ["A: Pink, Purple, Blue",
     "B: Purple, Green, Blue",
     "C: Pink, Green, Yellow",
     "D: Purple, Green, Red"],

    ["A: United Kingdom", "B: Netherlands", "C: Spain", "D: Italy"],

    ["A: UK", "B: FBNL", "C: Iberia", "D: All of the above"],

    [
        "A: First-of-its-kind shower cap for direct to floor application",
        "B: Redesigned formula for deeper stain removal",
        "C: Smart bottle with automatic dosage system",
        "D: Eco-friendly refillable packaging system"
    ],

    ["A: 18 Months", "B: 24 Months", "C: 8 Months", "D: 21 Months"],

    ["A: YES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 😊", "B: No 🙁", "C: Not sure 🤔", "D: I guess? 🤷‍♂️"]
]


correct_answers = ["A", "C", "C", "B", "A", "A", "C", "A"]


explanations = {

    "A1": "Correct! Production is 800k bottles per month.",

    "C2": "Correct! There are currently 3 variants.",

    "C3": "Correct! The colors are Pink, Green, and Yellow. + Orange to come in March!",

    "B4": "Correct! Cinderella is produced in the Netherlands.",

    "A5": "Correct! The only market (for now!) is the UK.",

    "A6": "Correct! The special shower cap enables direct to floor application.",

    "C7": "Correct! PC to SOP took ONLY 8 months!",

    "A8": "Correct! Enthusiasm is key 😄"
}


# ==================================================
# FUNCTIONS
# ==================================================
def check_answer(answer):

    idx = st.session_state.current_step
    correct = correct_answers[idx]

    key = f"{correct}{idx+1}"
    explanation = explanations.get(key, "Correct answer.")

    if answer == correct:
        st.session_state.score += 1
        st.session_state.last_feedback = f"✅ {explanation}"

    else:
        st.session_state.last_feedback = (
            f"❌ Wrong!\n\n"
            f"Correct answer: {correct}\n\n"
            f"{explanation}"
        )

    st.session_state.show_feedback = True


def next_question():

    st.session_state.show_feedback = False
    st.session_state.last_feedback = ""

    st.session_state.current_step += 1

    if st.session_state.current_step >= len(questions):
        st.session_state.game_over = True


def restart_game():

    st.session_state.started = False
    st.session_state.current_step = 0
    st.session_state.score = 0
    st.session_state.show_feedback = False
    st.session_state.last_feedback = ""
    st.session_state.game_over = False

    st.rerun()


# ==================================================
# MAIN QUIZ UI (NO IMAGES)
# ==================================================

# Centered layout
left, center, right = st.columns([1, 2, 1])

with center:

    st.title("Cinderella Knowledge Quiz")


    # ------------------ GAME OVER ------------------
    if st.session_state.game_over:

        total = len(questions)
        score = st.session_state.score

        st.success("🎉 Quiz Completed!")

        st.markdown(f"""
        ## 📊 Final Score

        **{score} / {total}**

        Accuracy: **{round(score/total*100,1)}%**
        """)

        if score == total:
            st.balloons()
            st.success("🎉 PERFECT SCORE! You are officially a Cinderella legend 👑✨")

        elif score >= total * 0.7:
            st.info("🔥 Great job! So close to Cinderella perfection… we’re impressed 😎👏 - rematch?")

        else:
            st.warning("😅 Not bad! Every Cinderella expert starts somewhere — rematch? 💪🚀")


        if st.button("🔁 Play Again"):
            restart_game()


    # ------------------ GAME ACTIVE ------------------
    else:

        q_idx = st.session_state.current_step

        st.subheader(f"Question {q_idx+1} / {len(questions)}")
        st.write(questions[q_idx])


        # ------------------ ANSWERS ------------------
        if not st.session_state.show_feedback:

            for option in choices[q_idx]:

                letter = option[0]

                if st.button(option, key=f"{q_idx}_{option}"):
                    check_answer(letter)
                    st.rerun()


        # ------------------ FEEDBACK ------------------
        else:

            if st.session_state.last_feedback.startswith("✅"):
                st.success(st.session_state.last_feedback)
            else:
                st.error(st.session_state.last_feedback)

            if st.button("➡️ Next Question"):
                next_question()
                st.rerun()


        # ------------------ PROGRESS ------------------
        st.markdown("---")

        progress = st.session_state.current_step / len(questions)
        st.progress(progress)

        st.markdown(f"**Score:** {st.session_state.score} / {len(questions)}")
