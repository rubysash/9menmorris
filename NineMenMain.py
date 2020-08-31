import pygame
from pygame.locals import *

import sys
import time
import pygame.freetype
import re
import random

from NineMenConfig import *
from NineMenFunctions import *

# import numpy as np
# import math


pygame.init()

"""
Instructions:
    Copy all files to directory
    Install Modules required
    Run NineMenMain.py


version .1:
    displays board
    tracks event loop
    mouse up/down/move
    tracks if clicked
    flops turns (bugged)
    tracks valid moves and current moves

version .2:
    flops turns correctly
    displays peices

version .3:
    issues kill move

version .4:
    while loop bug fixed
    phase 2 enabled 

version .5:
    moved into separate files (mostly, only draw_board is left)
    code more commented
    fixme comments added to track what needs work
    debug flag
    removed large branche of main code that was redundant

version .6:
    phase 2 working
    fixme: find the time wait and remove
    fixme: adjacent errors

Version .7:
    phase 3 working
    Peices can fly
    fix ctrl + c cleanliness

version .8:
    consolidated draw_board  removing duplicate code
    added no valid move check
    Make prettier status messages
    silence the debug messages
    Hover highlights working
    optimized main event loop some removing some duplicate code
    cleaned up get_valid_moves
    Some Pep-8
    added instructions
    added license

version .9
    added sound and image to background


version .91 working on..
    Must choose open string first in kill choices
    More Pep-8
    More optimization and refactor
    change append to assign to optimize code
    render fonts in cache to optimize code


MAKE PRETTY
    Window box background image that scrolls
    make prettier graphics instead of no antialiased circles
    Make a nicer UI, at least the communication back to player

GENERAL FIXME:
    font failback
    Add menu for other games
    hide the console (most)
    Add button for Quit, Replay

OPTIMIZATION:
    Refactor code so calls are not in event handlers
    cache font
    move in/out of existing list instead of appends
    read pyglet optimizations
    force to full/windowed based on criteria
    numpy for math calcs


BUGS:
 
0001: Bug->Click off Screen in Full screen mode:
 NineMenFunctions.py", line 61, in is_token_move_valid
    if (int(cb[r][c]) == int(turn)):
IndexError: list index out of range
0001: Fix->Bound get_coord to screen, else it returns default

0002: Bug->Holds old message from queue if mouse off screen
0002: Fix->Bug 1 might fix, but can set messages manually too


"""

VERSION = 8

class PlaceImage(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Button():
    # fixme: this just draws black button, like it needs to be updated
    def __init__(self, text, x=0, y=0, width=100, height=50, command=None):
        self.text = text
        self.command = command
        
        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill(GREEN)

        self.image_hovered = pygame.Surface((width, height))
        self.image_hovered.fill(RED)

        self.image = self.image_normal
        self.rect = self.image.get_rect()

        font = pygame.font.SysFont('comicsansms', 15)
        
        text_image = font.render(text, True, WHITE)
        text_rect = text_image.get_rect(center = self.rect.center)
        
        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)

        # you can't use it before `blit` 
        self.rect.topleft = (x, y)

        self.hovered = False
        self.clicked = False

    def update(self):
        if self.hovered: self.image = self.image_hovered
        else: self.image = self.image_normal
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                print('Clicked:', self.text)
                if self.command:
                    self.command()


"""
DESCRIPTION:   Draws the lines, squares, peices and 
INPUT:  
GLOBAL: 
OUTPUT: 
FIXME: 
    PEP 8 and move to Functions.   "NameError: name 'DISPSURF' is not defined" if I move it
    Is there a better way to update screen/faster?
    why does this have to be in main file?
"""


def draw_board(msg, phase, color, turn, p1men, p2men, moves, kills, winner):
    # console really drains low end systems like a pi/chromebook, especially if it's alot
    if (DEBUG == 1): print("draw_board: msg:", msg)

    # format for pygame vs console
    msg = msg.replace("\t", " ")
    player = str(PLAYER[int(turn)])

    # draw the lines that make up the game board
    for x in range(len(LINES)):
        pygame.draw.line(DISPSURF, LINE, 
                    (LINES[x][0] * SQUARESIZE, SQUARESIZE * LINES[x][1]),
                    (LINES[x][2] * SQUARESIZE, LINES[x][3] * SQUARESIZE), 5)

    # draw the peices/placeholders in their current spots
    for r in range(ROWS):
        for c in range(COLS):
            radius = RADIUS
            color2 = LINE
            if (int(CB[r][c]) == PLAY1): (color2,radius) = (RED,radius)
            elif (int(CB[r][c]) == PLAY2): (color2,radius) = (BLACK,radius)
            elif (int(VB[r][c] == VALID)): radius = int(RADIUS/2)
            else: radius = 0

            pygame.draw.circle(DISPSURF, color2,
                            (int(c * SQUARESIZE + SQUARESIZE / 2), 
                            int(r * SQUARESIZE + SQUARESIZE / 2)), radius)

    # on hover, or other actions, shows green circle 
    # fixme: I want green halo on pieces, green empty circle on valid moves
    # fixme: I want them on hover, not on clic, but it's sluggish on Pi
    for move in (moves):
        if (DEBUG == 1): print("draw_board move:", move)
        r, c = move[0], move[1]
        pygame.draw.circle(DISPSURF, GREEN,
                        (int(c * SQUARESIZE + SQUARESIZE / 2), 
                        int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS, 2)

    # draw the message space
    for c in range(COLS):
        pygame.draw.rect(DISPSURF, WHITE, 
                        (c * SQUARESIZE, ROWS * SQUARESIZE, SQUARESIZE, SQUARESIZE))

    # fixme: cache the fonts and blit images?
    # fixme: can't figure out how to make colors a variable tuple
    #GAMEFONT.render_to(DISPSURF, (2.8 * SQUARESIZE, 3 * SQUARESIZE), "P1: " + str(p1men), (RED))
    #GAMEFONT.render_to(DISPSURF, (3.7 * SQUARESIZE, 3 * SQUARESIZE), "P2: " + str(p2men), (BLACK))

    if (winner):
        msg = "{} WON!! Hit ESC key to QUIT".format(PLAYER[int(winner)])
        pygame.display.set_caption(msg)
        GAMEFONT.render_to(
                DISPSURF, (.5 * SQUARESIZE, 7 * SQUARESIZE), msg, (BLUE))
        #btn1.draw(DISPSURF)
        #btn1.update()
        # pygame.display.update()
        # pygame.display.flip()
    else:
        GAMEFONT.render_to(DISPSURF, 
                        (.5 * SQUARESIZE, 7 * SQUARESIZE), msg,(color))

    if (DEBUG == 1):
        GAMEFONT.render_to(DISPSURF, 
                        (.5 * SQUARESIZE, 7.5 * SQUARESIZE),
                        "DEBUG: P{},T{},P1{},P2{},K{}".format(phase, turn, p1men, p2men, kills), (BLUE))


"""
DESCRIPTION: main function loop
INPUT: user input via mouse/keyboard
GLOBAL:
OUTPUT:
FIXME:
"""
def main():
    if (STATUS): print(COPYLICENSE)
    print(INSTRUCTIONS)

    # fixme: readup on what globals actually do besides the obvious
    global FPSCLOCK, DISPSURF, BASICFONT, GAMEFONT, QUIT, KEYUP, BG, LINE, TOKEN, MUSIC

    randtheme = random.randrange(1,8)
    BG      = THEME[randtheme][0]
    LINE    = THEME[randtheme][1]
    TOKEN   = THEME[randtheme][2]
    MUSIC   = THEME[randtheme][3]

        # pygame setup stuff
    FPSCLOCK = pygame.time.Clock()
    GAMEFONT = pygame.freetype.Font(FONTFILE, 20)

    # Windowed or fullscreen, 8 or 16 BPP color
    if (DEBUG == 2): DISPSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 8) 
    elif (WEAKCOMP): DISPSURF = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN, 8) 
    else:            DISPSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 16)  

    msg = "9 Men's Morris"
    pygame.display.set_caption(msg)

    # fixme:  why can't all these variables go into config?
    moves = [(0, 0)]
    p1men = 9
    p2men = 9

    # for flips isntead of modulus
    (P1,P2) = (1,2)
    t = {P1: P2, P2: P1}

    # basic  config/main variables
    # fixme:  is this best here or in config.py?
    turn = P1
    phase = 1
    kills = 0  # fixme: does this limit kills to only 1 as it resets every loop? Maybe move outside of main()
    winner = 0
    waiting = False
    counter = 0
    silence = 0
    plays = 1
    action = "add"

    # fixme:  this is ugly! It's an out of bounds place holder
    oldr = 7
    oldc = 7
    run = True 

    # define sound object latyer just.play() it
    click_sound = pygame.mixer.Sound('click.wav')


    # load our ambient music
    pygame.mixer.music.load(MUSIC)
    pygame.mixer.music.play(-1)

    BackGround = PlaceImage(BG, [0,0])

    # fixme: I want a button to popup for quit, replay
    #btnmsg = "{} WON!!".format(PLAYER[int(winner)])
    #btn = Button('Hello', 200, 50, 100, 50)

    while run: 
        empty = []      # used for the moves possible placement
        color = BLUE   # default color
        DISPSURF.fill(WHITE)
        DISPSURF.blit(BackGround.image, BackGround.rect)

        # fixme: I want a fps counter if debug
        #if (DEBUG == 3): DISPSURF.blit(update_fps(FPSCLOCK), (10,0))

        # if 18 plays, then both have played their 9, enter phase 2
        if (plays > MEN): phase = 2

        if (phase == 1):   msg = "{} Turn, PLACE Your Piece".format(str(PLAYER[int(turn)]))
        elif (phase == 2): msg = "{} Turn, MOVE Your Piece".format(str(PLAYER[int(turn)]))


        # phase 3 for that player (underdog rule)
        # check before check_pinned
        if ((int(turn) == PLAY1) and (p1men == 3)): phase = 3
        if ((int(turn) == PLAY2) and (p2men == 3)): phase = 3
        if (phase == 3): msg = "{} can now FLY!".format(str(PLAYER[int(turn)]))

        # check if they have no valid moves, if so, they lose
        if (phase == 2):
            pinned = check_pinned(turn, CB)
            if (turn == P1): 
                if ((turn == P1) and (pinned)): winner = P2
            if (turn == P2):
                if ((turn == P2) and (pinned)): winner = P1

        # fixme: can events be limited to speed up frames?
        # pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN])
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: run = False

            # fixme: if I want to handle the button
            #btn.handle_event(event)
            clicked = None  # resets every time and is only "clicked" for a single event
            counter += 1  # tracks mouse movement mostly so I know program isn't crashed in logs
            
            (r, c) = get_coords(pygame.mouse.get_pos())
            if (DEBUG == 1): msg = "{}\tT{}\tM{}\tK{}\tP1:{}\tP2:{}\tr{}\tc{}".format(
                    counter, turn, plays, kills,c) + "\tEVENTLOOP\tPS:" + str(phase)
            
            # ----------------
            # generic code, happens in every phase
            # only MOUSEUPBUTTON code changes by phase
            # ----------------

            if (turn == P1): 
                if (p1men < 3): winner = P2

            if (turn == P2):
                if (p2men < 3): winner = P1

            if (winner): msg = "GAME OVER.  {} is the winner".format(PLAYER[int(winner)])

            # shows them it's their time to take a piece
            # fixme: change hover color on the screen and object if it's valid
            elif ((kills > 0) and (event.type == MOUSEMOTION)):
                msg = "Waiting for {} to take a piece.".format(PLAYER[int(turn)])

                # fixme:  this just blips, does it do anything besides if debug?
                if (is_kill_valid(turn, r, c)):
                    if (DEBUG == 1): msg = "{}\tT{}\tM{}\tK{}\tP1:{}\tP2:{}\tr{}\tc{}".format(
                            counter, turn, plays,kills, p1men, p2men, r,c) + "\tGOOD KILL"
                    color = GREEN
                else:
                    if (DEBUG == 1): msg = "{}\tT{}\tM{}\tK{}\tP1:{}\tP2:{}\tr{}\tc{}".format(
                            counter, turn, plays,c) + "\tBAD KILL"
                    color = RED

            # if a kill is made, they remove an opponent peice.  Mouse up is the "check spot"
            # check ANY time there is a kill count
            # fixme: cannot break string unless no other option available
            elif ((kills > 0) and (event.type == MOUSEBUTTONUP)):
                if (DEBUG == 1): msg = "{}\tT{}\tM{}\tK{}\tP1:{}\tP2:{}\tr{}\tc{}".format(
                        counter, turn, plays, kills,p1men, p2men, r,c) + "\tM_UP KILL"
                
                # they have a valid kill, so modify the board and update turns, kills
                if (is_kill_valid(turn, r, c)):
                    action = "remove"
                    modify_cb(action, phase, r, c, None, None, turn)
                    kills -= 1
                    if (int(turn) == 1): p2men -= 1
                    if (int(turn) == 2): p1men -= 1

                    msg = "KILLED A PIECE!!!"

                # keep going if they happen to have had more than 1 kill, else swap turns
                if (kills > 0): pass
                else:
                    msg = "KILLED A PIECE!!! Next Player Turn"                     
                    turn = t[turn]

            # ----------------------
            #  PHASE 1 - Placing Tokens until all 9 placed
            # ----------------------
            elif ((event.type == MOUSEBUTTONUP) and (phase == 1)):
                mx, my = event.pos
                clicked = get_clicked(mx, my)
                if (DEBUG == 1): msg = "{}\tT{}\tM{}\tK{}\tP1:{}\tP2:{}\tr{}\tc{}".format(
                        counter, turn, plays, kills,c) + "\tM_UP KILL + 1"

                if (is_move_valid(phase, r, c, None, None, moves)):
                    color, action = GREEN, "add"
                    plays += 1
                    if (DEBUG): msg = "{}\tT{}\tM{}\tK{}\tP1:{}\tP2:{}\tr{}\tc{}".format(
                            counter, turn, plays, kills, p1men, p2men, r, c) + "\tM_UP KILL MOVE VALID + 1"
                    
                    modify_cb(action, phase, None, None, r, c, turn)
                    click_sound.play()

                    # did it just make a kill?  if so run through kill logic next iteration
                    # need to keep branch because it must be a valid move in order to check kills
                    # fixme; make sure they actually moved before giving control to other player
                    kills = check_kills(turn, r, c, CB)
                    if (kills > 0):  pass
                    else: turn = t[turn]
                    msg = ""

            # -----------------------------------
            # phase 2 stuff.  they can slide peices now
            # -----------------------------------
            elif (phase == 2) :
                if (event.type == MOUSEMOTION):
                    if (WEAKCOMP):
                        pass
                    else:
                        moves = is_token_move_valid(turn, r, c, CB)
                        if (len(moves) > 1): 
                            empty = moves
                            color = GREEN
                        else:
                            color = BLACK

                elif (event.type == MOUSEBUTTONDOWN):

                    # find the "old" coorindates
                    (oldr, oldc) = get_coords(pygame.mouse.get_pos())

                    moves = is_token_move_valid(turn, oldr, oldc, CB)
                    if (len(moves) > 1): empty = moves

                    # verify it's my token that I've selected
                    # wait for mouse button up event to get "new"
                    if (valid_click_pos(phase, oldr, oldc, turn)):
                        color = GREEN
                        if (DEBUG == 1): msg = "{}\tT{}\tM{}\tK{}\tP1:{}\tP2:{}\tr{}\tc{}".format(counter, turn, plays,
                                kills, p1men, p2men, r,c) + "\tM_DOWN GOOD CHOICE + 2"
                        
                    else:
                        oldr = 7
                        oldc = 7
                        color = RED
                        # fixme: put a red outline on pieces right here
                        if (DEBUG == 1): msg = "{}\tT{}\tM{}\tK{}\tP1:{}\tP2:{}\tr{}\tc{}".format(
                                counter, turn, plays,kills, p1men, p2men, r,c) + "\tM_DOWN BAD CHOICE + 2"
                        # wait for valid mouse down

                elif (event.type == MOUSEBUTTONUP):
                    # find the "new" coorindates
                    (nr, nc) = get_coords(pygame.mouse.get_pos())

                    if (DEBUG == 1): msg = "{}\tT{}\tM{}\tK{}\tP1:{}\tP2:{}\tr{}\tc{}".format(
                            counter, turn, plays, kills,p1men, p2men, r,c) + "\tM_UP 2"

                    # verify we have valid old cooridinates
                    # fixme: this is an ugly hack for the out of bounds error
                    if (oldr == 7):  pass
                    else:

                        # if there are valid moves, do something with them
                        moves = is_token_move_valid(turn, oldr, oldc, CB)
                        if (len(moves) > 1):

                            # they can't just click an old string to count it as a "move"
                            if (is_move_valid(phase, oldr, oldc, nr, nc, moves) and ((nr, nc) != (oldr, oldc))):
                                color, action = GREEN, "move"
                                if (DEBUG == 1): msg = "{}\tT{}\tM{}\tK{}\tP1:{}\tP2:{}\tr{}\tc{}".format(
                                        counter, turn,plays, kills,p1men, p2men, r,c) + "\tM_UP GOOD MOVE 2"

                                # updateboard with move
                                modify_cb(action, phase, oldr, oldc, nr, nc, turn)
                                click_sound.play()

                                # check kills
                                kills = check_kills(turn, r, c, CB)
                                if (kills > 0): pass
                                else:
                                    # make sure they actually moved before giving control to other player
                                    if (str(oldr) + str(oldc) == str(nr) + str(nc)):  pass
                                    else: turn = t[turn]
                        else:
                            color = RED
                            if (DEBUG == 1): msg = "{}\tT{}\tM{}\tK{}\tP1:{}\tP2:{}\tr{}\tc{}".format(
                                    counter, turn, plays,kills, p1men, p2men,r,c) + "\tM_UP NO MOVES 2"

           # -----------------------------------
            # phase 3 stuff.  Player can "fly"
            # -----------------------------------
            elif (phase == 3):
                if (event.type == MOUSEBUTTONUP):
                    if (DEBUG): print("main released at {},{} from {},{}".format(r,c,oldr,oldc))
                    moves = get_valid_moves(phase, oldr, oldc)                    
                    if (is_move_valid(phase, r, c, oldr, oldc, moves)):
                        color, action = GREEN, "move"
                        modify_cb(action, phase, oldr, oldc, r, c, turn)
                        click_sound.play()

                        # did it just make a kill?  if so run through kill logic next iteration
                        # need to keep branch because it must be a valid move in order to check kills
                        # fixme; make sure they actually moved before giving control to other player
                        kills = check_kills(turn, r, c, CB)
                        if (kills > 0):  pass
                        else: turn = t[turn] 

                elif (event.type == MOUSEBUTTONDOWN):
                    # find the "old" coorindates
                    (oldr, oldc) = get_coords(pygame.mouse.get_pos())
                    moves = get_valid_moves(phase, oldr, oldc)
                    if (len(moves) > 1): empty = moves

                    msg = ""
                elif (event.type == MOUSEMOTION):

                    if (WEAKCOMP):
                        pass
                    else:
                        moves = get_valid_moves(phase, oldr, oldc)
                        if (len(moves) > 1):
                            empty = moves
                            color = GREEN
                        else:
                            color = BLACK

            # slow down the console, chromebook can't keep up
            # fixme:  this makes log cleaner, but chromebook still can't keep up
            
            if (silence):
                pass
            elif (DEBUG == 1):
                if re.search("EVENTLOOP", msg):
                    if (counter % 50 == 0): draw_board(msg, phase, GRAY, turn, p1men, p2men, empty, kills, winner)
                elif re.search("INVALID KILL", msg):
                    if (counter % 10 == 0): draw_board(msg, phase, RED, turn, p1men, p2men, empty, kills, winner)
                else:
                    draw_board(msg, phase, color, turn, p1men, p2men, empty, kills, winner)

        # for
    # while

        # fixme: can't get the button to show up, shows a black box instead
        #btn.draw(DISPSURF)
        #btn.update()

            draw_board(msg, phase, color, turn, p1men, p2men, empty, kills, winner)
            pygame.display.update()
        
        FPSCLOCK.tick(FPS)
        #pygame.display.flip()

if __name__ == '__main__':

    # uncomment the profiler to see what to optimize
    #import cProfile, pstats
    #profiler = cProfile.Profile()
    #profiler.enable()

    # don't comment out "main"
    main()

    # disable profiler when done
    #profiler.disable()
    

    # then choose how to sort your data.  I like cumtime
    #stats = pstats.Stats(profiler).sort_stats('ncalls')
    #stats = pstats.Stats(profiler).sort_stats('cumtime') 
    #stats = pstats.Stats(profiler).sort_stats('pcalls')
    #stats = pstats.Stats(profiler).sort_stats('tottime')
    #stats = pstats.Stats(profiler).sort_stats('name')
    
    # finally strip dirs or not then print status
    #stats.strip_dirs()
    #stats.print_stats()


