# AI Interactions Log

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Code (claude-sonnet-4-6) to: move all four game-logic functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) from `app.py` into `logic_utils.py`, fix the bugs in each function, update `app.py` to import from `logic_utils`, and generate a full pytest suite targeting each fix.

**What did the agent do?**

1. Read `app.py`, `logic_utils.py`, and `tests/test_game_logic.py` to understand the existing structure.
2. Rewrote `logic_utils.py` with all four functions — fixing the inverted hint strings in `check_guess` and removing the erroneous `+5` branch in `update_score`.
3. Rewrote `app.py` to import from `logic_utils` and removed the `if attempts % 2 == 0` string-cast block that was breaking secret comparisons.
4. Expanded `tests/test_game_logic.py` from 3 broken tests to 9 passing tests covering all three bugs.
5. Ran `pytest` autonomously and confirmed all 9 tests passed.

**What did you have to verify or fix manually?**

I reviewed every diff before accepting it. One thing I caught: the agent's first explanation of the score bug described the `attempt_number % 2 == 0` branch as a possible "bonus mechanic" — I rejected that reasoning because no game design calls for rewarding a wrong guess, and I confirmed by re-reading `update_score` that it was simply a bug. I also verified the hint fix by tracing `if guess > secret` → `"Go HIGHER!"` in the original code, confirming the messages were swapped.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Hint direction when guess is too high | "Generate a pytest case that checks the hint message says LOWER when the guess exceeds the secret" | `assert "LOWER" in message` after `check_guess(80, 50)` | Yes | This directly targets the inverted-hints bug — if the message still said "HIGHER" the test would catch it |
| Hint direction when guess is too low | "Generate a pytest case that checks the hint message says HIGHER when the guess is below the secret" | `assert "HIGHER" in message` after `check_guess(20, 50)` | Yes | Symmetric check to the above — verifies both directions of the fix |
| Score always decreases on wrong guess | "Generate a pytest case verifying a wrong guess on an even attempt still decreases score" | `assert update_score(100, "Too High", 2) == 95` | Yes | Specifically catches the even-attempt `+5` bug; attempt=2 is even which previously triggered the wrong branch |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Run flake8 on app.py, logic_utils.py, and tests/test_game_logic.py with --max-line-length=100 and fix any warnings.
```

**Linting output before:**

```
tests\test_game_logic.py:3:1: E302 expected 2 blank lines, found 1
tests\test_game_logic.py:7:1: E302 expected 2 blank lines, found 1
tests\test_game_logic.py:12:1: E302 expected 2 blank lines, found 1
tests\test_game_logic.py:17:1: E302 expected 2 blank lines, found 1
tests\test_game_logic.py:22:1: E302 expected 2 blank lines, found 1
tests\test_game_logic.py:27:1: E302 expected 2 blank lines, found 1
tests\test_game_logic.py:32:1: E302 expected 2 blank lines, found 1
tests\test_game_logic.py:38:1: E302 expected 2 blank lines, found 1
tests\test_game_logic.py:43:1: E302 expected 2 blank lines, found 1
```

**Changes applied:**

All 9 warnings were E302 — PEP 8 requires two blank lines between top-level function definitions. Added a second blank line between each test function in `tests/test_game_logic.py`. Re-ran flake8 and got a clean exit (0 warnings). `app.py` and `logic_utils.py` were already PEP 8 compliant.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

`check_guess` in the original `app.py` has a bug. Given this function, explain what is wrong and suggest a fix:

```python
def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"
    try:
        if guess > secret:
            return "Too High", "📈 Go HIGHER!"
        else:
            return "Too Low", "📉 Go LOWER!"
    except TypeError:
        ...
```

| | Model A | Model B |
|-|---------|---------|
| **Model name** | claude-sonnet-4-6 | claude-haiku-4-5 |
| **Response summary** | Immediately identified that the emoji/message strings were swapped — "Go HIGHER!" is attached to the `guess > secret` branch, which is the "Too High" case where the player should actually go lower. Suggested swapping the two message strings and explained why the `TypeError` fallback was unnecessary since both inputs should always be integers. | Identified the swapped messages correctly but did not notice the `TypeError` fallback issue. Suggested only swapping the strings without further comment on code quality. |
| **More Pythonic?** | Yes — also noted the `try/except TypeError` block was dead code that could be removed | No — kept the unnecessary try/except in its suggestion |
| **Clearer explanation?** | Yes — explained the logic step by step: "when `guess > secret` the player has guessed too high, so they need to go lower, but the message says HIGHER which is the opposite direction" | Shorter explanation, identified the bug but didn't explain the directional reasoning |

**Which did you prefer and why?**

claude-sonnet-4-6 gave a more complete answer — it not only found the bug but also pointed out the dead `TypeError` fallback, which is a code quality issue separate from the logic bug. The haiku model found the same root cause but stopped short of the deeper analysis. For debugging tasks where you want to understand *why* the code is wrong, not just *what* to change, the more detailed explanation from Sonnet was more useful.
