# challenge

This package scrapes data from imot.bg

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Requirements

- Python Version > 3.8
- poetry <https://python-poetry.org/docs/#installation>

## Setting up your virtual environment with poetry

From your project directory install one of the two options (for Windows 10
use PowerShell):

- all dependencies `poetry install`
- neglect development dependencies `poetry install --no-dev`

You should now be able for find your virtual environment in the project
directory at the `./venv/` location.

## Setting up pre-commit hooks

Run `poetry run pre-commit install` in the project directory once in
order for pre-commit hooks to work automatically at each git commit!

## Testing

In the base directory execute `poetry run pytest --cov tests/`.

## Branches

- master - verified version of the code

## TODO

- [x] export to DB using SQLAlchemy
- [x] loop over all result pages
- [ ] extract ad data by following each card's link
- [ ] add the following information:
  - agency/broker
  - home type (house)
  - address
  - days_online
  - text
  - floor & area
