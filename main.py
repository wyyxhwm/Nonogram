import pygame
import json
import numpy
import interface
import game

# 初始化
pygame.init()
now_interface = "标题画面"
color = "black"
level_buttons = []
answer = []
levels = []
with open('level.json', 'r', encoding='utf-8') as f:
    l = json.load(f)["levels"]
for i in range(len(l)):
    levels.append(numpy.array(l[i]['level_list']))

# 创建窗口
window = pygame.display.set_mode((960, 540))

# 播放背景音乐
pygame.mixer.music.load('music/背景音乐.mp3')
pygame.mixer.music.play(0, fade_ms=5000)

# 加载初始页面
interface.interface_draw('interface.json', window, now_interface)

isRunning = True
while isRunning:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False
            break
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if now_interface == "游戏界面":
                now_game.process_input(ev.button)
                now_game.draw()
                if now_game.judge():
                    now_interface = "游戏胜利"
                    pass
            else:
                # 打印界面信息
                buttons = interface.interface_draw('interface.json', window, now_interface)

                # 界面交互处理
                if now_interface == "关卡选择":
                    level_buttons = game.display_level_buttons(window, levels)
                    for i in range(len(level_buttons)):
                        if level_buttons[i].collidepoint(pos):
                            answer = levels[i]
                            now_game = game.Game(window, answer, color)
                            now_interface = "游戏界面"
                            now_game.draw()
                            break

                else:
                    for i in buttons.values():
                        if i[0].collidepoint(pos):
                            if i[1] == 'goto':
                                now_interface = interface.handle_events(window, buttons, pos)
                            elif i[1] == 'toggle_music':
                                if pygame.mixer.music.get_busy():
                                    pygame.mixer.music.stop()
                                else:
                                    pygame.mixer.music.rewind()
                                    pygame.mixer.music.play()
                            elif i[1] == 'set_color':
                                color = i[2]
                                now_interface = "设置界面"

    pygame.display.update()