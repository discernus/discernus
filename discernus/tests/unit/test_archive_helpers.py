from pathlib import Path

from discernus.cli import _detect_run_mode


def test_detect_run_mode_specific_session(tmp_path):
    exp = tmp_path / "projects" / "exp"
    run = exp / "runs" / "20250101T000000Z"
    session = exp / "session" / "20250101T000000Z"
    run.mkdir(parents=True, exist_ok=True)
    session.mkdir(parents=True, exist_ok=True)
    (session / "manifest.json").write_text(
        '{"run_mode": {"mode_type": "statistical_prep"}}', encoding="utf-8"
    )

    mode = _detect_run_mode(run)
    assert mode == "statistical_prep"


