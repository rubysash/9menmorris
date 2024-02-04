# 9menmorris
9 Men Morris game, in Python Pygame

# Setup
git clone https://github.com/rubysash/9menmorris.git <br />
python -m venv 9menmorris <br />
cd 9menmorris <br />
scripts\activate <br />
python -m pip install -r requirements.txt <br />
python NineMenMain.py <br />


# Instructions

You win when you remove 7 tokens from the opponent

Each player gets 9 tokens. 

In phase 1 they place the tokens 1 at a time, taking turns. If you get 3 in a row, you remove one of the other person's tokens.

In phase 2, you stop adding tokens and instead you move them, still trying to get 3 in a row.

In phase 3, you only have 3 tokens and you are not bound by the lines and can "fly" to any open spot on your move.

Once you get opponent down to 2 tokens, they lose and it should pop up a "somecolor won" box then wait for escape keydown, close, or restart the game.



# Print Version
https://rubysash.com/wp-content/uploads/9menspython.svg
