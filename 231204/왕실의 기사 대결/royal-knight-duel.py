from collections import deque

def inputs():
    global L, N, Q, board, knights, commands, k_board, chess
    board = []
    knights = [0]
    commands = []
    L, N, Q = map(int, input().split())
    k_board = [[0] * L for _ in range(L)]
    chess = dict()

    for _ in range(L):
        board.append(list(map(int, input().split())))

    for i in range(1, N + 1):
        r, c, h, w, k = map(int, input().split())
        knights.append([r - 1, c - 1, h, w, k])
        chess[i] = []
        for j in range(h):
            for k in range(w):
                k_board[r - 1 + j][c - 1 + k] = i
                chess[i].append([r - 1 + j, c - 1 + k])

    
    for _ in range(Q):
        i, d = map(int, input().split())
        commands.append([i, d])

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

inputs()
damage = [0] * (N + 1)
for i, d in commands:
    if knights[i] == 0:
        continue
    
    wall = 0
    x, y, h, w, k = knights[i]
    q = deque()
    q.append([x, y])
    check = [[0] * L for _ in range(L)]
    check[x][y] = 1

    move_k = [0] * (N + 1)
    move_k[i] = 1

    while q:
        x, y = q.popleft()
        for c in range(4):
            nx, ny = x + dx[c], y + dy[c]
            if 0 <= nx < L and 0 <= ny < L:
                if check[nx][ny] == 0:
                    if k_board[x][y] == k_board[nx][ny]:
                        q.append([nx, ny])
                        check[nx][ny] = 1
            if d == c: # 다른 기사 미는지 또는 벽인지 확인
                if 0 <= nx < L and 0 <= ny < L:
                    if check[nx][ny] == 0:
                        if k_board[nx][ny] > 0 and k_board[nx] != k_board[x][y]:
                            check[nx][ny] = 1
                            move_k[k_board[nx][ny]] = 1
                            q.append([nx, ny])
                        if board[nx][ny] == 2:
                            wall = 1
                            break
                else:
                    wall = 1
                    break
        if wall == 1:
            break

    tmp_k_board = [[0] * L for _ in range(L)]
    if wall == 0:
        for idx in range(1, N + 1):
            if move_k[idx] == 1:
                tmp_chess = []
                for x, y in chess[idx]:
                    nx = x + dx[d]
                    ny = y + dy[d]
                    tmp_k_board[nx][ny] = idx
                    tmp_chess.append([nx, ny])
                chess[idx] = tmp_chess
                knights[idx][:2] = chess[idx][0]

        for x in range(L):
            for y in range(L):
                if k_board[x][y] > 0 and tmp_k_board[x][y] == 0:
                    if move_k[k_board[x][y]] == 1:
                        k_board[x][y] = 0
                if tmp_k_board[x][y] > 0:
                    k_board[x][y] = tmp_k_board[x][y]
        for x in range(L):
            for y in range(L):
                if board[x][y] == 1 and k_board[x][y] > 0:
                    idx = k_board[x][y]
                    if move_k[idx] == 1 and idx != i:
                        if knights[idx] != 0:
                            knights[idx][-1] -= 1
                            damage[idx] += 1
                            if knights[idx][-1] == 0:
                                knights[idx] = 0
                                damage[idx] = 0
                                for xx, yy in chess[idx]:
                                    k_board[xx][yy] = 0
                                continue

print(sum(damage))