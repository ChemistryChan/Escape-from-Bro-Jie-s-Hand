import sys
import pygame

'''在屏幕指定位置显示文字  Display text at a specified location on the screen'''
def showText(screen, font, text, color, position):
    text_render = font.render(text, True, color)
    rect = text_render.get_rect()
    rect.left, rect.top = position
    screen.blit(text_render, rect)
    return rect.right



'''游戏开始/关卡切换/游戏结束界面  Interface of GAMESTART/LEVELSWITCH/GAMEOVER'''
class Button:
    pixel_font_path = 'resources/font/PixeloidSansBold-RpeJo.ttf'
    def __init__(self, screen, position, text):
        self.screen = screen
        self.position = position
        self.text = text
        self.font = pygame.font.Font(self.pixel_font_path, 24)
        self.rect = pygame.Rect(position[0], position[1], 150, 50)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((0, 0, 0))
        self.image.set_alpha(100)

    def draw(self):
        self.screen.blit(self.image, self.position)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

def Interface(screen, cfg, mode='game_start'):
    pygame.display.set_mode(cfg.SCREENSIZE)
    background = pygame.image.load('resources/images/interfaceBG.png').convert_alpha()

    clock = pygame.time.Clock()
    while True:
        screen.blit(background, (0, 0))

        if mode == 'game_start':
            button_1 = Button(screen, (240, 200), 'START')
            button_2 = Button(screen, (240, 300), 'QUIT')
        elif mode == 'game_switch':
            button_1 = Button(screen, (240, 200), 'NEXT')
            button_2 = Button(screen, (240, 300), 'QUIT')
        elif mode == 'game_end':
            button_1 = Button(screen, (240, 200), 'RESTART')
            button_2 = Button(screen, (240, 300), 'QUIT')
        else:
            raise ValueError('Interface.mode unsupported: %s' % mode)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(-1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.rect.collidepoint(pygame.mouse.get_pos()):
                    return True
                elif button_2.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit(-1)

        button_1.draw()
        button_2.draw()
        pygame.display.update()
        clock.tick(cfg.FPS)

# Example usage:
# cfg = Config()  # You need to define your own Config class
# screen = pygame.display.set_mode(cfg.SCREENSIZE)
# Interface(screen, cfg, mode='game_start')