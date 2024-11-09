import pygame as p
import ChessEngine 
import random
#thông tin về bàn cờ
WIDTH = HEIGHT = 512 # kích thước 
DIMENSION = 8 # số ô cờ
SQ_SIZE = HEIGHT // DIMENSION # kích thước các ô cờ
MAX_FPS = 20 #  tốc độ khung hình khi di chuyển chuột
IMAGES = {} # 1 dict để lưu các quân cờ
#Hàm  load các hình ảnh quân cờ
def loadImages():
    pieces = ['wp','wR','wN','wB','wK', 'wQ','bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main_menu():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT)) # tạo kích thước cửa sổ 
    p.display.set_caption("Chess Game - Choose Mode") # tiêu đề
    font = p.font.SysFont("Arial", 32)
    clock = p.time.Clock() # khởi tạo  clock để điều khiể fps

    while True:
        screen.fill(p.Color("white")) # làm sạch màn hình = màu trắng 

        # Hiển thị hai tùy chọn
        pvp_text = font.render("1. Player vs Player", True, p.Color("black"))
        pvai_text = font.render("2. Player vs AI", True, p.Color("black"))
        # vẽ văn bản lên màn hình 
        screen.blit(pvp_text, (WIDTH // 2 - pvp_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(pvai_text, (WIDTH // 2 - pvai_text.get_width() // 2, HEIGHT // 2 + 20))

        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                return None
            elif e.type == p.KEYDOWN: # nhấn phím để lựa chọn chế độ chơi
                if e.key == p.K_1:  # nhấn phím 1 để người vs người
                    return "PvP"
                elif e.key == p.K_2:   # nhấn 2 để người và máy
                    return "PvAI"

        p.display.flip()
        clock.tick(MAX_FPS)


def start_pvp():
    screen = p.display.set_mode((WIDTH, HEIGHT))  # Tạo cửa sổ trò chơi
    clock = p.time.Clock()  # Tạo đối tượng clock để điều khiển tốc độ khung hình
    screen.fill(p.Color("white"))  # Làm sạch màn hình với màu trắng
    gs = ChessEngine.GameState()  # Khởi tạo trạng thái trò chơi
    validMoves = gs.getValidMoves()  # Lấy danh sách các nước đi hợp lệ
    moveMade = False  # Biến theo dõi xem đã có nước đi nào được thực hiện hay chưa
    animate = False  # Biến theo dõi xem có cần hiệu ứng chuyển động không
    loadImages()  # Tải ảnh quân cờ
    running = True  # Biến điều khiển vòng lặp trò chơi
    sqSelected = ()  # Biến lưu vị trí ô được chọn
    playerClicks = []  # Danh sách các lần nhấp chuột của người chơi
    gameOver = False  # Biến xác định liệu trò chơi đã kết thúc chưa

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:  # Nếu người chơi đóng cửa sổ
                running = False  # Thoát khỏi vòng lặp
            elif e.type == p.MOUSEBUTTONDOWN:  # Nếu người chơi nhấp chuột
                if not gameOver:
                    location = p.mouse.get_pos()  # Lấy vị trí chuột
                    col = location[0] // SQ_SIZE  # Tính cột
                    row = location[1] // SQ_SIZE  # Tính hàng
                    if sqSelected == (row, col):  # Nếu ô đã chọn giống ô vừa nhấp
                        sqSelected = ()  # Deselect ô
                        playerClicks = []  # Xóa danh sách các lần nhấp chuột
                    else:
                        sqSelected = (row, col)  # Chọn ô mới
                        playerClicks.append(sqSelected)  # Thêm ô vào danh sách nhấp chuột

                    if len(playerClicks) == 2:  # Nếu đã chọn 2 ô
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)  # Tạo nước đi từ 2 ô
                        for i in range(len(validMoves)):  # Kiểm tra xem nước đi có hợp lệ không
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])  # Thực hiện nước đi
                                if move.isPawnPromotion:  # Nếu quân tốt lên hàng cuối
                                    chosenPiece = choosePromotionPiece(screen, move.pieceMoved[0])  # Chọn quân mới
                                    gs.board[move.endRow][move.endCol] = chosenPiece  # Phong quân tốt thành quân mới
                                moveMade = True  # Đánh dấu đã có nước đi
                                animate = True  # Kích hoạt hiệu ứng di chuyển
                                sqSelected = ()  # Reset ô đã chọn
                                playerClicks = []  # Reset danh sách các lần nhấp chuột
                        if not moveMade:  # Nếu không có nước đi hợp lệ
                            playerClicks = [sqSelected]  # Lưu lại ô đã chọn để tiếp tục di chuyển

            elif e.type == p.KEYDOWN:  # Nếu nhấn phím
                if e.key == p.K_z:  # Phím 'z' để hoàn tác
                    gs.undoMove()  # Hoàn tác nước đi
                    animate = False  # Tắt hiệu ứng
                    moveMade = True  # Đánh dấu đã có nước đi
                if e.key == p.K_r:  # Phím 'r' để làm lại trò chơi
                    gs = ChessEngine.GameState()  # Khởi tạo lại trạng thái trò chơi
                    validMoves = gs.getValidMoves()  # Lấy danh sách các nước đi hợp lệ
                    sqSelected = ()  # Reset ô đã chọn
                    playerClicks = []  # Reset danh sách nhấp chuột
                    moveMade = False  # Reset trạng thái nước đi
                    animate = False  # Tắt hiệu ứng

        if moveMade:  # Nếu đã có nước đi
            if animate:  # Nếu cần hiệu ứng di chuyển
                animateMove(gs.moveLog[-1], screen, gs.board, clock)  # Hiển thị hiệu ứng di chuyển
            validMoves = gs.getValidMoves()  # Lấy lại danh sách nước đi hợp lệ
            moveMade = False  # Reset trạng thái nước đi

        drawGameState(screen, gs, validMoves, sqSelected)  # Vẽ trạng thái trò chơi lên màn hình

        if gs.checkMate:  # Nếu ván cờ kết thúc bằng chiếu hết
            gameOver = True  # Đánh dấu trò chơi kết thúc
            if gs.whiteToMove:
                drawEndGameText(screen, "Vua Trang Da Bi Chieu")  # Hiển thị thông báo vua trắng bị chiếu
            else:
                drawEndGameText(screen, "Vua Den Da Bi Chieu")  # Hiển thị thông báo vua đen bị chiếu
        if gs.staleMate:  # Nếu ván cờ kết thúc bằng hòa do bí
            gameOver = True  # Đánh dấu trò chơi kết thúc
            drawEndGameText(screen, "Hoa")  # Hiển thị thông báo hòa

        clock.tick(MAX_FPS)  # Giới hạn tốc độ khung hình
        p.display.flip()  # Cập nhật màn hình

# Tạo IA
def start_pvai(): # chưa được chỉnh sửa từ các hàm minimax vẫn đang ở tình trạng cũ : chưa test
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and gs.whiteToMove:  
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade: 
                            playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    animate = False
                    moveMade = True
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False

        if not gs.whiteToMove and not gameOver: 
            ai_move = findBestMove(gs, validMoves)  
            if ai_move:
                gs.makeMove(ai_move)
                moveMade = True
                animate = True

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen,"Vua Trang Da Bi Chieu")
            else:
                drawEndGameText(screen,"Vua Den Da Bi Chieu")
        if gs.staleMate:
            gameOver = True
            drawEndGameText("Hoa")

        clock.tick(MAX_FPS)
        p.display.flip()

def findBestMove(gs, validMoves): # chưa được định nghĩa
    if validMoves:
        return random.choice(validMoves)
    return None

def minimax(gs, depth, maxPlayer, alpha, beta): # thuật toán minimax cắt tỉa alpha beta
    validMoves = gs.getValidMoves()  # Lấy tất cả các nước đi hợp lệ
    if depth == 0 or gs.checkMate or gs.staleMate:
        return scoreBoard(gs)  # Trả về điểm của bảng cờ tại vị trí này

    if maxPlayer:  # Maximizing player (AI)
        maxEval = float('-inf')
        for move in validMoves:
            gs.makeMove(move)  # Thực hiện nước đi
            eval = minimax(gs, depth - 1, False, alpha, beta)  # Đệ quy cho minimizing player
            gs.undoMove()  # Hoàn tác nước đi
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:  # Cắt tỉa nếu không cần phải xét tiếp nhánh này
                break
        return maxEval
    else:  # Minimizing player (Đối thủ)
        minEval = float('inf')
        for move in validMoves:
            gs.makeMove(move)  # Thực hiện nước đi
            eval = minimax(gs, depth - 1, True, alpha, beta)  # Đệ quy cho maximizing player
            gs.undoMove()  # Hoàn tác nước đi
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:  # Cắt tỉa nếu không cần phải xét tiếp nhánh này
                break
        return minEval
def scoreBoard(gs): # hảm đánh giá để áp dụng minimax
    # các đánh giá hiện có: 
    # Tiêu chí 1: Dựa vào số quân theo màu đang có trên board (done)
    #  lượt của max thì ứng với mỗi quân trăng sẽ + điểm và - điểm khi có quân đen: score của max sẽ có xu hướng lớn và dương
    # lượt của min thì ngược lại : score của min có xu hướng thấp và có thể âm
    # Tiêu chí 2: Mỗi quân cờ khi ở các vị trí thuận lợi sẽ được cộng thêm điểm (chưa)
    # Tiêu chí 3:Kiểm soát vị trí trung tâm (done)
    center_positions = {(3, 3), (3, 4), (4, 3), (4, 4)}
    # Tiêu chí 4: Tính Linh Hoạt và Số Lượng Nước Đi Hợp Lệ (chưa)
    # Tiêu chí 5 : Bảo Vệ và Tấn Công (chưa)
    # Tiêu chí 6 :Cấu Trúc Tốt (Quân Tốt và Chuỗi Tốt) (chưa)
    # Tiêu chí 7 :Sự An Toàn của Vua (chưa)
    # Tiêu chí 8 : Vị Trí của Quân Xe và Hậu Khả Năng Tấn Công vào Vùng của Đối Thủ (chưa)
    # Tiêu chí 9 : Khả Năng Tấn Công vào Vùng của Đối Thủ (chưa)
    score = 0
    for row in len (gs.board):
        for col in len (gs.board[row]):
            square=gs.board[row][col]
            if square != '--':  # Nếu không phải ô trống
                piece_val = pieceValue(square)  # Giá trị quân cờ
                piece_color = square[0]  # Màu của quân cờ (Trắng = 'w', Đen = 'b')

                if piece_color == 'w':  # Nếu quân là quân trắng (maxPlayer)
                    score += piece_val
                elif piece_color == 'b':  # Nếu quân là quân đen (minPlayer)
                    score -= piece_val

                #  Tiêu chí 2: Đánh giá vị trí của quân cờ nếu ở 1 vị trí có lợi
                if square[1] == 'N':  # Nếu là quân Mã
                    score += knightPositionValue(square, gs)
                elif square[1] == 'R':  # Nếu là quân Xe
                    score += rookPositionValue(square, gs)
                elif square[1] == 'Q':  # Nếu là quân Hậu
                    score += queenPositionValue(square, gs)
                elif square[1] == 'P':  # Tốt
                    score += pawnPositionValue(square, gs)
                elif square[1] == 'K':  # Vua
                    score += kingPositionValue(square, gs)

                # Tiêu chí 3: Đánh giá vị trí trung tâm
                piece_pos=(row,col)
                if piece_pos in center_positions:
                    if piece_color == 'w': # Quân trắng ở trung tâm
                       score += 0.5
                else:  # Quân đen ở trung tâm
                    score -= 0.5


                

                # Có thể thêm các yếu tố chiến lược khác vào

    return score

def knightPositionValue(piece, gs):
    # Đánh giá vị trí quân Mã trên bàn cờ (đánh giá cao cho Mã ở trung tâm)
    knight_positions = {
        (3, 3): 3, (3, 4): 3, (4, 3): 3, (4, 4): 3,  # Trung tâm
        # Có thể thêm các vị trí khác
    }
    return knight_positions.get(piece[0], 0)

def rookPositionValue(piece, gs):
    # Đánh giá vị trí quân Xe (Ví dụ, Xe mạnh khi kiểm soát các đường thẳng)
    rook_positions = {
        (0, 0): 5, (0, 7): 5, (7, 0): 5, (7, 7): 5,  # Các góc quan trọng
        # Các đường thẳng khác
    }
    return rook_positions.get(piece[0], 0)

def queenPositionValue(piece, gs):
    # Đánh giá vị trí quân Hậu, quân Hậu mạnh khi kiểm soát cả các hàng, cột và đường chéo
    queen_positions = {
        (3, 3): 10, (3, 4): 10, (4, 3): 10, (4, 4): 10,  # Trung tâm
        # Có thể thêm các vị trí khác
    }
    return queen_positions.get(piece[0], 0)

def pawnPositionValue(piece, position):
    row, col = position

    # Bảng điểm cho quân Tốt theo vị trí trên bàn cờ.
    # Giá trị ở các hàng cao hơn khuyến khích quân Tốt tiến về phía đối thủ.
    pawn_position_scores = [
        [0, 0, 0, 0, 0, 0, 0, 0],         # Hàng 0
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],  # Hàng 1
        [0.5, 1, 1, 1, 1, 1, 1, 0.5],       # Hàng 2
        [0.5, 1, 2, 2, 2, 2, 1, 0.5],       # Hàng 3
        [0.5, 1, 2, 2, 2, 2, 1, 0.5],       # Hàng 4
        [0.5, 1, 1, 1, 1, 1, 1, 0.5],       # Hàng 5
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],  # Hàng 6
        [0, 0, 0, 0, 0, 0, 0, 0]            # Hàng 7
    ]

    # mục đích là white gần row 0 thì có điểm cao, black thì gần row 7 có giá trị cao
    # nhưng vì black đi từ trên xuống nên ta cần 
    # Nếu là quân Tốt đen:
    # ví trị black đang ở row 5 thì sẽ là [7-5][col]=[2][cpl] 
    # tốt trăng thì dùng index của pawn_position_scores
    return pawn_position_scores[row][col] if piece[0] == 'w' else pawn_position_scores[7-row][col]

def kingPositionValue(piece, position, endgame=False): # chưa hoàn thiện xong, biến endgame này chưa được định nghĩa
    row, col = position
    # Đánh giá vị trí của Vua ở giai đoạn mở đầu
    opening_position_scores = [
        [2, 2, 1, 0, 0, 1, 2, 2],  # Hàng 0
        [2, 2, 1, 0, 0, 1, 2, 2],  # Hàng 1
        [1, 1, 0, 0, 0, 0, 1, 1],  # Hàng 2
        [0, 0, 0, 0, 0, 0, 0, 0],  # Hàng 3
        [0, 0, 0, 0, 0, 0, 0, 0],  # Hàng 4
        [1, 1, 0, 0, 0, 0, 1, 1],  # Hàng 5
        [2, 2, 1, 0, 0, 1, 2, 2],  # Hàng 6
        [2, 3, 1, 0, 0, 1, 3, 2]   # Hàng 7
    ]
    # Đánh giá vị trí của Vua ở tàn cuộc
    endgame_position_scores = [
        [0, 0, 1, 2, 2, 1, 0, 0],  # Hàng 0
        [0, 1, 2, 3, 3, 2, 1, 0],  # Hàng 1
        [1, 2, 3, 4, 4, 3, 2, 1],  # Hàng 2
        [2, 3, 4, 5, 5, 4, 3, 2],  # Hàng 3
        [2, 3, 4, 5, 5, 4, 3, 2],  # Hàng 4
        [1, 2, 3, 4, 4, 3, 2, 1],  # Hàng 5
        [0, 1, 2, 3, 3, 2, 1, 0],  # Hàng 6
        [0, 0, 1, 2, 2, 1, 0, 0]   # Hàng 7
    ]
    if endgame:
        return endgame_position_scores[row][col]
    else:
        return opening_position_scores[row][col]


def pieceValue(piece): # Đánh giá giá trị quân cờ, ví dụ: quân tốt = 1, quân mã = 3, quân xe = 5, v.v.
    pieceValues = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000}
     # Dùng chữ cái thứ 2 trong chuỗi như 'P', 'N', 'R', v.v. 
     #nếu k có quân cờ trả về giá trị 0
    return pieceValues.get(piece[1], 0) 

def aiMove(gs): # hàm IA di chuyển chưa chỉnh sửa
    validMoves = gs.getValidMoves()
    bestMove = None
    bestScore = float('-inf')

    for move in validMoves:
        gs.makeMove(move)
        boardScore = minimax(gs, 3, False, float('-inf'), float('inf'))  # Sử dụng độ sâu 3 để tìm kiếm nước đi
        gs.undoMove()

        if boardScore > bestScore:
            bestScore = boardScore
            bestMove = move

    return bestMove



def highlightMoves(screen, gs, validMoves, sqSelected): # tô màu các ô di chuyển
    # nếu đã chọn 1 ô
    if sqSelected != ():
        #lấy vị trí ô đó
        r, c = sqSelected
        piece = gs.board[r][c]
        #check màu 
        if piece[0] == ('w' if gs.whiteToMove else 'b'): 
            # tô màu cho ô cờ
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # tô màu  xanh cho ô cờ hợp lệ và đỏ cho ô cờ có quân địch đang đứng trên đó
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    if gs.board[move.endRow][move.endCol] != "--":  
                        s.fill(p.Color('red'))  
                    else:
                        s.fill(p.Color('lightgreen')) 
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))



def drawGameState(screen, gs, validMoves, sqSelected): # thực hiện vẽ
    drawBoard(screen)  
    drawPieces(screen, gs.board)
    highlightMoves(screen, gs, validMoves, sqSelected)

def drawBoard(screen): #vẽ bàn cờ và  các ô cờ trắng đen
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board): # vẽ các quân cờ lên bàn cờ
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # Nếu ô không trống
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
 

def animateMove(move, screen, board , clock): # hiệu ứng chuyển động  khi di chuyển 1 quân cờ
    global colors
    # tinh toan khoang cach 
    dR = move.endRow - move.startRow 
    dC = move.endCol - move.startCol
    # toc do khung hinh (sqeed tang thi khung hinh giam)
    frameSpeed  = 5
    frameCount = (abs(dR) + abs(dC)) * frameSpeed

    for frame in range (frameCount + 1):
        r ,c  =(move.startRow + dR*frame/frameCount, move.startCol +dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquares = p.Rect(move.endCol* SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen, color, endSquares)

        if move.pieceCaptured != '--':
            screen.blit (IMAGES[move.pieceCaptured], endSquares)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawEndGameText (screen, text): # in ra thông báo kết thúc
    font = p.font.SysFont("Arial", 32, True, False)
    textObject =font.render(text, 0, p.Color("Black"))
    textLocation = p .Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2,
                                                    HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject,textLocation)


def choosePromotionPiece(screen, color): # lựa chọn các quân khi phong tốt 
    promotionPieces = ['Q', 'R', 'B', 'N']  
    pieceImages = {}
    # duyệt qua các quân cờ và tải ảnh lên
    for piece in promotionPieces:
        pieceImages[piece] = p.transform.scale(p.image.load(f"images/{color + piece}.png"), (SQ_SIZE, SQ_SIZE)) 
    #tạo list ô lựa chọn để nhấp dô
    choiceRect = [p.Rect((WIDTH - (len(promotionPieces) * SQ_SIZE)) // 2 + i * SQ_SIZE, HEIGHT // 2 - SQ_SIZE // 2, SQ_SIZE, SQ_SIZE) for i in range(len(promotionPieces))]

    #vòng lặp kiểm tra khi nhấp chuột
    #vị trí nhấp chuột có đúng vào ô  list các quân có thể phong lên không
    while True:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                mouseX, mouseY = p.mouse.get_pos()
                for i, rect in enumerate(choiceRect):
                    if rect.collidepoint(mouseX,mouseY):
                        return color + promotionPieces[i]
        
        for i, rect in enumerate(choiceRect):
            screen.blit(pieceImages[promotionPieces[i]], rect)
            p.draw.rect(screen,p.Color("black"), rect,1)
        
        p.display.flip()
            
if __name__ == "__main__":
    mode = main_menu()
    if mode == "PvP":
        start_pvp()
    elif mode == "PvAI":
        start_pvai()
