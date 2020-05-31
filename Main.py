import pygame
import random
import math
from pygame import mixer
# import pickle

# initialize the pygame
pygame.init()

# create the game screen
# left-top corner has coordinate (0, 0)
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

try:
	with open('score.txt', 'r') as file:
		line = file.readline()
		highest_score = int(line)
except:
	highest_score = 0

# player
# image size 64px
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

player_lives = 5

# enemyies
# image size 64px
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemy_bulletImg = []
enemy_bulletX = []
enemy_bulletY = []
enemy_bulletY_change = []
enemy_bullet_fire = []
num_enemy = 0

def add_enemy():
	enemyImg.append(pygame.image.load('ufo.png'))
	enemyX.append(random.randint(10, 726))
	enemyY.append(random.randint(50, 150))
	enemyX_change.append(2) # slower than player
	enemy_bulletImg.append(pygame.image.load('enemy_bullet.png'))
	enemy_bulletX.append(enemyX[num_enemy-1])
	enemy_bulletY.append(enemyY[num_enemy-1])
	enemy_bulletY_change.append(3) # slower than player bullet
	enemy_bullet_fire.append(True)

# bullet
# image size 32px
bulletImg = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = playerY
bulletY_change = 4
bullet_fire = False

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

lives_text_font = pygame.font.Font('freesansbold.ttf', 32)
lives_text = lives_text_font.render("Lives: ", True, (192, 192, 192))

livesImg = []
for i in range(player_lives):
	livesImg.append(pygame.image.load('lives.png'))

game_over_font = pygame.font.Font('freesansbold.ttf', 64)
try_again_font = pygame.font.Font('freesansbold.ttf', 64)

def draw_lives(i):
	screen.blit(lives_text, (580, 40))
	screen.blit(livesImg[i], (680 + 20*i, 50))

def game_over_text():
	game_over = game_over_font.render("GAME OVER", True, (255, 0, 0))
	screen.blit(game_over, (200, 250))

def try_again_text():
	try_again = try_again_font.render("TRY AGAIN?", True, (192, 192, 192))
	screen.blit(try_again, (200, 350))

def show_score(x, y):
	score = font.render("Score: " + str(score_value), True, (192, 192, 192))
	screen.blit(score, (x, y))

def show_highest_score(x, y):
	personal_high = font.render("Personal High: " + str(highest_score), True, (192, 192, 192))
	screen.blit(personal_high, (x, y))

def player(x, y):
	# draw the player image
	screen.blit(playerImg, (x, y))

def enemy(x, y, i):
	# draw the player image
	screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
	global bullet_fire
	bullet_fire = True
	screen.blit(bulletImg, (x + 16, y + 10))

# does the bullet hit the enemy?
def is_collision(x1, y1, x2, y2):
	distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
	if distance < 27:
		return True
	return False

running = True

while running:
	screen.fill((0, 128, 128))
	# background Image
	screen.blit(background, (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		# check the keystroke pressed
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -4
			if event.key == pygame.K_RIGHT:
				playerX_change = 4
			if event.key == pygame.K_UP:
				playerY_change = -4
			if event.key == pygame.K_DOWN:
				playerY_change = 4
			if event.key == pygame.K_SPACE:
				if bullet_fire is False:
					bullet_sound = mixer.Sound('laser.wav')
					bullet_sound.play()
					bulletX = playerX
					bulletY = playerY
					fire_bullet(bulletX, bulletY)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				playerY_change = 0

	playerX += playerX_change
	playerY += playerY_change

	# check boundaries
	if playerX <= 10:
		playerX = 10
	elif playerX >= 726:
		playerX = 726
	if playerY <= 10:
		playerY = 10
	elif playerY >= 526:
		playerY = 526

	if score_value / 10 >= num_enemy and num_enemy < 5:
		num_enemy += 1
		player_lives = 5
		add_enemy()

	for i in range(num_enemy):
		enemy_bulletY[i] += enemy_bulletY_change[i]
		screen.blit(enemy_bulletImg[i], (enemy_bulletX[i] + 16, enemy_bulletY[i] + 10))

		collision = is_collision(playerX, playerY, enemy_bulletX[i], enemy_bulletY[i])

		if (enemy_bulletY[i] >= 600 or collision):
			enemy_bulletX[i] = enemyX[i]
			enemy_bulletY[i] = enemyY[i]

		if collision:
			collision = False
			player_lives -= 1

		for j in range(player_lives):
			draw_lives(j)

		# game over
		if player_lives == 0 or enemyY[i] > 486:
			for j in range(num_enemy):
				enemyY[i] = 1000 # make sure they disappear from screen
			game_over_text()
			try_again_text()
			break

		enemyX[i] += enemyX_change[i]
		# enemy movement
		if enemyX[i] <= 10 or enemyX[i] >= 726:
			enemyX_change[i] = -enemyX_change[i]
			enemyY[i] += 30

		hitten = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
		if hitten and bullet_fire is True:
			explosion_sound = mixer.Sound('explosion.wav')
			explosion_sound.play()
			bullet_fire = False
			bulletX = playerX
			bulletY = playerY
			score_value += 1
			enemyX[i] = random.randint(10, 726)
			enemyY[i] = random.randint(50, 150)

		enemy(enemyX[i], enemyY[i], i)

	# recycle bullets
	if bulletY <= 0:
		bullet_fire = False

	# bullet movement
	if bullet_fire is True:
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change

	# update personal high
	if score_value > highest_score:
		highest_score = score_value
		# write highest score
		with open('score.txt', 'w+') as file:
			file.write(str(highest_score))

	player(playerX, playerY)
	show_score(textX, textY)
	show_highest_score(textX, textY + 30)

	pygame.display.update()