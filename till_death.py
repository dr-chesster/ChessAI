import requests
import chess
import os
import random
import time
clear = lambda: os.system('cls')



local_history = []
fen_history = []
board = chess.Board()

step_url = 'http://localhost:3001/step'
checkmate_url = 'http://localhost:3001/check-mate'


def checkDraw():
    for f in fen_history:
        occurrences = fen_history.count(f)
        if occurrences > 2:
            print("||DRAW|| (Threefold repetition)")
            requests.post(  step_url, 
                            data = {"exit_cause": "Threefold repetition"
                            }
                    )   
            uploadGame('d')
            quit()

def getAIMove():
    response = requests.post(  step_url, 
                        data = {"fen": board.fen(),
                        "history": local_history,
                        
                        }
                    )   
    return response.text.split("|")[0]

def uploadGame(winner):
    requests.post(  checkmate_url, 
                        data = {"fen": fen_history[-1],
                        "history": local_history,
                        "winner": winner  #b|w|d
                        }
                    )   

def applyMove(move):
    try:
        board.push_san(move)
        fen_history.append(board.fen().split(" ")[0])
    except:
        print("Handeling invalid move? Is it promotion?")
        column = move[-2]
        row = move[-1]
        if row == 8:
            previous_row = '7'
        else:
            previous_row = '2'
        if 'x' in move:
            previous_column = move[0]
            move = previous_column + previous_row + 'x' + column + row + 'q' 
        else:
            move = column + previous_row + column + row + 'q'  #   Eg.: a7a8q
        print("Corrected move "+move)
        board.push_san(move)

#start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq c3 0 0"

first_moves = { #PAWN STARTS
                "c1" : "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq c1 0 1",
                "c2" :"rnbqkbnr/pppppppp/8/8/1P6/8/P1PPPPPP/RNBQKBNR b KQkq c2 0 1",
                "c3" :"rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq c3 0 1",
                "c4" :"rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq c4 0 1",
                "c5" :"rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq c5 0 1",
                "c6" :"rnbqkbnr/pppppppp/8/8/5P2/8/PPPPP1PP/RNBQKBNR b KQkq c6 0 1",
                "c7" :"rnbqkbnr/pppppppp/8/8/6P1/8/PPPPPP1P/RNBQKBNR b KQkq c7 0 1",
                "c8" : "rnbqkbnr/pppppppp/8/8/7P/8/PPPPPPP1/RNBQKBNR b KQkq c8 0 1",
                #HORSE STARTS
                "Na3"  :  "rnbqkbnr/pppppppp/8/8/8/N7/PPPPPPPP/R1BQKBNR b KQkq - 1 1",
                "Nc3"  : "rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR b KQkq - 1 1",
                "Nf3"  : "rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1",
                "Nh3"  :  "rnbqkbnr/pppppppp/8/8/8/7N/PPPPPPPP/RNBQKB1R b KQkq - 1 1"

}

#MAKE FIRST STEP MANUALY (AND PSEUDO RANDOM)
san, fen = random.choice(list(first_moves.items()))
board.set_board_fen(fen.split(' ')[0])
board.turn = chess.BLACK
local_history.append(san)



start = time.time()
while True:
    move = getAIMove()
    local_history.append(move)
    if "#" in move or "++" in move:
        applyMove(move)
        clear()
        print(board)
        print("GAME OVER")
        #TODO CHECK WIN CONDITION
        if len(local_history) %2 == 0:
            print("BLACK WON in {} moves".format(len(local_history)))
            uploadGame('b')
        else:
            print("WHITE WON in {} moves".format(len(local_history)))
            uploadGame('w')

        break

    if 'stalemate' in move or "=" in move:
        clear()
        print(board)
        print("GAME OVER")
        print("STALEMATE")
        uploadGame('d')
        break
    applyMove(move)
    fen_history.append(board.fen().split(" ")[0])

    checkDraw()

    clear()
    print(board)
    if board.turn:
        print("White's turn")
    else:
        print("Black's turn")


end = time.time()
print()
print()
print("Total game time:{:.2f}".format(end - start))
print()
print()
print("Last steps:")
try:
    print(local_history[-10:])
except:
    print(local_history)


####################################################
############      RANDY WUS HERE     ###############    
####################################################