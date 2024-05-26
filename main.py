import sys
import cfg
import random
import pygame
from modules import *
from modules.Sprites import Prop

'''游戏主程序  Main Program of Game'''
def main(cfg):
    # 初始化  Initialization
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(cfg.BGMPATH)
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.75)
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('逃出杰哥的手掌心_Lite')
    # 开始界面  Interface of Start
    Interface(screen, cfg, mode='game_start')
    # 游戏主循环  Main Loop of Game
    custom_font_path = 'resources/font/MonsterFriendBack.otf'
    font = pygame.font.Font(custom_font_path, 22)
    for gamemap_path in cfg.GAMEMAPPATHS:
        # -地图  Map
        map_parser = mapParser(gamemap_path, bg_paths=cfg.BACKGROUNDPATHS, wall_paths=cfg.WALLPATHS, blocksize=cfg.BLOCKSIZE)
        # -道具  Prop
        prop_sprite_group = pygame.sprite.Group()
        used_spaces = []
        for i in range(5):
            coordinate = map_parser.randomGetSpace(used_spaces)
            used_spaces.append(coordinate)
            prop_sprite_group.add(Prop(random.choice(cfg.PROPPATHS), coordinate=coordinate, blocksize=cfg.BLOCKSIZE))
        # -我方Hero  Player's Hero
        coordinate = map_parser.randomGetSpace(used_spaces)
        used_spaces.append(coordinate)
        ourhero = Hero(imagepaths=cfg.HEROWEIPATHS, coordinate=coordinate, blocksize=cfg.BLOCKSIZE, map_parser=map_parser, hero_name='WEI')
        # -电脑Hero  Program's Hero
        aihero_sprite_group = pygame.sprite.Group()
        coordinate = map_parser.randomGetSpace(used_spaces)
        aihero_sprite_group.add(Hero(imagepaths=cfg.HEROJIEPATHS, coordinate=coordinate, blocksize=cfg.BLOCKSIZE, map_parser=map_parser, hero_name='JIE'))
        used_spaces.append(coordinate)
        # -炸弹  bomb
        bomb_sprite_group = pygame.sprite.Group()
        # -用于判断游戏胜利或者失败的flag  Flag used to determine game victory or defeat
        is_win_flag = False
        # -加载音效  Sound FX Load
        upSound = pygame.mixer.Sound('resources/audio/up.wav')
        downSound = pygame.mixer.Sound('resources/audio/down.wav')
        leftSound = pygame.mixer.Sound('resources/audio/left.wav')
        rightSound = pygame.mixer.Sound('resources/audio/right.wav')
        bomb_putSound = pygame.mixer.Sound('resources/audio/bomb_put.wav')
        # -主循环  Main Loop
        screen = pygame.display.set_mode(map_parser.screen_size)
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(cfg.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)
                # --↑↓←→键控制上下左右, 空格键丢炸弹  Direction Keys control the direction, and Space Key for putting bombs.
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        ourhero.move('up')
                        upSound.play()
                    elif event.key == pygame.K_DOWN:
                        ourhero.move('down')
                        downSound.play()
                    elif event.key == pygame.K_LEFT:
                        ourhero.move('left')
                        leftSound.play()
                    elif event.key == pygame.K_RIGHT:
                        ourhero.move('right')
                        rightSound.play()
                    elif event.key == pygame.K_SPACE:
                        if ourhero.bomb_cooling_count <= 0:
                            bomb_sprite_group.add(ourhero.generateBomb(imagepath=cfg.BOMBPATH, digitalcolor=cfg.AZURE, explode_imagepath=cfg.FIREPATH))
                            bomb_putSound.play()
            screen.fill(cfg.WHITE)
            # --电脑Hero随机行动  AI hero Random Actions
            for hero in aihero_sprite_group:
                action, flag = hero.randomAction(dt)
                if flag and action == 'dropbomb':
                    bomb_sprite_group.add(hero.generateBomb(imagepath=cfg.BOMBPATH, digitalcolor=cfg.IVORY, explode_imagepath=cfg.FIREPATH))
            # --吃到道具加生命值(只要是Hero, 都能加)  Eating props for adding the life value (Valid for any kind of hero)
            ourhero.eatProp(prop_sprite_group)
            for hero in aihero_sprite_group:
                hero.eatProp(prop_sprite_group)
            # --游戏元素都绑定到屏幕上  Game elements are all tied to the screen.
            map_parser.draw(screen)
            for bomb in bomb_sprite_group:
                if not bomb.is_being:
                    bomb_sprite_group.remove(bomb)
                explode_area = bomb.draw(screen, dt, map_parser)
                if explode_area:
                    # --爆炸火焰范围内的Hero生命值将持续下降
                    # The health of Hero within the explosion flame range will continue to decrease.
                    if ourhero.coordinate in explode_area:
                        ourhero.health_value -= bomb.harm_value
                    for hero in aihero_sprite_group:
                        if hero.coordinate in explode_area:
                            hero.health_value -= bomb.harm_value
            prop_sprite_group.draw(screen)
            for hero in aihero_sprite_group:
                hero.draw(screen, dt)
            ourhero.draw(screen, dt)
            # --左上角显示生命值  The health value is displayed in the upper left corner.
            pos_x = showText(screen, font, text=ourhero.hero_name+'(our):'+str(ourhero.health_value), color=cfg.MIDNIGHTBLUE, position=[10, 10])
            for hero in aihero_sprite_group:
                pos_x, pos_y = pos_x + 25, 10
                pos_x = showText(screen, font, text=hero.hero_name+'(ai):'+str(hero.health_value), color=cfg.FIREBRICK, position=[pos_x, pos_y])
            # --我方玩家生命值小于等于0/电脑方玩家生命值任意一方小于等于0则判断游戏结束
            # If the health value of our player is less than or equal to 0/
            # the health value of the computer player is less than or equal to 0, the game will be judged to be over.
            if ourhero.health_value <= 0:
                is_win_flag = False
                break
            for hero in aihero_sprite_group:
                if hero.health_value <= 0:
                    aihero_sprite_group.remove(hero)
            if len(aihero_sprite_group) == 0:
                is_win_flag = True
                break
            pygame.display.update()
            clock.tick(cfg.FPS)
        if is_win_flag:
            Interface(screen, cfg, mode='game_switch')
        else:
            break
    Interface(screen, cfg, mode='game_end')


'''run'''
if __name__ == '__main__':
    while True:
        main(cfg)
