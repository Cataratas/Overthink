import pygame, time, sys
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from PyPDF2 import PdfFileReader
from Modules import ptext

screen = pygame.display.set_mode((1280, 720))
pygame.font.init()


class Languages:
	def __init__(self):
		self.list = ["" for i in range(45)]
	
	def en(self):
		self.list[0] = "Start"
		self.list[1] = "Return"
		self.list[2] = "Previous"
		self.list[3] = "Next"
		self.list[4] = "Delete"
		self.list[5] = "New"
		self.list[6] = "Edit"
		self.list[7] = "Play"
		self.list[8] = "Exit"
		self.list[9] = "New Question"
		self.list[10] = "Delete Question"
		self.list[11] = "Save and Exit"
		self.list[12] = "Type title here"
		self.list[13] = "Type answer here"
		self.list[14] = "Give Up"
		self.list[15] = "Skip Question"
		self.list[16] = "Games"
		self.list[17] = "Play Again"
		self.list[18] = "Start Menu"
		self.list[19] = "Victory"
		self.list[20] = "Defeat"
		self.list[21] = "TicTacToe"
		self.list[22] = "Hangman"
		self.list[23] = "Minesweeper"
		self.list[24] = "Maze"
		self.list[25] = "Sudoku"
		self.list[26] = "Memory"
		self.list[27] = "Type question here"
		self.list[28] = "Language"
		self.list[29] = "Apply"
		self.list[30] = "Cancel"
		self.list[31] = "Are you sure you want to delete this quiz?"
		self.list[32] = "'{}' will be lost forever! (A long time!)"
		self.list[33] = "Play and get coins!"
		self.list[34] = "Language Selection"
		self.list[35] = "Are you sure you want to give up this quiz?"
		self.list[36] = "Print"
		self.list[37] = "One Column"
		self.list[38] = "Two Columns"
		self.list[39] = "With Answers"
		self.list[40] = "Without Answers"
		self.list[41] = "Print All"
		self.list[42] = "Date: __/__/__"
		self.list[43] = "Name:___________________________________________"
		self.list[44] = "Grade: _______"
		
	def pt(self):
		self.list[0] = "Iniciar"
		self.list[1] = "Voltar"
		self.list[2] = "Anterior"
		self.list[3] = "Próximo"
		self.list[4] = "Excluir"
		self.list[5] = "Novo"
		self.list[6] = "Editar"
		self.list[7] = "Jogar"
		self.list[8] = "Sair"
		self.list[9] = "Nova Questão"
		self.list[10] = "Excluir Questão"
		self.list[11] = "Salvar e Sair"
		self.list[12] = "Digite o título aqui"
		self.list[13] = "Digite a resposta aqui"
		self.list[14] = "Desistir"
		self.list[15] = "Pular Questão"
		self.list[16] = "Jogos"
		self.list[17] = "Jogar Novamente"
		self.list[18] = "Menu Inicial"
		self.list[19] = "Vitória"
		self.list[20] = "Derrota"
		self.list[21] = "Jogo da Velha"
		self.list[22] = "Jogo da Forca"
		self.list[23] = "Campo Minado"
		self.list[24] = "Labirinto"
		self.list[25] = "Sudoku"
		self.list[26] = "Memória"
		self.list[27] = "Digite a questão aqui"
		self.list[28] = "Idioma"
		self.list[29] = "Aplicar"
		self.list[30] = "Cancelar"
		self.list[31] = "Você realmente deseja excluir esse quiz?"
		self.list[32] = "'{}' será perdido para sempre! (Muito tempo!)"
		self.list[33] = "Jogue e ganhe moedas!"
		self.list[34] = "Seleção de Idioma"
		self.list[35] = "Você realmente deseja desistir desse quiz?"
		self.list[36] = "Imprimir"
		self.list[37] = "Uma Coluna"
		self.list[38] = "Duas Colunas"
		self.list[39] = "Com Gabarito"
		self.list[40] = "Sem Gabarito"
		self.list[41] = "Imprimir Todas"
		self.list[42] = "Data: __/__/__"
		self.list[43] = "Nome:___________________________________________"
		self.list[44] = "Nota: _______"
	
	def es(self):
		self.list[0] = "Comenzar"
		self.list[1] = "Volver"
		self.list[2] = "Anterior"
		self.list[3] = "Siguiente"
		self.list[4] = "Eliminar"
		self.list[5] = "Nuevo"
		self.list[6] = "Editar"
		self.list[7] = "Jugar"
		self.list[8] = "Salir"
		self.list[9] = "Nueva Pregunta"
		self.list[10] = "Eliminar Pregunta"
		self.list[11] = "Guardar y Salir"
		self.list[12] = "Escribe el título aquí"
		self.list[13] = "Escriba la respuesta aquí"
		self.list[14] = "Rendirse"
		self.list[15] = "Saltar Pregunta"
		self.list[16] = "Juegos"
		self.list[17] = "Jugar de Nuevo"
		self.list[18] = "Menu de Inicio"
		self.list[19] = "Victoria"
		self.list[20] = "Derrota"
		self.list[21] = "Tres en Raya"
		self.list[22] = "Verdugo"
		self.list[23] = "Dragaminas"
		self.list[24] = "Laberinto"
		self.list[25] = "Sudoku"
		self.list[26] = "Memoria"
		self.list[27] = "Escriba la pregunta aquí"
		self.list[28] = "Idioma"
		self.list[29] = "Aplicar"
		self.list[30] = "Cancelar"
		self.list[31] = "¿Estás seguro de que quieres eliminar este cuestionario?"
		self.list[32] = "'{}' se perderá para siempre! (¡Mucho tiempo!)"
		self.list[33] = "¡Juega y consigue monedas!"
		self.list[34] = "Selección de Idioma"
		self.list[35] = "¿Estás seguro de que quieres abandonar este cuestionario?"
		self.list[36] = "Imprimir"
		self.list[37] = "Una Columna"
		self.list[38] = "Dos Columnas"
		self.list[39] = "Con Respuestas"
		self.list[40] = "Sin Respuestas"
		self.list[41] = "Imprimir Todo"
		self.list[42] = "Fecha: __/__/__"
		self.list[43] = "Nombre:___________________________________________"
		self.list[44] = "Grado: _______"


class Time:
	def __init__(self):
		self.start = time.time()
		self.seconds = 0
		self.minutes = 0

	def update(self):
		self.seconds = round(time.time() - self.start)
		if self.seconds > 59: 
			self.minutes += 1
			self.start = time.time()
	
	def reset(self):
		self.start = time.time()
		self.seconds = 0
		self.minutes = 0
	
	def get_time(self): return "{:02}:{:02}".format(self.minutes, self.seconds)


class Question:
	def __init__(self, question, answer):
		self.question = question
		self.answer = answer
	
	def check(self, user):
		return self.answer[-1] == user


class Button:
	def __init__(self, text, color, r_size = (195, 42)):
		self.rect = pygame.Rect((0, 0), r_size)
		self.text = text
		self.color = color
		self.r_size = r_size
	
	def set_pos(self, x, y):
		self.rect.x = x
		self.rect.y = y
	
	def set_text(self, text):
		self.text = text
	
	def show(self, mouse, x , y, bool = True, pressed = False, mirror = False, lh = 0.675, fontname="./Fonts/berlin-sans-fb-demi-bold.ttf", f_size = 26):
		self.set_pos(x, y)
		if x+self.rect.width > mouse[0] > x and y+self.rect.height > mouse[1] > y and bool and not pressed:
			draw('./Buttons/{} 2.png'.format(self.color), x, y, mirror)
		elif pressed:
			draw('./Buttons/{} 3.png'.format(self.color), x, y, mirror)
		elif not bool:
			draw('./Buttons/{} 0.png'.format(self.color), x, y, mirror)
		else: draw('./Buttons/{}.png'.format(self.color), x, y, mirror)
		ptext.draw(self.text, center = (x+self.rect.width/2, y+self.rect.height/2), color = (255, 255, 255), width = self.rect.width, align = "center", fontname=fontname, fontsize = f_size, lineheight = lh)
		
	def click(self, event, bool = True):
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and bool: return self.rect.collidepoint(event.pos)


def centerprint(variable, x, y, sizeX, sizeY, color=(255, 255, 255), font=pygame.font.Font('./Fonts/berlin-sans-fb-demi-bold.ttf', 21)):
	text = font.render(str(variable), True, color)
	rect = pygame.Rect((x, y, sizeX, sizeY))
	text_rect = text.get_rect()
	text_rect.center = rect.center
	screen.blit(text, text_rect)
	# pygame.draw.rect(screen, pygame.Color("#FF0000"), rect, 1)


def printt(variable, x, y, color=(25, 25, 25), font=pygame.font.Font('./Fonts/berlin-sans-fb-demi-bold.ttf', 21)):
	text = font.render(str(variable), True, color)
	screen.blit(text, (x, y))


def draw(path, x, y, mirror=False):
	if mirror: screen.blit(pygame.transform.flip(pygame.image.load(path), True, False), (x, y))
	else: screen.blit(pygame.image.load(path).convert_alpha(), (x, y))


def window(event):
	if event.type == pygame.QUIT: sys.exit()
	elif event.type == pygame.VIDEORESIZE:
		if event.w < 1280: event.w = 1280
		if event.h < 720: event.h = 720
		pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


# TODO: FIX SKIP QUESTION BUG ... SOMEHOW
def pdf(File, Quiz, Active, feedback, column, Language):
	global step
	step, x, width, height, step2 = -1, 21.6, 550, 735, False

	def header():
		canvas.setFont("Times-Roman", 12)

		canvas.drawImage("./Layout/PrintLogo.png", 25, 768, 72, 52, preserveAspectRatio=True)
		canvas.drawString(140, 800, File)
		canvas.drawString(470, 800, Language.list[42])
		canvas.drawString(140, 782, Language.list[43])
		canvas.drawString(470, 782, Language.list[44])
		canvas.line(125, 820, 560, 820)
		canvas.line(125, 820, 125, 770)
		canvas.line(125, 770, 560, 770)
		canvas.line(560, 820, 560, 770)

	def quest(text1, text2, w, h):
		global step
		letters = ["a", "b", "c", "d"]
		if step == -1:
			style = ParagraphStyle(name="Normal", fontName="Times-Roman", fontSize=11, leading=14, spaceBefore=8, alignment=4)
			story = [Paragraph(text1, style=style)]
			frame.addFromList([KeepInFrame(w, h, story, mode="error")], canvas)
			step += 1
		style = ParagraphStyle(name="Normal", fontName="Times-Roman", fontSize=11, leading=14, leftIndent=25, bulletIndent=10, alignment=4)
		while step <= 3:
			story = [Paragraph(text2[step], style=style, bulletText=str(letters[step] + "."))]
			frame.addFromList([KeepInFrame(w, h, story, mode="error")], canvas)
			step += 1
		step = -1

	def answer(text1, text2):
		story = [Paragraph(str("{}. ".format(text2) + text1), style=style)]
		frames[step].addFromList([KeepInFrame(79, 800, story, mode="error")], canvas)

	canvas = Canvas("Quiz.pdf", pagesize=A4)
	header()

	if not column: width /= 2
	frame = Frame(x, 20, width, height)
	total, i = 1, 0
	while i < len(Quiz):
		if Active[i]:
			try:
				quest(str("{}. ".format(total) + Quiz[i].question), Quiz[i].answer, width, height)
				total += 1; i += 1
			except:
				if not column:
					if step2: canvas.showPage(); x = 21.6; height = 800
					else: x = 296.6
					step2 = not step2
				else: canvas.showPage(); height = 800
				frame = Frame(x, 20, width, height)
		else: i += 1

	if feedback:
		style = ParagraphStyle(name="Normal", fontName="Times-Roman", fontSize=11, leading=14)
		canvas.showPage(); frames = []
		for k in range(7): frames.append(Frame(.3 * inch + k * 79, 20, 79, 800))

		step, total, i = 0, 1, 0
		while i < len(Quiz):
			if Active[i]:
				try:
					answer(Quiz[i].answer[-1], total)
					total += 1; i += 1
				except:
					if step == 6:
						step, frames = 0, []; canvas.showPage()
						for k in range(7): frames.append(Frame(.3 * inch + k * 79, 20, 79, 800))
					else: step += 1
			else: i += 1

	canvas.save()


def pdfpagecount(path):
	with open(path, 'rb') as fl:
		return PdfFileReader(fl).getNumPages()
