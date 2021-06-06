black "."
isort .
pdoc --force --html -o docs airJugaad
mv docs/airJugaad/index.html docs/index.md
mv docs/airJugaad/* docs/
if [[ ! -z $1 ]]; then
        git add . && git commit -m $1 && git push
fi
