@echo OFF

cd tests\test_cases
pytest -rA TestLogin.py
pytest -rA TestUseCases.py
pytest -rA TestCreatePlaygroundItems.py
pytest -rA TestRemovePlaygroundItems.py


PAUSE