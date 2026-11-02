"""Train/serve-consistent features. Do NOT include privileged annotations."""

ALLOWED = ("question_text", "correct_answer", "topic_name", "grade")
FORBIDDEN = ("root_code", "transcription_steps", "final_answer_correct", "clean", "misconceptions")


def metadata_text(row) -> str:
    """Serialize only columns actually present at inference time."""
    def value(key: str) -> str:
        v = row.get(key, "")
        return "" if v is None or str(v).lower() == "nan" else str(v)

    return " | ".join(f"{key}: {value(key)}" for key in ALLOWED)
