# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

Initially, I was able to view the secret number in the Developer Debug Info panel, and never win the game no matter which secret number I typed (even the correct secret one) and never get the right answer from the hints. Three issues immediately sprang to mind: the hint messages were inverted (a higher guess was suggested when it was wrong and a lower guess when it was right); the secret number seemed to give less consistent comparisons on alternate turns; and sometimes the score could go up on incorrect guesses, as opposed to always going down.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 60, secret 50 | "Too High" hint → told to go LOWER | Message said "Go HIGHER!" (wrong direction) | none |
| Guess 50 (exact match), attempt #2 | Win / "Correct!" | Treated as a miss — secret was cast to string "50", int 50 ≠ str "50" | none |
| Wrong guess on attempt #2 (even) with outcome "Too High" | Score decreases by 5 | Score increased by 5 due to `attempt_number % 2 == 0` branch | none |

---

## 2. How did you use AI as a teammate?

Claude Code (claude-sonnet-4-6) was my AI coding assistant for the entire project. It helped me read and trace the buggy logic, plan the refactor to logic_utils.py and create the first pytest cases.

One correct AI suggestion was that the hint messages in `check_guess` were reversed: "Go HIGHER!" was returned if guess was too low (and vice versa). I did this by following the condition `if guess > secret` in the original code and I saw that the other message had been attached to it. Manual play-test was performed and correct hints were immediately seen after changing the strings.

Claude misunderstood the score bug and gave the impression that the bug was by design and a "bonus" mechanic, when in reality it was a bug. I turned this down because the game description stated that scores can go haywire and that the player should only be awarded a correct win. Carefully read the update_score: there is no reason to keep the conditional, any wrong guess would lose 5 points anyway.

---

## 3. Debugging and testing your fixes

I considered a bug to be fixed if it passed a targeted pytest case and additionally appeared to work properly when manually played in the live Streamlit app. For instance, I added test_hint_message_too_high which asserts that "LOWER" is in the message if the guess is too big. pytest passed all 9 tests with no regressions when running pytest tests/ -v. For the string-comparison bug, I added test_winning_guess, which checks the guess of 50 in an even attempt — on even attempts, secret was still being cast to a string, this test would fail, and I'd get a repeatable red/green indicator.

---

## 4. What did you learn about Streamlit and state?

Streamlit automatically runs your whole python script again from the first line to the last whenever a user interacts with your page, such as clicking a button, typing text into a text box, etc. Any variable defined (e.g. secret) will be re-created on every rerun of the app, which is why the secret seemed to "change" after each guess; by using st.session_state, you can store variables in a persistent dictionary that is carried over reruns within the same browser session.

---

## 5. Looking ahead: your developer habits

Before I make any code changes, something I'd like to continue doing is to make a bug reproduction table. Compelling myself to record the “input → expected → actual → error” helped to make each bug real and provided me with a clear test case to automate. When I use AI to help with a debugging task next time, I won't take the first diff it has to offer, but rather ask for an explanation of why it made the changes, step by step, because as was the case with the score bug: an explanation that at the time seemed plausible (bonus mechanic") turned out to be completely wrong. This was a terrific reminder that AI generated code is code from any junior dev and therefore should be treated with suspicion, tests should be run and code should not be trusted more than the confidence level of the AI.
