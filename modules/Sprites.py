import copy
import random
import pygame

'''墙类  Walls class'''
class Wall(pygame.sprite.Sprite):
	def __init__(self, imagepath, coordinate, blocksize, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imagepath)
		self.image = pygame.transform.scale(self.image, (blocksize, blocksize))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = coordinate[0] * blocksize, coordinate[1] * blocksize
		self.coordinate = coordinate
		self.blocksize = blocksize
	'''画到屏幕上  Draws them onto the screen'''
	def draw(self, screen):
		screen.blit(self.image, self.rect)
		return True


'''背景类  Backgrounds Class'''
class Background(pygame.sprite.Sprite):
	def __init__(self, imagepath, coordinate, blocksize, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imagepath)
		self.image = pygame.transform.scale(self.image, (blocksize, blocksize))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = coordinate[0] * blocksize, coordinate[1] * blocksize
		self.coordinate = coordinate
		self.blocksize = blocksize
	'''画到屏幕上  Draws them onto the screen'''
	def draw(self, screen):
		screen.blit(self.image, self.rect)
		return True


'''道具类  Props Class'''
class Prop(pygame.sprite.Sprite):
	def __init__(self, imagepath, coordinate, blocksize, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.kind = imagepath.split('/')[-1].split('.')[0]
		if self.kind == 'drink':
			self.value = 5
		elif self.kind == 'puff':
			self.value = 10
		else:
			raise ValueError('Unknow prop %s...' % self.kind)
		self.image = pygame.image.load(imagepath)
		self.image = pygame.transform.scale(self.image, (blocksize, blocksize))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = coordinate[0] * blocksize, coordinate[1] * blocksize
		self.coordinate = coordinate
		self.blocksize = blocksize
	'''画到屏幕上  Draws them onto the screen'''
	def draw(self, screen):
		screen.blit(self.image, self.rect)
		return True


'''炸弹类  Bombs Class'''
class Bomb(pygame.sprite.Sprite):
	def __init__(self, imagepath, coordinate, blocksize, digitalcolor, explode_imagepath, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imagepath)
		self.image = pygame.transform.scale(self.image, (blocksize, blocksize))
		self.explode_imagepath = explode_imagepath
		self.rect = self.image.get_rect()
		# 像素位置  Pixel Position
		self.rect.left, self.rect.top = coordinate[0] * blocksize, coordinate[1] * blocksize
		# 坐标(元素块为单位长度)  Coordinate (Block of elements is unit length)
		self.coordinate = coordinate
		self.blocksize = blocksize
		# 爆炸倒计时  Explosion Countdown
		self.explode_millisecond = 500 * 1 - 1
		self.explode_second = int(self.explode_millisecond / 100)
		self.start_explode = False
		# 爆炸持续时间  Explosion Duration
		self.exploding_count = 200 * 1
		# 炸弹伤害能力  Bomb Damage Capability
		self.harm_value = 2
		# 该炸弹是否还存在  The bomb still exists or not
		self.is_being = True
		self.font = pygame.font.SysFont('Consolas', 20)
		self.digitalcolor = digitalcolor
	'''画到屏幕上  Draws them onto the screen'''
	# 爆炸音效  Explosion Sound FX
	pygame.mixer.init()
	bomb_cdSound = pygame.mixer.Sound('resources/audio/bomb_countdown.wav')
	bomb_exploSound = pygame.mixer.Sound('resources/audio/bomb_explosion.wav')
	def draw(self, screen, dt, map_parser):
		if not self.start_explode:
			# 爆炸倒计时  Explosion Countdown
			self.explode_millisecond -= dt
			self.explode_second = int(self.explode_millisecond / 1000)
			self.bomb_cdSound.play(maxtime=1000)
			if self.explode_millisecond < 0:
				self.start_explode = True
				self.bomb_cdSound.stop()
			screen.blit(self.image, self.rect)
			text = self.font.render(str(self.explode_second), True, self.digitalcolor)
			rect = text.get_rect(center=(self.rect.centerx-5, self.rect.centery+5))
			screen.blit(text, rect)

			return False
		else:
			# 爆炸持续倒计时  Counting down of Explosion Continuing
			self.bomb_exploSound.play(maxtime=2800)
			self.exploding_count -= dt
			if self.exploding_count > 0:
				self.bomb_exploSound.stop()
				return self.__explode(screen, map_parser)
			else:
				self.is_being = False
				return False
	'''爆炸效果  Explosion Effects'''
	def __explode(self, screen, map_parser):
		explode_area = self.__calcExplodeArea(map_parser.instances_list)
		for each in explode_area:
			image = pygame.image.load(self.explode_imagepath)
			image = pygame.transform.scale(image, (self.blocksize, self.blocksize))
			rect = image.get_rect()
			rect.left, rect.top = each[0] * self.blocksize, each[1] * self.blocksize
			screen.blit(image, rect)

		return explode_area
	'''计算爆炸区域  Calculate the explosion area'''
	def __calcExplodeArea(self, instances_list):
		explode_area = []
		# 区域计算规则为墙可以阻止爆炸扩散, 且爆炸范围仅在游戏地图范围内  The area calculation rule is that walls can prevent\N
		# the explosion from spreading, and the explosion range is only within the game map.
		for ymin in range(self.coordinate[1], self.coordinate[1]-5, -1):
			if ymin < 0 or instances_list[ymin][self.coordinate[0]] in ['w', 'x', 'z', 'a', 'b', 'c', 'd', 'e']:
				break
			explode_area.append([self.coordinate[0], ymin])
		for ymax in range(self.coordinate[1]+1, self.coordinate[1]+5):
			if ymax >= len(instances_list) or instances_list[ymax][self.coordinate[0]] in ['w', 'x', 'z', 'a', 'b', 'c', 'd', 'e']:
				break
			explode_area.append([self.coordinate[0], ymax])
		for xmin in range(self.coordinate[0], self.coordinate[0]-5, -1):
			if xmin < 0 or instances_list[self.coordinate[1]][xmin] in ['w', 'x', 'z', 'a', 'b', 'c', 'd', 'e']:
				break
			explode_area.append([xmin, self.coordinate[1]])
		for xmax in range(self.coordinate[0]+1, self.coordinate[0]+5):
			if xmax >= len(instances_list[0]) or instances_list[self.coordinate[1]][xmax] in ['w', 'x', 'z', 'a', 'b', 'c', 'd', 'e']:
				break
			explode_area.append([xmax, self.coordinate[1]])
		return explode_area


'''角色类  Characters Class'''
class Hero(pygame.sprite.Sprite):
	def __init__(self, imagepaths, coordinate, blocksize, map_parser, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.imagepaths = imagepaths
		self.image = pygame.image.load(imagepaths[-1])
		self.image = pygame.transform.scale(self.image, (blocksize, blocksize))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = coordinate[0] * blocksize, coordinate[1] * blocksize
		self.coordinate = coordinate
		self.blocksize = blocksize
		self.map_parser = map_parser
		self.hero_name = kwargs.get('hero_name')
		# 生命值  Life Value
		self.health_value = 20
		# 炸弹冷却时间  Bomb Cooldown Time
		self.bomb_cooling_time = 500
		self.bomb_cooling_count = 0
		# 随机移动冷却时间(仅AI电脑用)  Random movement cooling time (only for AI)
		self.randommove_cooling_time = 75
		self.randommove_cooling_count = 0
	'''角色移动  Characters Movement'''
	def move(self, direction):
		self.__updateImage(direction)
		dx, dy = 0, 0
		if direction == 'left':
			dx = -1
		elif direction == 'right':
			dx = 1
		elif direction == 'up':
			dy = -1
		elif direction == 'down':
			dy = 1
		else:
			raise ValueError('Unknown direction %s...' % direction)
		new_x = self.coordinate[0] + dx
		new_y = self.coordinate[1] + dy
		# 先检查是否越界  First, check whether it is out of bounds.
		if 0 <= new_x < self.map_parser.width and 0 <= new_y < self.map_parser.height:
			# 再检查是否遇到障碍物  Then check to see if there are any obstacles.
			if self.map_parser.getElemByCoordinate([new_x, new_y]) not in ['w', 'x', 'z', 'a', 'b', 'c', 'd', 'e']:
				self.coordinate[0] = new_x
				self.coordinate[1] = new_y
				self.rect.left, self.rect.top = self.coordinate[0] * self.blocksize, self.coordinate[1] * self.blocksize
				return True
		return False
	'''随机行动(AI电脑用)  Random Actions (for AI)'''
	def randomAction(self, dt):
		# 冷却倒计时
		if self.randommove_cooling_count > 0:
			self.randommove_cooling_count -= dt
		action = random.choice(['left', 'left', 'right', 'right', 'up', 'up', 'down', 'down', 'dropbomb'])
		flag = False
		if action in ['left', 'right', 'up', 'down']:
			if self.randommove_cooling_count <= 0:
				flag = True
				self.move(action)
				self.randommove_cooling_count = self.randommove_cooling_time
		elif action in ['dropbomb']:
			if self.bomb_cooling_count <= 0:
				flag = True
				self.bomb_cooling_count = self.bomb_cooling_time
		return action, flag
	'''生成炸弹  Generate Bombs'''
	def generateBomb(self, imagepath, digitalcolor, explode_imagepath):
		return Bomb(imagepath=imagepath, coordinate=copy.deepcopy(self.coordinate), blocksize=self.blocksize, digitalcolor=digitalcolor, explode_imagepath=explode_imagepath)
	'''画到屏幕上  Drawing them onto the Screen'''
	def draw(self, screen, dt):
		# 冷却倒计时
		if self.bomb_cooling_count > 0:
			self.bomb_cooling_count -= dt
		screen.blit(self.image, self.rect)
		return True
	'''吃道具  Eating Props'''
	def eatProp(self, prop_sprite_group):
		eaten_prop = pygame.sprite.spritecollide(self, prop_sprite_group, True, None)
		for prop in eaten_prop:
			self.health_value += prop.value
	'''更新角色朝向  Update the characters' orientation'''
	def __updateImage(self, direction):
		directions = ['left', 'right', 'up', 'down']
		idx = directions.index(direction)
		self.image = pygame.image.load(self.imagepaths[idx])
		self.image = pygame.transform.scale(self.image, (self.blocksize, self.blocksize))
