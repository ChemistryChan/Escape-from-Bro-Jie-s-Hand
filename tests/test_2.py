import pygame

# 初始化
pygame.init()

# 设置屏幕尺寸
screen_width, screen_height = 400, 200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hello, Pygame!")

# 设置字体
font = pygame.font.SysFont("Cambria", 32)

# 创建文本
text = font.render("Hello, Pygame!", True, (255, 255, 255))

# 创建描边效果
outline_text = font.render("Hello, Pygame!", True, (255, 255, 255))
outline_text.set_alpha(100)

# 创建阴影效果
shadow_text = font.render("Hello, Pygame!", True, (255, 255, 255))
shadow_text.set_alpha(100)

# 渲染到屏幕
screen.blit(outline_text, (50, 50))
screen.blit(shadow_text, (52, 52))
screen.blit(text, (50, 50))

# 刷新屏幕
pygame.display.flip()

# 等待退出
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
