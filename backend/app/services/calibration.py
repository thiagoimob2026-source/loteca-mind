"""
Calibration Service — Assertiveness logging and weight recalibration.
Compares predictions vs actual results to improve agent accuracy over time.
Phase 1: Stub implementation. Phase 2: Supabase integration.
"""

from typing import Optional


class CalibrationService:
    """Tracks prediction accuracy and recalibrates agent weights."""

    def __init__(self):
        self._history = []

    def log_prediction(self, round_number: int, match_id: int,
                       predicted_column: str, actual_result: Optional[str] = None):
        """Log a prediction for later comparison."""
        self._history.append({
            "round": round_number,
            "match_id": match_id,
            "predicted": predicted_column,
            "actual": actual_result,
        })

    def get_accuracy(self, last_n_rounds: int = 5) -> dict:
        """Calculate accuracy for the last N rounds."""
        completed = [h for h in self._history if h["actual"] is not None]
        if not completed:
            return {"total": 0, "correct": 0, "accuracy": 0.0}

        recent = completed[-last_n_rounds * 14:]
        correct = sum(1 for h in recent if h["predicted"] == h["actual"])

        return {
            "total": len(recent),
            "correct": correct,
            "accuracy": round(correct / len(recent), 3) if recent else 0.0,
        }


# Singleton
calibration_service = CalibrationService()
