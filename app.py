import random
import streamlit as st
from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score



st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FIX: Track difficulty changes and reset everything when it changes
if "current_difficulty" not in st.session_state:
    st.session_state.current_difficulty = difficulty

if st.session_state.current_difficulty != difficulty:
    st.session_state.current_difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    # FIX: Clear old messages when switching difficulty
    if "last_message" in st.session_state:
        del st.session_state.last_message
    st.rerun()

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.input_key}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)
    
if new_game:
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.secret = random.randint(low, high)
    st.session_state.input_key += 1  # ← clears the input box

    # FIX: Clear last_message so old win/lose messages 
    # don't show on new game
    if "last_message" in st.session_state:
        del st.session_state.last_message
    st.rerun()

if st.session_state.status != "playing":
    # Show the final result message first
    if "last_message" in st.session_state:
        msg_type, msg_text = st.session_state.last_message
        if msg_type == "win":
            st.balloons()
            st.success(msg_text)
        elif msg_type == "lost":
            st.error(msg_text)
    # Then show the prompt to start a new game
    if st.session_state.status == "won":
        st.info("🎉 Start a new game to play again.")
    else:
        st.info("😞 Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.last_message = ("error", err)
    else:
        st.session_state.history.append(guess_int)
        secret = st.session_state.secret
        outcome, message = check_guess(guess_int, secret)

        # Store hint and outcome in session state so they 
        # persist after rerun
        st.session_state.last_message = ("hint", message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.session_state.last_message = (
                "win",
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.session_state.last_message = (
                "lost",
                f"Out of attempts! The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

    st.rerun()  # Force immediate refresh so display updates instantly

# Only show hints and errors during active gameplay
if "last_message" in st.session_state:
    msg_type, msg_text = st.session_state.last_message
    if msg_type == "error":
        st.error(msg_text)
    elif msg_type == "hint" and show_hint:
        st.warning(msg_text)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
