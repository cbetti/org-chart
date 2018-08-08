# Org Chart

## Before you do anything

This project requires Python 3.6. We use pipenv to make dependencies simple.

Run this from the root directory:

    pipenv install -d

## Viewing the Org Chart

The org chart is really the data itself. Just look at it:

    cat TEAMS.yaml
    cat PEOPLE.yaml

Or render an image. "reporting" and "teams" structures are supported at this
time. Make sure you have graphviz' 'dot' on your path, and try this:

    pipenv run python orgchart/picture.py reporting
    pipenv run python orgchart/picture.py teams

## Changing the Org Chart

Simply change PEOPLE.yaml and TEAMS.yaml, and commit. These files serve as both
a direct reference, as well as inputs to the helpful tools in this project.

Before committing your work, validate your changes:

    pipenv run python orgchart/validate.py

## Changing the Code

Run the test:

    pipenv run ./tests/run

Run the scripts on the current org chart as a sanity check:

    pipenv run python orgchart/validate.py

Run the linters:

    pipenv shell
    cd orgchart
    pycodestyle .
    pytest --pylint
