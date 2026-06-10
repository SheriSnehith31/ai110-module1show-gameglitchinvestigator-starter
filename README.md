# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** A number guessing game where the player tries to guess a secret number within a limited number of attempts, receiving "Too High" or "Too Low" hints after each guess.
- [x] **Bugs found:**
  - Inverted hint messages — "Go HIGHER!" shown when guess was too high (should be "Go LOWER!")
  - String/int comparison bug — secret was cast to `str` on even-numbered attempts, breaking equality checks
  - Score bug — wrong guesses incorrectly added 5 points on even attempts instead of always deducting
- [x] **Fixes applied:**
  - Swapped hint strings in `check_guess` in `logic_utils.py`
  - Removed the `if attempts % 2 == 0` string-cast in `app.py`; always pass integer secret to `check_guess`
  - Simplified `update_score` to always deduct 5 for any wrong guess

## 📸 Demo Walkthrough

1. User opens the app; difficulty defaults to Normal (range 1–100, 8 attempts).
2. Secret number is generated once and stored in `st.session_state` — it does not change between guesses.
3. User enters a guess of **40**. Game returns "📈 Go HIGHER!" — guess is too low.
4. User enters a guess of **70**. Game returns "📉 Go LOWER!" — guess is too high.
5. Score decreases by 5 after each wrong guess.
6. User enters the correct guess (e.g., **55**). Game shows "🎉 Correct!", balloons appear, and final score is displayed.
7. User clicks "New Game 🔁" to reset state (new secret, score back to 0, attempts reset).

## 🧪 Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.0.3, pluggy-1.6.0
collected 9 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 11%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 22%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 33%]
tests/test_game_logic.py::test_hint_message_too_high PASSED              [ 44%]
tests/test_game_logic.py::test_hint_message_too_low PASSED               [ 55%]
tests/test_game_logic.py::test_score_decreases_on_wrong_guess PASSED     [ 66%]
tests/test_game_logic.py::test_parse_guess_valid PASSED                  [ 77%]
tests/test_game_logic.py::test_parse_guess_empty PASSED                  [ 88%]
tests/test_game_logic.py::test_parse_guess_non_number PASSED             [100%]

============================== 9 passed in 0.10s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
