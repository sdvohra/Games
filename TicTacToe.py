# Shriya Vohra, 09-17-15

# Tic-Tac-Toe

board = []
turn = "X"
hum = ""
comp = ""
difficulty = 0

import random

def display_instruct():
    print ("Welcome to Tic-Tac-Toe! Your goal is to get 3-in-a-row first.")

def ask_yes_no(question):
    answer = raw_input(question)
    return answer

def ask_number(question, low, high):
    answer = -1
    while (answer < low or answer > high):
        answer = int(raw_input(question))
    return answer

def pieces():
    userFirst = True
    ans = ask_yes_no("Would you like to go first? (Y/N)")
    if (ans == "Y"):
        print("You are X. You will go first.")
        userFirst = True
    else:
        print("You are O. You will go second.")
        userFirst = False
    return userFirst
        
def new_board():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]

def display_board(board):
    for i in range(0,9,3):
        print board[i],board[i+1],board[i+2]

def legal_moves(board, possibleMove):
    if (possibleMove <= 0):
        return False
    elif (possibleMove > 9):
        return False
    elif (board[possibleMove-1] == "X" or board[possibleMove-1] == "O"):
        return False
    else:
        return True

def winner(board):
    allLetters = True
    for i in range(9):
        if (board[i] != "X" and board[i] != "O"):
            allLetters = False
    if (allLetters):
        return "T"
    
    winMoves = ((1,2,3), (4,5,6), (7,8,9),
                (1,4,7), (2,5,8), (3,6,9),
                (1,5,9), (3,5,7))
    for combo in winMoves:
        if (board[combo[0]-1] == board[combo[1]-1] and board[combo[0]-1] == board[combo[2]-1]):
            return board[combo[0]-1]
    return -1

def human_move(board, human):
    legalMove = False
    while (legalMove == False):
        move = ask_number("Enter coordinate to place piece: ",1,9)
        legalMove = legal_moves(board, move)
    board[move-1] = human

def computer_move(board, computer, human, diff):
    if (diff == 1):
        # Random
        randSpot = random.randrange(0,9)
        while (board[randSpot] == "X" or board[randSpot] == "O"):
            randSpot = random.randrange(0,9)
        board[randSpot] = computer
    elif (diff == 2):
        # Best Available Move
        if (board[4] != "X" and board[4] != "O"):
            board[4] = computer
        elif ((board[0] != "X" and board[0] != "O") or (board[2] != "X" and board[2] != "O") or (board[6] != "X" and board[6] != "O") or (board[8] != "X" and board[8] != "O")):
            randSpot = random.choice([0,2,6,8])
            while (board[randSpot] == "X" or board[randSpot] == "O"):
                randSpot = random.choice([0,2,6,8])
            board[randSpot] = computer
        elif ((board[1] != "X" and board[1] != "O") or (board[3] != "X" and board[3] != "O") or (board[5] != "X" and board[5] != "O") or (board[7] != "X" and board[7] != "O")):
            randSpot = random.choice([1,3,5,7])
            while (board[randSpot] == "X" or board[randSpot] == "O"):
                randSpot = random.choice([1,3,5,7])
            board[randSpot] = computer
    elif (diff == 3):
        # Goes for Win
        # Come up with algorithm for this
        goodMove = False
        winMoves = ((1,2,3), (4,5,6), (7,8,9),
                    (1,4,7), (2,5,8), (3,6,9),
                    (1,5,9), (3,5,7))
        for combo in winMoves:
            if ((board[combo[0]-1] == computer) or (board[combo[1]-1] == computer) or (board[combo[2]-1] == computer)):
                if ((board[combo[0]-1] == board[combo[1]-1]) and legal_moves(board,combo[2])):
                    board[combo[2]-1] = computer
                    goodMove = True
                    return
                elif ((board[combo[0]-1] == board[combo[2]-1]) and legal_moves(board,combo[1])):
                      board[combo[1]-1] = computer
                      goodMove = True
                      return
                elif ((board[combo[1]-1] == board[combo[2]-1]) and legal_moves(board,combo[0])):
                      board[combo[0]-1] = computer
                      goodMove = True
                      return
        if (not goodMove):
            computer_move(board, computer, human, 2)
    elif (diff == 4):
        # Goes for Tie
        # Come up with algorithm for this
        goodMove = False
        winMoves = ((1,2,3), (4,5,6), (7,8,9),
                    (1,4,7), (2,5,8), (3,6,9),
                    (1,5,9), (3,5,7))
        for combo in winMoves:
            if ((board[combo[0]-1] == human) or (board[combo[1]-1] == human) or (board[combo[2]-1] == human)):
                if ((board[combo[0]-1] == board[combo[1]-1]) and legal_moves(board,combo[2])):
                    board[combo[2]-1] = computer
                    goodMove = True
                    return
                elif ((board[combo[0]-1] == board[combo[2]-1]) and legal_moves(board,combo[1])):
                    board[combo[1]-1] = computer
                    goodMove = True
                    return
                elif ((board[combo[1]-1] == board[combo[2]-1]) and legal_moves(board,combo[0])):
                    board[combo[0]-1] = computer
                    goodMove = True
                    return
        if (not goodMove):
            computer_move(board, computer, human, 2)

def next_turn(turn):
    if (turn == "X"):
        return "O"
    else:
        return "X"

def congrat_winner(the_winner, computer, human):
    if (the_winner == computer):
        print "Congrats,", the_winner,"!"
        print "COMPUTER WINS. SORRY."
    elif (the_winner == human):
        print "Congrats,", the_winner,"!"
        print "YAY. HUMAN WINS."
    else:
        print "IT'S A TIE."

def main():
    display_instruct()
    
    print("Difficulty Levels:")
    print ("(1) Random")
    print ("(2) Best Move")
    print ("(3) Win")
    print ("(4) Tie")
    print
    difficulty = ask_number("Select your difficulty: ", 1, 4)
    print difficulty

    turn = "X"

    uFirst = pieces()
    board = new_board()
    display_board(board)
    
    if (uFirst):
        hum = "X"
        comp = "O"
    else:
        hum = "O"
        comp = "X"

    isWinner = False;
    winPerson = ""

    while (isWinner == False):
        if (hum == turn):
            human_move(board, hum)
        elif (comp == turn):
            computer_move(board, comp, hum, difficulty)
            print "Computer's move:"
        winPerson = winner(board)
        display_board(board)
        turn = next_turn(turn)
        if (winPerson != -1):
             isWinner = True

    congrat_winner(winPerson, comp, hum)
    
main()
raw_input("\nPress the enter key to quit.")
