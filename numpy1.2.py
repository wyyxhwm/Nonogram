import numpy
import pygame
import json

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

def button(window, json_name, interface):
    buttons = {}
    with open(json_name,'r',encoding='utf-8') as f:
        data = json.load(f)
    interface = data['interface'][interface]
    texts,  start_y = interface['texts'], interface['start_y']
    row_num, col_num = interface['row_num'], interface['col_num']
    texts_font = pygame.font.SysFont(interface['font_name'], interface['font_size'])
    x, y = window.get_size()
    x = x // col_num // 2
    y = y // 2
    for i in range(len(texts)):

        c = i // row_num
        text = texts_font.render(texts[i + c * row_num], True, interface['color'][i])
        text_rect = text.get_rect()
        text_rect.center = (x + c * x, y + i * 2 * interface['font_size'])
        window.blit(text, text_rect)
        buttons[f'{texts[i]}'] = text_rect
    return buttons

class Interface:
    def __init__(self, window):
        self.window = window
        self.width, self.height = window.get_size()
        self.interface = '初始界面'
        self.buttons = {}
        self.title_font = pygame.font.SysFont('SimHei', 60)
        self.start_font = pygame.font.SysFont('SimHei', 20)

        print('Interface对象创建成功')

    def draw(self, levels): #打印界面
        if not levels:
            levels = None
        self.window.fill('white')

        # 打印初始界面
        if self.interface == '初始界面':
            self.buttons = {}
            # 打印标题
            title = self.title_font.render('数织游戏', True, 'black')
            title_rect = title.get_rect()
            title_rect.center = (self.width // 2, self.height // 3 )
            self.window.blit(title, title_rect)

            self.buttons = button(self.window,'button.json',0)

        # 打印关卡选择界面
        elif self.interface == '关卡选择':
            self.buttons = []
            start_width = self.width // 4
            start_height = self.height // 4
            for i in range(len(levels)):
                row = i // 5
                col = i % 5
                x = start_width + col*80
                y = start_height + row*40
                text = self.start_font.render(f'第{i+1}关', True, 'black')
                text_rect = text.get_rect()
                text_rect.center = (x + 30, y + 10) # 按钮宽60，中心点偏移
                # 打印关卡名
                self.window.blit(text, text_rect)
                # 打印关卡框
                self.buttons.append(pygame.draw.rect(self.window, 'black',(x, y, 60, 20), 1))

        elif self.interface == '设置界面':
            button(self.window,'button.json',1)

        elif self.interface == '颜色选择界面':
            self.buttons = button(self.window, 'button.json',2)

        elif self.interface == '游戏胜利':
            title = self.title_font.render('游戏胜利', True, 'black')
            title_rect = title.get_rect()
            title_rect.center = (self.width // 2, self.height // 3)
            self.window.blit(title, title_rect)

            self.buttons = button(self.window,'button.json',3)

class Game:
    def __init__(self, window, answer):
        self.window = window
        self.answer = answer
        self.player = numpy.zeros_like(self.answer)
        self.display_top_clues, self.display_left_clues = format_clues(self.answer)
        self.width, self.height = window.get_size()
        self.rect = None
        self.color = 'black'
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

    def judge(self):
        return numpy.array_equal(self.player == 1, self.answer == 1)

def main():
    with open('button.json', 'r', encoding='utf-8') as f:
        interface = json.load(f)
    with open('level.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    levels = data['levels']
    pygame.init()
    # 加载音乐
    pygame.mixer.music.load('music/背景音乐.mp3')
    pygame.mixer.music.play(0, fade_ms=5000)  # 循环次数，开始的时间，淡入浅出事件（ms）

    window = pygame.display.set_mode((960, 540))
    I = Interface(window)
    game = None
    isRunning = True
    while isRunning:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False
                break
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
    #             if I.interface == '初始界面':
    #                 if I.buttons['开始游戏'].collidepoint(mouse_pos):
    #                     I.interface = '关卡选择'
    #                     I.draw(levels)
    #
    #                 elif I.buttons['游戏设置'].collidepoint(mouse_pos):
    #                     I.interface = '设置界面'
    #                     I.draw(levels)
    #
    #             elif I.interface == '设置界面':
    #                 if I.buttons['格子颜色'].collidepoint(mouse_pos): # 修改涂色的颜色
    #                     I.interface = '颜色选择界面'
    #                     I.draw(levels)
    #
    #                 elif I.buttons["音乐开关"].collidepoint(mouse_pos): # 开关背景音乐
    #                     if pygame.mixer.music.get_busy():
    #                         pygame.mixer.music.stop()
    #                     else:
    #                         pygame.mixer.music.rewind()
    #                         pygame.mixer.music.play()
    #
    #                 elif I.buttons["返回初始界面"].collidepoint(mouse_pos): # 返回初始界面
    #                     I.interface = '初始界面'
    #                     I.draw(levels)
    #
    #             elif I.interface == '颜色选择界面':
    #
    #                 if I.buttons['black'].collidepoint(mouse_pos):
    #                     I.color = 'black'
    #
    #                 elif I.buttons['blue'].collidepoint(mouse_pos):
    #                     I.color = 'blue'
    #
    #                 elif I.buttons['orange'].collidepoint(mouse_pos):
    #                     I.color = 'orange'
    #
    #                 elif I.buttons['red'].collidepoint(mouse_pos):
    #                     I.color = 'red'
    #                 I.interface = '设置界面'
    #                 I.draw(levels)
    #
    #             elif I.interface == '游戏胜利':
    #                 if I.buttons['选择关卡'].collidepoint(mouse_pos):
    #                     I.interface = '关卡选择'
    #                     I.draw(levels)
    #                 elif I.buttons['返回标题画面'].collidepoint(mouse_pos):
    #                     I.interface = '初始界面'
    #                     I.draw(levels)
    #
    #             elif I.interface == '关卡选择':
    #                 for i in range(len(I.buttons)):
    #                     if I.buttons[i].collidepoint(mouse_pos):
    #                         game = Game(window, levels[i])
    #                         I.interface = '游戏界面'
    #                         game.draw()
    #
    #             elif I.interface == '游戏界面':
    #                 game.color = I.color
    #                 pos_x, pos_y = pygame.mouse.get_pos()
    #                 if game.rect.collidepoint((pos_x, pos_y)):
    #                     y = (pos_x - game.start_x) // 20
    #                     x = (pos_y - game.start_y) // 20
    #                     if ev.button == 1:
    #                         if game.player[x][y] == 1:
    #                             game.player[x][y] = 0
    #                         elif game.player[x][y] == 0:
    #                             game.player[x][y] = 1
    #
    #                     if ev.button == 3:
    #                         if game.player[x][y] == 2:
    #                             game.player[x][y] = 0
    #                         else:
    #                             game.player[x][y] = 2
    #                 game.draw()
    #
    #     I.draw(levels)
    #     if I.interface == '游戏界面':
    #         game.draw()
    #         if game.judge():
    #             I.interface = '游戏胜利'
    #             I.draw(levels)
    #
    #     pygame.display.update()

















if __name__ == '__main__':
    main()
    pygame.quit()