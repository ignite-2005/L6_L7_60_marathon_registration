import pytest

from marathon_registration import entry_fee, finisher_status, start_wave


def test_entry_fee_standard_and_addons():
    assert entry_fee("10k", 30, False, False) == 800
    assert entry_fee("5k", 30, False, True) == 800
    assert entry_fee("10k", 30, True, False) == 600
    assert entry_fee("10k", 65, False, False) == 400
    assert entry_fee("full", 70, True, True) == 975


def test_entry_fee_invalid_race_and_age():
    with pytest.raises(ValueError, match="unknown race"):
        entry_fee("ultra", 30, False, False)
    with pytest.raises(ValueError, match="too young"):
        entry_fee("5k", 11, False, False)
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("half", 17, False, False)
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("full", 17, False, False)


def test_start_wave_all_groups():
    assert start_wave(None, "full") == "D"
    assert start_wave(150, "full") == "A"   # <= 75% of full cutoff
    assert start_wave(90, "10k") == "A"    # <= 75% of non-full cutoff
    assert start_wave(200, "full") == "B"
    assert start_wave(100, "10k") == "B"
    assert start_wave(241, "full") == "C"
    assert start_wave(121, "10k") == "C"


def test_finisher_status_all_outcomes():
    assert finisher_status(100, "full", 0) == "finisher"
    assert finisher_status(361, "full", 0) == "DNF"
    assert finisher_status(180, "half", 0) == "finisher"
    assert finisher_status(181, "half", 0) == "DNF"
    assert finisher_status(90, "5k", 0) == "finisher"
    assert finisher_status(91, "10k", 0) == "DNF"
    assert finisher_status(1, "full", 1) == "DSQ"
