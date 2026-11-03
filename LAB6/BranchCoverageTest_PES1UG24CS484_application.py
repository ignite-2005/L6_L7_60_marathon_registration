import pytest

from marathon_registration import entry_fee, finisher_status, start_wave


@pytest.mark.parametrize(
    "race,age,early,tshirt,expected",
    [
        ("5k", 12, False, False, 500),
        ("10k", 30, False, False, 800),
        ("half", 18, False, False, 1200),
        ("full", 64, False, False, 1800),
        ("5k", 30, True, False, 375),
        ("10k", 30, True, True, 900),
        ("10k", 65, False, False, 400),
        ("full", 70, True, True, 975),
    ],
)
def test_entry_fee_valid_branches(race, age, early, tshirt, expected):
    assert entry_fee(race, age, early, tshirt) == expected


@pytest.mark.parametrize(
    "race,age,message",
    [
        ("unknown", 30, "unknown race"),
        ("5k", 11, "too young"),
        ("half", 17, "too young for this distance"),
        ("full", 17, "too young for this distance"),
    ],
)
def test_entry_fee_rejections(race, age, message):
    with pytest.raises(ValueError, match=message):
        entry_fee(race, age, False, False)


@pytest.mark.parametrize(
    "best_time,race,expected",
    [
        (None, "full", "D"),
        (180, "full", "A"),
        (90, "10k", "A"),
        (200, "full", "B"),
        (100, "10k", "B"),
        (241, "full", "C"),
        (121, "10k", "C"),
    ],
)
def test_start_wave_branches(best_time, race, expected):
    assert start_wave(best_time, race) == expected


@pytest.mark.parametrize(
    "elapsed,race,missed,expected",
    [
        (1, "full", 1, "DSQ"),
        (360, "full", 0, "finisher"),
        (361, "full", 0, "DNF"),
        (180, "half", 0, "finisher"),
        (181, "half", 0, "DNF"),
        (90, "5k", 0, "finisher"),
        (91, "10k", 0, "DNF"),
    ],
)
def test_finisher_status_branches(elapsed, race, missed, expected):
    assert finisher_status(elapsed, race, missed) == expected
