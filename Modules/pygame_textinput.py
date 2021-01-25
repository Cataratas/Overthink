"""
Copyright 2017, Silas Gyger, silasgyger@gmail.com, All rights reserved.

Borrowed from https://github.com/Nearoo/pygame-text-input under the MIT license.
"""

import os.path
import pyperclip

import pygame
import pygame.locals as pl

pygame.font.init()


class TextInput:
	def __init__(self, input_string="", font_family="", limit=0, lines=False, click=False, message=None, rect=None, font_size=24, antialias=True, text_color=(0, 0, 0), surf_color=None, cursor_color=(0, 0, 0), contain=False):
		
		self.input_string = input_string
		self.font_family = ""
		self.font_size = font_size
		self.antialias = antialias
		self.surf_color = surf_color
		self.text_color = text_color
		self.cursor_color = cursor_color
		self.limit = limit
		self.mult_line = lines
		self.click = click
		self.prompt = message
		self.rect = rect
		self.focus = "always"
		self.contain = contain
		self.cursor_toggle = True

		repeat_keys_initial_ms = 400
		repeat_keys_interval_ms = 35
		pygame.key.set_repeat(repeat_keys_initial_ms, repeat_keys_interval_ms)
		
		if click: self.focus = False
		
		if not os.path.isfile(font_family):
			font_family = pygame.font.match_font(font_family)
		
		self.font_object = pygame.font.Font(font_family, font_size)
		
		# Text-surface will be created during the first update call:
		self.surface = pygame.Surface((1, 1))
		self.surface.set_alpha(0)

		# Vars to make keydowns repeat after user pressed a key for some time:
		self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
		self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
		self.keyrepeat_interval_ms = repeat_keys_interval_ms

		# Things cursor:
		self.cursor_surface = pygame.Surface((int(self.font_size / 20 + 1), self.font_size))
		self.cursor_surface.fill(cursor_color)
		self.cursor_position = len(input_string)  # Inside text
		self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
		self.cursor_switch_ms = 750  # /|\
		self.cursor_ms_counter = 0
		self.clock = pygame.time.Clock()

	def update(self, events):
		Type, word_height = False, 0
		for event in events:
				
			# Click on text box to type
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.focus == "always":
				self.focus = self.rect.collidepoint(event.pos)
			
			if event.type == pl.KEYUP and event.key == pl.K_RIGHT:
				self.cursor_toggle, self.cursor_visible = True, True
			elif event.type == pl.KEYDOWN and event.key == pl.K_RIGHT:
				self.cursor_toggle, self.cursor_visible = False, True
			elif event.type == pl.KEYUP and event.key == pl.K_LEFT:
				self.cursor_toggle, self.cursor_visible = True, True
			elif event.type == pl.KEYDOWN and event.key == pl.K_LEFT:
				self.cursor_toggle, self.cursor_visible = False, True

			if event.type == pygame.TEXTINPUT and self.focus:
				self.cursor_visible = True  # So the user sees where he writes

				# If none exist, create counter for that key:
				if event.text not in self.keyrepeat_counters:
					self.keyrepeat_counters[event.text] = [0, event.text]

				# Controls character limit
				temp = self.font_object.render(self.input_string, self.antialias, self.text_color)
				temp_width, temp_height = temp.get_size()
				if self.contain and not self.mult_line and self.rect is not None:
					if temp_width < self.rect.width-self.font_object.size(' ')[0]*2: Type = True
				elif len(self.input_string) < self.limit or self.limit == 0: Type = True
				
				if Type:
					# If no special key is pressed, add unicode of key to input_string
					self.input_string = (
							self.input_string[:self.cursor_position]
							+ event.text
							+ self.input_string[self.cursor_position:]
						)
					self.cursor_position += len(event.text)  # Some are empty, e.g. K_UP
			
			elif event.type == pl.KEYDOWN and self.focus:

				if event.key == pl.K_BACKSPACE:
					self.input_string = (
						self.input_string[:max(self.cursor_position - 1, 0)]
						+ self.input_string[self.cursor_position:]
						)
						
					# Subtract one from cursor_pos, but do not go below zero:
					self.cursor_position = max(self.cursor_position - 1, 0)
				
				elif event.key == pl.K_DELETE:
					self.input_string = (
						self.input_string[:self.cursor_position]
						+ self.input_string[self.cursor_position + 1:]
					)

				elif event.key == pl.K_RETURN or event.key == pl.K_KP_ENTER:
					return True

				elif event.key == pl.K_RIGHT:
					# Add one to cursor_pos, but do not exceed len(input_string)
					self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

				elif event.key == pl.K_LEFT:
					# Subtract one from cursor_pos, but do not go below zero:
					self.cursor_position = max(self.cursor_position - 1, 0)

				elif event.key == pl.K_END:
					self.cursor_position = len(self.input_string)
	
				elif event.key == pl.K_HOME:
					self.cursor_position = 0
				
				# Paste functionality
				elif pygame.key.get_mods() & pygame.KMOD_CTRL and event.key == pl.K_v:
					if len(self.input_string + pyperclip.paste()) <= self.limit or self.limit == 0:
						self.input_string += pyperclip.paste()
						self.cursor_position = len(self.input_string)

			elif event.type == pl.KEYUP:
				# *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
				if event.key in self.keyrepeat_counters:
					del self.keyrepeat_counters[event.key]

		# Update key counters:
		for key in self.keyrepeat_counters:
			self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

			# Generate new key events if enough time has passed:
			if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
				self.keyrepeat_counters[key][0] = (
					self.keyrepeat_intial_interval_ms
					- self.keyrepeat_interval_ms
				)

				event_key, event_unicode = key, self.keyrepeat_counters[key][1]
				pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=event_key, unicode=event_unicode))

		if self.rect is not None: self.surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA, 32)
		
		# Re-render text surface
		if not self.focus and len(self.input_string) == 0:
			if self.surf_color is not None: self.surface.fill(self.surf_color)
			self.surface.blit(self.font_object.render(self.prompt, self.antialias, self.text_color), (0, 0))

		elif self.mult_line:
			if self.surf_color is not None: self.surface.fill(self.surf_color)
			x, y = 0, 0
			space = self.font_object.size(' ')[0]
			words = [word.split() for word in self.input_string.splitlines()]
			for line in words:
				for word in line:
					word_surface = self.font_object.render(word, self.antialias, self.text_color)
					word_width, word_height = word_surface.get_size()
					if x + word_width >= self.rect.w:
						x = 0
						y += word_height
					self.surface.blit(word_surface, (x, y))
					x += word_width + space
				x = 0; y += word_height

		else:
			if self.surf_color is not None: self.surface.fill(self.surf_color)
			if self.input_string == "": self.surface.blit(self.font_object.render(" ", self.antialias, self.text_color), (0, 0))
			else: self.surface.blit(self.font_object.render(self.input_string, self.antialias, self.text_color), (0, 0))
			if self.rect is None: self.surface = self.font_object.render(self.input_string, self.antialias, self.text_color)

		# Update self.cursor_visible
		if self.cursor_toggle:
			self.cursor_ms_counter += self.clock.get_time()
			if self.cursor_ms_counter >= self.cursor_switch_ms:
				self.cursor_ms_counter %= self.cursor_switch_ms
				self.cursor_visible = not self.cursor_visible

		if self.cursor_visible and self.focus:
			cursor_x_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]

			# Without this, the cursor is invisible when self.cursor_position > 0
			if self.cursor_position > 0:
				cursor_x_pos -= self.cursor_surface.get_width()
			self.surface.blit(self.cursor_surface, (cursor_x_pos, 0))

		self.clock.tick()
		return False

	def get_surface(self): return self.surface

	def get_text(self): return self.input_string

	def get_cursor_position(self): return self.cursor_position

	def get_active(self): return self.focus

	def clear_text(self):
		self.input_string = ""
		self.cursor_position = 0


if __name__ == "__main__":
	pygame.init()

	# Create TextInput-object
	rect = pygame.Rect(10, 10, 980, 180)
	TextInput = TextInput(rect=rect, font_size=32, lines=True)

	screen = pygame.display.set_mode((1000, 200))
	clock = pygame.time.Clock()

	while True:
		screen.fill((225, 225, 225))

		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT: exit()

		# Feed it with events every frame
		TextInput.update(events)
		# Blit its surface onto the screen
		screen.blit(TextInput.get_surface(), (10, 10))

		pygame.display.update(); clock.tick(15)
