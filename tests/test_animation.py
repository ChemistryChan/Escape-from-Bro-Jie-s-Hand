import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置窗口大小
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('GIF Animation')

# 加载GIF图像（假设文件名为animation.gif）
gif_frames = []  # 存储每一帧的图像对象
all_frames = 10  # GIF动图的总帧数

for i in range(all_frames):
    frame_filename = f'animation_frame_{i}.png'  # 假设你已经将GIF分解为PNG帧
    frame_image = pygame.image.load(frame_filename)
    gif_frames.append(frame_image)

# 游戏循环
current_frame = 0
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 绘制当前帧
    window_surface.fill((255, 255, 255))  # 清空屏幕
    window_surface.blit(gif_frames[current_frame], (0, 0))  # 绘制当前帧

    # 更新帧索引
    current_frame = (current_frame + 1) % all_frames

    pygame.display.flip()
    clock.tick(30)  # 控制帧率

# 退出Pygame
pygame.quit()
sys.exit()
