# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### 🎮 Game Purpose
Game Glitch Investigator is a number guessing game built with 
Python and Streamlit. The player picks a difficulty level, then 
tries to guess a secret number within a limited number of attempts. 
After each guess, the game gives a hint telling the player to go 
higher or lower. The player earns points for guessing correctly 
and loses points for wrong guesses. The game was intentionally 
shipped with bugs as a learning exercise — the goal is to find, 
diagnose, and fix the glitches using AI tools like Claude Code 
in VS Code.

---

### 🐛 Bugs Found

**Bug 1 — Hints pointed the player in the wrong direction (Logic Error)**
The `check_guess` function had swapped return messages. When a 
guess was too high, the game said "Go HIGHER" instead of "Go LOWER", 
making the game nearly unwinnable if the player trusted the hints.

**Bug 2 — Attempts counter started at 1 instead of 0 (Off-by-One Error)**
The session state initialized `attempts = 1`, so players lost one 
guess before they even started. On Normal difficulty, the game 
showed 7 attempts left instead of 8.

**Bug 3 — Hard mode range was easier than Normal (Logic Error)**
`get_range_for_difficulty` returned `(1, 50)` for Hard mode, which 
is a narrower range than Normal `(1, 100)`. Hard mode should be 
harder, not easier.

**Bug 4 — Wrong guesses could increase the score (Logic Error)**
The `update_score` function rewarded the player with +5 points on 
even-numbered wrong attempts due to an `attempt_number % 2 == 0` 
condition that made no logical sense.

**Bug 5 — New Game button did not fully reset the game (Logic Error)**
Clicking New Game only reset the secret number. The status, score, 
history, and attempts were left unchanged, freezing the player out 
of a new round.

**Bug 6 — String/int type switching every other attempt (Logic Error)**
The submit block converted the secret number to a string on even 
attempts, causing incorrect comparisons and unreliable hints every 
other guess.

---

### 🔧 Fixes Applied

**Fix 1 — Swapped hint messages in `check_guess`:**
Moved `check_guess` from `app.py` into `logic_utils.py` using 
Claude Code Agent Mode. Fixed the return messages so 
`guess > secret` returns "Go LOWER" and `guess < secret` returns 
"Go HIGHER". Verified with pytest and live gameplay.

**Fix 2 — Attempts counter initialized to 0:**
Changed `st.session_state.attempts = 1` to 
`st.session_state.attempts = 0` in `app.py`. The attempts left 
counter now correctly shows the full number of attempts at the 
start of each game.

**Fix 3 — Hard mode range corrected:**
Changed `return 1, 50` to `return 1, 200` in 
`get_range_for_difficulty`. This bug was caught automatically 
by the pytest test `test_hard_range_wider_than_normal` after 
Claude missed it during the initial refactor.

**Fix 4 — Score logic cleaned up:**
Removed the `attempt_number % 2 == 0` condition from 
`update_score`. Wrong guesses now always deduct 5 points 
regardless of attempt number.

**Fix 5 — New Game fully resets all state:**
Updated the New Game button handler to reset attempts, score, 
status, history, last_message, and input field. Also added 
difficulty change detection to reset everything when the player 
switches difficulty.

**Fix 6 — Removed string/int type switching:**
Deleted the buggy `if st.session_state.attempts % 2 == 0` block 
from the submit handler. The secret is now always compared as an 
integer. Also removed the now-unnecessary `try/except TypeError` 
block from `check_guess` in `logic_utils.py`.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
