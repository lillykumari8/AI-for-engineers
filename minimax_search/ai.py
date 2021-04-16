################################################################################################
# AUTHOR - Lilly Kumari, UWNetID - lkumari@uw.edu
# please set t=1000 milliseconds (1 sec) since I am getting my best results at that value.

# If the timer part is not needed, please comment out the timer code at lines 298-300
# Comment out the print lines since I've added them for sake of understanding what/how exactly is happening at each depth
# Also comment out the self.print_state() lines if no need to check the temp possible states 
#################################################################################################

import time
import random 
import io
from copy import deepcopy

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"
        
class ai:
    def __init__(self, moves = 0):
        pass


    class state:
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin
            

    def  print_state(self, state):
        """printing the state function similar to the KALAH board"""
        print "\t"
        first = "    "
        for i in range(0,6):
            first = first + str(state.a[5-i]) + "  "
        print first
        print str(state.a_fin) + "\t\t\t" + str(state.b_fin)
        second = "    "
        for i in range(0,6):
            second = second + str(state.b[i]) + "  "
        print second

    # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately


    def move(self, a, b, a_fin, b_fin, t):
        
        '''defining the kalah state from the incoming parameters
        This function takes the state parameters as input and outputs the most viable hole number for the AI (in this case, a, a_fin - player) using
        the minimax search algorithm '''

        kalah_state = ai.state(a, b, a_fin, b_fin)
        depth = 7

        # f = open('timer__7.txt', 'a')
        # f.write('depth = '+str(depth)+'\n')
        # t_start = time.time()
        
        hole_num = ai.minimax(self, kalah_state, -float('inf'), float('inf'), depth-1, True, t)
       
        # f.write(str(time.time()-t_start)+'\n')
        # f.close()

        return hole_num


    def make_move_by_rules(self, state, hole_num, max_flag):

        """This function is written using the updateLocalState fn in the main.py script
        Input - state, hole_num (or array position) and a maximizing flag (if true, means the move for the maximizing player i.e. the AI, 
        if false, means minimizing player)
        Output - max_player (in case of maximizing player, max_player == True means maximizing players gets another move, False means no extra move;
                        in case of minimizing player, max_player == False means minimizing player gets another move, True means no extra move)
                extra_stones (if player's last stone lands in his own empty hole, extra_stones represents the sum of stones in his final hole ans stones in opponent's
                        opposite slot; else it's 0)"""

        max_player = not max_flag

        # maximizing player's turn
        if max_flag:
            extra_stones = 0
            ao = state.a[:]
            all = state.a[hole_num:] + [state.a_fin] + state.b + state.a[:hole_num]
            count = state.a[hole_num]
            all[0] = 0
            p = 1
            while count > 0:
                all[p] += 1
                p = (p+1) % 13
                count -= 1
            state.a_fin = all[6 - hole_num]
            state.b = all[7 - hole_num:13 - hole_num]
            state.a = all[13 - hole_num:] + all[:6 - hole_num]

            ceat = False
            p = (p - 1) % 13
            # if maximizing player gets another move
            if p == 6 - hole_num:
                max_player = max_flag
            if p <= 5 - hole_num and ao[hole_num] < 14:
                id = p + hole_num
                if (ao[id] == 0 or p % 13 == 0) and state.b[5 - id] > 0:
                    ceat = True
            elif p >= 14 - hole_num and ao[hole_num] < 14:
                id = p + hole_num - 13
                if (ao[id] == 0 or p % 13 == 0) and state.b[5 - id] > 0:
                    ceat = True
            # if last stone lands in his own empty hole
            if ceat:
                state.a_fin += state.a[id] + state.b[5-id]
                state.b[5-id] = 0
                state.a[id] = 0
                extra_stones = state.a[id] + state.b[5-id]

            # if maximizing player has all empty holes
            if sum(state.a)==0:
                state.b_fin += sum(state.b)
                state.b[0] = 0
                state.b[1] = 0
                state.b[2] = 0
                state.b[3] = 0
                state.b[4] = 0
                state.b[5] = 0
    
            return max_player, extra_stones
        # minimizing player's turn
        else:
            extra_stones = 0
            bo = state.b[:]
            all = state.b[hole_num:] + [state.b_fin] + state.a + state.b[:hole_num]
            count = state.b[hole_num]
            all[0] = 0
            p = 1
            while count > 0:
                all[p] += 1
                p = (p+1) % 13
                count -= 1
            state.b_fin = all[6 - hole_num]
            state.a = all[7 - hole_num:13 - hole_num]
            state.b = all[13 - hole_num:] + all[:6 - hole_num]

            ceat = False
            p = (p - 1) % 13
            # if minimizing player gets another move
            if p == 6 - hole_num:
                max_player = max_flag
            if p <= 5 - hole_num and bo[hole_num] < 14:
                id = p + hole_num
                if (bo[id] == 0 or p % 13 == 0) and state.a[5 - id] > 0:
                    ceat = True
            elif p >= 14 - hole_num and bo[hole_num] < 14:
                id = p + hole_num - 13
                if (bo[id] == 0 or p % 13 == 0) and state.a[5 - id] > 0:
                    ceat = True

            # if last stone lands in his own empty hole
            if ceat:
                state.b_fin += state.b[id] + state.a[5-id]
                state.a[5-id] = 0
                state.b[id] = 0
                extra_stones = state.b[id] + state.a[5-id]

            # if minimizing player has all empty holes
            if sum(state.b)==0:
                state.a_fin += sum(state.a)
                state.a[0] = 0
                state.a[1] = 0
                state.a[2] = 0
                state.a[3] = 0
                state.a[4] = 0
                state.a[5] = 0
       
            return max_player, extra_stones


    def utility_value(self, state):
        """Returns the utility value of an input state given its state label as mzximizing or minimizing player. It follows certain heuristics so as to tune up
        the score for favorable conditions for the maximizing player & tune down for favorable conditions for minimizing player"""
        value = 0
        holes = [i for i in range(6)]

        # if opponent's kalah contains stones less than 12 (i.e. for the starting 1/3rd part of game, the AI (maximizing player) plays in a defensive mode)
        if state.b_fin < 12:
            value = state.a_fin * 0.75 - state.b_fin * 1
        # for the end 2/3rd part of game, the maximizing player (AI) goes all offensive
        else:
            value = state.a_fin * 1 - state.b_fin * 0.6

        # if last stone of maximizing player lands in his kalah, increase the value by 2
        for hole_num in holes:
            if (state.a[hole_num] == 6 - hole_num):
                value += 2
        # if last stone of minimizing player lands in his kalah, decrease the value by 2
        for hole_num in holes:
            if (state.b[hole_num] == 6 - hole_num):
                value -= 2

        # decrease the value by 10 if more than 4 of maximizing player's holes become empty   
        if state.a.count(0) > 4:
            value -= 10
        # increase the value by 10 if more than 5 of minimizing player's holes become empty
        if state.b.count(0) > 5:
            value += 10
                
        # increase the value by the opposite hole stone count
        for hole_num in holes:
            extra_stones = state.b[5 - hole_num]
            value += extra_stones
            value += state.a[hole_num]
            
        # decrease the value by your own hole's stone count since the opponent will try to make moves in order to capture them
        for hole_num in holes:
            extra_stones = state.a[5 - hole_num]
            value -= extra_stones
            value -= state.b[hole_num]

        return value
        # return state.a_fin - state.b_fin


    def minimax(self, state, alpha, beta, depth, max_flag, t):

        """This is the minimax algorithm function which takes the following input params:
        state - current kalah game state
        alpha - lower bound on the value taken by a maximizing node
        beta - upper bound on the value taken by a minimizing node
        depth - depth upto which the game states can be searched & evaluated
        max_flag - True if searching for a maximizing player, False for minimizing
        t - the specified time for which the states are searched recursively (set it to 1000 ms for best performance)
        
        It outputs the best hole_num (move) in accordance with the evaluated utility value 
        """
        best_hole = 0
        best_alpha = -float('inf')
        best_state = state

        holes = [i for i in range(6)]
        start = time.time()
        for hole_num in holes: 
           # only if the hole is not empty
            if (state.a[hole_num] > 0):
                # best_hole = hole_num
                # creating a deep copy of the state for saving new_state
                new_state = deepcopy(state)
                max_player, _ = self.make_move_by_rules(new_state, hole_num, max_flag)
                if max_player:
                    print "max turn at upper level: " + str(max_player)

                print "-------------------------------------------"
                self.print_state(new_state)
                print "-------------------------------------------"

                # if the leaf node is reached, select the hole_num with best alpha (utility_value in this case)
                if (depth == 1):
                    alpha = self.utility_value(new_state)
                    print "Moving from: " + str(hole_num) + "\t" + "Utility value at depth 1: " + str(alpha)
                else:
                    # recursively call the minimax_with_alphabeta function to get the best alpha & beta by decreasing depth at each consequent level & switching
                    # turns wrt to maximizing/ minimizing player
                    alpha = self.minimax_with_alphabeta(new_state, alpha, beta, depth-1, max_player)
                # return the state & hole_num if alpha is greater than the best_alpha till now
                if (alpha > best_alpha):
                    best_alpha = alpha
                    best_hole = hole_num
                    best_state = new_state

                # this is to take care of boundary case where alpha never exceeds the -infinity value, in those case, the last non-empty hole_num is returned 
                if best_alpha == -float('inf'):
                    best_hole = hole_num

######################################################################################################
                # taking care of the timer part of the assignment, PLEASE COMMENT OUT IF NEEDED
                elapsed_time = time.time() - start
                if elapsed_time*1000 >= t:
                    return best_hole
######################################################################################################

        print "-------------------------------------------"
        print "utility value of chosen move:   " + str(self.utility_value(best_state))
        self.print_state(best_state)
        print "alpha-beta   " + str(alpha)
        print "best move position " + str(best_hole)
        print "-------------------------------------------"
        return best_hole
        

    def minimax_with_alphabeta(self, state, alpha, beta, depth, max_flag):

        """This is the alpha beta pruning algorithm which takes the following input parameters:
        state - current kalah game state
        alpha - lower bound on the value taken by a maximizing node
        beta - upper bound on the value taken by a minimizing node
        depth - depth upto which the game states can be searched & evaluated
        max_flag - True if searching for a maximizing player, False for minimizing
        
        It outputs the alpha/beta values based on the maximizing/ minimizing player's turn
        """

        # if the terminal stage is reached (i.e. when the states have been searched till specified depth & either of the kalah's contain more than 36 stones)
        if (depth == 0 or state.a.count(0) == 6 or state.b.count(0) == 6 or state.a_fin > 36 or state.b_fin > 36):
            print "Utility value at depth 0 : " + str(self.utility_value(state))
            return self.utility_value(state)

        # maximizing (AI) player's turn
        if (max_flag): 
            holes = [i for i in range(6)]
            for hole_num in holes:
                # only if the hole is not empty
                if (state.a[hole_num] > 0):
                    # creating a deep copy of the state for saving new_state
                    new_state = deepcopy(state)
                    max_player, _ = self.make_move_by_rules(new_state, hole_num, max_flag)

                    self.print_state(new_state)
                    if max_player:
                        print "another turn for maximizing player:" + str(max_player)

                    # recursively calling the function in order to get the best alpha value upto the specified depth, hence reducing depth by 1 & switching between maximizing
                    # & minimizing player based on max_player value
                    alpha = max(alpha, self.minimax_with_alphabeta(new_state, alpha, beta, depth-1, max_player))
                    if (beta <= alpha):
                        # alpha beta pruning
                        print "beta cut-off,  " + "alpha = " + str(alpha) + ",  beta = " + str(beta)
                        break
                    print "no cut-off,  " + "alpha = " + str(alpha) + ",  beta = " + str(beta)
            return alpha
       
        # Minimizing (opponent) player's turn
        else:
            holes = [i for i in range(6)]
            for hole_num in holes:
                # only if the hole is not empty
                if (state.b[hole_num] > 0):
                    # creating a deep copy of the state for saving new_state
                    new_state = deepcopy(state)
                    max_player, _ = self.make_move_by_rules(new_state, hole_num, max_flag)

                    self.print_state(new_state)
                    if max_player == False:
                        print "another turn for minimizing player: " + str(max_player)

                    # recursively calling the function in order to get the best alpha value upto the specified depth, hence reducing depth by 1 & switching between maximizing
                    # & minimizing player based on max_player value
                    beta = min(beta, self.minimax_with_alphabeta(new_state, alpha, beta, depth-1, max_player))
                    if (beta <= alpha):
                        # alpha beta pruning
                        print "alpha cut-off,  " + "alpha = " + str(alpha) + ",  beta = " + str(beta)
                        break
                    print "no cut-offf,  " + "alpha = " + str(alpha) + ",  beta = " + str(beta)
            return beta