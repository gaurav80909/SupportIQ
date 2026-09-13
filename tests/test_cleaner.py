import pytest
from src.data.cleaner import clean_text

def test_clean_text():
    raw = "Hello   world https://t.co/abc  "
    cleaned = clean_text(raw)
    assert cleaned == "Hello world"

def test_empty_text():
    assert clean_text("") == ""
    assert clean_text(None) == ""
