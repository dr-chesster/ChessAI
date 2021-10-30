import board, ai
import chess
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


hostName = "localhost"
serverPort = 6969


class MyServer(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length).decode('utf8').replace("'", '"'))
        fen = post_data['FenString']

        print("#"*100)
        print("#"*100)
        print()

        _board = board.Board.empty()
        _board.loadFenString(fen)
        print(_board.to_string())

        ai_move = ai.AI.get_ai_move(_board, [])
        _board.perform_move(ai_move)
        print(_board.to_string())
        print("{}:{}-->{}:{}".format(ai_move.xfrom,ai_move.yfrom,ai_move.xto,ai_move.yto))
        san = move2Algebraic(ai_move, fen)
        print(san)


        self._set_response()
        resp = {'AI Move':san}
        self.wfile.write(json.dumps(resp).encode('utf-8'))




def getSquare(x, y):
    return x + 8 * y

def move2Algebraic(ai_move, fen):
    fen = fen.split(" ")[0]

    lib_board = chess.Board()
    
    lib_board.set_board_fen(fen)
    #print(lib_board)

    move = chess.Move(getSquare(ai_move.xfrom,ai_move.yfrom), getSquare(ai_move.xto,ai_move.yto))
    return lib_board.san(move)


if __name__ == "__main__":
    
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))


    webServer.serve_forever()


    webServer.server_close()
    print("Server stopped.")










