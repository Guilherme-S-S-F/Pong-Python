import random
import pygame, sys

# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# Setting up the ball properties
ball_Yspeed = 7
ball_Xspeed = 7
ball_color = (255, 0, 0)
ball_size = (20, 20)
ball_rect = pygame.Rect(screen_width/2 - 10, screen_height/2 - 10, ball_size[0], ball_size[1])

# Setting up the paddles
paddle_size = (10, 100)
paddle_color = (255, 255, 255)

paddle_bot_speed = 7
paddle_player_speed = 0
player_speed = 6

paddle_player_rect = pygame.Rect(0, screen_height/2 - (paddle_size[1]/2), paddle_size[0], paddle_size[1])
paddle_bot_rect = pygame.Rect(screen_width - paddle_size[0], screen_height/2 - (paddle_size[1]/2), paddle_size[0], paddle_size[1])

# Scores
player_score = 0
bot_score = 0

# Score Text
score_font = pygame.font.Font('freesansbold.ttf', 32)

def opponent_ai():
	global paddle_bot_rect, ball_rect
	if paddle_bot_rect.top < ball_rect.y:
		paddle_bot_rect.y += paddle_bot_speed
	if paddle_bot_rect.bottom > ball_rect.y:
		paddle_bot_rect.y -= paddle_bot_speed

	if paddle_bot_rect.top <= 0:
		paddle_bot_rect.top = 0
	if paddle_bot_rect.bottom >= screen_height:
		paddle_bot_rect.bottom = screen_height

def ball_animation():
	global ball_Xspeed, ball_Yspeed, ball_rect, paddle_player_rect,paddle_bot_rect, bot_score, player_score
	
	ball_rect.x += ball_Xspeed
	ball_rect.y += ball_Yspeed

	if ball_rect.top <= 0 or ball_rect.bottom >= screen_height:
		ball_Yspeed *= -1
	if ball_rect.left <= 0 or ball_rect.right >= screen_width:
		ball_Xspeed *= -1

	if ball_rect.left <= 0:
		ball_start()
		bot_score += 1

	if ball_rect.right >= screen_width:
		ball_start()
		player_score += 1

	if ball_rect.colliderect(paddle_player_rect) or ball_rect.colliderect(paddle_bot_rect):
		ball_Xspeed *= -1

def ball_start():
	global ball_Xspeed, ball_Yspeed, ball_rect

	ball_rect.center = (screen_width/2, screen_height/2)
	ball_Yspeed *= random.choice((1,-1))
	ball_Xspeed *= random.choice((1,-1))

def player_animation():
	global paddle_player_rect, paddle_player_speed

	paddle_player_rect.y += paddle_player_speed

	if paddle_player_rect.top <= 0:
		paddle_player_rect.top = 0
	if paddle_player_rect.bottom >= screen_height:
		paddle_player_rect.bottom = screen_height

keys = []
random1 = random.Random()
while True:
	screen.fill((0, 0, 0))
	#Handling input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				paddle_player_speed -= player_speed
			if event.key == pygame.K_DOWN:
				paddle_player_speed += player_speed
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				paddle_player_speed += player_speed
			if event.key == pygame.K_DOWN:
				paddle_player_speed -= player_speed
	
	player_animation()	
	ball_animation()

	opponent_ai()

	pygame.draw.aaline(screen, (255, 255, 255), (screen_width/2,0), (screen_width/2,screen_height))
	pygame.draw.rect(screen, paddle_color, paddle_player_rect)
	pygame.draw.rect(screen, paddle_color, paddle_bot_rect)
	pygame.draw.ellipse(screen, ball_color, ball_rect)

	bot_text = score_font.render(f'{bot_score}',True,(200,200,200))
	screen.blit(bot_text,(660,470))

	player_text = score_font.render(f'{player_score}',True,(200,200,200))
	screen.blit(player_text,(600,470))

	
	# Updating the window 
	pygame.display.flip()
	clock.tick(60)
