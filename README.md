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

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo


<img width="1512" height="982" alt="1" src="https://github.com/user-attachments/assets/3dbe41a8-b9a3-4547-8098-a9938d3384d0" />
<img width="1512" height="982" alt="2" src="https://github.com/user-attachments/assets/dfe06f86-420a-4454-926a-b682a6f40373" />
<img width="1512" height="982" alt="3" src="https://github.com/user-attachments/assets/ec7720ba-573b-4cf7-911e-65fc317ab785" />
<img width="1512" height="982" alt="4" src="https://github.com/user-attachments/assets/7fe9fd84-f65e-4849-890e-4de8c2b0a25e" />


## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
