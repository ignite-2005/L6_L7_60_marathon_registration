<<<<<<< HEAD
# Lab 6 — Code and Branch Coverage

Application: `marathon_registration.py`

## Run code coverage (line coverage)
```powershell
python -m pytest -q CodeCoverageTest_PES1UG24CS484_application.py
coverage run --source=marathon_registration -m pytest -q CodeCoverageTest_PES1UG24CS484_application.py
coverage report -m
```

## Run branch coverage
```powershell
coverage erase
coverage run --branch --source=marathon_registration -m pytest -q BranchCoverageTest_PES1UG24CS484_application.py
coverage report -m
```

The two test files are deliberately separate to match the Lab 6 deliverables. Keep the terminal output from both runs as evidence. Run commands from this `LAB6` directory.
=======
# L6_L7_60 — Marathon Registration

Lab 6: Code and Branch Coverage

## About

A small Python module that works out race entry fees by distance, age and early-bird booking, assigns runners to a start wave and decides each runner's finishing status.

## Files

| File | Description |
|------|-------------|
| `marathon_registration.py` | The module under test |
| `test_marathon_registration.py` | Starter test file |

Keep all your Lab 6 work in this `LAB6` folder. Lab 7 will be added to this repo later.

Refer to the lab handout for instructions.
>>>>>>> origin/main
