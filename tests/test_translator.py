"""Tests for translator (mock mode — no real API calls)."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from linguaflow.translator import LANGUAGE_NAMES


def test_language_names_are_complete():
    """All language codes should have a name."""
    assert "zh-CN" in LANGUAGE_NAMES
    assert "ja" in LANGUAGE_NAMES
    assert "ko" in LANGUAGE_NAMES
    assert "en" in LANGUAGE_NAMES


def test_language_names_are_unique():
    """No duplicate language names."""
    names = list(LANGUAGE_NAMES.values())
    assert len(names) == len(set(names))


def test_common_languages_exist():
    """Common target languages should be available."""
    for lang in ["zh-CN", "ja", "ko", "es", "fr", "de", "pt-BR", "ru", "ar"]:
        assert lang in LANGUAGE_NAMES, f"Missing: {lang}"