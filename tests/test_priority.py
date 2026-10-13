
from app.priority import classify_priority


def test_fire_is_critical():
    assert classify_priority("Electrical", "Fire in laboratory") == "Critical"


def test_power_outage_is_high():
    assert classify_priority("Electrical", "Power outage in classroom") == "High"


def test_broken_chair_is_medium():
    assert classify_priority("Furniture", "Broken chair in library") == "Medium"


def test_unknown_issue_is_low():
    assert classify_priority("General", "Notice board needs cleaning") == "Low"
