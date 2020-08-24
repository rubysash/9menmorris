
import pygame
import sys
from NineMenConfig import *
from NineMenMain import *

"""
DESCRIPTION: Attempt at a fps counter
INPUT: 
GLOBAL:
OUTPUT: 
FIXME:  just shows black blob, doesn't render text
"""
def update_fps(clock):
    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont(FONTNAME, 18)
    #fps_text = font.render(DISPSURF, (.5*SQUARESIZE, 7*SQUARESIZE), str(fps), (BLUE))
    fps_text = font.render(fps, 1, pygame.Color("blue"))
    #GAMEFONT.render_to(DISPSURF, (.5*SQUARESIZE, 7*SQUARESIZE), msg, (BLUE))
    return fps_text


"""
DESCRIPTION: Can we legally play in the spot it's asking about?
INPUT: 
GLOBAL:
OUTPUT: 
FIXME:  update description
"""
def is_move_valid(phase, r, c, nr, nc,moves):
    if (DEBUG == 1): print("is_move_valid(phase:{},r:{},c:{},nr:{},nc:{}".format(phase,r,c,nr,nc))
    if ((phase == 1) or (phase == 3)):
        return [r, c] in get_valid_moves(phase,r,c)
    elif (phase == 2):
        # fixme:  This is supposed to search the list of moves, does it?
        for itemof in moves:
            newb1 = str(itemof[0]) + str(itemof[1])
            newb2 = str(nr) + str(nc)
            if (newb1 == newb2):
                if (DEBUG == 1): print("is_move_valid: MATCH")
                return 1
        if (DEBUG == 1): print("is_move_valid: FAIL")
        return 0


"""
DESCRIPTION:   Checks for valid adjacent moves
INPUT:  turn, row, column and the current board
GLOBAL:  BLANK
OUTPUT: returns r,c and list of tuples available
fixme: double check all cooridinates and possibilities, looks like duplicate code of check_pinned
"""
def is_token_move_valid(turn,r,c,cb):

    if (DEBUG == 1): print("is_token_move_valid: turn, r, c, cb",turn,r,c,cb)
    possible_moves = [(r,c)]
    turn = int(turn)
    adjacent = []

    # is it really our token?
    if (DEBUG == 1): print("is_token_move_valid: checking if our turn first...")
    if (int(cb[r][c]) == int(turn)):
        if (DEBUG == 1): print("is_token_move_valid: it's our turn!")

        # ok, what moves do we have?
        # fixme:  this could be a dictionary lookup for speed boost maybe?
        if (r == 0):
            if   (c == 0): adjacent = [(0,3),(3,0)]
            elif (c == 3): adjacent = [(0,0),(1,3),(0,6)]
            elif (c == 6): adjacent = [(0,3),(3,6)]
        elif (r == 1):
            if   (c == 1): adjacent = [(3,1),(1,3)]
            elif (c == 3): adjacent = [(1,1),(0,3),(1,5),(2,3)]
            elif (c == 5): adjacent = [(1,3),(3,5)]
        elif (r == 2):
            if   (c == 2): adjacent = [(3,2),(2,3)]
            elif (c == 3): adjacent = [(2,2),(1,3),(2,4)]
            elif (c == 4): adjacent = [(2,3),(3,4)]
        elif (r == 3):
            if   (c == 0): adjacent = [(0,0),(3,1),(6,0)]
            elif (c == 1): adjacent = [(3,0),(1,1),(3,2),(5,1)]
            elif (c == 2): adjacent = [(3,1),(2,2),(4,2)]
            elif (c == 4): adjacent = [(2,4),(4,4),(3,5)]
            elif (c == 5): adjacent = [(3,4),(1,5),(3,6),(5,5)]
            elif (c == 6): adjacent = [(3,5),(0,6),(6,6)]
        elif (r == 4):
            if   (c == 2): adjacent = [(3,2),(4,3)]
            elif (c == 3): adjacent = [(4,2),(5,3),(4,4)]
            elif (c == 4): adjacent = [(4,3),(3,4)]
        elif (r == 5):
            if   (c == 1): adjacent = [(3,1),(5,3)]
            elif (c == 3): adjacent = [(5,1),(4,3),(5,5),(6,3)]
            elif (c == 5): adjacent = [(5,3),(3,5)]
        elif (r == 6):
            if   (c == 0): adjacent = [(3,0),(6,3)]
            elif (c == 3): adjacent = [(6,0),(5,3),(6,6)]
            elif (c == 6): adjacent = [(6,3),(3,6)]

        for (y,x) in adjacent:
            if (DEBUG == 1): print("is_token_move_valid->testing: ",y,x)
            if (int(cb[y][x]) == int(BLANK)):
                if (DEBUG == 1): print("is_token_move_valid->adding: ",y,x)
                possible_moves.append((y,x))

    # if so, return a good answer, a list of moves, else just 0
    if (len(possible_moves)>1):
        if (DEBUG == 1): print("is_token_move_valid: (YES)",possible_moves)
        return possible_moves
    else:
        if (DEBUG == 1): print("is_token_move_valid: (NO)",possible_moves)
        return possible_moves


"""
DESCRIPTION:  see if they have any valid moves left.  
INPUT:  
GLOBAL: 
OUTPUT: 
FIXME: another log function that should be written cleaner. Looks like duplicate code of is_token_move_valid
"""
def check_pinned(turn,cb):
    if (DEBUG == 1): print("check_pinned: turn->",turn,PLAYER[int(turn)])
    possible_moves = [(-1,-1)]
    turn = int(turn)
    adjacent = []

    for r in range(ROWS):
        for c in range(COLS):
            if (int(cb[r][c]) == int(turn)):

                # ok, what possible moves are there even?
                if (r == 0):
                    if   (c == 0):
                        adjacent.append((0,3)) #
                        adjacent.append((3,0)) #
                    elif (c == 3):
                        adjacent.append((0,0)) #
                        adjacent.append((1,3)) #
                        adjacent.append((0,6)) #
                    elif (c == 6):
                        adjacent.append((0,3)) #
                        adjacent.append((3,6)) #
                elif (r == 1):
                    if   (c == 1):
                        adjacent.append((3,1)) #
                        adjacent.append((1,3)) #
                    elif (c == 3):
                        adjacent.append((1,1)) #
                        adjacent.append((0,3)) #
                        adjacent.append((1,5)) #
                        adjacent.append((2,3)) #
                    elif (c == 5):
                        adjacent.append((1,3)) #
                        adjacent.append((3,5)) #
                elif (r == 2):
                    if   (c == 2):
                        adjacent.append((3,2)) #
                        adjacent.append((2,3)) #
                    elif (c == 3):
                        adjacent.append((2,2)) #
                        adjacent.append((1,3)) #
                        adjacent.append((2,4)) #
                    elif (c == 4):
                        adjacent.append((2,3)) #
                        adjacent.append((3,4)) #
                elif (r == 3):
                    if   (c == 0):
                        adjacent.append((0,0)) #
                        adjacent.append((3,1)) #
                        adjacent.append((6,0)) #
                    elif (c == 1):
                        adjacent.append((3,0)) #
                        adjacent.append((1,1)) #
                        adjacent.append((3,2)) #
                        adjacent.append((5,1)) #
                    elif (c == 2):
                        adjacent.append((3,1)) #
                        adjacent.append((2,2)) #
                        adjacent.append((4,2)) #
                    elif (c == 4):
                        adjacent.append((2,4)) #
                        adjacent.append((4,4)) #
                        adjacent.append((3,5)) #
                    elif (c == 5):
                        adjacent.append((3,4)) #
                        adjacent.append((1,5)) #
                        adjacent.append((3,6)) #
                        adjacent.append((5,5)) #
                    elif (c == 6):
                        adjacent.append((3,5)) #
                        adjacent.append((0,6)) #
                        adjacent.append((6,6)) #
                elif (r == 4):
                    if   (c == 2):
                        adjacent.append((3,2)) #
                        adjacent.append((4,3)) #
                    elif (c == 3):
                        adjacent.append((4,2)) #
                        adjacent.append((5,3)) #
                        adjacent.append((4,4)) #
                    elif (c == 4):
                        adjacent.append((4,3)) #
                        adjacent.append((3,4)) #
                elif (r == 5):
                    if   (c == 1):
                        adjacent.append((3,1)) #
                        adjacent.append((5,3)) #
                    elif (c == 3):
                        adjacent.append((5,1)) #
                        adjacent.append((4,3)) #
                        adjacent.append((5,5)) #
                        adjacent.append((6,3)) #
                    elif (c == 5):
                        adjacent.append((5,3)) #
                        adjacent.append((3,5)) #
                elif (r == 6):
                    if   (c == 0):
                        adjacent.append((3,0)) #
                        adjacent.append((6,3)) #
                    elif (c == 3):
                        adjacent.append((6,0)) #
                        adjacent.append((5,3)) #
                        adjacent.append((6,6)) #
                    elif (c == 6):
                        adjacent.append((6,3)) #
                        adjacent.append((3,6)) #

    # only runs if there are moves on the list, builds final list
    # searches through all possible moves and applies to position we are asking about
    for (r,c) in adjacent:
        if (DEBUG == 1): print("is_token_move_valid->testing: ",turn,r,c, cb[r][c])
        if (int(cb[r][c]) == int(BLANK)):
            if (DEBUG == 1): print("check_pinned r:{},c{} = {}".format(turn,r,c,cb[r][c]))
            possible_moves.append((r,c))
            if (DEBUG == 1): print("check_pinned(): {} can move to {},{}: ".format(turn,r,c))

    # if so, return a good answer, a list of moves, else just 0
    if (DEBUG == 1): print("check_pinned,",len(possible_moves))
    if (len(possible_moves)>1): return 0
    else: return 1

"""
DESCRIPTION:   Checks for 3 in a row in various locations
INPUT:  turn, row, column and the current board
GLOBAL: 
OUTPUT: returns an int for the number of total kills found
fixme: is there a way to make this not take up 3 pages?
make "kills" data structure (list of kills?)
loop over structure
    if rc is in a this loop
    addto list

return the list
This will loop instead of have large branched code - which is faster?

"""
def check_kills(turn,r,c,cb):

    kills = 0
    score = []
    turn = int(turn)

    if (r == 0):
        if ((cb[0][0] == turn) and (cb[0][3] == turn) and (cb[0][6] == turn)): # north 1 row
            scorethis = ([cb[0][0]],[cb[0][3]],[cb[0][6]])
            score.append(scorethis)
        if (c == 0):
            if ((cb[0][0] == turn) and (cb[3][0] == turn) and (cb[6][0] == turn)): # west 1 col
                scorethis = ([cb[0][0]],[cb[3][0]],[cb[6][0]])
                score.append(scorethis)
        elif (c == 3):
            if ((cb[0][3] == turn) and (cb[1][3] == turn) and (cb[2][3] == turn)): # east +
                scorethis = ([cb[0][3]],[cb[1][3]],[cb[2][3]])
                score.append(scorethis)

        elif (c == 6):
            if ((cb[0][6] == turn) and (cb[3][6] == turn) and (cb[6][6] == turn)): # east 3 col
                scorethis = ([cb[0][6]],[cb[3][6]],[cb[6][6]])
                score.append(scorethis)

    elif (r == 1):
        if ((cb[1][1] == turn) and (cb[1][3] == turn) and (cb[1][5] == turn)): # north 2 row
            scorethis = ([cb[1][1]],[cb[1][3]],[cb[1][5]])
            score.append(scorethis)
        if (c == 1):
            if ((cb[1][1] == turn) and (cb[3][1] == turn) and (cb[5][1] == turn)): # west 2 column
                scorethis = ([cb[1][1]],[cb[3][1]],[cb[5][1]])
                score.append(scorethis)
        elif (c == 3):
            if ((cb[0][3] == turn) and (cb[1][3] == turn) and (cb[2][3] == turn)): # north +
                scorethis = ([cb[0][3]],[cb[1][3]],[cb[2][3]])
                score.append(scorethis)
        elif (c == 5):
            if ((cb[1][5] == turn) and (cb[3][5] == turn) and (cb[5][5] == turn)): # east 2 colum
                scorethis = ([cb[1][5]],[cb[3][5]],[cb[5][5]])
                score.append(scorethis)

    elif (r == 2):
        if ((cb[2][2] == turn) and (cb[2][3] == turn) and (cb[2][4] == turn)): # north 3 row
            scorethis = ([cb[2][2]],[cb[2][3]],[cb[2][4]])
            score.append(scorethis)
        if (c == 2):
            if ((cb[2][2] == turn) and (cb[3][2] == turn) and (cb[4][2] == turn)): # west 3 column
                scorethis = ([cb[2][2]],[cb[3][2]],[cb[4][2]])
                score.append(scorethis)
        elif (c == 3):
            if ((cb[0][3] == turn) and (cb[1][3] == turn) and (cb[2][3] == turn)): # north +
                scorethis = ([cb[0][3]],[cb[1][3]],[cb[2][3]])
                score.append(scorethis)
        elif (c == 4):
            if ((cb[2][4] == turn) and (cb[3][4] == turn) and (cb[4][4] == turn)): # east 1 colum
                scorethis = ([cb[2][4]],[cb[3][4]],[cb[4][4]])
                score.append(scorethis)

    elif (r == 3):
        if (c == 0):
            if ((cb[0][0] == turn) and (cb[3][0] == turn) and (cb[6][0] == turn)): # north1 col
                scorethis = ([cb[0][0]],[cb[3][0]],[cb[6][0]])
                score.append(scorethis)
            if ((cb[3][0] == turn) and (cb[3][1] == turn) and (cb[3][2] == turn)): # west1 +
                scorethis = ([cb[3][0]],[cb[3][1]],[cb[3][2]])
                score.append(scorethis)
        elif (c == 1):
            if ((cb[1][1] == turn) and (cb[3][1] == turn) and (cb[5][1] == turn)): # north2 col
                scorethis = ([cb[1][1]],[cb[3][1]],[cb[5][1]])
                score.append(scorethis)
            if ((cb[3][0] == turn) and (cb[3][1] == turn) and (cb[3][2] == turn)): # west1 +
                scorethis = ([cb[3][0]],[cb[3][1]],[cb[3][2]])
                score.append(scorethis)
        elif (c == 2):
            if ((cb[2][2] == turn) and (cb[3][2] == turn) and (cb[4][2] == turn)): # north3 col
                scorethis = ([cb[2][2]],[cb[3][2]],[cb[4][2]])
                score.append(scorethis)
            if ((cb[3][0] == turn) and (cb[3][1] == turn) and (cb[3][2] == turn)): # west1 +
                scorethis = ([cb[3][0]],[cb[3][1]],[cb[3][2]])
                score.append(scorethis)
        elif (c == 4):
            if ((cb[2][4] == turn) and (cb[3][4] == turn) and (cb[4][4] == turn)): # east1 col
                scorethis = ([cb[2][4]],[cb[3][4]],[cb[4][4]])
                score.append(scorethis)
            if ((cb[3][4] == turn) and (cb[3][5] == turn) and (cb[3][6] == turn)): # east1 +
                scorethis = ([cb[3][4]],[cb[3][5]],[cb[3][6]])
                score.append(scorethis)
        elif (c == 5):
            if ((cb[1][5] == turn) and (cb[3][5] == turn) and (cb[5][5] == turn)): # east2 col
                scorethis = ([cb[1][5]],[cb[3][5]],[cb[5][5]])
                score.append(scorethis)
            if ((cb[3][4] == turn) and (cb[3][5] == turn) and (cb[3][6] == turn)): # east1 +
                scorethis = ([cb[3][4]],[cb[3][5]],[cb[3][6]])
                score.append(scorethis)
        elif (c == 6):
            if ((cb[0][6] == turn) and (cb[3][6] == turn) and (cb[6][6] == turn)): # east3 col
                scorethis = ([cb[0][6]],[cb[3][6]],[cb[6][6]])
                score.append(scorethis)
            if ((cb[3][4] == turn) and (cb[3][5] == turn) and (cb[3][6] == turn)): # east1 +
                scorethis = ([cb[3][4]],[cb[3][5]],[cb[3][6]])
                score.append(scorethis)

    elif (r == 4):
        if ((cb[4][2] == turn) and (cb[4][3] == turn) and (cb[4][4] == turn)): # south 1 row
            scorethis = ([cb[4][2]],[cb[4][3]],[cb[4][4]])
            score.append(scorethis)
        if (c == 2):
            if ((cb[4][2] == turn) and (cb[3][2] == turn) and (cb[2][2] == turn)): # west 3 column
                scorethis = ([cb[4][2]],[cb[3][2]],[cb[2][2]])
                score.append(scorethis)
        elif (c == 3):
            if ((cb[4][3] == turn) and (cb[5][3] == turn) and (cb[6][3] == turn)): # south +
                scorethis = ([cb[4][3]],[cb[5][3]],[cb[6][3]])
                score.append(scorethis)
        elif (c == 4):
            if ((cb[2][4] == turn) and (cb[3][4] == turn) and (cb[4][4] == turn)): # east 1 colum
                scorethis = ([cb[2][4]],[cb[3][4]],[cb[4][4]])
                score.append(scorethis)

    elif (r == 5):
        if ((cb[5][1] == turn) and (cb[5][3] == turn) and (cb[5][5] == turn)): # south 2 row
            scorethis = ([cb[5][1]],[cb[5][3]],[cb[5][5]])
            score.append(scorethis)
        if (c == 1):
            if ((cb[1][1] == turn) and (cb[3][1] == turn) and (cb[5][1] == turn)): # west 2 column
                scorethis = ([cb[1][1]],[cb[3][1]],[cb[5][1]])
                score.append(scorethis)
        elif (c == 3):
            if ((cb[4][3] == turn) and (cb[5][3] == turn) and (cb[6][3] == turn)): # south +
                scorethis = ([cb[4][3]],[cb[5][3]],[cb[6][3]])
                score.append(scorethis)
        elif (c == 5):
            if ((cb[1][5] == turn) and (cb[3][5] == turn) and (cb[5][5] == turn)): # east 2 colum
                scorethis = ([cb[1][5]],[cb[3][5]],[cb[5][5]])
                score.append(scorethis)

    elif (r == 6):
        if ((cb[6][0] == turn) and (cb[6][3] == turn) and (cb[6][6] == turn)): # south 3 row
            scorethis = ([cb[6][0]],[cb[6][3]],[cb[6][6]])
            score.append(scorethis)
        if (c == 0):
            if ((cb[0][0] == turn) and (cb[3][0] == turn) and (cb[6][0] == turn)): # west 1 column
                scorethis = ([cb[0][0]],[cb[3][0]],[cb[6][0]])
                score.append(scorethis)
        elif (c == 3):
            if ((cb[4][3] == turn) and (cb[5][3] == turn) and (cb[6][3] == turn)): # south 3 +
                scorethis = ([cb[4][3]],[cb[5][3]],[cb[6][3]])
                score.append(scorethis)
        elif (c == 6):
            if ((cb[0][6] == turn) and (cb[3][6] == turn) and (cb[6][6] == turn)): # east 3 column
                scorethis = ([cb[0][6]],[cb[3][6]],[cb[6][6]])
                score.append(scorethis)

    kills = len(score)
    return kills


"""
DESCRIPTION: returns list of enemy tokens
INPUT:  turn, r, c
GLOBAL: ROWS, COLS, DEBUG
OUTPUT: list of all possible spots we can remove.
"""
def get_valid_kills(turn,nr,nc):
    moves = []
    if (DEBUG == 1): print("get_valid_kills1 ", turn, type(turn))
    for r in range(ROWS):
        for c in range(COLS):
            if (int(turn) == 2):
                if (DEBUG == 1): print("get_valid_kills2 ", type(turn))
                if(int(CB[r][c]) == 1):
                    moves.append([r,c])
            else:
                if (DEBUG == 1): print("get_valid_kills3 ", type(turn))
                if(int(CB[r][c]) == 2):
                    moves.append([r,c])

    if (DEBUG == 1): print("get_valid_kills:",moves)
    return moves


"""
DESCRIPTION: looks for token we want to take from list of enemy tokens
INPUT: 
GLOBAL:
OUTPUT: 
FIXME:  Why can't we move this 1 line to get_valid_kills loop instead of function?
"""
def is_kill_valid(turn,nr,nc):
    if (DEBUG == 1):
        answer = [nr, nc] in get_valid_kills(turn,nr,nc)
        print("is_kill_valid: ", answer)
    return [nr, nc] in get_valid_kills(turn,nr,nc)


"""
DESCRIPTION: Is mouse clicked or not
INPUT: x,y mouse cooridinates
GLOBAL: 
OUTPUT: just returns a 1
FIXME: Why can't we use mouse down event?  
"""
def get_clicked(x,y):
    return 1


"""
DESCRIPTION: converts x,y into row,col for board mapping, came from simon code, not sure i need
INPUT: x,y mouse cooridinates
GLOBAL: SQUARSIZE
OUTPUT: row, col
"""
def get_coords(mouse_pos):
    col = int(mouse_pos[0] / SQUARESIZE)
    row = int((mouse_pos[1]) / SQUARESIZE)
    return row, col


"""
DESCRIPTION: returns 1 for valid, 0 for invalid move
INPUT: Phase, row, column
GLOBAL: turn, valid, blank
OUTPUT: 1 or 0
FIXME: compare to get_valid_moves, might not need both.
"""
def valid_click_pos(phase,r, c,turn):
    # in phase 1 we can place anywhere, no rules
    # can be in any valid spot, as long as it's 

    if (DEBUG == 1): print("valid_click_pos: phase:{},r:{},c:{},turn:{}".format(phase,r,c,turn))

    if((phase == 1) or (phase == 3)):
        if (VB[r][c] == VALID):
            if(CB[r][c] == BLANK): return 1
            else: return 0
        return 0

    # in phase 2 we are moving pieces, not placing them.
    # so, make sure it's a valid spot on the board
    # and make sure we move our own piece
    # fixme: verify it uses this code
    elif ((phase == 2) or (phase == 3)):
        if (VB[r][c] == VALID):
            if int(turn) == int(PLAY1):
                if (DEBUG == 1): print("valid_click_pos (PLAY1):",phase,r,c,type(turn),type(CB[r][c]))
                return (int(CB[r][c]) == int(PLAY1))
            else:
                if (DEBUG == 1): print("valid_click_pos (PLAY2):",phase,r,c,type(turn),type(CB[r][c]))
                return (int(CB[r][c]) == int(PLAY2))
        return 0



"""
DESCRIPTION: checks the board to see if the location is a valid move  based on VB and if CB if it's blank
INPUT: phase, r,c source position
GLOBAL: ROWS, COLS, BLANK, CB, VB
OUTPUT: returns a list of the valid r,c tuples
FIXME:  is this pulling static CB from config or from active memory?
"""
def get_valid_moves(phase,r,c):
    if (DEBUG == 1): print("get_valid_moves(phase:{},r:{},c:{}".format(phase,r,c))
    moves = []
    for r in range(ROWS):
        for c in range(COLS):
            if(int(VB[r][c]) == VALID) and (int(CB[r][c]) == BLANK):
                moves.append([r,c])
    if (DEBUG == 1): print("get_valid_moves moves",moves)
    return moves


"""
DESCRIPTION: modifies the current board list of lists, and later draw_board displays this
INPUT: some action (remove, move, add), the phase, r,c, nr,nc, and who's turn
GLOBAL: PLAY1, PLAY2, 
OUTPUT: 
FIXME: what about phase 3?   Should take same code as phase 2
"""
def modify_cb(action,phase,r, c, nr, nc,turn):
    if (DEBUG == 1): print("update_board(action:{},phase:{},r:{},c:{},nr:{},nc:{},turn:{}".format(action,phase,r,c,nr,nc,turn))

    # remove a token
    if ((action == "remove") or (action == "move")):
        if (DEBUG == 1): print("update_board: , removed {}{}".format(r,c))
        CB[r][c] = BLANK

    # add a token
    if ((action == "add") or (action == "move")):
        if (DEBUG == 1): print("update_board: , added {}{}".format(nr,nc))
        if (int(turn) == int(PLAY1)):
            if (DEBUG == 1): print("update_obard: , P1: ",PLAY1)
            CB[nr][nc] = PLAY1
        else:
            if (DEBUG == 1): print("update_obard: , P2: ",PLAY2)
            CB[nr][nc] = PLAY2

    if (DEBUG == 1): print("update_board",CB)
    if (STATUS): print("9Men-> PHASE: {},\tPLAYER: {},\tOLD: {},{}\tNEW: {},{}\t'{}'".format(phase,PLAYER[int(turn)],r,c,nr,nc,action))
    #fixme: we aren't using the return
    return CB


"""
Font Draw Optimization (inactive code to research)
text = create_text("Hello, World", font_preferences, 72, (0, 128, 0))
FIXME: render all the characters or words then just blit the images?
"""

def make_font(fonts, size):
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names
    choices = map(lambda x:x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)


_cached_fonts = {}
def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font == None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font

_cached_text = {}
def create_text(text, fonts, size, color):
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = _cached_text.get(key, None)
    if image == None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image
