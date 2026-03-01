# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

🐛 Bug 1: Hints Point the Player in the Wrong Direction
While playing, I noticed something felt off after several wrong guesses. I kept following the hints but kept getting further from the secret number. After running out of attempts, I checked the secret number and realized the hints were completely backwards , when my guess was too high, the game told me "Go higher", when it was too low, it said "Go Lower". I played a second round to confirm it, and the same thing happened consisteny. This made the game nearly unwinnable if you trusted the hints.
Expected: If the guess is too high, the hint should tell the player to go lower, and vice versa.
What happened: The hint messages are swapped, then the game points the player in the wrong direction every single time.

🐛 Bug 2: Attempts Counter is Off : Player Loses a Guess Before Playing

Under Normal difficulty, the sidebar clearly states "Attempts allowed: 8." However, when the game loads, the attempts left already shows 7 before I even submitted a single guess. After playing through, I confirmed I only got 7 actual guesses instead of 8. The counter appears to start at 1 instead of 0, so the game has already silently "used" one attempt before the player does anything. This also likely throws off the score calculation since the attempt number is wrong from the very beginning. This is not only under Normal difficulty, also in all other level of difficulties.
Expected: Attempts should start at 0 before any guess is made, giving the player the full number of attempts shown on screen.
What happened: The game starts with attempts already at 1, so the player gets one fewer guess than promised, and the score math is off from the start.

🐛 Bug 3: New Game Button Does Not Fully Reset the Game
When I clicked "New Game" after winning or losing, the game showed the success or game-over message and appeared stuck. It said things like "You already won. Start a new game to play again." and "Game over. Start a new game to try again." but clicking New Game did not clear those messages or restore the input. Only the secret number seemed to reset internally, but the game status, attempts, score, and history were not cleared, so the game was essentially unplayable after the first round without refreshing the whole page. A new game button should wipe everything and start completely fresh.
Expected: Clicking "New Game" should fully reset the game by clearing status, attempts, score, history, and generating a new secret number.
What happened: The button only resets the secret number but leaves the old game status intact, freezing the player out of a new round.

🐛 Bug 4: Switching Difficulty Does Not Change the Actual Number Range
When I switched to Easy mode, the sidebar correctly showed the range as "1 to 20," and Hard mode showed "1 to 50." However, while playing I noticed the game was still accepting and comparing guesses as if the range were 1 to 100. The info bar at the top also always displayed "Guess a number between 1 and 100" regardless of what difficulty was selected. This means the display and the actual game behavior are out of sync, then the label updates but the secret number and game logic do not respect the difficulty range.
Expected: Switching difficulty should change both the displayed range and the actual range used to generate the secret number.
What happened: The sidebar label updates correctly, but the game still behaves as if the range is always 1 to 100.

---

## 2. How did you use AI as a teammate?

**AI tool used:** Claude Code (Anthropic's CLI agent)

**Correct AI suggestion : fixing the swapped hint messages (Bug 1):**
When I asked Claude Code to move `check_guess` into `logic_utils.py` 
and fix the hint bug, Claude scanned the function and immediately 
identified that the return messages were swapped: when a guess was 
greater than the secret, the code returned `"Go HIGHER!"` instead of 
`"Go LOWER!"`. Claude suggested swapping the messages so `guess > secret` 
maps to `"📉 Go LOWER!"` and `guess < secret` maps to `"📈 Go HIGHER!"`. 
It also correctly added the import line in `app.py` and removed the 
original function to avoid duplication. I verified the fix two ways: 
first by running `pytest -v` where `test_check_guess_too_high` and 
`test_check_guess_too_low` both passed immediately, and then by playing 
several rounds in the live Streamlit app; I deliberately guessed high 
(e.g., 90 when the secret was 30) and confirmed the game correctly told 
me to go lower, then guessed low (e.g., 5) and confirmed it told me to 
go higher.

**Incorrect / misleading AI suggestion : attempts counter patch (Bug 2):**
When I described Bug 2 (the attempts counter starting at 1 instead of 0), 
Claude's first suggestion was to patch only the *display* line in `app.py` 
by changing `attempt_limit - st.session_state.attempts` to 
`attempt_limit - st.session_state.attempts + 1` so the number shown on 
screen would look correct. This was misleading: it would have made the 
sidebar *appear* right while leaving `st.session_state.attempts` still 
initialized at 1 internally. This meant the `update_score` call would 
use an off-by-one attempt number, and the score formula 
`100 - 10 * attempt_number` would unfairly penalize the player an extra 
10 points on the very first guess, giving a max score of 90 instead of 
100. I verified this by tracing the score math in `logic_utils.py` and 
confirmed the bug was deeper than just the display. I pushed back on 
Claude's suggestion and the correct fix ; which Claude agreed with after 
I explained the issue ; was to initialize `st.session_state.attempts = 0` 
and leave the display formula completely unchanged. This experience showed 
me that AI suggestions can look correct on the surface while hiding a 
deeper problem, and that human judgment is essential to verify not just 
what the fix looks like but how it affects the rest of the code.

---

## 3. Debugging and testing your fixes

**How did you decide whether a bug was really fixed?**
I used two layers of verification for every fix. First, I ran 
`pytest -v` to check the automated tests, if a test passed, 
the logic was provably correct. Second, I ran the live Streamlit 
app with `python -m streamlit run app.py` and played through the 
game manually to confirm the fix felt right during actual gameplay. 
I did not consider a bug truly fixed until both layers agreed,
code that passed tests but felt wrong in the game, or felt right 
in the game but failed a test, meant the fix was incomplete.

**Describe at least one test you ran and what it showed you:**
The most valuable test was `test_hard_range_wider_than_normal`. 
I had asked Claude to move and fix `get_range_for_difficulty` 
into `logic_utils.py`, and the diff looked correct on the surface 
; the function moved cleanly and the import was added. However, 
when I ran `pytest -v`, this test failed with the message: 
"Hard range (1, 50) should be wider than Normal (1, 100)". 
This showed me that Claude had moved the function correctly but 
silently skipped the actual bug fix inside it. The test caught 
something neither I nor the AI noticed just by reading the diff. 
After manually changing `return 1, 50` to `return 1, 200`, 
all 6 tests passed.

**Did AI help you design or understand any tests? How?**
Yes, I asked Claude Code to generate the pytest cases in 
`tests/test_game_logic.py`. Claude noticed that the existing 
starter tests were broken because they compared the full tuple 
return value of `check_guess` to a plain string, for example 
`assert result == "Win"` instead of correctly unpacking the 
tuple with `outcome, _ = check_guess(50, 50)`. Claude rewrote 
all 6 tests to unpack tuples correctly and added meaningful 
assertions like `assert "LOWER" in message` to verify not just 
the outcome but also the hint direction. This was a correct and 
helpful suggestion, I accepted it after reviewing the diff and 
confirming the assertions matched the expected behavior of each 
fixed function.

---

## 4. What did you learn about Streamlit and state?

**Why the secret number kept changing in the original app:**
The secret number kept changing because Streamlit reruns the 
entire script from top to bottom every time the user interacts 
with anything such as: clicking a button, typing in a box, or changing 
the difficulty dropdown. In the original code, the secret was 
generated with `random.randint(low, high)` at the top level of 
the script without checking if one already existed. This meant 
every rerun picked a brand new secret number, making it 
impossible to guess correctly since the target kept moving.

**How I would explain Streamlit reruns and session state:**
Imagine Streamlit like a soccer match where every time the referee blows the whistle, the entire field resets to kickoff. The ball goes back to the center. Players reposition. It’s like the play starts over from scratch. Regular variables are like drawing the score in the dirt on the field. Every time the whistle blows, the field gets cleaned and the score disappears.

But `st.session_state` is like the official stadium scoreboard. Even when the referee stops play, even when there’s a foul, substitution, or VAR check — the scoreboard still remembers:

- The score ⚽

- The number of shots 🎯

- The yellow cards 🟨

- The time played ⏱

In Streamlit, every click (button, slider, input) is like the referee blowing the whistle. The script reruns from top to bottom — the field resets.If you want something to persist between plays (like the score), you must store it in `st.session_state`. Otherwise, it resets to 0–0 every time someone touches the ball.

**What change finally gave the game a stable secret number:**
The fix was wrapping the secret generation in a check:
`if "secret" not in st.session_state`. This means the secret 
is only generated once on the very first run. Every rerun 
after that skips the generation because the key already exists 
in session state. The same pattern was applied to attempts, 
score, status, and history to keep all game data stable across 
reruns.

---

## 5. Looking ahead: your developer habits

**One habit I want to reuse in future projects:**
I want to keep using the two-layer verification approach — 
running automated pytest tests AND manually testing in the 
live app before marking anything as fixed. The most important 
moment in this project was when `test_hard_range_wider_than_normal` 
failed even though the diff looked correct. That taught me that 
reading code and running code are two completely different things, 
and I should never trust my eyes alone to verify a fix.

**One thing I would do differently next time:**
Next time I work with AI on a debugging task, I would write the 
pytest tests BEFORE asking the AI to fix the bugs, not after. 
If the tests had existed from the start, the Hard mode range bug 
would have failed immediately and Claude would have had a clear 
target to fix. Writing tests first forces both me and the AI to 
agree on what "correct" actually means before any code is changed.

**How this project changed the way I think about AI generated code:**
Before this project, I assumed AI-generated code was either 
correct or obviously broken. Now I understand it can be 
confidently wrong; it looks clean, runs without errors, and 
still does the wrong thing. AI is a fast and useful collaborator, 
but it needs a human with tests and critical thinking to catch 
the subtle mistakes it makes without any warning.