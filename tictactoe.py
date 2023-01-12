import sys
import pygame 
import numpy as np
import copy
import random
from constants import *

#pygame
pygame.init()
screen = pygame.display.set_mode((width , height))
pygame.display.set_caption("TicTacToe AI")
screen.fill(bg_colors)


class Board:
    def __init__(self) :
        self.squares = np.zeros((rows,cols))
        self.empty_sqrs = self.squares #  at beg all squares are empty
        self.marked_sqrs = 0 # This is number of marked squares at beg

    def final_state(self,show = False):
        '''
          This function checks the final state of the game 
          return 0 if no one wins 
          return 1 if player 1 wins 
          return 2 if player 2 wins 
        '''
        #vertical wins 
        for col in range(cols):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = circle_color if self.squares[0][col] == 2 else line_color
                    iPos = (col*sqsize + sqsize //2,20)
                    fPos = (col*sqsize + sqsize //2,height-20)
                    pygame.draw.line(screen,color,iPos,fPos,line_width)
                    if self.squares[0][col] == 2:
                        print("AI has Won")
                    else :
                        print("You have won")

                return self.squares[0][col]
        #horizontal wins 
        for row in range(rows):
            if self.squares[row][0]== self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = circle_color if self.squares[row][0] == 2 else line_color
                    iPos = (20,row *sqsize+sqsize//2)
                    fPos = (width-20,row*sqsize+sqsize//2)
                    pygame.draw.line(screen,color,iPos,fPos,line_width)
                    if self.squares[row][0] == 2:
                        print("AI has Won")
                    else :
                        print("You have won")
                
                return self.squares[row][0]

        #diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                    color = circle_color if self.squares[1][1] == 2 else line_color
                    iPos = (20,20)
                    fPos = (width-20,height-20)
                    pygame.draw.line(screen,color,iPos,fPos,line_width)
                    if self.squares[1][1] == 2:
                        print("AI has Won")
                    else :
                        print("You have won")
            return self.squares[1][1]

        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            if show:
                    color = circle_color if self.squares[1][1] == 2 else line_color
                    iPos = (20,height-20)
                    fPos = (width-20,20)
                    pygame.draw.line(screen,color,iPos,fPos,line_width)
                    if self.squares[1][1] == 2:
                        print("AI has Won")
                    else :
                        print("You have won")
            return self.squares[1][1]

        return 0


    def mark_sqr(self,row,col,player):
        self.squares[row][col] = player
        self.marked_sqrs+=1

    def check_empty(self,row,col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(rows):
            for col in range(cols):
                if self.check_empty(row,col):
                    empty_sqrs.append((row,col))
        return empty_sqrs

    def isFull(self):
        return self.marked_sqrs==9 

    def isEmpty(self):
        return self.marked_sqrs==0


class AI:
    def __init__(self,level=1,player=2):
        self.level = level
        self.player = player


    def rnd(self,board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0,len(empty_sqrs))
        return empty_sqrs[idx] #(row,col)


    def minimax(self, board, maximizing):
        
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isFull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move
            

    def eval(self,main_board):
        if self.level== 0:
            #random choice
            eval = 'random'
            move = self.rnd(main_board)

        else :
            #minimax
            eval,move = self.minimax(main_board,False)
            
        print(f"The AI has chosen to mark the square at pos {move} with an eval of {eval}") 
        return move # (row,col)
 

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.gamemode = 'ai' # pvp or AI
        self.running = True
        self.show_lines()
        self.player = 1#1-X 2 - O


    def make_move(self,row,col):
        self.board.mark_sqr(row,col,self.player)
        self.draw_fig(row,col)  
        self.next_turn()

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
        
    def show_lines(self):
        #vertical
        pygame.draw.line(screen,line_color,(sqsize,0),(sqsize,height),line_width)
        pygame.draw.line(screen,line_color,(width-sqsize,0),(width-sqsize,height),line_width)

        #horizontal
        pygame.draw.line(screen,line_color,(0,width-(2*sqsize)),(width,width-(2*sqsize)),line_width)
        pygame.draw.line(screen,line_color,(0,width-sqsize),(width,width-sqsize),line_width)

    def draw_fig(self,row,col):
        if self.player==1:
            #draw crosses
            #desc line 
            start_desc = (col*sqsize + offset,row *sqsize +offset)
            end_desc = (col*sqsize+sqsize-offset,row*sqsize+sqsize-offset)
            pygame.draw.line(screen,cross_color,start_desc,end_desc,cross_width)
            #asc line 
            start_asc = (col*sqsize + offset,row *sqsize + sqsize - offset)
            end_asc = (col*sqsize+sqsize-offset,row*sqsize+offset)  
            pygame.draw.line(screen,cross_color,start_asc,end_asc,cross_width) 


        elif self.player == 2:
            #draw circles
            centre = (col * sqsize + sqsize // 2, row * sqsize + sqsize // 2)
            pygame.draw.circle(screen,circle_color,centre,radius,circle_width)
            
    def next_turn(self):
        self.player = self.player%2 +1

    def isover(self):
        return self.board.isFull() or self.board.final_state(show = True)!=0


def main():

    #game object
    game = Game()
    board = game.board
    ai = game.ai

    #mainloop
    while(True):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1]//sqsize
                col = pos[0]//sqsize

                if board.check_empty(row,col):
                    game.make_move(row,col)
                    if game.isover():
                        game.running = False
                    # print(board.squares)

            if event.type == pygame.KEYDOWN:
                #g -gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                #0 - random 
                if event.key == pygame.K_0:
                    ai.level = 0
                # 1 - ai
                if event.key == pygame.K_1:
                    ai.level = 1



        if game.gamemode=='ai' and game.player == ai.player and game.running:
            #update the screen
            pygame.display.update()
            #ai methods
            row,col = ai.eval(board)
            game.make_move(row,col)
            if game.isover():
                game.running = False
            

        pygame.display.update()


main()
