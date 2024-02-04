# 9menmorris
9 Men Morris game, in Python Pygame

## Demo

![](https://github.com/rubysash/9menmorris/blob/master/example.png?raw=true)

## Setup (Windows)
```
git clone https://github.com/rubysash/9menmorris.git
python -m venv 9menmorris
cd 9menmorris
scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python NineMenMain.py
```
## Setup (Linux)
```
git clone https://github.com/rubysash/9menmorris.git
python3 -m venv 9menmorris
cd 9menmorris
source bin\activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 NineMenMain.py
```

# Instructions

You win when you remove 7 tokens from the opponent

Each player gets 9 tokens. 

In phase 1 they place the tokens 1 at a time, taking turns. If you get 3 in a row, you remove one of the other person's tokens.

In phase 2, you stop adding tokens and instead you move them, still trying to get 3 in a row.

In phase 3, you only have 3 tokens and you are not bound by the lines and can "fly" to any open spot on your move.

Once you get opponent down to 2 tokens, they lose and it should pop up a "somecolor won" box then wait for escape keydown, close, or restart the game.



# Print Version
https://rubysash.com/wp-content/uploads/9menspython.svg
