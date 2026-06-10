from logic_utils import check_guess, update_score, parse_guess

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # Guess of 60 against secret 50 should return "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # Guess of 40 against secret 50 should return "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_hint_message_too_high():
    # When guess is too high, hint should direct player to go lower
    _, message = check_guess(80, 50)
    assert "LOWER" in message

def test_hint_message_too_low():
    # When guess is too low, hint should direct player to go higher
    _, message = check_guess(20, 50)
    assert "HIGHER" in message

def test_score_decreases_on_wrong_guess():
    # Wrong guesses should always decrease score by 5
    assert update_score(100, "Too High", 2) == 95
    assert update_score(100, "Too Low", 3) == 95

def test_parse_guess_valid():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_empty():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_guess_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
