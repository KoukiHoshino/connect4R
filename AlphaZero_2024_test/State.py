import numpy as np
BLACK, WHITE = 1, -1  # 先手後手

class State_osero:
    X, Y = 'ABCDEFG', '1234567'
    C = {0: '_', BLACK: '●', WHITE: '○',3:' '}

    def __init__(self):
        self.board = np.zeros((7, 7))  # (x, y)
        self.board[6,:] = 3
        self.board[:,6] = 3
        self.board[2][2], self.board[2][3] = WHITE, BLACK
        self.board[3][2], self.board[3][3] = BLACK, WHITE
        self.color = 1
        self.win_color = 3
        self.record = []
        self.dirs = [-8, -7, -6, -1, 1, 6, 7, 8]
        self.countB = 0
        self.countW = 0

    def action2str(self, a):
        return self.X[a // 7] + self.Y[a % 7]

    def str2action(self, s):
        return self.X.find(s[0]) * 7 + self.Y.find(s[1])

    def record_string(self):
        return ' '.join([self.action2str(a) for a in self.record])

    def __str__(self):
        # 表示
        s = '   ' + ' '.join(self.Y) + '\n'
        for i in range(7):
            s += self.X[i] + ' ' + ' '.join([self.C[self.board[i, j]] for j in range(7)]) + '\n'
        s += 'record = ' + self.record_string()
        return s
    
    def _check(self, board, move, flip=False):
        x, y = move // 7, move % 7
        if not (ret := False) and not board[x,y]:
          if move  != 0:

            for i in range(8):
               #8方向を精査
                count = value = move + self.dirs[i]

                x, y = value // 7, value % 7
                # if x >6:
                #    print("x")
                #try:
                while board[x,y] ==  -self.color:
                    #コマが相手のコマである場合は同じ動作を繰り返す
                    value += self.dirs[i]
                    x, y = value // 7, value % 7
                    if value >=49 or value < 0:
                        x,y = 6, 6
                        count = value
                        break
                if count != value and board[x,y] == self.color:
                    #もし自分のコマと挟めているのであれば置くことが可能としてvalueをリセットし配列に入れる
                    ret = value = move
                    while flip:
                        x, y = value // 7, value % 7
                        board[x,y]= self.color
                        value += self.dirs[i]
                        x, y = value // 7, value % 7
                        if board[x,y] == self.color:
                             break
                #except:
                 #  print("value",value)
                  # print("move",move)
                   #print("x",x)
                   #k = 0
          if move  == 0:
            #print('banana')
            for i in range(4,8):
               #8方向を精査
                count = value = move + self.dirs[i]
                x, y = value // 7, value % 7
                
                while board[x,y] ==  -self.color:
                  #コマが相手のコマである場合は同じ動作を繰り返す
                    value += self.dirs[i]
                    #print("success1")
                    x, y = value // 7, value % 7
                    if value >=49 or value < 0:
                         x,y = 6, 6
                         count = value
                         break
                         
                if count != value and board[x,y] == self.color:

                  #もし自分のコマと挟めているのであれば置くことが可能としてvalueをリセットし配列に入れる
                    value = move
                    ret = True
                    #print("success2")
                    while flip:
                        x, y = value // 7, value % 7
                        board[x,y]= self.color
                        value += self.dirs[i]
                        x, y = value // 7, value % 7
                        if board[x,y] == self.color:
                            break   
        return ret
    
    def legal_actions(self):
      valid_moves = []
      for i in range(7):
        for j in range(7):
            move = i * 6 + j
            if self._check(self.board, move, flip=False):
                valid_moves.append(move)
            
            #if len(valid_moves) == 0 :
              #return -1
      return valid_moves
    
    def play(self, action):
        # 行動で状態を進める関数
        # action は board 上の位置 (0 ~ 35) または行動系列の文字列
        if isinstance(action, str):
            for astr in action.split():
                self.play(self.str2action(astr))
            return self
        #print(f"action ={action}")
        x, y = action // 7, action % 7
        #print(f"x ={x}")
        #print(f"y ={y}")

        self._check(self.board, action, flip= True)
        self.board[x, y] = self.color
        actions = self.legal_actions()
        if np.all(self.board != 0) or not(actions): # 越川変更
        
        # if np.all(self.board != 0) or np.all(actions = None): # 越川変更
          for i in range(42):
            x, y = i // 7, i % 7
            if self.board[x,y] == 1:
              self.countB +=1
            if self.board[x,y] == -1:
              self.countW +=1
          #print(self.countB)
          #print(self.countW)
          if self.countB < self.countW:
            self.win_color == BLACK
            #print("BLACK win")
          elif self.countW > self.countB:
            self.win_color == WHITE
            #print("WHITE win")
          elif self.countW == self.countB:
            self.win_color == 0
            #print("DRAW")
          #print(self.terminal_reward)
        self.color = -self.color
        self.record.append(action)
        return self
    
    def terminal_reward(self):
      self.win_color = self.pass_drop()
       #print(self.win_color )
      return self.win_color if self.color == BLACK else -self.win_color
    
    def pass_drop(self):
      winner = 0
      self.countB = 0
      self.countW = 0
      for i in range(42):
        x, y = i // 7, i % 7
        if self.board[x,y] == 1:
          self.countB +=1
        if self.board[x,y] == -1:
          self.countW +=1
      #print(self.countW)
      #print(self.countB)
      if self.countB > self.countW:
        self.win_color == BLACK
        winner = BLACK

      elif self.countW > self.countB:
        self.win_color == WHITE
        winner = WHITE
      else:
        self.win_color == 0
      return winner

    def terminal(self):
     if np.all(self.board != 0) or self.win_color != 3:
        return True
     else:
        return False
    
    def feature(self):
        # ニューラルネットに入力する状態表現を返す
        return np.stack([self.board == self.color, self.board == -self.color]).astype(np.float32)


class State_7_7_4:
    '''○×ゲームの盤面実装'''
    X, Y = 'ABCDEFG',  '0123456'
    C = {0: '_', BLACK: 'O', WHITE: 'X'}

    def __init__(self):
        self.board = np.zeros((7, 7)) # (x, y)
        self.color = 1
        self.win_color = 0
        self.record = []
        self.reverse_num = 0
        self.round = 0

    def get_board(self):
       return self.board
    
    def action2str(self, a):
        return self.X[a // 7] + self.Y[a % 7]

    def str2action(self, s):
        return self.X.find(s[0]) * 7 + self.Y.find(s[1])

    def record_string(self):
        return ' '.join([self.action2str(a) for a in self.record])

    def __str__(self):
        # 表示
        s = '   ' + ' '.join(self.Y) + '\n'
        for i in range(7):
            s += self.X[i] + ' ' + ' '.join([self.C[self.board[i, j]] for j in range(7)]) + '\n'
        s += 'record = ' + self.record_string()
        return s

    def play(self, action, net, state):
        self.round += 1
        # 行動で状態を進める関数
        # action は board 上の位置 (0 ~ 8) または行動系列の文字列
        if isinstance(action, str):
            for astr in action.split():
                self.play(self.str2action(astr))
            return self

        x, y = action // 7, action % 7
        self.board[x, y] = self.color

        # 4つ揃ったか調べる(縦横)
        for i in range(4):
          if self.board[x,i:i+4].sum() == 4*self.color\
          or self.board[i:i+4,y].sum() == 4*self.color:
            self.win_color = self.color
        
        #置いた箇所の斜め
        #右斜め
        if x<=y:
          a = np.diag(self.board[0:,y-x:],k=0)
        else:
          a = np.diag(self.board[x-y:,0:],k=0)
        #左斜め
        if(x+y >= 6):
          b = np.diag((np.fliplr(self.board))[(x+y)-6:,0:],k=0)
        else:
          b = np.diag((np.fliplr(self.board))[0:,6-(x+y):],k=0)

        if len(a) > 3:
          for i in range (len(a)-3):
            if a[i:i+4].sum() == 4*self.color:
              self.win_color = self.color

        if len(b) > 3:
          for i in range (len(b)-3):
            if b[i:i+4].sum() == 4*self.color:
              self.win_color = self.color


        # # 3つ揃ったか調べる
        # if self.board[x, :].sum() == 5 * self.color \
        #   or self.board[:, y].sum() == 5 * self.color \
        #   or (x == y and np.diag(self.board, k=0).sum() == 5 * self.color) \
        #   or (x == 2 - y and np.diag(self.board[::-1,:], k=0).sum() == 5 * self.color):
        #     self.win_color = self.color

        #print("round: " + str(self.round))
        if self.jadge(net, state) and self.round >= 8 and self.reverse_num < 8:
           #if self.jadge(net, state):
              self.reverse()
              self.reverse_num += 1
              self.color = -self.color
        
        self.color = -self.color
        self.record.append(action)
        return self

    def terminal(self):
        # 終端状態かどうか返す
        return self.win_color != 0 or len(self.record) == 7 * 7 

    def terminal_reward(self):
        # 終端状態での勝敗による報酬を返す
        return self.win_color if self.color == BLACK else -self.win_color

    def legal_actions(self): #コードを変更
        # 可能な行動リストを返す
        vaild_pos = []
        for col in range(7):
           for row in range(6, -1, -1):
              if self.board[row, col] == 0:
                 vaild_pos.append(row*7+col)
                 break
        return vaild_pos

    def feature(self):
        # ニューラルネットに入力する状態表現を返す
        return np.stack([self.board == self.color, self.board == -self.color]).astype(np.float32)

    def jadge(self, net, state) -> bool:  #コードを書き加える
      _, v = net.predict(state)
      pt_upper_limit = 0.8 #上限 
      pt_lower_limit = 0.6 #下限
      print("reward: " + str(v))
      if pt_lower_limit <= v <= pt_upper_limit:
         return True 
      else:
         return False
    """  
    def reverse(self):
       for col in range(7):
          for row in range(7):
              self.board[row][col] *= -1
    """
    def reverse(self):
       for col in range(7):
          for row in range(6, -1, -1):
            if self.board[row][col] != 0:
              self.board[row][col] *= -1
            else:
               break


class State_3_3_3:
    '''○×ゲームの盤面実装'''
    X, Y = 'ABC',  '123'
    C = {0: '_', BLACK: 'O', WHITE: 'X'}

    def __init__(self):
        self.board = np.zeros((3, 3)) # (x, y)
        self.color = 1
        self.win_color = 0
        self.record = []

    def action2str(self, a):
        return self.X[a // 3] + self.Y[a % 3]

    def str2action(self, s):
        return self.X.find(s[0]) * 3 + self.Y.find(s[1])

    def record_string(self):
        return ' '.join([self.action2str(a) for a in self.record])

    def __str__(self):
        # 表示
        s = '   ' + ' '.join(self.Y) + '\n'
        for i in range(3):
            s += self.X[i] + ' ' + ' '.join([self.C[self.board[i, j]] for j in range(3)]) + '\n'
        s += 'record = ' + self.record_string()
        return s

    def play(self, action):
        # 行動で状態を進める関数
        # action は board 上の位置 (0 ~ 8) または行動系列の文字列
        if isinstance(action, str):
            for astr in action.split():
                self.play(self.str2action(astr))
            return self

        x, y = action // 3, action % 3
        self.board[x, y] = self.color

        # 3つ揃ったか調べる
        if self.board[x, :].sum() == 3 * self.color \
          or self.board[:, y].sum() == 3 * self.color \
          or (x == y and np.diag(self.board, k=0).sum() == 3 * self.color) \
          or (x == 2 - y and np.diag(self.board[::-1,:], k=0).sum() == 3 * self.color):
            self.win_color = self.color

        self.color = -self.color
        self.record.append(action)
        return self

    def terminal(self):
        # 終端状態かどうか返す
        return self.win_color != 0 or len(self.record) == 3 * 3

    def terminal_reward(self):
        # 終端状態での勝敗による報酬を返す
        return self.win_color if self.color == BLACK else -self.win_color

    def legal_actions(self):
        # 可能な行動リストを返す
        return [a for a in range(3 * 3) if self.board[a // 3, a % 3] == 0]

    def feature(self):
        # ニューラルネットに入力する状態表現を返す
        return np.stack([self.board == self.color, self.board == -self.color]).astype(np.float32)

class State_6_8_4:
    '''○×ゲームの盤面実装'''
    X, Y = 'ABCDEF',  '12345678'
    C = {0: '_', BLACK: 'O', WHITE: 'X'}

    def __init__(self):
        self.board = np.zeros((6, 8)) # (x, y)
        self.color = 1
        self.win_color = 0
        self.record = []
        self.reverse_num = 0
        self.round = 1
    
    def get_board(self):
       return self.board

    def action2str(self, a):
        return self.X[a // 8] + self.Y[a % 8]

    def str2action(self, s):
        return self.X.find(s[0]) * 8 + self.Y.find(s[1])

    def record_string(self):
        return ' '.join([self.action2str(a) for a in self.record])

    def __str__(self):
        # 表示
        s = '   ' + ' '.join(self.Y) + '\n'
        for i in range(6):
            s += self.X[i] + ' ' + ' '.join([self.C[self.board[i, j]] for j in range(8)]) + '\n'
        s += 'record = ' + self.record_string()
        return s
    
    def row_color(self, row_list :list) -> bool:
        color_count = 0
        for index in range(len(row_list)):
            if row_list[index] == self.color:
                color_count += 1
            else:
                color_count = 0
            if color_count == 4:
                return True
        return False

    #左上から右下
    def extract_diag(self, x, y) -> list:
        for i in range(x-1, -1, -1):
            y -= 1
        new_list = np.diag(self.board, k=y)
        return new_list
    
    #右上から左下
    def extract_diag2(self, x, y) -> list:
        for i in range(x, -1, -1):
            if y == 7:
                y += 1
                break
            y += 1
    
        new_list = []
        x = i
        y -= 1

        while(1):
            if x > 5 or y < 0:
                break
            new_list.append(self.board[x][y])
            x += 1
            y -= 1
        return new_list

    def play(self, action, net, state):
        # 行動で状態を進める関数
        # action は board 上の位置 (0 ~ 8) または行動系列の文字列
        if isinstance(action, str):
            for astr in action.split():
                self.play(self.str2action(astr))
            return self

        x, y = action // 8, action % 8
        self.board[x, y] = self.color

        """
        # 4つ揃ったか調べる
        if self.board[x, :].sum() == 4 * self.color \
          or self.board[:, y].sum() == 4 * self.color \
          or (x == y and np.diag(self.board, k=0).sum() == 4 * self.color) \
          or (x == 2 - y and np.diag(self.board[::-1,:], k=0).sum() == 4 * self.color):
            self.win_color = self.color
        """
        #4つ揃ったか調べる
        if self.row_color(self.board[x, :]) \
          or self.board[:, y].sum() == 4 * self.color \
          or self.row_color(self.extract_diag(x, y)) \
          or self.row_color(self.extract_diag2(x, y)):
            self.win_color = self.color
        
        print("round: " + str(self.round))
        if self.jadge(net, state) and self.reverse_num < 3 and self.round>8:
           #if self.jadge(net, state):
              self.reverse()
              self.reverse_num += 1
              self.color *= -1

        self.color = -self.color
        self.record.append(action)
        self.round += 1
        return self

    def terminal(self):
        # 終端状態かどうか返す
        return self.win_color != 0 or len(self.record) == 6 * 8

    def terminal_reward(self):
        # 終端状態での勝敗による報酬を返す
        return self.win_color if self.color == BLACK else -self.win_color

    ##############################################################
    def legal_actions(self): #コードを変更
        # 可能な行動リストを返す
        vaild_pos = []
        for col in range(8):
           for row in range(5, -1, -1):
              if self.board[row, col] == 0:
                 vaild_pos.append(row*8+col)
                 break
        return vaild_pos
        #return [a for a in range(6 * 8) if self.board[a // 8, a % 8] == 0]

    def feature(self):
        # ニューラルネットに入力する状態表現を返す
        return np.stack([self.board == self.color, self.board == -self.color]).astype(np.float32)
    
    ##################################################
    def jadge(self, net, state) -> bool:  #コードを書き加える
      p, v = net.predict(state)
      pt_upper_limit = 0.9 #上限 
      pt_lower_limit = 0.6 #下限
      print("v:" + str(v))
      if pt_lower_limit <= abs(v) <= pt_upper_limit:
         return True 
      else:
         return False
      
    def reverse(self):
       for col in range(8):
          for row in range(5, -1, -1):
            if self.board[row][col] != 0:
              self.board[row][col] *= -1
            else:
               break
            
class State_6_8_4_train:
    '''○×ゲームの盤面実装'''
    X, Y = 'ABCDEF',  '12345678'
    C = {0: '_', BLACK: 'O', WHITE: 'X'}

    def __init__(self):
        self.board = np.zeros((6, 8)) # (x, y)
        self.color = 1
        self.win_color = 0
        self.record = []
        self.reverse_num = 0
        self.round = 0

    def action2str(self, a):
        return self.X[a // 8] + self.Y[a % 8]

    def str2action(self, s):
        return self.X.find(s[0]) * 8 + self.Y.find(s[1])

    def record_string(self):
        return ' '.join([self.action2str(a) for a in self.record])

    def __str__(self):
        # 表示
        s = '   ' + ' '.join(self.Y) + '\n'
        for i in range(6):
            s += self.X[i] + ' ' + ' '.join([self.C[self.board[i, j]] for j in range(8)]) + '\n'
        s += 'record = ' + self.record_string()
        return s

    def row_color(self, row_list :list) -> bool:
        color_count = 0
        for index in range(len(row_list)):
            if row_list[index] == self.color:
                color_count += 1
            else:
                color_count = 0
            if color_count == 4:
                return True
        return False

    #左上から右下
    def extract_diag(self, x, y) -> list:
        for i in range(x-1, -1, -1):
            y -= 1
        new_list = np.diag(self.board, k=y)
        return new_list
    
    #右上から左下
    def extract_diag2(self, x, y) -> list:
        for i in range(x, -1, -1):
            if y == 7:
                y += 1
                break
            y += 1
    
        new_list = []
        x = i
        y -= 1

        while(1):
            if x > 5 or y < 0:
                break
            new_list.append(self.board[x][y])
            x += 1
            y -= 1
        return new_list

    def play(self, action):
        # 行動で状態を進める関数
        # action は board 上の位置 (0 ~ 8) または行動系列の文字列
        if isinstance(action, str):
            for astr in action.split():
                self.play(self.str2action(astr))
            return self

        x, y = action // 8, action % 8
        self.board[x, y] = self.color

        """
        # 4つ揃ったか調べる
        if self.board[x, :].sum() == 4 * self.color \
          or self.board[:, y].sum() == 4 * self.color \
          or (x == y and np.diag(self.board, k=0).sum() == 4 * self.color) \
          or (x == 2 - y and np.diag(self.board[::-1,:], k=0).sum() == 4 * self.color):
            self.win_color = self.color
        """

        #4つ揃ったか調べる
        if self.row_color(self.board[x, :]) \
          or self.board[:, y].sum() == 4 * self.color \
          or self.row_color(self.extract_diag(x, y)) \
          or self.row_color(self.extract_diag2(x, y)):
            self.win_color = self.color
        
        #print("round: " + str(self.round))

        self.color = -self.color
        self.record.append(action)
        self.round += 1
        return self

    def terminal(self):
        # 終端状態かどうか返す
        return self.win_color != 0 or len(self.record) == 6 * 8

    def terminal_reward(self):
        # 終端状態での勝敗による報酬を返す
        return self.win_color if self.color == BLACK else -self.win_color

    ##############################################################
    def legal_actions(self): #コードを変更
        # 可能な行動リストを返す
        vaild_pos = []
        for col in range(8):
           for row in range(5, -1, -1):
              if self.board[row, col] == 0:
                 vaild_pos.append(row*8+col)
                 break
        return vaild_pos
        #return [a for a in range(6 * 8) if self.board[a // 8, a % 8] == 0]

    def feature(self):
        # ニューラルネットに入力する状態表現を返す
        return np.stack([self.board == self.color, self.board == -self.color]).astype(np.float32)
    
    ##################################################
    def jadge(self, net, state) -> bool:  #コードを書き加える
      p, v = net.predict(state)
      pt_upper_limit = 0.7 #上限 
      pt_lower_limit = 0.6 #下限

      if pt_lower_limit <= v <= pt_upper_limit:
         return True 
      else:
         return False
      
    def reverse(self):
       for col in range(8):
          for row in range(5, -1, -1):
            if self.board[row][col] != 0:
              self.board[row][col] *= -1
            else:
               break