import math
import sys

import pygame
import soundcard
import numpy

from audio_analyzer import AudioAnalyzer

# initialize pygame 
pygame.init()

# setup config vars 
window_scale = 0.75 # set to 1 for production

size = width, height = math.floor(1920 * window_scale), math.floor(1080 * window_scale)
black = 0, 0, 0 

screen = pygame.display.set_mode(size) 

speaker = soundcard.default_speaker()
soundIn = soundcard.get_microphone(speaker._id, 1)

# fps / samplerate config ... ?
fps = 60
b_debug_draw = False

# create audio analyzer instance 
analyzer = AudioAnalyzer()
analyzer.b_debug_draw = b_debug_draw

clock = pygame.time.Clock()


font = pygame.font.Font(None, 30)



# keep track of overall average 

# scale multipliers config
spike_multiplier = 0.25 
spike_multiplier_surround = 0.25



overall_average = 0

# define thresholds 

pulse_threshold = 0.6

# decay config 
overall_average_decay = 0.90 # value gets multiplied by this amount every frame 
logo_scale_factor_decay = 0.96

# images config stuff 

img_logo = pygame.image.load("resources/logo_icon.png").convert_alpha()
img_logo_surround = pygame.image.load("resources/logo_surround.png").convert_alpha()
logo_size = 600
logo_scale_factor = 1
logo_scale_factor_max = 2
logo_surround_scale_factor = 1
logo_surround_scale_factor_max = 2


img_background = pygame.image.load("resources/background.png").convert()


def pulse(spike):
	global logo_scale_factor, logo_surround_scale_factor
	logo_scale_factor = min(max(logo_scale_factor, 1 + (spike * spike_multiplier)), logo_scale_factor_max)
	logo_surround_scale_factor = min(max(logo_surround_scale_factor, 1 + (spike * spike_multiplier_surround)), logo_surround_scale_factor_max)

	return 

def apply_decay():
	global logo_scale_factor, logo_surround_scale_factor, logo_scale_factor_decay, overall_average
	logo_scale_factor = max(logo_scale_factor_decay * logo_scale_factor, 1)
	logo_surround_scale_factor = max(logo_scale_factor_decay * logo_surround_scale_factor, 1)
	overall_average = max(overall_average * overall_average_decay, 0)


def on_beat(strength):
	pulse(strength)

analyzer.add_beat_callback(on_beat)

def update(dt):
	analyzer.update(dt)
	apply_decay()

def draw():
	screen.fill(black)	

	# draw background image
	bg = pygame.transform.scale(img_background, (width, height))
	screen.blit(bg, (0, 0))

	# draw logo's circle bg
	logo_surround = pygame.transform.scale(img_logo_surround, (math.floor(
		logo_size * logo_surround_scale_factor), math.floor(logo_size * logo_surround_scale_factor)))
	rect = logo_surround.get_rect(center=(width / 2, height / 2))
	screen.blit(logo_surround, rect)

	# draw logo icon
	logo = pygame.transform.scale(img_logo, (math.floor(
		logo_size * logo_scale_factor), math.floor(logo_size * logo_scale_factor)))
	rect = logo.get_rect(center=(width / 2, height / 2))
	screen.blit(logo, rect)

	analyzer.draw(screen, width, height)

	pygame.display.flip()
	pygame.display.update()

done = False 
while not done:

	# lock to 60 fps
	clock.tick(fps)
	dt = clock.get_time()

	update(dt)

	draw()

	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			done = True 



pygame.quit()
