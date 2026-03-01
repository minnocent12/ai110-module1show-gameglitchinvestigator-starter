
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Refactored from app.py using Claude Code Agent Mode.
    # Bug fixed: Hard mode returned (1, 50) which was easier than Normal (1, 100).
    # Claude moved the function but missed the fix — caught by pytest and fixed manually.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200   # was 1, 50 — fixed after pytest caught it
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: Refactored from app.py using Claude Code Agent Mode.
    # No bug here — clean move only. Claude correctly preserved all logic.
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # FIX: Refactored from app.py using Claude Code Agent Mode.
        # Bug fixed: hint messages were swapped — Go HIGHER/LOWER were reversed.
        # Claude moved the function and corrected the condition logic.
        if guess > secret:
            return "Too High", "📉 Go LOWER!" # was "Go HIGHER" before fix
        else:
            return "Too Low", "📈 Go HIGHER!" # was "Go LOWER" before fix
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: Refactored from app.py using Claude Code Agent Mode.
    # Bug fixed: wrong guesses on even attempts were rewarding +5 points.
    # Claude removed the attempt_number % 2 condition that caused score to go up.
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5    # was: if even attempt, +5 (wrong!)

    if outcome == "Too Low":
        return current_score - 5

    return current_score
