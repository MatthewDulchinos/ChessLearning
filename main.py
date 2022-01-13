"""
This program requests files from Chess.com and then gives you feedback on them
"""
from stockfish import Stockfish
from datetime import datetime
import chess.pgn
import chess.engine
import requests
import os
import shutil
from os.path import exists

def downloadFullFiles(user, monthsBack):
    #Delete old directory and makes a new one
    if exists(user):
        shutil.rmtree(user)
    os.mkdir(user)

    #Download files, one month at a time
    year = datetime.now().year
    month = datetime.now().month
    for x in range(monthsBack):
        downloadFromChessDotCom(user, str(year), str(month))
        month -= 1
        if month == 0:
            year -= 1
            month = 12

def downloadFromChessDotCom(user, year, month):
    request = "https://api.chess.com/pub/player/" + user + "/games/" + year + "/" + month + "/pgn"
    response = requests.get(request)
    
    filename = user+"/"+year+"_"+month+".pgn"
    open(filename, "wb").write(response.content)

def individualGame(game, user, stockfish):
    yourMove = game.headers["White"].casefold() == user.casefold()
    posGood = yourMove
    currentPos = []
    worstMove = 0
    for move in game.mainline_moves():
        
        if yourMove:
            stockfish.get_top_moves(1)
            bestMove = stockfish.get_top_moves(1)[0]['Move']
            option = currentPos.copy()
            option.append(bestMove)
            stockfish.set_position(option)
            bestMoveVal = stockfish.get_evaluation()['value']
            if(len(currentPos) == 45 or len(currentPos) == 46):
                print(stockfish.get_board_visual())

            currentPos.append(move)
            stockfish.set_position(currentPos)
            yourMoveVal = stockfish.get_evaluation()['value']
            if(len(currentPos) == 45 or len(currentPos) == 46):
                #stockfish.
                #stockfish.set_position(currentPos)
                print(stockfish.get_board_visual())
            print(len(currentPos), bestMoveVal, yourMoveVal, move)
            
        else:
            currentPos.append(move)
            stockfish.set_position(currentPos)
        yourMove = not yourMove
        print(len(currentPos), stockfish.get_evaluation())

def individualGameLichess(game, user):
    

def main():
    user = "DJ_Dulch"
    stockfish = Stockfish("D:\Programs\Chess Learning\stockfish_20011801_x64")
    print(stockfish.get_parameters())
    
    #downloadFullFiles(user, 5)
    pgn = open("sampleGame.pgn")
    current_game = chess.pgn.read_game(pgn)
    while(current_game is not None):
        individualGame(current_game, user, stockfish)
        current_game = chess.pgn.read_game(pgn)
    
    
main()
