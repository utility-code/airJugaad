#!/bin/bash
black "."
isort .
pdoc --force --html -o docs airjugaad
mv docs/airjugaad/index.html docs/index.md
mv docs/airjugaad/* docs/
git add . && git commit -m $1 && git push
