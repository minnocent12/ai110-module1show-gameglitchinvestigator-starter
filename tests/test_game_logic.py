from logic_utils import check_guess, update_score, get_range_for_difficulty

# Bug 1: guess above secret should return "Too High" and direct player lower
def test_check_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "Go LOWER" in message
# Bug 2: guess below secret should return "Too Low" and direct player higher
def test_check_guess_too_low():
    outcome, message = check_guess(30, 50)
    assert outcome == "Too Low"
    assert "Go HIGHER" in message

# Bug 3: exact guess should return "Win" outcome
def test_check_guess_correct():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

# Bug 4: "Too High" outcome on an even attempt should always decrease score
def test_update_score_too_high_decreases():
    for even_attempt in (2, 4, 6):
        original = 100
        new_score = update_score(original, "Too High", even_attempt)
        assert new_score < original, (
            f"Score should decrease on even attempt {even_attempt}, "
            f"got {new_score} from {original}"
        )

# Bug 5: Hard difficulty should have a wider range than Normal (1, 100)
def test_hard_range_wider_than_normal():
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard range (1, {hard_high}) should be wider than Normal (1, {normal_high})"
    )
# Bug 6: a correct guess on attempt 1 should increase the score
def test_update_score_win_attempt_1_increases():
    original = 50
    new_score = update_score(original, "Win", 1)
    assert new_score > original
