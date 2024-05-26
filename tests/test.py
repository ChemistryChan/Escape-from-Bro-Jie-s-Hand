# This py document is only for testing every kind of function/problem.
import pygame

pygame.init()

# 设置字体文件路径
font_path = '../resources/font/PixeloidSansBold-RpeJo.ttf'
font_size = 24

# 创建字体对象
custom_font = pygame.font.Font(font_path, font_size)

# 渲染文本
text_surface = custom_font.render('Hello, Pygame!', True, (255, 255, 255))

# 创建显示窗口
screen = pygame.display.set_mode((800, 600))
screen.fill((0, 0, 0))

# 在屏幕上绘制文本
screen.blit(text_surface, (100, 100))

pygame.display.flip()

# 等待退出
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
