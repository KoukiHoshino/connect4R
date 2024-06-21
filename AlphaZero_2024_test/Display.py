import pygame

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BEIGE = (240, 160, 30)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (211,211,211,100)

class Display:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.square_size = 100
        self.square_width_num = self.screen_width // self.square_size
        self.square_height_num = self.screen_height // self.square_size
        self.clock = pygame.time.Clock()

        font = pygame.font.SysFont(None, 100, bold=False, italic=False)

        self.black_win_surface = font.render("Black Win!", False, BLACK, RED)
        self.white_win_surface = font.render("White Win!", False, WHITE, RED)
        self.draw_surface = font.render("Draw...", False, BLUE, RED)
        self.reset_surface = font.render("Click to reset!",False, BLACK, RED)
        self.reverse_surface = font.render("!!!!REVERSE!!!!",False, RED, WHITE)
        self.start_text = font.render("PLAY",True,WHITE)
        self.end_text = font.render("END",True,WHITE)

        self.start_button = pygame.Rect(self.screen_width/2-120,self.screen_height/2-50,240,70)
        self.end_button = pygame.Rect(self.screen_width/2-120,self.screen_height/2+70,240,70)

        #反転イベント
        self.reverse_num = 0

    def reverse(self, state):
        board = state.get_board()
        for _ in range(FPS*2):
            self.screen.fill(LIGHT_GRAY)
            self.draw_grid()
            self.draw_board(board)
            self.screen.blit(self.reverse_surface, (self.screen_width/2-300,self.screen_height/2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            pygame.display.update()
            self.clock.tick(FPS)
        
    def draw_grid(self):
        for i in range(self.square_width_num):
            #縦線
            pygame.draw.line(self.screen, BLACK, (i * self.square_size, 0), (i * self.square_size, self.screen_height), 3)
        for i in range(self.square_height_num):
            #横線
            pygame.draw.line(self.screen, BLACK, (0, i * self.square_size), (self.screen_width, i * self.square_size), 3)

    def draw_board(self,board):
        for row_index, row in enumerate(board):
            for col_index, col in enumerate(row):
                if col == 1:
                    pygame.draw.circle(self.screen, BLACK, (col_index * self.square_size + 50, row_index * self.square_size + 50), 45)
                elif col == -1:
                    pygame.draw.circle(self.screen, WHITE, (col_index * self.square_size + 50, row_index * self.square_size + 50), 45)

    def put_stone(self, state):
        board = state.get_board()
        run = True

        if self.reverse_num > state.reverse_num:
            self.reverse(state)
            self.reverse_num += 1
        
        while run:
            self.screen.fill(LIGHT_GRAY)
            self.draw_grid()
            self.draw_board(board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    x = mx // self.square_size
                    y = my // self.square_size
                    
                    str_index = state.action2str(y*self.square_width_num+x)
                    print(str_index)
                    return str_index

            pygame.display.update()
            self.clock.tick(FPS)

    def start(self):
        run = True
        x = y = 10
        while run:
            self.screen.fill(WHITE)
            pygame.draw.rect(self.screen, BLACK, self.start_button)
            pygame.draw.rect(self.screen, BLACK, self.end_button)

            self.screen.blit(self.start_text,(self.screen_width/2-90,self.screen_height/2-45))
            self.screen.blit(self.end_text,(self.screen_width/2-70,self.screen_height/2+75))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 終了イベント
                    run = False
                    pygame.quit()  #pygameのウィンドウを閉じる
                    #sys.exit() #システム終了
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        return True
                    if self.end_button.collidepoint(event.pos):
                        return False
            
            pygame.display.update()
        
    def end(self):
        pygame.quit()
    
    def result(self, win_color):
        run = True
        while run:
            if win_color == 1:
                self.screen.blit(self.black_win_surface, (230, 200))
            elif win_color == -1:
                self.screen.blit(self.white_win_surface, (230, 200))
            else:
                self.screen.blit(self.draw_surface, (230, 200))

            self.screen.blit(self.reset_surface, (180, 400))