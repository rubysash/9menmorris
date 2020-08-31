
DEBUG = 0   # shows lots of extra debug trash
STATUS = 1  # shows very basic moves in console

FPS = 45

# a few very small tweaks to help with chromebook linux containers
# and Raspberry Pi machines
WEAKCOMP = 0
if (WEAKCOMP):
    FPS = 10

# to shorten typing elsewhere
T1 = {
    1 : "RED",
    2 : "BLACK"
}

# reverse to keep the % flips down
T2 = {
    2 : "RED",
    1 : "BLACK"
}

PLAYER = [None,"RED","BLACK"]

# board size and pieces
ROWS        = 7
COLS        = 7
SQUARESIZE  = 75
SMALLSIZE   = 50
RADIUS      = 20
WIDTH       = COLS * SQUARESIZE
HEIGHT      = (ROWS + 1) * SQUARESIZE
MEN         = 2 * 9 # 18 tokens for "9 men's"

# colors
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
ORANGE       = (255, 127,   0)
GRAY         = (210, 210, 210)

# fixme:  standardize, make failback, cache
FONTNAME = "Arial"      # for grabbing font by name
FONTFILE = "comic.ttf"  # the included font file

# board status
BLANK = 0 # an unplayable spot on the board
PLAY1 = 1 # holds player 1 location in board list
PLAY2 = 2 # holds player 2 location in board list
VALID = 3 # this is a valid placement

PHASEMSG = {
    1: ",PLACE Your Tokens: ",
    2: ",MOVE Your tokens: ",
    3: ",MOVE Your tokens: "
}

# draw the board
LINES = [
    # plus sign pattern
    [3.5,  .5, 3.5, 2.5], # N1 to N2
    [0.5, 3.5, 2.5, 3.5], # E1 to E2
    [3.5, 4.5, 3.5, 6.5], # S1 to S2
    [4.5, 3.5, 6.5, 3.5], # W1 to W2
    # ourer square
    [  .5,  .5, 6.5,  .5],
    [ 6.5,  .5, 6.5, 6.5],
    [ 6.5, 6.5,  .5, 6.5],
    [ 0.5, 6.5,  .5,  .5],
    # middle square
    [ 1.5, 1.5, 5.5, 1.5],
    [ 5.5,  1.5, 5.5, 5.5],
    [ 5.5, 5.5,  1.5, 5.5],
    [ 1.5, 5.5, 1.5, 1.5],
    # small square
    [ 2.5, 2.5, 4.5, 2.5],
    [ 4.5,  2.5, 4.5, 4.5],
    [ 4.5, 4.5,  2.5, 4.5],
    [ 2.5, 4.5, 2.5, 2.5],
]

# valid board positions
VB = [
    [3, 0, 0, 3, 0, 0, 3, 0], 
    [0, 3, 0, 3, 0, 3, 0, 0], 
    [0, 0, 3, 3, 3, 0, 0, 0], 
    [3, 3, 3, 0, 3, 3, 3, 0], 
    [0, 0, 3, 3, 3, 0, 0, 0], 
    [0, 3, 0, 3, 0, 3, 0, 0], 
    [3, 0, 0, 3, 0, 0, 3, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], # needed for valid hover position if on the "help section"
    ]

# tracks current position of peices
# fixme: not a constant as I use it, but labeled as such
CB = [
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    ]

# list of which rows are valid kills
# see if my test piece exists in one of these
# probably have to loop over all pieces and sort
# then use logic to determine if it's ok to break a string
KILLS = [
    [(0,0),(0,3),(0,6)], # row 0 north
    [(1,1),(1,3),(1,5)], # row 1 north
    [(2,2),(2,3),(2,4)], # row 2 north
    [(3,0),(3,1),(3,2)], # row 3 middle west side
    [(3,4),(3,5),(3,6)], # row 3 middle east side
    [(4,2),(4,3),(4,4)], # row 4 south
    [(5,1),(5,3),(5,5)], # row 5 south
    [(6,0),(6,3),(6,6)], # row 6 south
    [(0,0),(3,0),(6,0)], # col 0 west
    [(1,1),(3,1),(5,1)], # col 1 west
    [(2,2),(3,2),(4,2)], # col 2 west
    [(0,3),(1,3),(2,3)], # col 3 middle top
    [(4,3),(5,3),(6,3)], # col 3 middle bottom
    [(2,4),(3,4),(4,4)], # col 4 east
    [(1,5),(3,5),(5,5)], # col 5 east
    [(0,6),(3,6),(6,6)], # col 6 east

]


THEME = {
1: ['1.png',BLACK,BLACK,'1.mp3'], 
2: ['2.png',BLUE,BLUE,'2.mp3'],
3: ['3.png',BLACK,BLACK,'3.mp3'],
4: ['4.png',BLACK,BLACK,'4.mp3'],
5: ['5.png',YELLOW,ORANGE,'5.mp3'],
6: ['6.png',BLACK,BLACK,'6.mp3'],
7: ['7.png',BLACK,BLACK,'7.mp3'],
8: ['8.png',BLACK,BLACK,'8.mp3'],
}

"""
though something like this would make code prettier
it would actually make the code slower 
fixme: what is a fast way to have pretty code without loops of loops

Currently it goes directly to a short append list on hover/click/test
LIke this it would have to build the key, then loop over the elements of key, 
finally I think it would still append... thinking

ADJACENT = {
    '00': [(0,3),(3,0)],
    '03': [(,),(,)],
    '06': [(,),(,)],
    '11': [(,),(,)],
    '13': [(,),(,)],
    '15': [(,),(,)],
    '22': [(,),(,)],
    '23': [(,),(,)],
    '24': [(,),(,)],
    '30': [(,),(,)],
    '31': [(,),(,)],
    '32': [(,),(,)],
    '34': [(,),(,)],
    '35': [(,),(,)],
    '36': [(,),(,)],
    '42': [(,),(,)],
    '43': [(,),(,)],
    '44': [(,),(,)],
    '51': [(,),(,)],
    '53': [(,),(,)],
    '55': [(,),(,)],
    '60': [(3,0),(6,3)],
    '63': [(6,0),(5,3),(6,6)],
    '66': [(6,3),(3,6)]
}
"""


COPYLICENSE = """

----------------------------
|       MIT License        |
----------------------------

Copyright (c) 2020 RUBY SASH CONSULTING LLC  https://rubysash.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

INSTRUCTIONS = """

-------------------------------
| 9 Men's Morris Instructions |
-------------------------------

OVERVIEW
9 Men's Morris is a strategy game that is easy to learn, and fun to play.
There is no luck or chance involved.    You will win by taking advantage
of your opponent's mistakes, or by pure strategy.

HISTORY:
9 Mens and it's variants (6 men, 12 men, etc) are very old.  There are 
copies found scratched in stone that are over several thousand years old.

OBJECT: 
Kill 7 of the enemy Tokens by getting 3 in a row for each kill.

SETUP:
Each player starts 9 tokens of the same color (RED or BLACK).

PHASE1: (Placement)
Place them on valid positions, 1 per turn.
While placing, if you get 3 in a row, take an enemy token then change turns.

PHASE2: (Movement)
Take turns sliding tokens 1 adjacent move at a time.
While sliding, if you get 3 in a row, take an enemy token then change turns.

PHASE3: (Underdog)
Underdog rule allows the person with only 3 tokens to jump instead of "slide".
A player in phase 3 can jump to any open spot on the board.
While jumping, if you get 3 in a row, take an enemy token then change turns.

STALEMATE:
3 moves that repeat are considered "stalemate" and the game is a tie.

FORCED CHOICES:
If an enemy has 3 in a row and other pieces not in a row, you must kill one
of the "other" pieces first.   



"""