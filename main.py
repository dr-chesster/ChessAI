import board, ai, pieces
import chess
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 6969

times = []
class MyServer(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        
        post_data = json.loads(self.rfile.read(content_length).decode('utf8').replace("'", '"'))
        try:
            fen = post_data['FenString']
        except:
            print("No FenString found in POST")
            print(post_data)
            self._set_response()
            self.wfile.write("bukta".encode('utf-8'))
            return
            
        turn = pieces.Piece.WHITE if fen.split(' ')[1] == 'w' else pieces.Piece.BLACK

        print("#"*100)
        print("#"*100)

        print()

        _board = board.Board.empty()
        
        _board.loadFenString(fen)
        print(_board.to_string())

        start = time.time()
        ai_move = ai.AI.get_ai_move(_board, [], turn)
        if ai_move == 0:
            print("STALEMATE!")
            san ='stalemate'
        else:
            _board.perform_move(ai_move)
            print(_board.to_string())

            #print("AI OUTPUT {}:{}-->{}:{}".format(ai_move.xfrom,ai_move.yfrom,ai_move.xto,ai_move.yto))
            san = move2Algebraic(ai_move, fen)
        
        end = time.time()
        times.append(end-start)
        print("AI Move: |{}| Average prediction time:{:.2f} (last:{:.2f})".format(san, sum(times)/len(times),times[-1]))


        self._set_response()
        resp = {'AI Move':san}
        self.wfile.write(json.dumps(resp).encode('utf-8'))



def getSquare(x, y):
    return ((7-y) *8) + x

def move2Algebraic(ai_move, full_fen):
    fen = full_fen.split(" ")[0]
    
    lib_board = chess.Board()
    lib_board.set_board_fen(fen)
    
    turn = full_fen.split(" ")[1]

    
    lib_board.turn = chess.BLACK if turn.lower() =='b'else chess.WHITE
  
    move = chess.Move(getSquare(ai_move.xfrom,ai_move.yfrom), getSquare(ai_move.xto,ai_move.yto))
    san = lib_board.san(move)
    
    
    lib_board.push(move)

    return san


if __name__ == "__main__":
    HTTPServer((hostName, serverPort), MyServer).serve_forever()











