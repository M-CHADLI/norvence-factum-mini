import json
from decimal import Decimal
from pathlib import Path

import pytest

from app.normalize import normalize_amount

FIXTURES = Path(__file__).parent / "fixtures" / "echantillons.jsonl"
ECHANTILLONS = [json.loads(line) for line in FIXTURES.read_text(encoding="utf-8").splitlines()]


def test_normalize_plain_amount():
    assert normalize_amount("1250.00") == Decimal("1250.00")


@pytest.mark.parametrize("echantillon", ECHANTILLONS, ids=lambda e: e["id"])
def test_normalize_echantillons(echantillon):
    assert normalize_amount(echantillon["montant_brut"]) == Decimal(echantillon["montant_attendu"])


@pytest.mark.parametrize(("brut", "attendu"), [(1250, "1250.00"), (980.5, "980.50")])
def test_normalize_numeric_input(brut, attendu):
    assert normalize_amount(brut) == Decimal(attendu)


@pytest.mark.parametrize("brut", [None, "douze euros"])
def test_normalize_rejects_unreadable(brut):
    with pytest.raises(ValueError):
        normalize_amount(brut)
