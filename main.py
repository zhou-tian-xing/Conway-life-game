from lifegame import LifeGame
import time
import pygame, sys

def floor(x): # 向下取整（Python的int是直接取整数部分，不是向下取整）
    if x >= 0: return int(x)
    else: return int(x) - 1

lg = LifeGame(-1)
pygame.init()
print("按键：滑动滚轮缩放大小，点击左键放置，点击右键摧毁，点击鼠标中键（滚轮）以鼠标为中心放大，上下左右键调整位置，\
      按空格暂停，按“-”减速，按“=”加速，按“s”执行单步，按“d”细节，按“c”清除全部，按“t”关闭/开启文字显示，按“o”回到原点")
print("Key: Slide the scroll wheel to zoom in and out, click the left button to place, click the right button to destroy, \
      click the middle mouse button (scroll wheel) to zoom in with the mouse as the center, adjust the position with the up, down, left and right keys, \
      pause with a space, slow down with a '-' button, accelerate with a '=' button, execute a single step with a 's' button, click 'd' for details, \
      click 'c' to clear everything, press 't' to turn off/on text display, and press 'o' to return to the origin")

'''
# 默认
a = 900
life_new_color = (51, 255, 220)
death_color = (182, 182, 182)
line_color = (210, 210, 210)
main_text_color = (0, 0, 0)
pressing_text_color = (230, 50, 50)
life_before_color = (162, 193, 188)  # 死亡后的生命颜色
life_old_color = (77, 240, 212)  # 没变的生命颜色
dark_life_color = (26, 128, 110)  # 文字用（details - 显示生命数量）
area = 45
'''

'''
# 类似官网https://conwaylife.com/
a = 900
life_new_color = (0, 0, 0)
death_color = (255, 255, 255)
line_color = (210, 210, 210)
main_text_color = (0, 0, 0)
pressing_text_color = (230, 50, 50)
life_before_color = (230, 230, 230)  # 死亡后的生命颜色
life_old_color = (80, 80, 80)  # 没变的生命颜色
dark_life_color = (0, 0, 0)  # 文字用（details - 显示生命数量）
area = 45
'''

'''
# https://nonoas.gitee.io/webproj/
a = 900
life_new_color = (232, 247, 245)
death_color = (35, 183, 174)
line_color = (255, 255, 255)
main_text_color = (0, 0, 0)
pressing_text_color = (230, 50, 50)
life_before_color = (74, 196, 188)  # 死亡后的生命颜色
life_old_color = (212, 241, 238)  # 没变的生命颜色
dark_life_color = (0, 0, 0)  # 文字用（details - 显示生命数量）
area = 45
'''

'''
# https://playgameoflife.com/
a = 900
life_new_color = (255, 255, 0)
death_color = (126, 126, 126)
line_color = (150, 150, 150)
main_text_color = (255, 255, 255)
pressing_text_color = (230, 50, 50)
life_before_color = (139, 139, 113)  # 死亡后的生命颜色
life_old_color = (229, 229, 25)  # 没变的生命颜色
dark_life_color = (228, 228, 0)  # 文字用（details - 显示生命数量）
area = 45
'''

a = 900
life_new_color = (51, 255, 220)
death_color = (182, 182, 182)
line_color = (210, 210, 210)
main_text_color = (0, 0, 0)
pressing_text_color = (230, 50, 50)
life_before_color = (162, 193, 188)  # 死亡后的生命颜色
life_old_color = (77, 240, 212)  # 没变的生命颜色
dark_life_color = (26, 128, 110)  # 文字用（details - 显示生命数量）
area = 45
# 以上这些参数可以自定义

screen = pygame.display.set_mode((a, a))
pygame.display.set_caption("Conway’s Game of Life")
l = a // area
pos = [0, 0]
pygame.key.stop_text_input()  # 使PyGame不检测输入，而是仅考虑按键按下事件
move = False
dt = 0.2
T0 = dt
rects = [pygame.Rect((x[0]-pos[0])*l, (x[1]-pos[1])*l, l, l) for x in lg._area]
last_rects = []
PUT, KILL = False, False
font_big = pygame.font.Font("SmileySans-Oblique.otf", 30)
font_small = pygame.font.Font("SmileySans-Oblique.otf", 20)
N = 0
TN = 0
speed = None
detail = False
TEXT = True
while 1:
    T1 = time.perf_counter()

    # 事件监测
    events = pygame.event.get()
    for event in events:
        # 退出
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in [1, 3]:
                if event.button == 1:
                    PUT = True
                elif event.button == 3:
                    KILL = True

            else:
                last_l = l
                lpos = pos[:]
                if event.button == 4:  # 向上滚动（放大）
                    area = max(int(area/2), 1)  # 防止放的太大回不来了
                    l = max(1, a // area)
                    area = a // l
                elif event.button == 5:  # 向下滚动（缩小）
                    area = max(int(area*2), 2)
                    l = max(1, a // area) 
                    area = a // l
                elif event.button == 2:  # 中键（有心放大）
                    x, y = pygame.mouse.get_pos()
                    pos = [round(pos[0]+floor(x/l)*0.5), round(pos[1]+floor(y/l)*0.5)]
                    area = max(int(area/2), 2)
                    l = max(1, a // area) 
                    area = a // l
                last_rects = [pygame.Rect((r.left/last_l+lpos[0]-pos[0])*l, (r.top/last_l+lpos[1]-pos[1])*l, l, l) for r in last_rects]
                rects = [pygame.Rect((x[0]-pos[0])*l, (x[1]-pos[1])*l, l, l) for x in lg._area]

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                PUT = False
            elif event.button == 3:
                KILL = False
        elif event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) in ['right', 'left', 'up', 'down']:
                lp = pos[:]
                if pygame.key.name(event.key) == 'right':
                    pos[0] += max(int(area / 8), 1)
                elif pygame.key.name(event.key) == 'left':
                    pos[0] -= max(int(area / 8), 1)
                if pygame.key.name(event.key) == 'up':
                    pos[1] -= max(int(area / 8), 1)
                elif pygame.key.name(event.key) == 'down':
                    pos[1] += max(int(area / 8), 1)
                rects = [pygame.Rect((x[0]-pos[0])*l, (x[1]-pos[1])*l, l, l) for x in lg._area]
                last_rects = [pygame.Rect((r.left/l+lp[0]-pos[0])*l, (r.top/l+lp[1]-pos[1])*l, l, l) for r in last_rects]
            if pygame.key.name(event.key) == "space":
                move = not move
            if pygame.key.name(event.key) == "-":
                dt *= 1.5
                T0 = 0
                continue
            elif pygame.key.name(event.key) == "=":
                dt /= 1.5
                T0 = 0
                continue
            elif pygame.key.name(event.key) in ["s", "S"]:
                lg.check()
                last_rects = rects[:]
                rects = [pygame.Rect((x[0]-pos[0])*l, (x[1]-pos[1])*l, l, l) for x in lg._area]
                N += 1
            elif pygame.key.name(event.key) in ["d", "D"]:
                detail = not detail
            elif pygame.key.name(event.key) in ["c", "C"]:
                lg._area = set()
                rects = []
                last_rects = []
            elif pygame.key.name(event.key) in ["t", "T"]:
                TEXT = not TEXT
            elif pygame.key.name(event.key) in ["o", "O"]:
                lp = pos[:]
                pos = [0, 0]
                rects = [pygame.Rect(x[0]*l, x[1]*l, l, l) for x in lg._area]
                last_rects = [pygame.Rect((r.left/l+lp[0])*l, (r.top/l+lp[1])*l, l, l) for r in last_rects]

    # 连续放置和杀死
    if PUT or KILL:
        x, y = pygame.mouse.get_pos()
        if PUT:
            lg.animate((floor(x/l+pos[0]), floor(y/l+pos[1])))
        if KILL:
            lg.kill((floor(x/l)+pos[0], floor(y/l)+pos[1]))
        rects = [pygame.Rect((x[0]-pos[0])*l, (x[1]-pos[1])*l, l, l) for x in lg._area]

    # 刷新速度控制机制
    if T0 >= dt:
        T0 = 0
        if move:  # 刷新，并形成新的绘制对象
            lg.check()
            last_rects = rects[:]
            rects = [pygame.Rect((x[0]-pos[0])*l, (x[1]-pos[1])*l, l, l) for x in lg._area]
            N += 1
            speed = round(1/(time.perf_counter() - TN), 3)
            TN = time.perf_counter()

    screen.fill(death_color)  # 背景，即使用死亡的颜色

    # 绘制每个生命
    for r0 in last_rects:  # 更改前生命
        if 0 <= r0.top <= a and 0 <= r0.left <= a and not r0 in rects:
            pygame.draw.rect(screen, life_before_color, r0)
    for r in rects:  # 更改后生命
        if 0 <= r.top <= a and 0 <= r.left <= a:
            if r in last_rects:
                pygame.draw.rect(screen, life_old_color, r)
            else:
                pygame.draw.rect(screen, life_new_color, r)

    # 分割线
    if l > 3:
        for i in range(a // l + 1):
            pygame.draw.line(screen, line_color, (l*i, 0), (l*i, a))
            pygame.draw.line(screen, line_color, (0, l*i), (a, l*i))

    # (0,0)处的标志
    pygame.draw.line(screen, (230, 20, 20), ((-pos[0])*l, (-pos[1])*l), ((-pos[0])*l, (1-pos[1])*l))
    pygame.draw.line(screen, (230, 20, 20), ((-pos[0])*l, (-pos[1])*l), ((1-pos[0])*l, (-pos[1])*l))
    pygame.draw.line(screen, (230, 20, 20), ((1-pos[0])*l, (1-pos[1])*l), ((1-pos[0])*l, (-pos[1])*l))
    pygame.draw.line(screen, (230, 20, 20), ((1-pos[0])*l, (1-pos[1])*l), ((-pos[0])*l, (1-pos[1])*l))
    
    # 文字
    if TEXT:
        text = font_big.render("Step: "+str(N), True, main_text_color)
        text.set_alpha(154)
        screen.blit(text, (5, 5))

        if detail:
            if move: text = font_small.render("RealSpeed: {}steps/sec".format(speed), True, main_text_color)
            else: text = font_small.render("RealSpeed: None", True, main_text_color)
            text.set_alpha(154)
            screen.blit(text, (5, 40))
            
            text = font_small.render("SetSpeed: {}steps/sec".format(round(1/dt, 2)), True, main_text_color)
            text.set_alpha(154)
            screen.blit(text, (5, 65))
            
            text = font_small.render("Moving: "+str(move), True, [main_text_color, pressing_text_color][move])
            text.set_alpha(154)
            screen.blit(text, (5, 90))

            text = font_small.render("Screen: {}x{}; Blocks: {}x{}".format(a, a, area, area), True, main_text_color)
            text.set_alpha(154)
            screen.blit(text, (5, 115))

            text = font_small.render("Lives: "+str(len(rects)), True, dark_life_color)
            text.set_alpha(154)
            screen.blit(text, (5, 140))

            text = font_small.render("T0: "+str(round(T0, 5)), True, main_text_color)
            text.set_alpha(154)
            screen.blit(text, (5, 165))

            text = font_small.render("PUT: {}".format(PUT), True, [main_text_color, pressing_text_color][PUT])
            text.set_alpha(154)
            screen.blit(text, (5, 190))
            text = font_small.render("KILL: {}".format(KILL), True, [main_text_color, pressing_text_color][KILL])
            text.set_alpha(154)
            screen.blit(text, (90, 190))

            text = font_small.render("POS at top left: {}".format(pos), True, main_text_color)
            text.set_alpha(154)
            screen.blit(text, (5, 215))

    pygame.display.flip()  # 刷新

    T0 += time.perf_counter() - T1  # 定时
