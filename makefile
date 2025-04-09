all: play

test: game.py
	python3 -m doctest game.py

play: game.py test
	python3 game.py
