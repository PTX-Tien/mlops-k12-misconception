from k12mlops.features import FORBIDDEN, metadata_text


def test_privileged_columns_are_ignored():
    basic = {"question_text": "1+1", "correct_answer": "2", "topic_name": "Arithmetic", "grade": 4}
    enriched = dict(basic, root_code="SECRET", transcription_steps="teacher-only", misconceptions="teacher-only")
    assert metadata_text(basic) == metadata_text(enriched)
    assert "teacher-only" not in metadata_text(enriched)
    assert "SECRET" not in metadata_text(enriched)
    assert "transcription_steps" in FORBIDDEN
