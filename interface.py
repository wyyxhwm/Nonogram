
import pygame
import json


def interface_draw( interface_json, window, interface):
    width, height = window.get_size()
    buttons = {}
    window.fill((245, 245, 220))
    with open(interface_json, 'r', encoding='utf-8') as f:
        j = json.load(f)
    for i in j['interface']:
        if i['name'] == interface:
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

def handle_events(window, buttons: dict, pos):
    for i in buttons.values():
        if i[0].collidepoint(pos):
            if i[1] == 'goto':
                now_interface = i[2]
                return now_interface
            elif i[1] == 'toggle_music':
                return False
            elif i[1] == 'set_color':
                return i[2]


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((800, 600))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        buttons = interface_draw('interface.json', window, '设置界面')
        print(buttons)
        pygame.display.update()