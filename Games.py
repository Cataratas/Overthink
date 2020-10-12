import random
import pygame.freetype
import time
# import pygame
from Functions import Button, draw, centerprint, Time
from Variables import *

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720))


def tictactoe():
	buttons = [[Button(" ", "Tile", (121, 121)) for i in range(3)] for j in range(3)]
	board = [[0 for i in range(3)] for j in range(3)]

	userscore, compscore, winscore, start, player = 0, 0, 3, True, True

	while True:
		mouse = pygame.mouse.get_pos()
		sw, sh = screen.get_size()

		for event in pygame.event.get():
			if event.type == pygame.QUIT: return False
			elif event.type == pygame.VIDEORESIZE:
				if event.w < 1280: event.w = 1280
				if event.h < 720: event.h = 720
				pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

			for i in range(3):
				for j in range(3):
					if buttons[i][j].click(event, board[i][j] == 0): board[i][j], player = "x", False

		if start:
			board = [[0 for i in range(3)] for j in range(3)]
			player, start = True, False

		# Victory / Draw
		if board[0][0] == board[0][1] == board[0][2] == "x" or board[1][0] == board[1][1] == board[1][2] == "x" or \
				board[2][0] == board[2][1] == board[2][2] == "x" or board[0][0] == board[1][0] == board[2][0] == "x" or \
				board[0][1] == board[1][1] == board[2][1] == "x" or board[0][2] == board[1][2] == board[2][2] == "x" or \
				board[0][0] == board[1][1] == board[2][2] == "x" or board[0][2] == board[1][1] == board[2][0] == "x":
			userscore += 1; start = True
		elif board[0][0] == board[0][1] == board[0][2] == "o" or board[1][0] == board[1][1] == board[1][2] == "o" or \
				board[2][0] == board[2][1] == board[2][2] == "o" or board[0][0] == board[1][0] == board[2][0] == "o" or \
				board[0][1] == board[1][1] == board[2][1] == "o" or board[0][2] == board[1][2] == board[2][2] == "o" or \
				board[0][0] == board[1][1] == board[2][2] == "o" or board[0][2] == board[1][1] == board[2][0] == "o":
			compscore += 1; start = True
		elif board[0][0] != 0 and board[0][1] != 0 and board[0][2] != 0 and board[1][0] != 0 and board[1][1] != 0 and \
				board[1][2] != 0 and board[2][0] != 0 and board[2][1] != 0 and board[2][2] != 0:
			start = True

		if userscore == winscore: return True
		elif compscore == winscore: return False

		while not player and not start:
			for t in ["o", "x"]:
				for i in range(3):
					x, y, dr1, dr2, dl1, dl2 = 2, 2, 0, 2, 0, 2
					for j in range(2):
						if board[i][j] == t and board[i][j+1] == t and board[i][x] == 0 and not player:  # Check for X-X-0 (row)
							board[i][x], player = "o", True
						else: x = 0
						if board[j][i] == t and board[j+1][i] == t and board[y][i] == 0 and not player:  # Check for X-X-0 (column)
							board[y][i], player = "o", True
						else: y = 0
						if board[i][j] == t and board[i][2] == t and board[i][j+1] == 0 and not player:  # Check for X-0-X (row)
							board[i][j+1], player = "o", True
						if board[j][i] == t and board[2][i] == t and board[j+1][i] == 0 and not player:  # Check for X-0-X (column)
							board[j+1][i], player = "o", True
						if board[dr1][dr1] == t and board[dr1+1][dr1+1] == t and board[dr2][dr2] == 0 and not player:  # Check X-X-0 (diagonal - right to left)
							board[dr2][dr2], player = "o", True
						else: dr1, dr2 = 1, 0
						if board[dl1][dl2] == t and board[1][1] == t and board[dl2][dl1] == 0 and not player:  # Check X-X-0 (diagonal - left to right)
							board[dl2][dl1], player = "o", True
						else: dl1, dl2 = 2, 0
						if board[0][0] == t and board[2][2] == t and board[1][1] == 0 and not player:  # Check X-0-X (diagonal - right to left)
							board[1][1], player = "o", True
						if board[0][2] == t and board[2][0] == t and board[1][1] == 0 and not player:  # Check X-0-X (diagonal - left to right)
							board[1][1], player = "o", True
			if not player:
				i = random.randint(0, 2)
				j = random.randint(0, 2)
				if board[i][j] == 0: board[i][j], player = "o", True

		screen.fill(white)

		for i in range(winscore):
			draw("./Layout/BlackCircle.png", sw//2 - 162 - 38*i, sh*.06)
			draw("./Layout/BlackCircle.png", sw//2 + 135 + 38*i, sh*.06)
		for i in range(userscore): draw("./Layout/BlueCircle.png", sw//2 - 162 - 38*i, sh*.06)
		for i in range(compscore): draw("./Layout/RedCircle.png", sw//2 + 135 + 38*i, sh*.06)

		for i in range(3):
			for j in range(3):
				buttons[i][j].show(mouse, sw//2 + 64 - 129*i, sh//2 + 64 - 129*j, board[i][j] == 0)
				if board[i][j] == "x": draw("./Layout/X.png", sw//2 + 87 - 129*i, sh//2 + 87 - 129*j)
				elif board[i][j] == "o": draw("./Layout/O.png", sw//2 + 87 - 129*i, sh//2 + 87 - 129*j)

		pygame.display.update(), clock.tick(25)


def minesweeper():
	class Tile:
		def __init__(self):
			self.bomb = False
			self.near = 0
			self.visible = False
			self.flag = False
			self.doubt = False

	global flags
	rows, columns, width, bombs = 16, 32, 40, 65
	defeat, seconds, flags, timepiece = False, None, bombs, Time()
	colors = [blue, green, red2, darkblue, darkred, s_darkgray, s_darkgray, s_darkgray]
	grid = [[Tile() for y in range(columns)] for x in range(rows)]
	win, startTime = None, None

	def bombcounter(x, y):  # Checks bombs near tile
		bombnear = 0
		for (cx, cy) in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
			try:
				if y+cy < 0 or x+cx < 0:  # Avoid off grid checking
					raise IndexError
				if grid[y+cy][x+cx].bomb:
					bombnear += 1
					grid[y][x].near = bombnear
				grid[y][x].visible = True
			except IndexError: pass

	def search(x, y, rows=rows, columns=columns):
		global flags
		if x >= 0 and x < columns and y >= 0 and y < rows:
			tile = grid[y][x]
			if tile.visible or tile.bomb: return
			bombcounter(x, y)
			if tile.flag: flags += 1
			if tile.near > 0: return
			tile.visible = True
			for (cx, cy) in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
				search(x+cx, y+cy)

	for b in range(bombs):  # Place the bombs
		while True:
			x, y = random.randint(0, rows-1), random.randint(0, columns-1)
			if not grid[x][y].bomb: grid[x][y].bomb = True; break

	while True:
		mouse = pygame.mouse.get_pos()
		sw, sh = screen.get_size()
		mx, my = (mouse[0] - (sw // 2 - (width * columns) // 2)) // width, (mouse[1] - (sh // 2 - (width * rows) // 2)) // width - 1

		for event in pygame.event.get():  # Check events
			if event.type == pygame.QUIT: return False
			elif event.type == pygame.VIDEORESIZE:
				if event.w < 1280: event.w = 1280
				if event.h < 720: event.h = 720
				pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

			if event.type == pygame.MOUSEBUTTONDOWN and not defeat and not win:
				if event.button == 1 and mx >= 0 and mx < columns and my >= 0 and my < rows:
					if not grid[my][mx].flag:  # Check clicked tile
						if grid[my][mx].bomb: defeat = True  # Defeat
						search(mx, my)

				if event.button == 3 and mx >= 0 and mx < columns and my >= 0 and my < rows:  # Right click tile
					if grid[my][mx].doubt: grid[my][mx].doubt, grid[my][mx].flag = False, False; break
					if not grid[my][mx].visible:
						if grid[my][mx].flag: grid[my][mx].flag = False; flags += 1
						elif flags > 0: grid[my][mx].flag = True; flags -= 1
					if not grid[my][mx].flag: grid[my][mx].doubt = not grid[my][mx].doubt

		if defeat:  # Defeat
			if seconds is None: startTime = time.time()
			seconds = round(int(time.time() - startTime))
			if seconds > 3: return False

		win = True  # Victory
		for r in grid:
			for t in r:
				if t.bomb and not t.flag:
					win = False; break
		if win:
			if seconds is None: startTime = time.time()
			seconds = round(int(time.time() - startTime))
			if seconds > 3: return True

		screen.fill(white)

		pygame.draw.rect(screen, orange, pygame.Rect((sw // 2 - 170, sh // 8 - 80, 110, 37)), 1); pygame.draw.rect(screen, gray2, pygame.Rect((sw // 2 + 60, sh // 8 - 80, 110, 37)), 1)
		centerprint(flags, sw // 2 - 170, sh // 8 - 80, 110, 37, orange); centerprint(timepiece.get_time(), sw // 2 + 60, sh // 8 - 80, 110, 37, gray2)

		y = (sh // 2) - (width * (rows-2)) // 2
		for row in grid:
			x = (sw // 2) - (width * columns) // 2
			for tile in row:

				if tile.bomb and defeat: pygame.draw.rect(screen, red2, [x, y, width, width])  # Display bomb location
				else: pygame.draw.rect(screen, lightgray, [x, y, width, width])  # Display tiles

				if tile.flag and not defeat: pygame.draw.rect(screen, lightorange, [x, y, width, width])  # Display flagged tiles
				if tile.doubt and not defeat: pygame.draw.rect(screen, lightgreen, [x, y, width, width])  # Display doubted tiles

				if tile.visible and not tile.bomb:  # Display quantity of near bombs
					pygame.draw.rect(screen, white, [x, y, width, width])
					if tile.near != 0: centerprint(tile.near, x, y, width, width, colors[tile.near - 1])

				rect = pygame.Rect((x, y, width+1, width+1))  # Display Grid
				if not tile.visible: pygame.draw.rect(screen, black, rect, 1)
				else: pygame.draw.rect(screen, darkgray, rect, 1)

				x += width
			y += width

		x = mx * width + ((sw // 2) - (width * columns) // 2)
		y = (my * width + width) + (sh // 2 - (width * rows) // 2)
		if mx >= 0 and mx < columns and my >= 0 and my < rows and grid[my][mx].near == 0 and not defeat and not grid[my][mx].visible and not win:  # Mouse following
			if grid[my][mx].flag: pygame.draw.rect(screen, orange, [x, y, width, width])  # Flag tile
			if grid[my][mx].doubt: pygame.draw.rect(screen, darkgreen, [x, y, width, width])  # Doubt tile
			if not grid[my][mx].flag and not grid[my][mx].doubt: pygame.draw.rect(screen, gray3, [x, y, width, width])  # Unchecked tile
			rect = pygame.Rect((x, y, width + 1, width + 1))
			pygame.draw.rect(screen, black, rect, 1)

		if not win and not defeat: timepiece.update()

		pygame.display.update(), clock.tick(25)


def maze():
	class Character:
		def __init__(self):
			self.x = 0
			self.y = 0
			self.radius = 2
			self.right = True

		def show(self, sw, sh):
			global n_keys
			if self.right: draw("./Layout/Player.png", (int(sw / 2 - 611) + width * self.x)+8, (int(sh / 2 - 296) + width * self.y)+3, True)
			else: draw("./Layout/Player.png", (int(sw / 2 - 611) + width * self.x)+8, (int(sh / 2 - 296) + width * self.y)+3, False)
			for i in range(3):
				try:
					if self.x == Keys[i].x and self.y == Keys[i].y:
						del Keys[i]
						n_keys += 1
				except IndexError: continue

		def update(self):
			p_k = pygame.key.get_pressed()
			if (p_k[pygame.K_RIGHT] or p_k[pygame.K_d]) and (Grid[self.x+1][self.y] != 1):
				self.x += 1
			elif (p_k[pygame.K_LEFT] or p_k[pygame.K_a]) and (Grid[self.x-1][self.y] != 1):
				self.x -= 1; self.right = False
			elif (p_k[pygame.K_UP] or p_k[pygame.K_w]) and (Grid[self.x][self.y-1] != 1):
				self.y -= 1
			elif (p_k[pygame.K_DOWN] or p_k[pygame.K_s]) and (Grid[self.x][self.y+1] != 1):
				self.y += 1
			if p_k[pygame.K_RIGHT] or p_k[pygame.K_d]: self.right = True
			if p_k[pygame.K_LEFT] or p_k[pygame.K_a]: self.right = False

	class Key:
		def __init__(self):
			self.x = 0
			self.y = 0

		def show(self, sw, sh):
			draw("./Layout/Key.png", (int(sw / 2 - 611) + width * self.x)+3, (int(sh / 2 - 296) + width * self.y)+3)

	class Exit:
		def __init__(self):
			self.x = 0
			self.y = 0

		def show(self, n_keys, sw, sh):
			if n_keys == 3: draw("./Layout/Door.png", (int(sw / 2 - 611) + width * self.x)+6, (int(sh / 2 - 296) + width * self.y)+3)
			else: draw("./Layout/Door 0.png", (int(sw / 2 - 611) + width * self.x)+6, (int(sh / 2 - 296) + width * self.y)+3)

	def create_grid(width, height):
		Grid = []
		for row in range(height):
			Grid.append([])
			for column in range(width):
				if column % 2 == 1 and row % 2 == 1:
					Grid[row].append(0)
				elif column == 0 or row == 0 or column == width - 1 or row == height - 1:
					Grid[row].append(1)
				else:
					Grid[row].append(1)
		return Grid

	def make_maze(Grid):
		w = (len(Grid[0]) - 1) // 2
		h = (len(Grid) - 1) // 2
		vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

		def walk(x: int, y: int):
			vis[y][x] = 1

			d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
			random.shuffle(d)
			for (xx, yy) in d:
				if vis[yy][xx]:
					continue
				if xx == x:
					Grid[max(y, yy) * 2][x * 2 + 1] = 0
				if yy == y:
					Grid[y * 2 + 1][max(x, xx) * 2] = 0

				walk(xx, yy)

		walk(random.randrange(w), random.randrange(h))

		return Grid

	global n_keys
	# Initialize Variables
	COLUMNS, ROWS, width, n_keys = 35, 17, 35, 0
	Player, Keys, Exit = Character(), [], Exit()
	Grid = create_grid(ROWS, COLUMNS)
	make_maze(Grid)

	# Randomly Position Stuff
	Player.x, Player.y = random.randint(0, COLUMNS-1), random.randint(0, ROWS-1)
	while Grid[Player.x][Player.y] != 0:
		Player.x, Player.y = random.randint(0, COLUMNS-1), random.randint(0, ROWS-1)
	for i in range(3):
		Keys.append(Key())
		Keys[i].x, Keys[i].y = random.randint(0, COLUMNS-1), random.randint(0, ROWS-1)
		while Grid[Keys[i].x][Keys[i].y] != 0:
			Keys[i].x, Keys[i].y = random.randint(0, COLUMNS - 1), random.randint(0, ROWS - 1)
	Exit.x, Exit.y = random.randint(0, COLUMNS - 1), random.randint(0, ROWS - 1)
	while Grid[Exit.x][Exit.y] != 0:
		Exit.x, Exit.y = random.randint(0, COLUMNS - 1), random.randint(0, ROWS - 1)

	while True:
		sw, sh = screen.get_size()

		for event in pygame.event.get():
			if event.type == pygame.QUIT: return False
			elif event.type == pygame.VIDEORESIZE:
				if event.w < 1280: event.w = 1280
				if event.h < 720: event.h = 720
				pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

		# Victory
		if n_keys == 3 and Player.x == Exit.x and Player.y == Exit.y: return True

		# Display Stuff
		screen.fill((25, 25, 25))

		for i in range(-n_keys + 3): Keys[i].show(sw, sh)
		Exit.show(n_keys, sw, sh)

		for x in range(1, COLUMNS-1):
			for y in range(1, ROWS-1):
				if Player.x + (Player.radius + 1) > x and Player.x - (Player.radius + 1) < x and Player.y + (Player.radius + 1) > y and Player.y - (Player.radius + 1) < y:
					if Grid[x][y] == 1: pygame.draw.rect(screen, blue, [int(sw/2 - 611)+width*x, int(sh/2 - 296)+width*y, width-3, width-3])
				else: pygame.draw.rect(screen, (151, 151, 151), [int(sw/2 - 611)+width*x, int(sh/2 - 296)+width*y, width-3, width-3])

		for x in range(COLUMNS):
			pygame.draw.rect(screen, red2, [int(sw/2 - 611)+width*x, int(sh/2 - 296), width-3, width-3])  # Top
			pygame.draw.rect(screen, red2, [int(sw / 2 - 611) + width * x, int(sh / 2 - 296)+(ROWS-1)*width, width - 3, width - 3])  # Bottom
			if width*x < 550: pygame.draw.rect(screen, red2, [int(sw / 2 - 611), int(sh / 2 - 296)+width*x, width - 3, width - 3])  # Left
			if width * x < 550: pygame.draw.rect(screen, red2, [int(sw / 2 + 579), int(sh / 2 - 296) + width * x, width - 3, width - 3])  # Right

		for x in range(3): draw("./Layout/Key 0.png", int(sw/2 - 45) + 35*x, int(sh / 2 - 342))
		for x in range(n_keys): draw("./Layout/Key.png", int(sw/2 - 45) + 35*x, int(sh / 2 - 342))

		Player.update(), Player.show(sw, sh)
		pygame.display.update(), clock.tick(12)


def sudoku():
	numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]

	def checkgrid(grid):
		for row in range(0, 9):
			for col in range(0, 9):
				if grid[row][col] == 0: return False
		return True

	def generatesudoku(grid):
		global counter
		row, col = 0, 0
		#  Find next empty cell
		for i in range(0, 81):
			row = i // 9
			col = i % 9
			if grid[row][col] == 0:
				random.shuffle(numberList)
				for value in numberList:
					#  Check that this value has not already be used on this row
					if not(value in grid[row]):
						#  Check that this value has not already be used on this column
						if value not in (grid[0][col], grid[1][col], grid[2][col], grid[3][col], grid[4][col], grid[5][col], grid[6][col], grid[7][col], grid[8][col]):
							#  Identify which of the 9 squares we are working on
							if row < 3:
								if col < 3: square = [grid[i][0:3] for i in range(0, 3)]
								elif col < 6: square = [grid[i][3:6] for i in range(0, 3)]
								else: square = [grid[i][6:9] for i in range(0, 3)]
							elif row < 6:
								if col < 3: square = [grid[i][0:3] for i in range(3, 6)]
								elif col < 6: square = [grid[i][3:6] for i in range(3, 6)]
								else: square = [grid[i][6:9] for i in range(3, 6)]
							else:
								if col < 3: square = [grid[i][0:3] for i in range(6, 9)]
								elif col < 6: square = [grid[i][3:6] for i in range(6, 9)]
								else: square = [grid[i][6:9] for i in range(6, 9)]
							#  Check that this value has not already be used on this 3x3 square
							if value not in (square[0] + square[1] + square[2]):
								grid[row][col] = value
								if checkgrid(grid): return True
								else:
									if generatesudoku(grid):
										return True
				break
		grid[row][col] = 0

	def remove(grid):
		global counter
		attempts = 1
		counter = 1
		while attempts > 0:
			#  Select a random cell that is not already empty
			row = random.randint(0, 8)
			col = random.randint(0, 8)
			while grid[row][col] == 0:
				row = random.randint(0, 8)
				col = random.randint(0, 8)
			#  Remember its cell value in case we need to put it back
			backup = grid[row][col]
			grid[row][col] = 0

			#  Take a full copy of the grid
			copyGrid = []
			for r in range(0, 9):
				copyGrid.append([])
				for c in range(0, 9):
					copyGrid[r].append(grid[r][c])

			#  Count the number of solutions that this grid has (using a backtracking approach implemented in the solvegrid() function)
			counter = 0
			solvegrid(copyGrid)
			#  If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
			if counter != 1:
				grid[row][col] = backup
				#  We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
				attempts -= 1

	def solvegrid(grid):
		global counter
		row, col = 0, 0
		#  Find next empty cell
		for i in range(0, 81):
			row = i // 9
			col = i % 9
			if grid[row][col] == 0:
				for value in range(1, 10):
					#  Check that this value has not already be used on this row
					if not(value in grid[row]):
						#  Check that this value has not already be used on this column
						if value not in (grid[0][col], grid[1][col], grid[2][col], grid[3][col], grid[4][col], grid[5][col], grid[6][col], grid[7][col], grid[8][col]):
							#  Identify which of the 9 squares we are working on
							if row < 3:
								if col < 3:
									square = [grid[i][0:3] for i in range(0, 3)]
								elif col < 6:
									square = [grid[i][3:6] for i in range(0, 3)]
								else:
									square = [grid[i][6:9] for i in range(0, 3)]
							elif row < 6:
								if col < 3:
									square = [grid[i][0:3] for i in range(3, 6)]
								elif col < 6:
									square = [grid[i][3:6] for i in range(3, 6)]
								else:
									square = [grid[i][6:9] for i in range(3, 6)]
							else:
								if col < 3:
									square = [grid[i][0:3] for i in range(6, 9)]
								elif col < 6:
									square = [grid[i][3:6] for i in range(6, 9)]
								else:
									square = [grid[i][6:9] for i in range(6, 9)]
							#  Check that this value has not already be used on this 3x3 square
							if value not in (square[0] + square[1] + square[2]):
								grid[row][col] = value
								if checkgrid(grid):
									counter += 1; break
								else:
									if solvegrid(grid): return True
				break
		grid[row][col] = 0

	def showsudoku(grid):
		for row in range(9):
			for col in range(9):
				rect = pygame.Rect(((sw//2 - 180)+row*width, (sh//2 - 220)+col*width, width+1, width+1))
				pygame.draw.rect(screen, (112, 112, 112), rect, 1)
				if grid[row][col] != 0: centerprint(grid[row][col], (sw//2 - 180)+row*width, (sh//2 - 220)+col*width, width, width, (51, 51, 51), FONT21)
		for i in range(4):
			pygame.draw.line(screen, black, ((sw//2 - 180), (sh//2 - 220)+120*i), ((sw//2 + 180), (sh//2 - 220)+120*i), 3)
			pygame.draw.line(screen, black, ((sw//2 - 180)+120*i, (sh//2 - 220)), ((sw//2 - 180)+120*i, sh//2 + 140), 3)

	class ButtonBox:
		def __init__(self, number, x=0, y=0):
			self.number = number
			self.rect = pygame.Rect((x, y), (47, 47))

		def set_pos(self, x, y):
			self.rect.x = x
			self.rect.y = y

		def show(self, mouse, x, y, active):
			self.set_pos(x, y)
			if active == self.number: pressed = True
			else: pressed = False
			if self.rect.x+self.rect.w > mouse[0] > self.rect.x and self.rect.y+self.rect.w > mouse[1] > self.rect.y and not pressed:
				pygame.draw.rect(screen, (117, 76, 36), [self.rect.x, self.rect.y, self.rect.w, self.rect.w])
				centerprint(self.number, self.rect.x, self.rect.y, self.rect.w, self.rect.w, white, FONT21)
			elif pressed:
				pygame.draw.rect(screen, (96, 56, 19), [self.rect.x, self.rect.y, self.rect.w, self.rect.w])
				centerprint(self.number, self.rect.x, self.rect.y, self.rect.w, self.rect.w, white, FONT21)
			else:
				pygame.draw.rect(screen, (96, 56, 19), pygame.Rect((self.rect.x, self.rect.y, self.rect.w, self.rect.w)), 1)
				centerprint(self.number, self.rect.x, self.rect.y, self.rect.w, self.rect.w, (96, 56, 19), FONT21)

		def click(self, event):
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1: return self.rect.collidepoint(event.pos)

	Grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(9)]

	width, active, actions, Timepiece = 40, None, [], Time()
	generatesudoku(Grid)

	s_grid = []
	for r in range(0, 9):
		s_grid.append([])
		for c in range(0, 9):
			s_grid[r].append(Grid[r][c])

	remove(Grid)

	m_grid = []
	for r in range(0, 9):
		m_grid.append([])
		for c in range(0, 9):
			m_grid[r].append(Grid[r][c])

	buttons = []
	for i in range(11):
		if i == 0: buttons.append(ButtonBox("✖"))
		elif i == 10: buttons.append(ButtonBox("↩"))
		else: buttons.append(ButtonBox(i))

	while True:
		mouse = pygame.mouse.get_pos()
		sw, sh = screen.get_size()
		mx, my = (mouse[0] - (sw//2 - 160 - 20)) // width, (mouse[1] - (sh//2 - 220)) // width

		win = True
		for i in range(9):
			for j in range(9):
				if s_grid[i][j] != Grid[i][j]: win = False; break
		if win: return True

		for event in pygame.event.get():
			if event.type == pygame.QUIT: return False
			elif event.type == pygame.VIDEORESIZE:
				if event.w < 1280: event.w = 1280
				if event.h < 720: event.h = 720
				pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

			for i in range(11):
				if buttons[i].click(event):
					if i == 0: active = "✖"
					elif i == 10:
						try:
							revert = actions[-1]
							Grid[revert[0]][revert[1]] = revert[2]
							del actions[-1]
						except IndexError: continue
					else: active = i

			if mx >= 0 and mx <= 8 and my >= 0 and my <= 8:
				if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					if Grid[mx][my] == 0 and active is not None and active != "✖":
						p = Grid[mx][my]
						Grid[mx][my] = active
						actions.append([mx, my, p])
					elif m_grid[mx][my] == 0 and active == "✖":
						p = Grid[mx][my]
						Grid[mx][my] = 0
						actions.append([mx, my, p])

		screen.fill(white)

		for i in range(9):
			for j in range(9):
				if active == "✖" and Grid[i][j] != m_grid[i][j]:
					pygame.draw.rect(screen, (253, 171, 159), [(sw//2 - 180)+i*width, (sh//2 - 220)+j*width, width, width])
				elif Grid[i][j] == active:
					pygame.draw.rect(screen, (210, 210, 210), [(sw//2 - 180)+i*width, (sh//2 - 220)+j*width, width, width])

		if mx >= 0 and mx <= 8 and my >= 0 and my <= 8 and Grid[mx][my] == 0 and active is not None and active != "✖":
			centerprint(active, (sw//2 - 180)+mx*width, (sh//2 - 220)+my*width, width+1, width+1, (125, 125, 125), FONT21)
		if active == "✖" and mx >= 0 and mx <= 8 and my >= 0 and my <= 8 and m_grid[mx][my] == 0 and Grid[mx][my] != 0:
			pygame.draw.rect(screen, (253, 112, 104), [(sw//2 - 180)+mx*width, (sh//2 - 220)+my*width, width, width])

		showsudoku(Grid)

		centerprint(Timepiece.get_time(), sw//2 - 65, 40, 130, 40, (96, 56, 19), FONT21)

		for i in range(11):
			buttons[i].show(mouse, sw//2 - 305+56*i, sh//2 + 220, active)

		pygame.display.update(), Timepiece.update(), clock.tick(25)


def memory():
	def freetypeprint(variable, x, y, sizeX, sizeY, color, font=pygame.freetype.Font('./Fonts/seguiemj.ttf', 50)):
		color = color[:-1] + (255, )
		text = font.render(str(variable), color)
		rect = pygame.Rect((x, y, sizeX, sizeY))
		text_rect = text[0].get_rect()
		text_rect.center = rect.center
		screen.blit(text[0], text_rect)

	class Tile:
		def __init__(self, symbol, color):
			self.symbol = symbol
			self.color = color
			self.visible = False
			self.paired = False

		def show(self, x, y, mouse, tile, w=121):
			s = pygame.Surface((w, w), pygame.SRCALPHA)
			s.fill((230, 230, 230))
			if mouse == tile and second is None: s.fill((214, 214, 214))
			if self.visible or self.paired:
				s.fill(self.color)
				freetypeprint(self.symbol, x, y, w, w, self.color)
			screen.blit(s, (x, y))

	rows, columns, flips, check, startTime, first, second = 5, 8, 0, False, None, None, None
	start, Timepiece, = True, Time()

	symbols = [["⚓", (251, 176, 59, 75)], ["🍇", (102, 45, 145, 75)], ["♻", (57, 181, 74, 75)], ["🐟", (41, 171, 226, 75)], ["💼", (117, 76, 36, 75)], ["🗽", (0, 169, 157, 75)], ["🛰", (27, 20, 100, 75)], ["🧠", (255, 123, 172, 75)], ["🦋", (163, 123, 15, 75)], ["🦊", (241, 90, 36, 75)], ["🦉", (199, 178, 153, 75)], ["🦅", (58, 46, 0, 75)], ["🔮", (160, 113, 167, 75)], ["👽", (0, 104, 55, 75)], ["☂", (0, 113, 188, 75)], ["🐦", (193, 39, 45, 75)], ["👁", (131, 138, 150, 75)], ["🌷", (216, 149, 164, 75)], ["❄", (161, 205, 231, 75)], ["⛄", (136, 157, 201, 75)]]
	symbols += symbols
	random.shuffle(symbols)

	grid = [["" for y in range(columns)] for x in range(rows)]
	for i in range(rows):
		for j in range(columns):
			grid[i][j] = Tile(symbols[-1][0], symbols[-1][1])
			del symbols[-1]

	while True:
		mouse = pygame.mouse.get_pos()
		sw, sh = screen.get_size()
		mx, my = (mouse[1] - (sh//2 - 317)) // 128, (mouse[0] - (sw//2 - 508)) // 128

		if start:
			for i in range(rows):
				for j in range(columns):
					grid[i][j].visible = True
			if Timepiece.seconds > 3:
				for i in range(rows):
					for j in range(columns):
						grid[i][j].visible = False
				start = False; Timepiece.reset()

		for event in pygame.event.get():
			if event.type == pygame.QUIT: return False
			elif event.type == pygame.VIDEORESIZE:
				if event.w < 1280: event.w = 1280
				if event.h < 720: event.h = 720
				pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

			if event.type == pygame.MOUSEBUTTONUP:
				if mx >= 0 and my >= 0 and mx < rows and my < columns and not grid[mx][my].paired and not grid[mx][my].visible and second is None:
					grid[mx][my].visible = True
					if flips == 0: first = grid[mx][my]
					elif flips == 1: second = grid[mx][my]
					flips += 1
					if flips == 2: check = True; Timepiece.reset()

		screen.fill(white)

		x, y = sw//2 - 508, sh//2 - 445
		win = True
		for i in range(rows):
			y += 128
			x = sw//2 - 508
			for j in range(columns):
				grid[i][j].show(x, y, (mx, my), (i, j))
				if not grid[i][j].paired: win = False
				x += 128

		if win: return True

		if first is not None and second is not None and first.symbol == second.symbol:
			first.paired, second.paired = True, True
			first, second, flips, check = None, None, 0, False

		if check and Timepiece.seconds >= 1:
			first.visible, second.visible = False, False
			first, second, flips, check = None, None, 0, False

		pygame.display.update(), Timepiece.update(), clock.tick(25)


def hangman(lang):
	alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

	list = []
	if lang == "pt": list = pt
	if lang == "en": list = en
	if lang == "es": list = es

	word = list[random.randint(0, len(list)-1)]
	letters, life, win = [], 7, None

	while True:
		sw, sh = screen.get_size()
		for i in range(len(word)):
			if word[i] not in letters: win = False; break
			win = True
		if win: pygame.time.delay(3000); return True

		for event in pygame.event.get():
			if event.type == pygame.QUIT: return False
			elif event.type == pygame.VIDEORESIZE:
				if event.w < 1280: event.w = 1280
				if event.h < 720: event.h = 720
				pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

			for i in alphabet:
				if event.type == pygame.TEXTINPUT and event.text.lower() == i and i not in letters:
					letters.append(event.text.lower())
					if event.text not in word: life -= 1

		screen.fill(white)

		draw("./Layout/Post.png", (sw//2) - 300, sh*.275)
		if life <= 6: draw("./Layout/Head.png", (sw//2) - 199, sh*.275 + 37)
		if life <= 5: draw("./Layout/Body.png", (sw//2) - 175, sh*.275 + 87)
		if life <= 4: draw("./Layout/Leg.png", (sw//2) - 202, sh*.275 + 153)
		if life <= 3: draw("./Layout/Leg.png", (sw//2) - 176, sh*.275 + 153, True)
		if life <= 2: draw("./Layout/Arm.png", (sw//2) - 194, sh*.275 + 98)
		if life <= 1: draw("./Layout/Arm.png", (sw//2) - 175, sh*.275 + 98, True)
		if life == 0:
			draw("./Layout/Face.png", (sw//2) - 187, sh*.275 + 52)
			pygame.display.update(), pygame.time.delay(3000)
			return False

		a = 1
		for i in range(len(word)):
			if i > 6: a += 1
		x = (sw//2) + 120 - (30*a)
		for i in word:
			if i in letters: centerprint(i.upper(), x, sh*.275 + 196, 15, 15, black, fontW)
			draw("./Layout/Blanks.png", x-6, sh*.275 + 214)
			x += 30

		x = (sw//2) - 390
		for i in range(len(alphabet)):
			if alphabet[i] in letters and alphabet[i] in word:
				centerprint(alphabet[i].upper(), x, sh*.275 + 452, 15, 15, (140, 198, 63), fontABC)
			elif alphabet[i] in letters:
				centerprint(alphabet[i].upper(), x, sh*.275 + 452, 15, 15, (193, 39, 45), fontABC)
			else: centerprint(alphabet[i].upper(), x, sh*.275 + 452, 15, 15, (230, 230, 230), fontABC)
			x += 30

		pygame.display.update(), clock.tick(25)
