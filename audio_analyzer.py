import soundcard
import numpy 
import pygame 
import math 
from util import remap

class AudioAnalyzer: 

	# static config vars 

	softest_magnitude = 0
	loudest_magnitude = 4

	def __init__(self, *args, **kwargs):
		# initialize instance properties 
		self.b_debug_draw = False

		self.sample_rate = 44100
		self.frame_sample = 256
		
		self.history_size = 30 

		self.samples = []
		
		speaker = soundcard.default_speaker()
		self.soundIn = soundcard.get_microphone(speaker._id, 1)

		# this will contain the last 44032 samples' energies 
		self.history_buffer = [0.] * self.history_size

		self.beat_callbacks = []
	
		return super().__init__(*args, **kwargs)

	def call_beat(self, beat_strength):
		# call beat callbacks 
		for cb in self.beat_callbacks:
			cb(beat_strength)

	def add_beat_callback(self, callback):
		self.beat_callbacks.append(callback)

	def get_instant_energy(self):
		res = 0 

		for i in range(0, self.frame_sample):
			res += math.pow(self.samples[i][0], 2) + math.pow(self.samples[i][1], 2)

		return res

	def get_local_average_energy(self):
		res = 0

		for n in self.history_buffer:
			res += n

		return res / len(self.history_buffer)

	def compute_variance(self, in_average_energy):
		res = 0 

		for n in self.history_buffer:
			res += math.pow(n - in_average_energy, 2)

		return res / len(self.history_buffer)

	def record(self):
		self.samples = self.soundIn.record(self.frame_sample, self.sample_rate, [0, 1])


	def analyze(self):
		instant_energy = self.get_instant_energy() 

		if (instant_energy > 0.001):

			local_average_energy = self.get_local_average_energy() 

			# print(local_average_energy)

			variance_energies = self.compute_variance(local_average_energy)

			# compute constant C (see reference)
			constant_C = (-0.0025714 * variance_energies) + 1.5142857

			self.history_buffer = numpy.roll(self.history_buffer, 1) 
			self.history_buffer[0] = instant_energy

			# detect beat :)

			if (instant_energy > constant_C * local_average_energy):
				self.call_beat(instant_energy - (constant_C * local_average_energy))
			
	# run on tick 
	def update(self, dt):

		# get ff-transformed audio data from default sound device 
		self.record()

		# analyze and detect beats 
		self.analyze()

		return 



	# debug only 
	def draw(self, surface, width, height):
		if (self.b_debug_draw):
			for frame, magnitude in enumerate(self.magnitudes):
				bandPixelHeight = remap(magnitude, self.softest_magnitude, self.loudest_magnitude, 0, height)
				bandPixelWidth = width / len(self.magnitudes)
				pygame.draw.rect(surface, (255, 255, 255), [
            		frame * bandPixelWidth, height - bandPixelHeight, bandPixelWidth, bandPixelHeight])
		return 

