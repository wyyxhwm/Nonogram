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


def Interface( interface_json, window, interface):
    width, height = window.get_size()
    with open(interface_json, 'r', encoding='utf-8') as f:
        j = json.load(f)
    for i in j['interface']:
        window.fill((245, 245, 220))
        if i['name'] == interface:
            buttons = {}
            size = i['font_size']
            font = pygame.font.SysFont(i['font'], size)
            max_button_len = max([len(x['text']) for x in i['buttons']])
            start_x = (width - (max_button_len + (len(i['buttons']) - 1) * size)) // 2
            start_y = (height - i['layout']['row_num'] * 2 * size)  // 2
            if interface == "标题画面":
                title_font = pygame.font.SysFont('SimHei', 60)
                title = title_font.render('数织游戏', True, 'black')
                title_rect = title.get_rect()
                title_rect.center = (width // 2, height // 3)
                window.blit(title, title_rect)
            x_up = (max_button_len + 1) * size
            y_up = size + 2
            x = max_button_len  * size + 2
            y = size + 2
            num = 0
            for r in range(i['layout']['row_num']):
                for c in range(i['layout']['col_num']):
                    rect = pygame.draw.rect(window, 'black', (start_x + x_up * c - max_button_len * size // 2, start_y + y_up * r * 2, x, y), 1)
                    title = font.render(i['buttons'][num]['text'], True, i['buttons'][num]['color'])
                    title_rect = title.get_rect()
                    title_rect.center = (start_x + x_up * c, start_y + y_up * r * 2 + size // 2)
                    window.blit(title, title_rect)
                    buttons[i['buttons'][num]['text']] = [rect,i['buttons'][num]['action'],i['buttons'][num]['target']]
                    num += 1

            return buttons
    return None


class Game:
    def __init__(self):
        pass

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

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    interface = Interface(window)
    interface.draw()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
