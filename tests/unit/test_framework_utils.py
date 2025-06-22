from pathlib import Path
from src.framework_utils import get_framework_yaml_path


def test_resolve_workspace_framework_path():
    path = get_framework_yaml_path("civic_virtue")
    assert path is not None
    assert path.endswith("civic_virtue_framework.yaml")
    assert Path(path).exists()


def test_resolve_main_framework_path():
    path = get_framework_yaml_path("moral_foundations_theory")
    assert path is not None
    assert path.endswith("moral_foundations_theory_framework.yaml")
    assert Path(path).exists()


def test_unknown_framework_returns_none():
    assert get_framework_yaml_path("unknown_framework") is None
