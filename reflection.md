# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I first ran the game, I could see the secret number in the Developer Debug Info panel but could never win — even typing the exact secret returned the wrong hint or no win. Three clear bugs stood out immediately: the hint messages were inverted (guessing too high told me to go higher), the secret number appeared to produce unpredictable comparisons on alternating turns, and the score would sometimes increase on wrong guesses instead of always decreasing.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 60, secret 50 | "Too High" hint → told to go LOWER | Message said "Go HIGHER!" (wrong direction) | none |
| Guess 50 (exact match), attempt #2 | Win / "Correct!" | Treated as a miss — secret was cast to string "50", int 50 ≠ str "50" | none |
| Wrong guess on attempt #2 (even) with outcome "Too High" | Score decreases by 5 | Score increased by 5 due to `attempt_number % 2 == 0` branch | none |

---

## 2. How did you use AI as a teammate?

I used Claude Code (claude-sonnet-4-6) as my AI coding assistant throughout the project. It helped me read and trace the buggy logic, plan the refactor into `logic_utils.py`, and generate the initial pytest cases.

**Correct AI suggestion:** Claude correctly identified that the hint messages in `check_guess` were swapped — "Go HIGHER!" was returned when the guess was too high (should be "Go LOWER!"). I verified this by tracing the condition `if guess > secret` in the original code and confirming the opposite message was attached. After swapping the strings, the manual play-test immediately showed correct hints.

**Incorrect / misleading AI suggestion:** When I asked Claude to explain the score bug, it initially suggested the `attempt_number % 2 == 0` branch was an intentional "bonus" mechanic rather than a bug. I rejected this because the game description said scores go haywire and the player should only be rewarded for a correct win. I verified by reading `update_score` carefully: there is no design reason for a wrong guess to add points, so I removed the conditional and always deducted 5 for any wrong outcome.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed when both a targeted pytest case passed *and* the live Streamlit app behaved correctly in manual play. For example, after fixing the inverted hints I added `test_hint_message_too_high` which asserts "LOWER" appears in the message when the guess exceeds the secret. Running `pytest tests/ -v` showed all 9 tests passing, confirming nothing regressed. For the string-comparison bug, I added `test_winning_guess` which calls `check_guess(50, 50)` — when `secret` was still being cast to a string on even attempts, this test would fail, giving me a repeatable red/green signal.

---

## 4. What did you learn about Streamlit and state?

Streamlit re-runs your entire Python script from top to bottom every time a user interacts with the page (button click, text input, etc.). Without `st.session_state`, any variable you set — like the secret number — gets re-initialized on every rerun, which is why the secret appeared to "change" after each guess. `st.session_state` is a persistent dictionary that survives reruns within the same browser session, so storing the secret there with `if "secret" not in st.session_state` ensures it is only generated once per game.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing a bug reproduction table before touching any code. Forcing myself to write down "input → expected → actual → error" made each bug concrete and gave me an exact test case to automate. Next time I work with AI on a debugging task I would ask it to explain its reasoning step-by-step before applying any edit, rather than accepting the first diff — the score bug showed how a plausible-sounding explanation ("bonus mechanic") can be wrong. This project reinforced that AI-generated code should be treated like code from any junior developer: review it line by line, run the tests, and trust the tests over the AI's confidence.
