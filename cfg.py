import os

'''屏幕大小  Screen Size'''
SCREENSIZE = (640, 480)
'''块大小  Block Size'''
BLOCKSIZE = 40
'''FPS'''
FPS = 30
'''游戏地图路径  Path of Game Maps'''
GAMEMAPPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/maps/1.map', 'resources/maps/2.map']]
'''墙路径  Path of Walls'''
WALLPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/images/misc/wall0.png', 'resources/images/misc/wall1.png', 'resources/images/misc/wall2.png', 'resources/images/misc/fridge.png', 'resources/images/misc/bookshelf.png', 'resources/images/misc/nightstand.png', 'resources/images/misc/chair.png', 'resources/images/misc/plant.png']]
'''英雄路径  Path of Heroes'''
HEROWEIPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/images/wei/wei_left.gif', 'resources/images/wei/wei_right.gif', 'resources/images/wei/wei_up.gif', 'resources/images/wei/wei_down.gif']]
HEROJIEPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/images/jie/jie_left.gif', 'resources/images/jie/jie_right.gif', 'resources/images/jie/jie_up.gif', 'resources/images/jie/jie_down.gif']]
'''道具路径  Path of Props'''
PROPPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/images/misc/drink.png', 'resources/images/misc/puff.png']]
'''背景路径  Path of Backgrounds'''
BACKGROUNDPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/images/misc/bg0.png', 'resources/images/misc/bg1.png', 'resources/images/misc/bg2.png']]
'''爆炸和发射路径  Path of Explosion and Launch'''
BOMBPATH = os.path.join(os.getcwd(), 'resources/images/misc/bomb.png')
FIREPATH = os.path.join(os.getcwd(), 'resources/images/misc/fire.png')
'''背景音乐路径  Path of Background Music'''
BGMPATH = os.path.join(os.getcwd(), 'resources/audio/bgm.ogg')
'''一些颜色  Several Colors'''
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FIREBRICK = (178, 34, 34)
MIDNIGHTBLUE = (25, 25, 112)
MEDIUMSPRINGGREEN = (0, 255, 127)
CRIMSON = (220, 20, 60)
AZURE = (240, 255, 255)
IVORY = (255, 255, 240)
CYAN = (0, 255, 255)
VIOLET = (238, 130, 238)

