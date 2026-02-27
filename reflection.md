# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

🐛 Bug 1: Hints Point the Player in the Wrong Direction
While playing, I noticed something felt off after several wrong guesses. I kept following the hints but kept getting further from the secret number. After running out of attempts, I checked the secret number and realized the hints were completely backwards , when my guess was too high, the game told me "Go higher", when it was too low, it said "Go Lower". I played a second round to confirm it, and the same thing happened consisteny. This made the game nearly unwinnable if you trusted the hints.
Expected: If the guess is too high, the hint should tell the player to go lower, and vice versa.
What happened: The hint messages are swapped, then the game points the player in the wrong direction every single time.

🐛 Bug 2: Attempts Counter is Off — Player Loses a Guess Before Playing

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

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
