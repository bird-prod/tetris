import pygame
import random

# 初始化pygame
pygame.init()

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# 游戏设置
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("俄罗斯方块")

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]], # J
    [[1, 1, 0], [0, 1, 1]], # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        
    def new_piece(self):
        # 随机选择一个方块和颜色
        shape = random.choice(SHAPES)
        color = COLORS[SHAPES.index(shape)]
        # 初始位置在顶部中间
        x = GRID_WIDTH // 2 - len(shape[0]) // 2
        y = 0
        return {'shape': shape, 'x': x, 'y': y, 'color': color}
    
    def valid_move(self, piece, x, y):
        for i in range(len(piece['shape'])):
            for j in range(len(piece['shape'][0])):
                if piece['shape'][i][j]:
                    if (x + j < 0 or x + j >= GRID_WIDTH or
                        y + i >= GRID_HEIGHT or
                        y + i >= 0 and self.grid[y + i][x + j]):
                        return False
        return True
    
    def merge_piece(self):
        for i in range(len(self.current_piece['shape'])):
            for j in range(len(self.current_piece['shape'][0])):
                if self.current_piece['shape'][i][j]:
                    self.grid[self.current_piece['y'] + i][self.current_piece['x'] + j] = self.current_piece['color']
    
    def remove_lines(self):
        lines_cleared = 0
        i = GRID_HEIGHT - 1
        while i >= 0:
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
            else:
                i -= 1
        self.score += lines_cleared * 100
    
    def rotate_piece(self):
        # 转置矩阵然后反转每一行来实现旋转
        shape = self.current_piece['shape']
        rotated = [[shape[j][i] for j in range(len(shape)-1, -1, -1)]
                  for i in range(len(shape[0]))]
        if self.valid_move({'shape': rotated,
                           'x': self.current_piece['x'],
                           'y': self.current_piece['y']},
                          self.current_piece['x'],
                          self.current_piece['y']):
            self.current_piece['shape'] = rotated

    def move(self, dx, dy):
        if self.valid_move(self.current_piece,
                          self.current_piece['x'] + dx,
                          self.current_piece['y'] + dy):
            self.current_piece['x'] += dx
            self.current_piece['y'] += dy
            return True
        return False

    def drop(self):
        if not self.move(0, 1):
            self.merge_piece()
            self.remove_lines()
            self.current_piece = self.new_piece()
            if not self.valid_move(self.current_piece,
                                 self.current_piece['x'],
                                 self.current_piece['y']):
                self.game_over = True

def draw_grid(screen, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x],
                               (x * BLOCK_SIZE, y * BLOCK_SIZE,
                                BLOCK_SIZE - 1, BLOCK_SIZE - 1))
            else:
                pygame.draw.rect(screen, WHITE,
                               (x * BLOCK_SIZE, y * BLOCK_SIZE,
                                BLOCK_SIZE - 1, BLOCK_SIZE - 1), 1)

def draw_piece(screen, piece):
    for i in range(len(piece['shape'])):
        for j in range(len(piece['shape'][0])):
            if piece['shape'][i][j]:
                pygame.draw.rect(screen, piece['color'],
                               ((piece['x'] + j) * BLOCK_SIZE,
                                (piece['y'] + i) * BLOCK_SIZE,
                                BLOCK_SIZE - 1, BLOCK_SIZE - 1))

def main():
    clock = pygame.time.Clock()
    game = Tetris()
    fall_time = 0
    fall_speed = 500  # 每0.5秒下落一格
    
    while not game.game_over:
        fall_time += clock.get_rawtime()
        clock.tick()
        
        if fall_time >= fall_speed:
            game.drop()
            fall_time = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.drop()
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    while game.move(0, 1):
                        pass
                    game.drop()
        
        screen.fill(BLACK)
        draw_grid(screen, game.grid)
        draw_piece(screen, game.current_piece)
        
        # 显示分数
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'分数: {game.score}', True, WHITE)
        screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 10))
        
        pygame.display.flip()
    
    # 游戏结束显示
    font = pygame.font.Font(None, 48)
    game_over_text = font.render('游戏结束!', True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH//3, SCREEN_HEIGHT//2))
    pygame.display.flip()
    
    # 等待几秒后退出
    pygame.time.wait(2000)
    pygame.quit()

if __name__ == '__main__':
    main()
