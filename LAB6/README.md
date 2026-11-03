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
