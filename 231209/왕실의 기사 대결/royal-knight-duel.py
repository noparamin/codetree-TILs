from collections import deque

def inputs():
    global L, N, Q, board, k_board, knights, commands, k_dic

    L, N, Q = map(int, input().split())
    board = []
    for i in range(L):
        board.append(list(map(int, input().split())))
    
    k_board = [[0] * L for _ in range(L)]
    knights = [0]
    k_dic = {}
    for i in range(1, N + 1):
        r, c, h, w, k = map(int, input().split())
        knights.append([r - 1, c - 1, h, w, k])
        k_dic[i] = []

        for j in range(h):
            for k in range(w):
                k_board[r + j - 1][c + k - 1] = i
                k_dic[i].append([r + j - 1, c + k - 1])


    commands = []
    for _ in range(Q):
        commands.append(list(map(int, input().split())))
    
inputs()

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

damage = [0] * (N + 1)
for i, d in commands:
    if k_dic[i] == 0:
        continue
    x, y, h, w, k = knights[i]
    q = deque()
    moved = [0] * (N + 1)
    visited = [[0] * L for _ in range(L)]

    q.append(k_dic[i][0])
    moved[i] = 1
    visited[x][y] = 1

    wall = 0
    while q:
        x, y = q.popleft()

        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]

            if 0 <= nx < L and 0 <= ny < L:
                if not visited[nx][ny]:
                    if d != k: # 방향 다름
                        if k_board[x][y] != k_board[nx][ny]: # 미는 방향이 아니고 현재 기사가 아님
                            continue
                        visited[nx][ny] = 1
                        q.append([nx, ny])
                    else: # 죽은 기사인지 체크 로직 필요
                        if board[nx][ny] == 2:
                            wall = 1
                            break
                        if k_board[nx][ny] == 0:
                            break

                        if k_board[x][y] != k_board[nx][ny] and k_board[nx][ny] > 0:
                            moved[k_board[nx][ny]] = 1
                        visited[nx][ny] = 1
                        q.append([nx, ny])
            else:
                if d == k:
                    wall = 1
                    break

            if wall == 1:
                break
        if wall == 1:
            break
    
    if wall == 0:
        # 벽 없으면 이동과 데미지 계산
        tmp_k_board = [[0] * L for _ in range(L)]
        tmp_k_dic = {}
        for idx in range(1, N + 1):
            if moved[idx] and k_dic[idx] != 0:
                tmp_k_dic[idx] = []
                #k_board, k_dic 갱신
                for x, y in k_dic[idx]:
                    nx, ny = x + dx[d], y + dy[d]
                    tmp_k_board[nx][ny] = idx
                    tmp_k_dic[idx].append([nx, ny])
                k_dic[idx] = tmp_k_dic[idx]
                knights[idx][:2] = k_dic[idx][0]
        
        for x in range(L):
            for y in range(L):
                # 갱신
                # 만약 tmp 현재 좌표 0이고 k_board 현재좌표 0아니면: 0으로 갱신
                # 만약 tmp 현재 좌표 0 아니면 갱신
                if tmp_k_board[x][y] == 0 and k_board[x][y] != 0:
                    if moved[k_board[x][y]] == 1:
                        k_board[x][y] = 0
                elif tmp_k_board[x][y] != 0:
                    k_board[x][y] = tmp_k_board[x][y]  
        
        for x in range(L):
            for y in range(L):
                idx = k_board[x][y]
                if not moved[idx]:
                    continue
                if k_board[x][y] > 0 and board[x][y] == 1:
                    if k_board[x][y] != i and knights[idx][-1] > 0:
                        knights[idx][-1] -= 1
                        damage[idx] += 1
                        if knights[idx][-1] == 0:
                            k_dic[idx] = 0
                            damage[idx] = 0

print(sum(damage))