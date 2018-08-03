# Org Chart

## Before you do anything

This project requires Python 3.6. We use pipenv to make dependencies simple.

Run this from the root directory:

    pipenv install -d

## Changing the Org Chart

Simply change PEOPLE.yaml and TEAMS.yaml, and commit. These files serve as both
a direct reference, as well as inputs to the helpful tools in this project.

Before committing your work, validate your changes:

    pipenv shell
    python orgchart/validate.py

## Changing the Code

Run the test:

    pipenv shell
    ./tests/run

Run the scripts on the current org chart as a sanity check:

    pipenv shell
    python orgchart/validate.py

Run the linters:

    pipenv shell
    cd orgchart
    pycodestyle .
    pytest --pylint
