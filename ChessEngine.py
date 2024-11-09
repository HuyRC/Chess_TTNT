
#class   cho game 
class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
       
        # các hàm tìm kiếm nước đi của các quân
        # sẽ ánh xạ các kí tự tương ứng với tên  quân cờ và hàm di chuyển
        self.moveFunction = {'p': self.getPawnMoves, 
                             'R':self.getRookMoves, 
                             'N':self.getKnightMoves, 
                             'B': self.getBishopMoves, 
                             'Q': self.getQueenMoves,
                             'K': self.getKingMoves}

        self.whiteToMove =True #lượt đi của quân trằng ,quân trắng luôn đi đầu
        self.moveLog=[] # dùng để undo nước di
        #vị trí cùa 2 vua white và black
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        self.checkMate = False #biến  kết thúc game
        self.staleMate = False #biến game kết quả hòa
        self.enPassantPossible = () #bắt tốt qua đường
        self.in_check = False  # biến check xem vua có bị chiếu không
        self.pins = [] #List các quân cờ bị ghìm
        self.checks= [] # list quân cờ đang chiếu vua
        #quyền castling
        self.current_Castling_Rights = CastleRights (True,True,True,True)
        #trạng thái quyền nhập thành mỗi khi có 1 nước được đi
        self.castleRightLog = [CastleRights(self.current_Castling_Rights.wK_Side, self.current_Castling_Rights.bK_Side, 
                                            self.current_Castling_Rights.wQ_Side, self.current_Castling_Rights.bQ_Side)] 

    def makeMove(self, move):
        print("")
        print("isPassantMove trong makeMove:", move.isEnPassantMove)
        self.board[move.startRow][move.startCol] = "--"  # Xóa quân tại vị trí bắt đầu
        self.board[move.endRow][move.endCol] = move.pieceMoved  # Đặt quân tại vị trí kết thúc
        self.moveLog.append(move)   # thêm vào  lịch sử di chuyển
        self.whiteToMove = not self.whiteToMove  # Đổi lượt chơi

        # Cập nhật vị trí của quân Vua
        if move.pieceMoved == "wK":  # Nếu quân di chuyển là Vua trắng
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":  # Nếu quân di chuyển là Vua đen
            self.blackKingLocation = (move.endRow, move.endCol) 
        #Phong Tốt nếu hợp lệ 
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # en passant : bắt tốt qua đường
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = "--"
        
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enPassantPossible = ()

        # Kiểm tra castling 
        if move.isCastleMove:
            if move.endCol - move.startCol  == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] #di chuyen quan xe 
                self.board[move.endRow][move.endCol + 1] = '--'
            if move.startCol - move.endCol  == 3:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'

        #Quyền Nhập thành -Khi vua hoặc xe di chuyển
        self.updateCastleRights(move)
        self.castleRightLog.append(CastleRights(self.current_Castling_Rights.wK_Side, self.current_Castling_Rights.bK_Side, 
                                                self.current_Castling_Rights.wQ_Side, self.current_Castling_Rights.bQ_Side))
        


    def undoMove(self):
        if len(self.moveLog) != 0: 
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]= move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved  == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            
            #undo bat tot qua duong
            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enPassantPossible = (move.endRow, move.endCol)
            #undo tot di 2 o 
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()
            #undo nhap thanh
            self.castleRightLog.pop()
            self.current_Castling_Rights = self.castleRightLog[-1]

            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endcol + 1]='--'
                else:
                    self.board[move.endRow][move.endCol +1] = self.board[move.endRow][move.endCol - 2]
                    self.board[move.endRow][move.endCol -2] = '--'


    def updateCastleRights(self, move):
        #neu con xe da bi an mat
        #kiểm tra xem con xe ở phía bên nào bị ăn
        if move.pieceCaptured == "wR":
            if move.endCol  == 0 :
                self.current_Castling_Rights.wQ_Side = False
            elif move.endCol == 7:
                self.current_Castling_Rights.wK_Side = False
        elif move.pieceCaptured == "bR":
            if move.endCol == 0 :
                self.current_Castling_Rights.bQ_Side = False
            elif move.endCol == 7:
                self.current_Castling_Rights.bK_Side = False
        # Nếu vua di chuyển, xóa quyền castling
        if move.pieceMoved == 'wK':
            self.current_Castling_Rights.wK_Side = False
            self.current_Castling_Rights.wQ_Side = False
        elif move.pieceMoved == 'bK':
            self.current_Castling_Rights.bK_Side = False
            self.current_Castling_Rights.bQ_Side = False
        # Nếu xe di chuyển , xóa quyền castling
        if move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.current_Castling_Rights.wK_Side = False
                if move.startCol  == 7:
                    self.current_Castling_Rights.wQ_Side = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0 :
                if move.startCol == 0:
                    self.current_Castling_Rights.bQ_Side = False
                if move.startCol == 7 :
                    self.current_Castling_Rights.bK_Side = False
    

    def getValidMoves(self): # các nước đi hợp lệ
        # lưu quyền castling tạm thời
        tempCastleRights = CastleRights(self.current_Castling_Rights.wK_Side, self.current_Castling_Rights.bK_Side, 
                                        self.current_Castling_Rights.wQ_Side, self.current_Castling_Rights.bQ_Side)
        moves = []
        self.in_Check, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.in_Check:
            if len(self.checks) == 1:  # Chỉ bị chiếu bởi một quân
                moves = self.getAllPossibleMoves()
                checkInfo = self.checks[0]  # Lấy thông tin về quân đang chiếu vua
                checkRow = checkInfo[0]
                checkCol = checkInfo[1]
                pieceChecking = self.board[checkRow][checkCol] # Lấy thông tin quân cờ  trên bàn cờ
                valid_Squares = [] # Danh sach nước cờ có thể đi để cứu vua
                
                if pieceChecking[1] == 'N': 
                    # Nếu quân mã chiếu vua, chỉ có thể ăn quân mã hoặc chạy vua
                    #cách đế ăn mã là các nước đi có thể đi chính là ô của quân mã
                    valid_Squares = [(checkRow, checkCol)]
                else:  # Nếu là quân khác, tìm các ô vua có thể trốn
                    for i in range(1, 8):
                        # từ vua ta tìm ra các hướng của Quân đich đang chiếu vua
                        # mỗi valid_square là các ô mà QUÂN TA có thể di chuyển tới để chặn chiếu vua
                        # để cứu vua ta phải di chuyển quân chặn các ô này
                        #checkinfo[2] và [3]: là hướng của quân địch tới ăn vua 
                        #vd bishop black ăn vua theo hướng trái lên :(-1,-1)
                        validSquare = (kingRow + checkInfo[2] * i, kingCol + checkInfo[3] * i)
                        valid_Squares.append(validSquare)
                        #khi các ô có thể di chuyển để cứu vua tới ô của Quân đang chiếu vua thì ta dừng for 
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                # Loại bỏ các nước đi không hợp lệ
                # Duyệt danh sách các nước đi của quân từ cuối về
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':  # Không phải là vua di chuyển
                        if not (moves[i].endRow, moves[i].endCol)  in valid_Squares:  # Nếu không nằm trong các ô cứu vua
                            moves.remove(moves[i]) #loại bỏ nước đi đó
            else:  # Bị chiếu đôi (double check)
                self.getKingMoves(kingRow, kingCol, moves)  # Chỉ quân vua mới có thể di chuyển
        else:
            moves = self.getAllPossibleMoves()  # Nếu không bị chiếu, lấy tất cả các nước đi
            if self.whiteToMove:
                self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1], moves)
            else: 
                self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        #nếu danh sách nước đi rỗng
        if len(moves) == 0:
            # vua bị chiếu
            if self.inCheck():
                self.checkMate = True # end game
            else:
                self.staleMate = True
        else:
            self.checkmate = False
            self.stalemate = False
        self.current_Castling_Rights = tempCastleRights

        return moves



    def inCheck(self): # Kiểm tra vua có bị tấn công không
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])  # ktra tra quân Vua trắng
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])  # ktra tra quân Vua đen

    def squareUnderAttack(self,r,c): # kiểm tra 1 quân cờ có bị tấn công không
        self.whiteToMove = not self.whiteToMove
        oppMoves =self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        # Kiểm tra xem ô (r, c) có nằm trong nước đi của quân đối phương không
        for move in oppMoves:
            # end_pos=> (endRow,endCol) là vị trí mà 1 quân cờ có thể đi tới
            if move.endRow == r and move.endCol == c:
                return True  # Ô bị tấn công
        return False  # Ô không bị tấn công
    
    def getAllPossibleMoves(self): #  1 list move , mỗi ptu là 1 obj move (start_pos,end_pos,board): các nước đi tương ứng vs các quân cờ
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]   
                if (turn == 'w' and self.whiteToMove) or (turn== 'b' and not self.whiteToMove):
                    piece =self.board[r][c][1]
                    self.moveFunction[piece](r,c,moves)
        return moves
    
    def checkForPinsAndChecks(self): # kiểm tra xem vua có bị chiếu không,danh sách quân bị ghìm, danh sách quân dịch ăn vua
        pins = []  # Quân cờ bị khóa
        checks = []  # Quân đang chiếu
        in_check = False       
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1),  # Các hướng theo hàng và cột
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Các hướng theo đường chéo
        # Duyệt các vị trí xung quanh vua. theo từng hướng
        for j in range(len(directions)):
            direction = directions[j]
            possiblePin = ()  # Lưu vị trí quân có thể bị khóa
            for i in range(1, 8):
                endRow = startRow + direction[0] * i
                endCol = startCol + direction[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Đảm bảo không ra ngoài bàn cờ
                    endPiece = self.board[endRow][endCol]
                    # Nếu gặp quân đồng minh và không phải là vua 
                    if endPiece[0] == allyColor and endPiece[1] != 'K':  
                        # Nếu chưa có quân đồng minh nào bị khóa
                        if possiblePin == ():  
                        # Đánh dấu quân này CÓ THỂ bị khóa trong trường hợp vua bị chiếu
                            possiblePin = (endRow, endCol, direction[0], direction[1])
                        else:  # Nếu đã có một quân bị khóa, dừng lại
                            break
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                            # Kiểm tra nếu có quân địch đang chiếu vua
                            #theo từng hướng ứng với các hướng có thể đi của quân cờ
                        if (0 <= j <= 3 and pieceType == 'R') or \
                            (4 <= j <= 7 and pieceType == 'B') or \
                            (i == 1 and pieceType == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                            (pieceType == 'Q') or (i == 1 and pieceType == 'K'):
                                # Không có quân bị khóa, vua bị chiếu
                                # Vòng for duyệt theo từng hướng 
                                # và hướng hiện tại không có quân nào che chắn cho vua
                                if possiblePin == ():  
                                    in_check = True
                                    checks.append((endRow, endCol, direction[0], direction[1]))
                                    break
                                else:  # Có quân bị khóa
                                    #thêm quân này list các quân bị ghìm
                                    pins.append(possiblePin)
                                    break
                        else:  # Quân địch không chiếu vua, dừng lại
                            break
                else:
                    break  # Nếu ra khỏi bàn cờ, dừng lại
        # Kiểm tra nước đi của quân mã
        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for m in knightMoves:
            #đây là khoảng cách từ mã đến vua
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Kiểm tra không ra khỏi bàn cờ
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':  # Nếu là quân mã địch
                    in_check = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return in_check, pins, checks # trả về vua có bị chiếu không,danh sách các quân bị ghìm ,danh sách các quân địch chiếu vua

    def getPawnMoves(self, r, c, moves):
        piecePinned = False  # Quân cờ có đang khóa không
        pinDirection = ()  # Hướng mà quân cờ bị ghìm
        # Kiểm tra xem quân cờ có bị khóa hay không
        # Duyệt từ cuối list các quân cờ bị khóa
        for i in range(len(self.pins) - 1, -1, -1):
            #kiểm tra có tìm được quân cờ (r,c) trong list cờ bị khóa không
            if self.pins[i][0] == r and self.pins[i][1] == c:
                # nếu có thực hiện khóa quân cờ
                piecePinned = True # khóa quân cờ ở (r,c)
                pinDirection = (self.pins[i][2], self.pins[i][3]) # thêm hướng di chuyển của cờ (r,c)
                self.pins.remove(self.pins[i])  
                # Xóa quân bị khóa khỏi danh sách vì đã xử lí xong, 
                # remove để tránh duyệt lại
                break

        if self.whiteToMove:  # Nước đi của quân trắng
            moveAmount = -1 #quân trắng đi lên nên bước đi là -1
            startRow = 6 # vị trí xuất phát 
            enemyColor = 'b' # màu đối phương 
        else:
            moveAmount = 1 # quân đen đi xuống nên sẽ là +1
            startRow = 1
            enemyColor = 'w'           
            # Các nước ăn chéo

        if self.board[r + moveAmount][c] == "--": #kiểm tra ô phía trước pawn là trống
            # pawn chỉ được di chuyển khi không khóa hoặc hướng đang bị ghìm
            if not piecePinned or pinDirection == (moveAmount, 0):
                moves.append(Move((r, c), (r + moveAmount, c), self.board))
                if r == startRow and self.board[r + 2 * moveAmount][c] == "--": #kiểm tra 2 ô phía trước có trống không
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))
        #kiếm tra ăn chéo trái
        if c - 1 >= 0 : 
            #không bị khóa hoặc hướng bị khóa cho phép đi sang trái
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c  - 1][0] == enemyColor:  
                    moves.append(Move((r,c),(r+moveAmount, c-1), self.board))
                #kiểm tra có vị trí cho phép bắt tốt qua đường không
                if (r + moveAmount,c - 1) == self.enPassantPossible: 
                    moves.append(Move((r, c), (r + moveAmount, c-1),self.board, isEnPassantMove = True ))
        # Kiểm tra ăn chéo phải
        if c + 1 <= 7 :
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:  
                    moves.append(Move((r,c), (r + moveAmount, c+1), self.board))
                if (r+moveAmount, c+1) == self.enPassantPossible:
                    moves.append(Move((r,c),(r + moveAmount, c+1), self.board, isEnPassantMove =  True))

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()  # Hướng bị ghìm
        # Kiểm tra xem quân cờ có bị khóa hay không
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':  
                    # Chỉ loại bỏ quân bị khóa nếu không phải là Hậu
                    #vì hậu kh bị khóa bởi quân cờ  tại có thể di chuyển theo cả hàng và cột
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Các hướng di chuyển của quân Xe
        enemyColor = 'b' if self.whiteToMove else 'w'  # Màu quân địch

        for direction in directions:
            for i in range(1, 8):  # Di chuyển tối đa 7 ô theo hướng
                endRow = r + direction[0] * i
                endCol = c + direction[1] * i
                
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Kiểm tra xem có nằm trong bàn cờ
                    if not piecePinned or pinDirection == direction or pinDirection == (-direction[0], -direction[1]):
                        #endPiece là các ô của quân rook di chuyển
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # Nếu ô đó trống
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:  # Nếu có quân địch
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break  # Quân Xe không thể tiếp tục sau khi ăn quân địch
                        else:
                            break  # Nếu gặp quân cùng màu
                else:
                    break  # Dừng lại nếu quân bị khóa

    def getKnightMoves(self, r, c, moves):
        piecePinned = False  # Quân cờ có đang khóa không (di chuyển vua sẽ bị chiếu)
        # Kiểm tra xem quân cờ có bị khóa hay không
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break  # Không cần xóa quân khóa, chỉ cần đánh dấu là bị khóa

        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        allyColor ='w' if self.whiteToMove else 'b' # Xác định quan cung mau
        
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Kiểm tra nước đi có trong bàn cờ không
                if not piecePinned:  # Nếu quân không bị khóa
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: # Nếu ô đó trống hoặc có quân địch
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        piecePinned = False  # quân cờ có đang khóa ko (di chuyển vua sẽ bị chiếu)
        pinDirection = ()  # hướng mà quân cờ bị khóa có thế di chuyển dễ vua k bị chiếu
         # Kiểm tra xem quân cờ có bị khóa hay không
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break        
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        enemyColor = "b" if self.whiteToMove else "w"
        for direction in directions: 
            for i in range(1,8):
                endRow = r + direction[0] * i
                endCol = c + direction[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == direction or pinDirection == (-direction[0], -direction[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c), (endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c), (endRow,endCol),self.board))
                            break
                        else:
                            break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1,  0,  0,  1,  1, 1) 
        colMoves = ( 1,  0,  1, -1,  1, -1 , 0, 1)    
        allyColor = 'w' if self.whiteToMove else 'b'  # Xác định màu quân đồng đội
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Kiểm tra nước đi có trong bàn cờ không
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  #nếu không phải quân cùng màu
                    if allyColor == "w":
                       self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow,endCol)
                    in_check, pins, checks =self.checkForPinsAndChecks()
                    if not in_check:
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    if allyColor == "w":
                        self.whiteKingLocation = (r,c)
                    else:
                        self.blackKingLocation = (r,c)
                
    def getCastleMoves (self ,r , c, moves):
        if self.squareUnderAttack (r,c):
            return
        if (self.whiteToMove and self.current_Castling_Rights.wK_Side) or (not self.whiteToMove and self.current_Castling_Rights.bK_Side):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.current_Castling_Rights.wQ_Side) or (not self.whiteToMove and self.current_Castling_Rights.bQ_Side):
            self.getQueenSideCastleMoves(r, c, moves)

    def getKingSideCastleMoves (self, r, c, moves):  #kiếm tra casling phía vua có hợp lệ không
        # kiểm tra các ô sẽ di chuyển tới có rỗng không
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
             # kiểm tra các ô này có bị 1 quân cờ khác tấn công không
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove = True))
    
    def getQueenSideCastleMoves(self, r, c, moves): # kiểm tra phía hậu, tương tự phía vua
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove = True))

class CastleRights():
    def __init__(self,wK_Side, bK_Side, wQ_Side, bQ_Side):
        #Nhap thanh ben phia vua
        self.wK_Side = wK_Side 
        self.bK_Side = bK_Side
        #nhap thanh ben phia hau
        self.wQ_Side = wQ_Side
        self.bQ_Side = bQ_Side



class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k , v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles =  {v: k for k , v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnPassantMove=False, isCastleMove = False):
        self.startRow = startSq[0] # vị trí bắt đầu
        self.startCol = startSq[1] 
        self.endRow = endSq[0] #vị trí kết thúc
        self.endCol = endSq[1]
        #trong class GameSate có 1 list move , mỗi ptu trong list này là 1 obj move gồm (pos_start,pos_end)
        self.pieceMoved = board[self.startRow][self.startCol] # start_end được dùng để đối chiếu lên  bàn cờ xem đây là quân cờ nào
        self.pieceCaptured = board[self.endRow][self.endCol] #ô cờ mà quân cò di chuyển đến
        #biến kiểm tra xem quân tốt có thỏa dk để phong hậu khôn
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7)
        #Enpassant bat tot qua duong
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"
        #CastleMove : nhap thanh
        self.isCastleMove = isCastleMove


        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol

    def __eq__(self, other) :
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):# Lấy ký hiệu cờ vua từ vị trí bắt đầu và kết thúc
        return self.getRankFile(self.startRow,self.startCol) + "->"+ self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self, r,c): # chuyen doi vi tri theo quy tat co vua
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    def getChessInfo (self):
        pieceInfo = self.pieceMoved
        return pieceInfo
