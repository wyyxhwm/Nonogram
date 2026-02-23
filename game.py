import numpy
import pygame

def display_level_buttons(window, levels):
    level_buttons = []
    font = pygame.font.SysFont('SimHei', 20)
    width, height = window.get_size()
    start_width = width // 4
    start_height = height // 4
    for i in range(len(levels)):
        row = i // 5
        col = i % 5
        x = start_width + col * 80
        y = start_height + row * 40
        text = font.render(f'第{i + 1}关', True, 'black')
        text_rect = text.get_rect()
        text_rect.center = (x + 30, y + 10)  # 按钮宽60，中心点偏移
        # 打印关卡名
        window.blit(text, text_rect)
        # 打印关卡框
        level_buttons.append(pygame.draw.rect(window, 'black', (x, y, 60, 20), 1))
    return level_buttons

def array_to_left_clues(array): # 获取左提示
    print('获取左提示')
    return [[len(z) for z in ''.join(map(str,i)).split('0') if z] for i in array]

def array_to_top_clues(array): # 获取上提示
    print('获取上提示')
    array = array.T
    return array_to_left_clues(array)

def format_clues(array): # 将提示转化为用于显示的列表
    print('将提示转化为用于显示的列表')
    left_clues = array_to_left_clues(array)
    top_clues = array_to_top_clues(array)
    display_left_clues = [i for i in left_clues]
    display_top_clues = [[] for _ in range(max([len(i) for i in top_clues]))]

    for i in display_left_clues:
        i.reverse()

    for i in range(len(display_top_clues)):
        for j in range(len(top_clues)):
            try:
                display_top_clues[i].append(top_clues[j][-(i+1)])
            except IndexError:
                display_top_clues[i].append(None)

    for i in range(len(left_clues)):
        if len(left_clues[i]) < max([len(z) for z in left_clues]):
            for j in range(max([len(i) for i in left_clues]) - len(left_clues[i])):
                display_left_clues[i].append(None)
    return display_top_clues, display_left_clues

class Game:
    def __init__(self, window, answer, color = 'black'):
        self.window = window
        self.answer = answer
        self.player = numpy.zeros_like(self.answer)
        self.display_top_clues, self.display_left_clues = format_clues(self.answer)
        self.width, self.height = window.get_size()
        self.rect = None
        self.color = color
        self.clue_font = pygame.font.SysFont('SmiHei', 30)
        self.start_x = 0
        self.start_y = 0
        print('Game对象创建成功')

    def draw(self):
        start_x = (960 - len(self.player) * 20) // 2
        self.start_x = start_x
        start_y = (540 - len(self.player) * 20) // 2
        self.start_y = start_y
        row = len(self.player[0]) * 20
        col = len(self.player) * 20
        self.window.fill('white')

        # 打印数织网格
        self.rect = pygame.draw.rect(self.window, 'black', (start_x, start_y, row, col), 1)
        for i in range(len(self.player[0])):
            pygame.draw.line(self.window, 'black', (start_x + i * 20, start_y),
                             (start_x + i * 20, start_y + len(self.player) * 20), 1)
        for i in range(len(self.player)):
            pygame.draw.line(self.window, 'black', (start_x, start_y + i * 20,),
                             (start_x + len(self.player[0]) * 20, start_y + i * 20), 1)

        # 打印上提示
        for i in range(len(self.display_top_clues)):
            for j in range(len(self.display_top_clues[0])):
                if self.display_top_clues[i][j] is not None:
                    clue = self.clue_font.render(str(self.display_top_clues[i][j]),True, 'black')
                    clue_rect = clue.get_rect()
                    clue_rect.center = (start_x + 10 + j * 20, start_y - 10 - i * 20)
                    self.window.blit(clue, clue_rect)

        # 打印左提示
        for i in range(len(self.display_left_clues)):
            for j in range(len(self.display_left_clues[0])):
                if self.display_left_clues[i][j] is not None:
                    clue = self.clue_font.render(str(self.display_left_clues[i][j]), True, 'black')
                    clue_rect = clue.get_rect()
                    clue_rect.center = (start_x - 10 - j * 20, start_y + 10 + i * 20)
                    self.window.blit(clue, clue_rect)

        # 打印玩家绘制内容
        for i in range(len(self.player)):
            for j in range(len(self.player[0])):
                if self.player[i][j] == 1:
                    pygame.draw.rect(self.window, self.color, (start_x + j * 20 + 2, start_y + i * 20 + 2,16,16),0)
                elif self.player[i][j] == 0:
                    pygame.draw.rect(self.window, 'white', (start_x + j * 20 + 2, start_y + i * 20 + 2, 16, 16), 0)
                elif self.player[i][j] == 2:

                    pygame.draw.rect(self.window, 'white', (start_x + j * 20 + 2, start_y + i * 20 + 2, 16, 16), 0)
                    pygame.draw.line(self.window,'red',(start_x + j * 20 + 2, start_y + i * 20 + 2),
                                     (start_x + j * 20 + 2+16, start_y + i * 20 + 2 + 16),1)
                    pygame.draw.line(self.window, 'red', (start_x + j * 20 + 2 + 16, start_y + i * 20 + 2),
                                     (start_x + j * 20 + 2 + 16 - 16, start_y + i * 20 + 2 + 16), 1)

    def process_input(self, button: int):
        pos_x, pos_y = pygame.mouse.get_pos()
        if self.rect.collidepoint((pos_x, pos_y)):
            y = (pos_x - self.start_x) // 20
            x = (pos_y - self.start_y) // 20
            if button == 1:
                if self.player[x][y] == 1:
                    self.player[x][y] = 0
                elif self.player[x][y] == 0:
                    self.player[x][y] = 1

            if button == 3:
                if self.player[x][y] == 2:
                    self.player[x][y] = 0
                else:
                    self.player[x][y] = 2

    def judge(self):
        return numpy.array_equal(self.player == 1, self.answer == 1)